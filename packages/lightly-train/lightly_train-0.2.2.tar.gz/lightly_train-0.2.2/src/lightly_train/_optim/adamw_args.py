#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import dataclasses
from dataclasses import dataclass
from typing import Tuple

from torch.optim import AdamW
from torch.optim import Optimizer as TorchOptimizer

from lightly_train._optim.optimizer_args import OptimizerArgs
from lightly_train._optim.optimizer_type import OptimizerType
from lightly_train.types import ParamsT


@dataclass
class AdamWArgs(OptimizerArgs):
    lr: float = 0.001
    betas: Tuple[float, float] = (0.9, 0.999)
    eps: float = 1e-8
    weight_decay: float = 0.01

    def __post_init__(self):
        # Make sure betas is actually a tuple because OmegaConf converts tuples to lists.
        self.betas = tuple(self.betas)

    @staticmethod
    def type() -> OptimizerType:
        return OptimizerType.ADAMW

    def get_optimizer(self, params: ParamsT, lr_scale: float) -> TorchOptimizer:
        kwargs = dataclasses.asdict(self)
        kwargs["lr"] *= lr_scale
        return AdamW(params=params, **kwargs)
