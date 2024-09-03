#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""DenseCLDINO

Implementation based on mixture of DenseCL and DINO. The method reuses all model parts
from DINO with the following differences:
* There is an extra local projection head
* There is an extra local loss term
* The local loss is calculated on features matched based on DenseCL
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from functools import partial
from typing import Callable

import torch
from lightly.loss import DINOLoss
from lightly.models import utils
from lightly.models.modules.heads import DINOProjectionHead
from lightly.models.utils import (
    update_momentum,
)
from lightly.transforms import DINOTransform
from lightly.utils.scheduler import cosine_schedule
from torch import Tensor
from torch.nn import AdaptiveAvgPool2d, Module
from torch.optim import Optimizer

from lightly_train import _scaling
from lightly_train._methods.dino import DINOArgs
from lightly_train._methods.method import Method
from lightly_train._methods.method_args import MethodArgs
from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train._optim.adamw_args import AdamWArgs
from lightly_train._optim.optimizer_args import OptimizerArgs
from lightly_train._optim.optimizer_type import OptimizerType
from lightly_train._optim.trainable_modules import TrainableModules
from lightly_train._scaling import IMAGENET_SIZE, ScalingInfo
from lightly_train.types import MultiViewBatch, Transform


@dataclass
class DenseCLDINOArgs(DINOArgs):
    """Args for DenseCLDINO method for ImageNet dataset."""

    # loss
    lambda_: float = 0.5  # Default from DenseCLArgs


