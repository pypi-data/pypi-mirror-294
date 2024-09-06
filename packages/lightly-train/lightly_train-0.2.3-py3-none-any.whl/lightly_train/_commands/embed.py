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
from pathlib import Path

# Import old types for compatibility with omegaconf.
from typing import Any, Sized, Tuple

from lightly.data import LightlyDataset
from lightly.transforms.utils import IMAGENET_NORMALIZE
from omegaconf import MISSING, DictConfig
from pytorch_lightning import Trainer
from pytorch_lightning.accelerators.accelerator import Accelerator
from torch.utils.data import DataLoader, Dataset

from lightly_train import _logging
from lightly_train._checkpoint import Checkpoint
from lightly_train._commands import _warnings, common_helpers
from lightly_train._commands.common_helpers import get_checkpoint_path, get_out_path
from lightly_train._configs import omegaconf_utils, validate
from lightly_train._configs.config import Config
from lightly_train._constants import DATALOADER_TIMEOUT
from lightly_train._embedding.embedding_format import EmbeddingFormat
from lightly_train._embedding.embedding_predictor import EmbeddingPredictor
from lightly_train._embedding.embedding_transform import EmbeddingTransform
from lightly_train._embedding.writers import writer_helpers
from lightly_train._embedding.writers.embedding_writer import EmbeddingWriter
from lightly_train._models.embedding_model import EmbeddingModel
from lightly_train.types import PathLike

logger = logging.getLogger(__name__)


def embed(
    out: PathLike,
    data: PathLike,
    checkpoint: PathLike,
    format: EmbeddingFormat | str,
    image_size: int | tuple[int, int] = 224,
    batch_size: int = 128,
    num_workers: int = 8,
    accelerator: str | Accelerator = "auto",
    overwrite: bool = False,
) -> None:
    """Embed images from a model checkpoint.

    Args:
        out:
            Filepath where the embeddings will be saved. For example "embeddings.csv".
        data:
            Directory containing the images to embed.
        checkpoint:
            Path to the LightlyTrain checkpoint file used for embedding. The location of
            the checkpoint depends on the train command. If training was run with
            `out="my_output_dir"`, then the last LightlyTrain checkpoint is saved to
            `my_output_dir/checkpoints/last.ckpt`.
        format:
            Format of the embeddings. Supported formats are ['csv', 'lightly_csv',
            'torch']. Use 'lightly_csv' if you want to use the embeddings as custom
            embeddings with the Lightly Worker. See the relevant docs for more
            information: https://docs.lightly.ai/docs/custom-embeddings
            Use `torch.load(out)` to load the embeddings if you choose 'torch' format.
        image_size:
            Size to which the images are resized before embedding. If a single integer
            is provided, the image is resized to a square with the given side length.
            If a (height, width) tuple is provided, the image is resized to the given
            height and width. Note that not all models support all image sizes.
        batch_size:
            Number of images per batch.
        num_workers:
            Number of workers for the dataloader.
        accelerator:
            Hardware accelerator. Can be one of ['cpu', 'gpu', 'tpu', 'ipu', 'hpu',
            'mps', 'auto']. 'auto' will automatically select the best accelerator
            available. For details, see:
            https://lightning.ai/docs/pytorch/stable/common/trainer.html#accelerator
        overwrite:
            Overwrite the output file if it already exists.
    """
    # Set up logging.
    _warnings.filter_embed_warnings()
    _logging.set_up_console_logging()
    logger.info(common_helpers.pretty_format_args(args=locals()))

    logger.info(f"Embedding images in '{data}'.")
    format = _get_format(format=format)
    out_path = get_out_path(out=out, overwrite=overwrite)
    checkpoint_path = get_checkpoint_path(checkpoint=checkpoint)
    writer = writer_helpers.get_writer(format=format, filepath=out_path)
    transform = _get_transform(image_size=image_size)
    dataset = _get_dataset(data=data, transform=transform)
    dataloader = _get_dataloader(
        dataset=dataset,
        batch_size=batch_size,
        num_workers=num_workers,
    )
    embedding_model = _get_embedding_model(checkpoint_path=checkpoint_path)
    embedding_predictor = EmbeddingPredictor(embedding_model=embedding_model)
    accelerator = common_helpers.get_accelerator(accelerator=accelerator)
    trainer = _get_trainer(accelerator=accelerator, writer=writer)
    trainer.predict(
        model=embedding_predictor,
        dataloaders=dataloader,
        return_predictions=False,
    )
    logger.info(f"Embeddings saved to '{out_path}'.")


