#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from typing import Callable

from lightly.utils.scheduler import CosineWarmupScheduler
from pytorch_lightning import LightningModule
from pytorch_lightning.utilities.types import OptimizerLRScheduler

from lightly_train._methods.method_args import MethodArgs
from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train._optim import optimizer
from lightly_train._optim.adamw_args import AdamWArgs
from lightly_train._optim.optimizer_args import OptimizerArgs
from lightly_train._optim.optimizer_type import OptimizerType
from lightly_train._optim.trainable_modules import TrainableModules
from lightly_train._scaling import ScalingInfo
from lightly_train.types import Transform


class Method(LightningModule):
    def __init__(
        self,
        method_args: MethodArgs,
        embedding_model: EmbeddingModel,
        batch_size_per_device: int,
    ):
        super().__init__()
        self.batch_size_per_device = batch_size_per_device
        self.optimizer_args: OptimizerArgs | None = None

    @staticmethod
    def default_method_args(scaling_info: ScalingInfo) -> MethodArgs:
        """Return the default method args.

        Overwrite this method to change the default method args.
        """
        raise NotImplementedError()

    @staticmethod
    def default_optimizer_args(optim_type: OptimizerType) -> OptimizerArgs:
        """Return the default optimizer args.

        Overwrite this method to change the default optimizer args.
        """
        if optim_type == OptimizerType.ADAMW:
            return AdamWArgs()
        raise ValueError(f"Invalid optimizer type: {optim_type}")

    def trainable_modules(self) -> TrainableModules:
        """Return the modules that should be optimized."""
        raise NotImplementedError()

    # Ignore the return type, because pytorch-lightning types it wrongly.
    # See https://github.com/Lightning-AI/pytorch-lightning/issues/20106
    def configure_optimizers(self) -> OptimizerLRScheduler:
        if self.optimizer_args is None:
            raise RuntimeError("Optimizer args are not set.")

        optim = optimizer.get_optimizer(
            optim_args=self.optimizer_args,
            trainable_modules=self.trainable_modules(),
            lr_scale=self.batch_size_per_device * self.trainer.world_size / 256,
        )

        if self.trainer.max_epochs is None:
            raise RuntimeError("Max epochs is not set.")

        max_epochs = max(1, self.trainer.max_epochs)

        # Warmup for 10 epochs or 10% of the total number of epochs if max_epochs < 100
        warmup_epochs = min(10, max_epochs // 10)
        scheduler = {
            "scheduler": CosineWarmupScheduler(
                optimizer=optim,
                warmup_epochs=int(
                    self.trainer.estimated_stepping_batches / max_epochs * warmup_epochs
                ),
                max_epochs=int(self.trainer.estimated_stepping_batches),
            ),
            "interval": "step",
        }
        return [optim], [scheduler]  # type: ignore[return-value]

    @staticmethod
    def transform_cls() -> Callable[..., Transform]:
        raise NotImplementedError()
