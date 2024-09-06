#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
"""DenseCL

- [0]: 2021, DenseCL: https://arxiv.org/abs/2011.09157
"""

from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Callable

import torch
from lightly.loss import NTXentLoss
from lightly.models import utils
from lightly.models.modules.heads import DenseCLProjectionHead
from lightly.transforms import DenseCLTransform
from lightly.utils.scheduler import cosine_schedule
from torch import Tensor
from torch.nn import AdaptiveAvgPool2d, Module

from lightly_train import _scaling
from lightly_train._methods.method import Method
from lightly_train._methods.method_args import MethodArgs
from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train._optim.trainable_modules import TrainableModules
from lightly_train._scaling import ScalingInfo
from lightly_train.types import MultiViewBatch, Transform


@dataclass
class DenseCLArgs(MethodArgs):
    # Default values for ImageNet1k pre-training from paper.

    # Projection head
    hidden_dim: int = 2048
    output_dim: int = 128

    # Loss
    lambda_: float = 0.5
    temperature: float = 0.2
    memory_bank_size: int = 65536
    gather_distributed: bool = True

    # Momentum
    momentum_start: float = 0.999
    momentum_end: float = 0.999


class DenseCLEncoder(Module):
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        hidden_dim: int,
        output_dim: int,
    ) -> None:
        super().__init__()
        self.embedding_model = embedding_model
        self.local_projection_head = DenseCLProjectionHead(
            input_dim=embedding_model.embed_dim,
            hidden_dim=hidden_dim,
            output_dim=output_dim,
        )
        self.global_projection_head = DenseCLProjectionHead(
            input_dim=embedding_model.embed_dim,
            hidden_dim=hidden_dim,
            output_dim=output_dim,
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


class DenseCL(Method):
    """DenseCL based on MoCo v2."""

    def __init__(
        self,
        method_args: DenseCLArgs,
        embedding_model: EmbeddingModel,
        batch_size_per_device: int,
    ):
        super().__init__(
            method_args=method_args,
            embedding_model=embedding_model,
            batch_size_per_device=batch_size_per_device,
        )
        self.method_args = method_args

        self.query_encoder = DenseCLEncoder(
            embedding_model=embedding_model,
            hidden_dim=method_args.hidden_dim,
            output_dim=method_args.output_dim,
        )
        self.key_encoder = copy.deepcopy(self.query_encoder)

        self.local_criterion = NTXentLoss(
            temperature=method_args.temperature,
            memory_bank_size=(method_args.memory_bank_size, method_args.output_dim),
            gather_distributed=method_args.gather_distributed,
        )
        self.global_criterion = copy.deepcopy(self.local_criterion)

    def training_step(self, batch: MultiViewBatch, batch_idx: int) -> Tensor:
        momentum = cosine_schedule(
            step=self.trainer.global_step,
            max_steps=self.trainer.estimated_stepping_batches,
            start_value=self.method_args.momentum_start,
            end_value=self.method_args.momentum_end,
        )
        utils.update_momentum(
            model=self.query_encoder, model_ema=self.key_encoder, m=momentum
        )
        views = batch[0]
        query_features, query_global, query_local = self.query_encoder(views[0])
        with torch.no_grad():
            key_features, key_global, key_local = self.key_encoder(views[1])

        key_local = utils.select_most_similar(query_features, key_features, key_local)
        query_local = query_local.flatten(end_dim=1)
        key_local = key_local.flatten(end_dim=1)

        local_loss = self.local_criterion(query_local, key_local)
        global_loss = self.global_criterion(query_global, key_global)
        lambda_ = self.method_args.lambda_
        loss = (1 - lambda_) * global_loss + lambda_ * local_loss
        self.log(
            "train_loss", loss, prog_bar=True, sync_dist=True, batch_size=len(batch[0])
        )
        return loss

    @staticmethod
    def default_method_args(scaling_info: ScalingInfo) -> MethodArgs:
        base_args = DenseCLArgs()

        # Default memory bank size is too large for small datasets.
        memory_bank_size = _scaling.get_bucket_value(
            input=scaling_info.dataset_size,
            buckets=[
                (0, 0),
                (10_000, 1024),
                (20_000, 2048),
                (50_000, 4096),
                (100_000, 8192),
                (500_000, 32768),
                (float("inf"), base_args.memory_bank_size),
            ],
        )

        return DenseCLArgs(
            memory_bank_size=memory_bank_size,
        )

    def trainable_modules(self) -> TrainableModules:
        return TrainableModules(modules=[self.query_encoder])

    @staticmethod
    def transform_cls() -> Callable[..., Transform]:
        return DenseCLTransform