def embed_from_config(config: DictConfig) -> None:
    logger.debug(f"Embedding images with config: {config}")
    config = _parse_config(config=config)
    config = _validate_config(config=config)
    config_dict = _config_to_dict(config=config)
    embed(**config_dict)


@dataclass
class EmbedConfig(Config):
    out: str = MISSING
    data: str = MISSING
    checkpoint: str = MISSING
    format: str = MISSING
    # OmegaConf doesn't support Union[int, Tuple[int, int]] so we have to use the
    # more general type here.
    image_size: Tuple[int, int] = (224, 224)
    batch_size: int = 128
    num_workers: int = 8
    accelerator: str = "auto"
    overwrite: bool = False


def _get_format(format: EmbeddingFormat | str) -> EmbeddingFormat:
    logger.debug(f"Getting embedding format for '{format}'.")
    try:
        return EmbeddingFormat(format)
    except ValueError:
        raise ValueError(
            f"Invalid embedding format: '{format}'. Valid formats are: "
            f"{sorted([f.value for f in EmbeddingFormat])}"
        )


def _get_transform(
    image_size: int | tuple[int, int],
) -> EmbeddingTransform:
    logger.debug(f"Getting embedding transform for image size {image_size}.")
    mean = tuple(IMAGENET_NORMALIZE["mean"])
    std = tuple(IMAGENET_NORMALIZE["std"])
    logger.debug(f"Using mean {mean} and std {std} for normalization.")
    assert len(mean) == len(std) == 3
    if isinstance(image_size, int):
        image_size = (image_size, image_size)
    return EmbeddingTransform(
        image_size=image_size,
        # TODO: Load mean and std from checkpoint. We can do this easily once we have
        # transform configs and save them in the checkpoint.
        mean=mean,
        std=std,
    )


def _get_dataset(
    data: PathLike | Dataset,
    transform: EmbeddingTransform,
) -> Dataset:
    if isinstance(data, Dataset):
        logger.debug("Using provided dataset.")
        return data
    else:
        logger.debug(f"Loading LightlyDataset from '{data}'.")
        return LightlyDataset(input_dir=str(data), transform=transform)


def _get_dataloader(
    dataset: Dataset,
    batch_size: int,
    num_workers: int,
) -> DataLoader:
    logger.debug(
        f"Getting dataloader with batch_size {batch_size} and num_workers {num_workers}."
    )
    if isinstance(dataset, Sized):
        dataset_size = len(dataset)
        if batch_size > dataset_size:
            old_batch_size = batch_size
            batch_size = dataset_size
            logger.warning(
                f"Detected dataset size {dataset_size} and batch size "
                f"{old_batch_size}. Reducing batch size to {batch_size}."
            )
    timeout = DATALOADER_TIMEOUT if num_workers > 0 else 0
    return DataLoader(
        dataset=dataset,
        batch_size=batch_size,
        num_workers=num_workers,
        shuffle=False,
        drop_last=False,
        timeout=timeout,
    )


def _get_embedding_model(checkpoint_path: Path) -> EmbeddingModel:
    logger.debug(f"Loading embedding model from '{checkpoint_path}'.")
    checkpoint = Checkpoint.from_path(checkpoint=checkpoint_path)
    return checkpoint.lightly_train.models.embedding_model


def _get_trainer(accelerator: str | Accelerator, writer: EmbeddingWriter) -> Trainer:
    logger.debug(f"Getting trainer with accelerator '{accelerator}'.")
    return Trainer(
        accelerator=accelerator,
        devices=1,
        inference_mode=True,
        callbacks=[writer],
        logger=False,
        enable_checkpointing=False,
    )


def _parse_config(config: DictConfig) -> DictConfig:
    config = _parse_image_size(config=config)
    return config


def _parse_image_size(config: DictConfig) -> DictConfig:
    """Parse image size from config and set it to a (height, width) tuple.

    We have to do this because OmegaConf doesn't support Union[int, Tuple[int, int]] in
    the config schema.
    """
    image_size = config.get("image_size")
    if isinstance(image_size, int):
        config["image_size"] = (image_size, image_size)
    return config


def _validate_config(config: DictConfig) -> DictConfig:
    return validate.validate_dictconfig(config=config, default=EmbedConfig)


def _config_to_dict(config: DictConfig) -> dict[str, Any]:
    config_dict = omegaconf_utils.config_to_dict(config=config)
    # Make sure image_size is a tuple. OmegaConf can return a list even though a field
    # is typed as tuple.
    config_dict["image_size"] = tuple(config_dict["image_size"])
    return config_dict
