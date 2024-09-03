#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from dataclasses import dataclass

from lightly_train._configs.config import Config


@dataclass
class MethodArgs(Config):
    """Arguments for a method.

    This does not include optimizer or scheduler arguments.
    """

    pass