class DenseCLDINOEncoder(Module):
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        hidden_dim: int,
        bottleneck_dim: int,
        output_dim: int,
        batch_norm: bool,
        freeze_last_layer: int,
        norm_last_layer: bool,
    ) -> None:
        super().__init__()
        self.embedding_model = embedding_model
        self.local_projection_head = DINOProjectionHead(
            input_dim=embedding_model.embed_dim,
            hidden_dim=hidden_dim,
            bottleneck_dim=bottleneck_dim,
            output_dim=output_dim,
            batch_norm=batch_norm,
            freeze_last_layer=freeze_last_layer,
            norm_last_layer=norm_last_layer,
        )
        self.global_projection_head = DINOProjectionHead(
            input_dim=embedding_model.embed_dim,
            hidden_dim=hidden_dim,
            bottleneck_dim=bottleneck_dim,
            output_dim=output_dim,
            batch_norm=batch_norm,
            freeze_last_layer=freeze_last_layer,
            norm_last_layer=norm_last_layer,
        )
        self.pool = AdaptiveAvgPool2d((1, 1))

    def forward(self, x: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        # B = batch size, C = number of channels, H = image height, W = image width, D = output_dim
        # (B, C, H, W)
        features = self.embedding_model(x)
        # (B, C, H, W) -> (B, C, 1, 1) -> (B, C)
        global_proj = self.pool(features).flatten(start_dim=1)
        # (B, C) -> (B, D)
        global_proj = self.global_projection_head(global_proj)
        # (B, C, H, W) -> (B, C, H*W) -> (B, H*W, C)
        features = features.flatten(start_dim=2).permute(0, 2, 1)
        # (B, H*W, C) -> (B, H*W, D)
        local_proj = self.local_projection_head(features)
        # Return: (B, H*W, C), (B, D), (B, H*W, D)
        return features, global_proj, local_proj


class DenseCLDINO(Method):
    def __init__(
        self,
        method_args: DenseCLDINOArgs,
        embedding_model: EmbeddingModel,
        batch_size_per_device: int,
    ):
        super().__init__(
            method_args=method_args,
            embedding_model=embedding_model,
            batch_size_per_device=batch_size_per_device,
        )
        self.method_args = method_args
        self.teacher_encoder = DenseCLDINOEncoder(
            embedding_model=embedding_model,
            hidden_dim=method_args.hidden_dim,
            bottleneck_dim=method_args.bottleneck_dim,
            output_dim=method_args.output_dim,
            batch_norm=method_args.batch_norm,
            freeze_last_layer=method_args.teacher_freeze_last_layer_epochs,
            norm_last_layer=method_args.norm_last_layer,
        )
        self.student_encoder = DenseCLDINOEncoder(
            embedding_model=copy.deepcopy(embedding_model),
            hidden_dim=method_args.hidden_dim,
            bottleneck_dim=method_args.bottleneck_dim,
            output_dim=method_args.output_dim,
            batch_norm=method_args.batch_norm,
            freeze_last_layer=method_args.student_freeze_last_layer_epochs,
            norm_last_layer=method_args.norm_last_layer,
        )

        self.local_criterion = DINOLoss(
            output_dim=self.method_args.output_dim,
            teacher_temp=self.method_args.teacher_temp,
            warmup_teacher_temp=self.method_args.warmup_teacher_temp,
            warmup_teacher_temp_epochs=self.method_args.warmup_teacher_temp_epochs,
            student_temp=self.method_args.student_temp,
            center_momentum=self.method_args.center_momentum,
        )
        self.global_criterion = DINOLoss(
            output_dim=self.method_args.output_dim,
            teacher_temp=self.method_args.teacher_temp,
            warmup_teacher_temp=self.method_args.warmup_teacher_temp,
            warmup_teacher_temp_epochs=self.method_args.warmup_teacher_temp_epochs,
            student_temp=self.method_args.student_temp,
            center_momentum=self.method_args.center_momentum,
        )

    def training_step(self, batch: MultiViewBatch, batch_idx: int) -> Tensor:
        momentum = cosine_schedule(
            step=self.trainer.global_step,
            max_steps=self.trainer.estimated_stepping_batches,
            start_value=self.method_args.momentum_start,
            end_value=self.method_args.momentum_end,
        )
        update_momentum(self.student_encoder, self.teacher_encoder, m=momentum)

        views = batch[0]
        global_views = torch.cat(views[:2])
        local_views = torch.cat(views[2:])

        # Forward teacher.
        with torch.no_grad():
            (
                features_teacher,
                global_proj_teacher,
                local_proj_teacher,
            ) = self.teacher_encoder(global_views)

        # Forward student.
        (
            global_features_student,
            global_global_proj_student,
            global_local_proj_student,
        ) = self.student_encoder(global_views)
        _, local_global_proj_student, _ = self.student_encoder(local_views)

        # Global loss (normal DINO loss).
        global_proj_student = torch.cat(
            [global_global_proj_student, local_global_proj_student], dim=0
        )
        global_loss = self.global_criterion(
            teacher_out=global_proj_teacher.chunk(2),
            student_out=global_proj_student.chunk(len(views)),
            epoch=self.current_epoch,
        )

        # Local loss (Dense matching + DINO loss). This is only calculated on the
        # global views as matching global with local views is tricky due to the
        # different number of features.
        global_local_proj_student = utils.select_most_similar(
            features_teacher, global_features_student, global_local_proj_student
        )

        local_proj_teacher = local_proj_teacher.flatten(end_dim=1)
        global_local_proj_student = global_local_proj_student.flatten(end_dim=1)

        local_loss = self.local_criterion(
            teacher_out=local_proj_teacher.chunk(2),
            student_out=global_local_proj_student.chunk(2),
            epoch=self.current_epoch,
        )

        # Final loss.
        lambda_ = self.method_args.lambda_
        loss = (1 - lambda_) * global_loss + lambda_ * local_loss

        self.log(
            "train_loss", loss, prog_bar=True, sync_dist=True, batch_size=len(views[0])
        )
        return loss

    @staticmethod
    def default_method_args(scaling_info: ScalingInfo) -> MethodArgs:
        dataset_size = scaling_info.dataset_size
        base_args = DenseCLDINOArgs()

        # Default output dim of 65536 is too large for small datasets.
        output_dim = _scaling.get_bucket_value(
            input=dataset_size,
            buckets=[
                (20_000, 1024),
                (50_000, 2048),
                (100_000, 4096),
                (200_000, 16384),
                (500_000, 32768),
                (float("inf"), base_args.output_dim),
            ],
        )

        # Default teacher temperature of 0.07 is too high for small datasets. Lower
        # temperature results in stronger sharpening which avoids collapse to uniform
        # distribution.
        teacher_temp = _scaling.interpolate(
            dataset_size,
            input_start=20_000,
            input_end=IMAGENET_SIZE,
            value_start=0.02,
            value_end=base_args.teacher_temp,
            round_ndigits=2,
        )

        # Default momentum start of 0.996 is too high for small datasets. Lower momentum
        # results in slower updates of the teacher model. This is important because with
        # high momentum (fast changing teacher) and a small dataset, the initial
        # training epochs become unstable.
        momentum_start = _scaling.interpolate(
            dataset_size,
            input_start=20_000,
            input_end=IMAGENET_SIZE,
            value_start=0.99,
            value_end=base_args.momentum_start,
            round_ndigits=3,
        )

        # TODO: For ViTs, norm_last_layer should be set to False. But we currently
        # have no way to detect the model type here.
        return DenseCLDINOArgs(
            output_dim=output_dim,
            teacher_temp=teacher_temp,
            warmup_teacher_temp=teacher_temp,
            momentum_start=momentum_start,
        )

    @staticmethod
    def default_optimizer_args(optim_type: OptimizerType) -> OptimizerArgs:
        if optim_type == OptimizerType.ADAMW:
            # TODO: DINO uses a weight decay schedule that linearly increases the weight
            # decay from 0.04 to 0.4 over the course of the training.
            return AdamWArgs(weight_decay=0.04)
        raise ValueError(f"Unsupported optimizer type: {optim_type}")

    def trainable_modules(self) -> TrainableModules:
        return TrainableModules(modules=[self.student_encoder])

    def configure_gradient_clipping(
        self,
        optimizer: Optimizer,
        gradient_clip_val: int | float | None = None,
        gradient_clip_algorithm: str | None = None,
    ) -> None:
        self.clip_gradients(
            optimizer=optimizer,
            gradient_clip_val=3.0,
            gradient_clip_algorithm="norm",
        )
        self.student_encoder.local_projection_head.cancel_last_layer_gradients(
            self.current_epoch
        )
        self.student_encoder.global_projection_head.cancel_last_layer_gradients(
            self.current_epoch
        )

    @staticmethod
    def transform_cls() -> Callable[..., Transform]:
        # TODO: Authors recommend to use different scales for convnets than
        # transformers. We should add a check for the model type and use the appropriate
        # scales accordingly.
        # https://github.com/facebookresearch/dino#resnet-50-and-other-convnets-trainings
        return partial(
            DINOTransform, global_crop_scale=(0.14, 1), local_crop_scale=(0.05, 0.14)
        )
