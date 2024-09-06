#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import logging
from dataclasses import dataclass

# Import old types for compatibility with omegaconf.
from typing import Any, Dict, Optional, Union

import pytorch_lightning
from omegaconf import MISSING, DictConfig
from pytorch_lightning.accelerators.accelerator import Accelerator
from pytorch_lightning.strategies.strategy import Strategy
from pytorch_lightning.trainer.connectors.accelerator_connector import _PRECISION_INPUT
from torch.nn import Module
from torch.utils.data import Dataset

from lightly_train import _logging
from lightly_train._commands import _warnings, common_helpers, train_helpers
from lightly_train._configs import omegaconf_utils, validate
from lightly_train._configs.config import Config
from lightly_train._models import package_helpers
from lightly_train.types import PathLike

logger = logging.getLogger(__name__)


def train(
    out: PathLike,
    data: PathLike | Dataset,
    model: str | Module,
    method: str = "simclr",
    method_args: dict[str, Any] | None = None,
    embed_dim: int | None = None,
    epochs: int = 100,
    batch_size: int = 128,
    num_workers: int = 8,
    devices: list[int] | str | int = "auto",
    num_nodes: int = 1,
    resume: bool = False,
    overwrite: bool = False,
    accelerator: str | Accelerator = "auto",
    strategy: str | Strategy = "auto",
    precision: _PRECISION_INPUT = "32-true",  # Default precision in PyTorch Lightning
    seed: int = 0,
    optim_args: dict[str, Any] | None = None,
    transform_args: dict[str, Any] | None = None,
    loader_args: dict[str, Any] | None = None,
    trainer_args: dict[str, Any] | None = None,
    model_args: dict[str, Any] | None = None,
) -> None:
    """Train a self-supervised model.

    The training process can be monitored with TensorBoard (requires
    `pip install lightly-train[tensorboard]`):
    ```
    tensorboard --logdir out
    ```

    Args:
        out:
            Output directory to save logs, checkpoints, and other artifacts.
        data:
            Path to a directory containing images or a PyTorch Dataset.
        model:
            Model name or instance to use for training.
        method:
            Self-supervised learning method name.
        method_args:
            Arguments for the self-supervised learning method. The available arguments
            depend on the `method` parameter.
        embed_dim:
            Embedding dimension. Set this if you want to train an embedding model with
            a specific dimension. If None, the output dimension of `model` is used.
        epochs:
            Number of training epochs.
        batch_size:
            Global batch size. The batch size per device/GPU is inferred from this value
            and the number of devices and nodes.
        num_workers:
            Number of worker processes for data loading per device/GPU.
        devices:
            Number of devices/GPUs to use for training. 'auto' will automatically select
            the best number of devices available.
        num_nodes:
            Number of nodes for distributed training.
        resume:
            Resume training from the last checkpoint.
        overwrite:
            Overwrite the output directory if it already exists. Warning, this might
            overwrite existing files in the directory!
        accelerator:
            Hardware accelerator. Can be one of ['cpu', 'gpu', 'tpu', 'ipu', 'hpu',
            'mps', 'auto']. 'auto' will automatically select the best accelerator
            available. For details, see:
            https://lightning.ai/docs/pytorch/stable/common/trainer.html#accelerator
        strategy:
            Training strategy. For example 'ddp' or 'auto'. 'auto' automatically
            selects the best strategy available. For details, see:
            https://lightning.ai/docs/pytorch/stable/common/trainer.html#strategy
        precision:
            Training precision. Select '16-mixed' for mixed 16-bit precision, '32-true'
            for full 32-bit precision, or 'bf16-mixed' for mixed bfloat16 precision.
            For details, see:
            https://lightning.ai/docs/pytorch/stable/common/trainer.html#precision
        seed:
            Random seed for reproducibility.
        optim_args:
            Arguments for AdamW optimizer. Available arguments are:
            - lr: float
            - betas: tuple[float, float]
            - weight_decay: float
        transform_args:
            Arguments for the image transform. The available arguments depend on the
            `method` parameter. For example, if `method='simclr'`, the arguments
            are passed to `lightly.transforms.SimCLRTransform`. See the lightly
            transforms documentation for available arguments:
            https://docs.lightly.ai/self-supervised-learning/lightly.transforms.html
        loader_args:
            Arguments for the PyTorch DataLoader. Should only be used in special cases
            as default values are automatically set. Prefer to use the `batch_size` and
            `num_workers` arguments instead. For details, see:
            https://pytorch.org/docs/stable/data.html#torch.utils.data.DataLoader
        trainer_args:
            Arguments for the PyTorch Lightning Trainer. Should only be used in special
            cases as default values are automatically set. For details, see:
            https://lightning.ai/docs/pytorch/stable/common/trainer.html
        model_args:
            Arguments for the model. The available arguments depend on the `model`
            parameter. For example, if `model=f'torchvision/{model_name}'`, the arguments
            are passed to `torchvision.models.get_model(model_name, **model_args)`.
    """
    # Get locals and set up output directory.
    args = locals()
    out_dir = common_helpers.get_out_dir(out=out, resume=resume, overwrite=overwrite)

    # Set up logging.
    _warnings.filter_train_warnings()
    _logging.set_up_console_logging()
    _logging.set_up_file_logging(out_dir / "train.log")
    logger.info(common_helpers.pretty_format_args(args=args))
    logger.info(f"Using output directory '{out_dir}'.")

    pytorch_lightning.seed_everything(seed=seed, workers=True)
    transform_instance = train_helpers.get_transform(
        method=method, transform_args=transform_args
    )
    dataset = train_helpers.get_dataset(data=data, transform=transform_instance)
    scaling_info = train_helpers.get_scaling_info(dataset=dataset)
    model_instance = package_helpers.get_model(model=model, model_args=model_args)
    embedding_model = train_helpers.get_embedding_model(
        model=model_instance, embed_dim=embed_dim
    )
    log_every_n_steps = train_helpers.get_lightning_logging_interval(
        dataset_size=scaling_info.dataset_size, batch_size=batch_size
    )
    trainer_instance = train_helpers.get_trainer(
        out=out_dir,
        model=model_instance,
        embedding_model=embedding_model,
        epochs=epochs,
        accelerator=accelerator,
        strategy=strategy,
        devices=devices,
        num_nodes=num_nodes,
        precision=precision,
        log_every_n_steps=log_every_n_steps,
        trainer_args=trainer_args,
    )
    dataloader = train_helpers.get_dataloader(
        dataset=dataset,
        global_batch_size=batch_size,
        world_size=trainer_instance.world_size,
        num_workers=num_workers,
        loader_args=loader_args,
    )
    assert dataloader.batch_size is not None
    method_instance = train_helpers.get_method(
        method=method,
        method_args=method_args,
        embedding_model=embedding_model,
        batch_size_per_device=dataloader.batch_size,
        scaling_info=scaling_info,
    )
    method_instance.optimizer_args = train_helpers.get_optimizer_args(
        optim_args=optim_args, method=method_instance
    )
    trainer_instance.fit(
        model=method_instance,
        train_dataloaders=dataloader,
        ckpt_path="last" if resume else None,
    )
    if epochs == 0:
        logger.info("No training epochs specified. Saving model and exiting.")
        trainer_instance.save_checkpoint(out_dir / "checkpoints" / "last.ckpt")
    logger.info("Training completed.")


def train_from_config(config: DictConfig) -> None:
    logger.debug(f"Training model with config: {config}")
    config = _validate_config(config=config)
    config_dict = omegaconf_utils.config_to_dict(config=config)
    train(**config_dict)


@dataclass
class TrainConfig(Config):
    out: str = MISSING
    data: str = MISSING
    model: str = MISSING
    method: str = "simclr"
    method_args: Optional[Dict[str, Any]] = None
    embed_dim: Optional[int] = None
    epochs: int = 100
    batch_size: int = 128
    num_workers: int = 8
    devices: Union[str, int] = "auto"
    num_nodes: int = 1
    resume: bool = False
    overwrite: bool = False
    accelerator: str = "auto"
    strategy: str = "auto"
    precision: str = "32-true"
    seed: int = 0
    optim_args: Optional[Dict[str, Any]] = None
    transform_args: Optional[Dict[str, Any]] = None
    loader_args: Optional[Dict[str, Any]] = None
    trainer_args: Optional[Dict[str, Any]] = None
    model_args: Optional[Dict[str, Any]] = None


def _validate_config(config: DictConfig) -> DictConfig:
    return validate.validate_dictconfig(config=config, default=TrainConfig)
