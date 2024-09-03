#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import warnings
from pathlib import Path
from typing import Any, Callable, Sized, Type

from lightly.data import LightlyDataset
from pytorch_lightning import Trainer
from pytorch_lightning.accelerators.accelerator import Accelerator
from pytorch_lightning.accelerators.cpu import CPUAccelerator
from pytorch_lightning.accelerators.cuda import CUDAAccelerator
from pytorch_lightning.callbacks import (
    DeviceStatsMonitor,
    EarlyStopping,
    LearningRateMonitor,
)
from pytorch_lightning.loggers import Logger
from pytorch_lightning.strategies.strategy import Strategy
from pytorch_lightning.trainer.connectors.accelerator_connector import _PRECISION_INPUT
from torch.nn import Module
from torch.utils.data import DataLoader, Dataset

from lightly_train._callbacks.checkpoint import ModelCheckpoint
from lightly_train._checkpoint import CheckpointLightlyTrainModels
from lightly_train._commands import common_helpers
from lightly_train._configs import validate
from lightly_train._constants import DATALOADER_TIMEOUT
from lightly_train._loggers.jsonl import JSONLLogger
from lightly_train._loggers.tensorboard import TensorBoardLogger
from lightly_train._methods import method_helpers
from lightly_train._methods.method import Method
from lightly_train._models import package_helpers
from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train._optim.optimizer_args import OptimizerArgs
from lightly_train._optim.optimizer_type import OptimizerType
from lightly_train._scaling import IMAGENET_SIZE, ScalingInfo
from lightly_train.types import PathLike, Transform

try:
    import timm
except ImportError:
    timm = None

try:
    import tensorboard
except ImportError:
    tensorboard = None


def get_transform(
    method: str | Method,
    transform_args: dict[str, Any] | None,
) -> Transform:
    method_cls = method_helpers.get_method_cls(method)
    if transform_args is not None:
        return method_cls.transform_cls()(**transform_args)  # type: ignore[misc]
    return method_cls.transform_cls()()  # type: ignore[misc]


def get_dataset(
    data: PathLike | Dataset,
    transform: Callable | None,
) -> Dataset:
    if isinstance(data, Dataset):
        return data

    data = Path(data).resolve()
    if not data.exists():
        raise ValueError(f"Data directory '{data}' does not exist!")
    elif not data.is_dir():
        raise ValueError(f"Data path '{data}' is not a directory!")
    elif data.is_dir() and not any(data.iterdir()):
        raise ValueError(f"Data directory '{data}' is empty!")

    # LightlyDataset runs some additional checks but error messages might not be
    # informative.
    return LightlyDataset(input_dir=str(data), transform=transform)


def get_dataloader(
    dataset: Dataset,
    global_batch_size: int,
    world_size: int,
    num_workers: int,
    loader_args: dict[str, Any] | None,
) -> DataLoader:
    """Creates a dataloader for the given dataset.

    Args:
        dataset:
            Dataset.
        global_batch_size:
            The global batch size. This is the total batch size across all nodes and
            devices. The batch size for the dataloader is calculated as
            global_batch_size // world_size.
        world_size:
            The total number of devices across all nodes.
        num_workers:
            Number of workers for the dataloader.
        loader_args:
            Additional arguments for the DataLoader. Additional arguments have priority
            over other arguments.

    Raises:
        ValueError: If the global batch size is not divisible by the world size.
    """
    # Limit batch size for small datasets.
    if isinstance(dataset, Sized):
        dataset_size = len(dataset)
        if dataset_size < global_batch_size:
            old_global_batch_size = global_batch_size
            global_batch_size = dataset_size
            warnings.warn(
                f"Detected dataset size {dataset_size} and batch size "
                f"{old_global_batch_size}. Reducing batch size to {global_batch_size}."
            )

    if global_batch_size % world_size != 0:
        raise ValueError(
            f"Batch size {global_batch_size} must be divisible by the world size "
            f"{world_size}. The world size is calculated as devices * num_nodes."
        )
    batch_size = global_batch_size // world_size
    timeout = DATALOADER_TIMEOUT if num_workers > 0 else 0
    dataloader_kwargs: dict[str, Any] = dict(
        dataset=dataset,
        batch_size=batch_size,
        shuffle=True,
        num_workers=num_workers,
        drop_last=True,
        timeout=timeout,
    )
    if loader_args is not None:
        dataloader_kwargs.update(**loader_args)
    return DataLoader(**dataloader_kwargs)


def get_embedding_model(model: Module, embed_dim: int | None = None) -> EmbeddingModel:
    feature_extractor_cls = package_helpers.get_feature_extractor_cls(model=model)
    feature_extractor = feature_extractor_cls(model=model)
    return EmbeddingModel(feature_extractor=feature_extractor, embed_dim=embed_dim)


