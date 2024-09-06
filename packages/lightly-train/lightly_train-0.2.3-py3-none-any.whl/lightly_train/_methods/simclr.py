#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from dataclasses import dataclass
from typing import Type

import torch
import torch.distributed as dist
from lightly.loss import NTXentLoss
from lightly.models.modules.heads import SimCLRProjectionHead
from lightly.transforms import SimCLRTransform
from torch import Tensor
from torch.nn import Flatten

from lightly_train._methods.method import Method
from lightly_train._methods.method_args import MethodArgs
from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train._optim.trainable_modules import TrainableModules
from lightly_train._scaling import ScalingInfo
from lightly_train.types import MultiViewBatch, Transform


@dataclass
class SimCLRArgs(MethodArgs):
    """Args for SimCLR method."""

    hidden_dim: int = 2048
    output_dim: int = 128
    num_layers: int = 2
    batch_norm: bool = True
    temperature: float = 0.1


class SimCLR(Method):
    def __init__(
        self,
        method_args: SimCLRArgs,
        embedding_model: EmbeddingModel,
        batch_size_per_device: int,
    ):
        super().__init__(
            method_args=method_args,
            embedding_model=embedding_model,
            batch_size_per_device=batch_size_per_device,
        )
        self.method_args = method_args
        self.embedding_model = embedding_model
        self.flatten = Flatten(start_dim=1)
        self.projection_head = SimCLRProjectionHead(
            input_dim=self.embedding_model.embed_dim,
            hidden_dim=self.method_args.hidden_dim,
            output_dim=self.method_args.output_dim,
            num_layers=self.method_args.num_layers,
            batch_norm=self.method_args.batch_norm,
        )
        self.criterion = NTXentLoss(
            temperature=self.method_args.temperature,
            gather_distributed=dist.is_available(),
        )

    def training_step(self, batch: MultiViewBatch, batch_idx: int) -> Tensor:
        views, targets = batch[0], batch[1]
        x = self.embedding_model(torch.cat(views))
        x = self.flatten(x)
        x = self.projection_head(x)
        x0, x1 = x.chunk(len(views))
        loss = self.criterion(x0, x1)
        self.log(
            "train_loss", loss, prog_bar=True, sync_dist=True, batch_size=len(targets)
        )
        return loss

    @staticmethod
    def default_method_args(scaling_info: ScalingInfo) -> MethodArgs:
        # No scaling needed for now as default parameters are quite robust.
        return SimCLRArgs()

    def trainable_modules(self) -> TrainableModules:
        return TrainableModules(modules=[self.embedding_model, self.projection_head])

    @staticmethod
    def transform_cls() -> Type[Transform]:
        return SimCLRTransform
