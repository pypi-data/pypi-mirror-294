#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import os
from pathlib import Path

from omegaconf import MISSING
from pytorch_lightning.accelerators.accelerator import Accelerator
from pytorch_lightning.accelerators.cpu import CPUAccelerator
from pytorch_lightning.accelerators.cuda import CUDAAccelerator
from pytorch_lightning.accelerators.mps import MPSAccelerator

from lightly_train.types import PathLike


def get_checkpoint_path(checkpoint: PathLike) -> Path:
    checkpoint_path = Path(checkpoint).resolve()
    if not checkpoint_path.exists():
        raise FileNotFoundError(f"Checkpoint '{checkpoint_path}' does not exist!")
    if not checkpoint_path.is_file():
        raise ValueError(f"Checkpoint '{checkpoint_path}' is not a file!")
    return checkpoint_path


def get_out_path(out: PathLike, overwrite: bool) -> Path:
    out_path = Path(out).resolve()
    if out_path.exists():
        if not overwrite:
            raise ValueError(
                f"Output '{out_path}' already exists! Set overwrite=True to overwrite "
                "the file."
            )
        if not out_path.is_file():
            raise ValueError(f"Output '{out_path}' is not a file!")
    return out_path


def get_accelerator(
    accelerator: str | Accelerator,
) -> str | Accelerator:
    if accelerator != "auto":
        # User specified an accelerator, return it.
        return accelerator

    # Default to CUDA if available.
    if CUDAAccelerator.is_available():
        return CUDAAccelerator()
    elif MPSAccelerator.is_available():
        return MPSAccelerator()
    else:
        return CPUAccelerator()


def get_default_out() -> str:
    return (
        "/out" if os.getenv("LIGHTLY_TRAIN_IS_DOCKER", "False") == "True" else MISSING
    )


def get_default_data() -> str:
    return (
        "/data" if os.getenv("LIGHTLY_TRAIN_IS_DOCKER", "False") == "True" else MISSING
    )


def get_out_dir(out: PathLike, resume: bool, overwrite: bool) -> Path:
    out_dir = Path(out).resolve()
    if out_dir.exists():
        if not out_dir.is_dir():
            raise ValueError(f"Output '{out_dir}' is not a directory!")
        dir_not_empty = any(out_dir.iterdir())
        if dir_not_empty and not (resume or overwrite):
            raise ValueError(
                f"Output '{out_dir}' is not empty! Set overwrite=True to overwrite the "
                "directory or resume=True to resume training."
            )
    out_dir.mkdir(parents=True, exist_ok=True)
    return out_dir