def get_trainer(
    out: Path,
    model: Module,
    embedding_model: EmbeddingModel,
    epochs: int,
    accelerator: str | Accelerator,
    strategy: str | Strategy,
    devices: list[int] | str | int,
    num_nodes: int,
    precision: _PRECISION_INPUT | None,
    trainer_args: dict[str, Any] | None,
) -> Trainer:
    # Set version and name to empty string to save logs directly in the root
    # directory.
    loggers: list[Logger] = [
        JSONLLogger(save_dir=out, name="", version=""),
    ]
    if tensorboard is not None:
        loggers.append(TensorBoardLogger(save_dir=out, name="", version=""))

    accelerator = common_helpers.get_accelerator(accelerator=accelerator)
    strategy = get_strategy(accelerator=accelerator, strategy=strategy, devices=devices)
    sync_batchnorm = get_sync_batchnorm(accelerator=accelerator)

    trainer_kwargs: dict[str, Any] = dict(
        default_root_dir=out,
        max_epochs=epochs,
        accelerator=accelerator,
        strategy=strategy,
        devices=devices,
        num_nodes=num_nodes,
        precision=precision,
        callbacks=[
            LearningRateMonitor(),
            DeviceStatsMonitor(),
            ModelCheckpoint(
                save_last=True,
                models=CheckpointLightlyTrainModels(
                    model=model, embedding_model=embedding_model
                ),
                dirpath=out / "checkpoints",
                enable_version_counter=False,
            ),
            # Stop if training loss diverges.
            EarlyStopping(monitor="train_loss", patience=int(1e12), check_finite=True),
        ],
        logger=loggers,
        sync_batchnorm=sync_batchnorm,
    )
    if trainer_args is not None:
        trainer_kwargs.update(trainer_args)

    return Trainer(**trainer_kwargs)


def get_strategy(
    strategy: str | Strategy,
    accelerator: str | Accelerator,
    devices: list[int] | str | int,
) -> str | Strategy:
    if strategy != "auto":
        return strategy

    accelerator_cls: Type[CUDAAccelerator] | Type[CPUAccelerator]
    if isinstance(accelerator, CUDAAccelerator) or accelerator == "gpu":
        accelerator_cls = CUDAAccelerator
    elif isinstance(accelerator, CPUAccelerator) or accelerator == "cpu":
        accelerator_cls = CPUAccelerator
    else:
        # For non CPU/CUDA accelerators we let PyTorch Lightning decide.
        return strategy

    if devices == "auto":
        num_devices = accelerator_cls.auto_device_count()
    else:
        parsed_devices = accelerator_cls.parse_devices(devices=devices)
        # None means that no devices were requested.
        if parsed_devices is None:
            return strategy
        num_devices = (
            len(parsed_devices) if isinstance(parsed_devices, list) else parsed_devices
        )

    if num_devices > 1:
        # If we have multiple CPU or CUDA devices, use DDP with find_unused_parameters.
        # find_unused_parameters avoids DDP errors for models/methods that have
        # extra parameters which are not used in all the forward passes. This is for
        # example the case in DINO where the projection head is frozen during the first
        # epoch.
        # TODO: Only set find_unused_parameters=True if necessary as it slows down
        # training speed. See https://github.com/pytorch/pytorch/pull/44826 on how
        # parameters can be ignored for DDP.
        return "ddp_find_unused_parameters_true"
    return strategy


def get_sync_batchnorm(accelerator: str | Accelerator) -> bool:
    # SyncBatchNorm is only supported on CUDA devices.
    assert accelerator != "auto"
    return accelerator == "gpu" or isinstance(accelerator, CUDAAccelerator)


def get_optimizer_args(
    optim_args: dict[str, Any] | None,
    method: Method,
) -> OptimizerArgs:
    # Hardcode OptimizerType.ADAMW for now as it is the only supported optimizer.
    optim_type = OptimizerType.ADAMW
    default_args = method.default_optimizer_args(optim_type=optim_type)
    return validate.validate_dict(config=optim_args, default=default_args)


def get_scaling_info(
    dataset: Dataset,
) -> ScalingInfo:
    if isinstance(dataset, Sized):
        dataset_size = len(dataset)
    else:
        dataset_size = IMAGENET_SIZE
    return ScalingInfo(dataset_size=dataset_size)


def get_method(
    method: str,
    method_args: dict[str, Any] | None,
    scaling_info: ScalingInfo,
    embedding_model: EmbeddingModel,
    batch_size_per_device: int,
) -> Method:
    method_cls = method_helpers.get_method_cls(method=method)
    default_args = method_cls.default_method_args(scaling_info=scaling_info)
    args = validate.validate_dict(config=method_args, default=default_args)
    return method_cls(
        method_args=args,
        embedding_model=embedding_model,
        batch_size_per_device=batch_size_per_device,
    )
