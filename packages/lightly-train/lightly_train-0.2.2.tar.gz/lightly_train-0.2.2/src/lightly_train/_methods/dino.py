#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import copy
from dataclasses import dataclass
from functools import partial
from typing import Callable

import torch
from lightly.loss import DINOLoss
from lightly.models.modules.heads import DINOProjectionHead
from lightly.models.utils import (
    update_momentum,
)
from lightly.transforms import DINOTransform
from lightly.utils.scheduler import cosine_schedule
from torch import Tensor
from torch.nn import Flatten
from torch.optim import Optimizer

from lightly_train import _scaling
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
class DINOArgs(MethodArgs):
    """Args for DINO method for ImageNet dataset."""

    # projection head
    hidden_dim: int = 2048
    bottleneck_dim: int = 256
    output_dim: int = 65536
    teacher_freeze_last_layer_epochs: int = 0
    student_freeze_last_layer_epochs: int = 1
    batch_norm: bool = False
    norm_last_layer: bool = True
    # loss
    teacher_temp: float = 0.07
    warmup_teacher_temp: float = 0.04
    warmup_teacher_temp_epochs: int = 30
    student_temp: float = 0.1
    center_momentum: float = 0.9
    # momentum
    momentum_start: float = 0.996
    momentum_end: float = 1.0


class DINO(Method):
    def __init__(
        self,
        method_args: DINOArgs,
        embedding_model: EmbeddingModel,
        batch_size_per_device: int,
    ):
        super().__init__(
            method_args=method_args,
            embedding_model=embedding_model,
            batch_size_per_device=batch_size_per_device,
        )
        self.method_args = method_args
        self.teacher_embedding_model = embedding_model
        self.teacher_projection_head = DINOProjectionHead(
            input_dim=self.teacher_embedding_model.embed_dim,
            hidden_dim=self.method_args.hidden_dim,
            bottleneck_dim=self.method_args.bottleneck_dim,
            output_dim=self.method_args.output_dim,
            batch_norm=self.method_args.batch_norm,
            freeze_last_layer=self.method_args.teacher_freeze_last_layer_epochs,
            norm_last_layer=self.method_args.norm_last_layer,
        )
        self.student_embedding_model = copy.deepcopy(self.teacher_embedding_model)
        self.student_projection_head = DINOProjectionHead(
            input_dim=self.student_embedding_model.embed_dim,
            hidden_dim=self.method_args.hidden_dim,
            bottleneck_dim=self.method_args.bottleneck_dim,
            output_dim=self.method_args.output_dim,
            batch_norm=self.method_args.batch_norm,
            freeze_last_layer=self.method_args.student_freeze_last_layer_epochs,
            norm_last_layer=self.method_args.norm_last_layer,
        )
        self.flatten = Flatten(start_dim=1)
        self.criterion = DINOLoss(
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
        update_momentum(
            self.student_embedding_model, self.teacher_embedding_model, m=momentum
        )
        update_momentum(
            self.student_projection_head, self.teacher_projection_head, m=momentum
        )

        views = batch[0]
        global_views = torch.cat(views[:2])
        local_views = torch.cat(views[2:])

        x_teacher = self._forward_teacher(global_views)
        x_student = torch.cat(
            [self._forward_student(global_views), self._forward_student(local_views)]
        )

        loss = self.criterion(
            teacher_out=x_teacher.chunk(2),
            student_out=x_student.chunk(len(views)),
            epoch=self.current_epoch,
        )
        self.log(
            "train_loss", loss, prog_bar=True, sync_dist=True, batch_size=len(views[0])
        )
        return loss

    @torch.no_grad()
    def _forward_teacher(self, x: Tensor) -> Tensor:
        x = self.teacher_embedding_model(x)
        x = self.flatten(x)
        x = self.teacher_projection_head(x)
        return x

    def _forward_student(self, x: Tensor) -> Tensor:
        x = self.student_embedding_model(x)
        x = self.flatten(x)
        x = self.student_projection_head(x)
        return x

    @staticmethod
    def default_method_args(scaling_info: ScalingInfo) -> MethodArgs:
        dataset_size = scaling_info.dataset_size
        base_args = DINOArgs()

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
        return DINOArgs(
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
        return TrainableModules(
            modules=[self.student_embedding_model, self.student_projection_head]
        )

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
        self.student_projection_head.cancel_last_layer_gradients(self.current_epoch)

    @staticmethod
    def transform_cls() -> Callable[..., Transform]:
        # TODO: Authors recommend to use different scales for convnets than
        # transformers. We should add a check for the model type and use the appropriate
        # scales accordingly.
        # https://github.com/facebookresearch/dino#resnet-50-and-other-convnets-trainings
        return partial(
            DINOTransform, global_crop_scale=(0.14, 1), local_crop_scale=(0.05, 0.14)
        )
