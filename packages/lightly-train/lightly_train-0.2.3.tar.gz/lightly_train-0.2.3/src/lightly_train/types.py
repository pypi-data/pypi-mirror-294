#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path
from typing import (
    Any,
    Dict,
    Generic,
    Iterable,
    List,
    Protocol,
    Tuple,
    TypeVar,
    Union,
)

import torch
from PIL.Image import Image as PILImage
from torch import Tensor

PathLike = Union[str, Path]
MultiViewBatch = Tuple[List[Tensor], Tensor, List[str]]
SingleViewBatch = Tuple[Tensor, Tensor, List[str]]
MultiViewTransformOutput = Union[List[Tensor], List[PILImage]]

# Replaces torch.optim.optimizer.ParamsT
# as it is only available in torch>=v2.2.
# Importing it conditionally cannot make typing work for both older
# and newer versions of torch.
ParamsT = Union[Iterable[torch.Tensor], Iterable[Dict[str, Any]]]

_T = TypeVar("_T", covariant=True)


class Transform(Generic[_T], Protocol):
    # `image` is a positional only argument because naming of the argument differs
    # between lightly, v1, and v2 transforms.
    def __call__(self, image: PILImage, /) -> _T: ...
