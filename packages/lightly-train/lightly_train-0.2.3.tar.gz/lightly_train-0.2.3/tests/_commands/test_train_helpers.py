#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest
import torch
from lightly.transforms import SimCLRTransform
from pytorch_lightning.strategies.ddp import DDPStrategy
from torch.utils.data import Dataset
from torchvision.datasets import FakeData
from torchvision.transforms import ToTensor

from lightly_train._commands import train_helpers
from lightly_train._methods.simclr import SimCLR
from lightly_train._models import package_helpers
from lightly_train._models.custom.custom import CustomFeatureExtractor
from lightly_train._optim.adamw_args import AdamWArgs
from lightly_train._scaling import IMAGENET_SIZE, ScalingInfo

from .. import helpers
from ..helpers import DummyCustomModel

REPRESENTATIVE_MODEL_NAMES = [
    "timm/vit_tiny_patch16_224",
    "timm/resnet18",
    "torchvision/convnext_tiny",
    "torchvision/resnet18",
]


def test_get_transform__method() -> None:
    assert isinstance(
        train_helpers.get_transform(method="simclr", transform_args=None),
        SimCLRTransform,
    )


def test_get_transform__method_and_transform_dict() -> None:
    transform = train_helpers.get_transform(
        method="simclr", transform_args={"normalize": None}
    )
    assert isinstance(transform, SimCLRTransform)
    assert isinstance(transform.transforms[0].transform.transforms[-1], ToTensor)


def test_get_dataset__path(tmp_path: Path) -> None:
    (tmp_path / "img.jpg").touch()
    _ = train_helpers.get_dataset(data=tmp_path, transform=None)


def test_get_dataset__path__nonexisting(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        train_helpers.get_dataset(data=tmp_path / "nonexisting", transform=None)


def test_get_dataset__path__nondir(tmp_path: Path) -> None:
    file = tmp_path / "img.jpg"
    file.touch()
    with pytest.raises(ValueError):
        train_helpers.get_dataset(data=file, transform=None)


def test_get_dataset__path__empty(tmp_path: Path) -> None:
    with pytest.raises(ValueError):
        train_helpers.get_dataset(data=tmp_path, transform=None)


def test_get_dataset__dataset() -> None:
    dataset = torch.utils.data.TensorDataset(torch.rand(10, 3, 224, 224))
    dataset_1 = train_helpers.get_dataset(data=dataset, transform=None)
    assert dataset == dataset_1


def test_get_dataloader():
    dataset = torch.utils.data.TensorDataset(torch.rand(10, 3, 224, 224))
    dataloader = train_helpers.get_dataloader(
        dataset=dataset,
        global_batch_size=2,
        world_size=1,
        num_workers=0,
        loader_args=None,
    )
    assert len(dataloader) == 5
    batches = list(dataloader)
    assert len(batches) == 5
    assert all(batch[0].shape == (2, 3, 224, 224) for batch in batches)


@pytest.mark.parametrize("model_name", REPRESENTATIVE_MODEL_NAMES)
@pytest.mark.parametrize("embed_dim", [None, 64])
@pytest.mark.parametrize("model_args", [None, {"num_classes": 42}])
def test_get_embedding_model(
    model_name: str, embed_dim: int | None, model_args: dict[str, Any] | None
) -> None:
    if model_name.startswith("timm/"):
        pytest.importorskip("timm")
    x = torch.rand(1, 3, 224, 224)
    model = package_helpers.get_model(model_name, model_args=model_args)
    embedding_model = train_helpers.get_embedding_model(model, embed_dim=embed_dim)
    embedding = embedding_model.forward(x)
    assert embedding.shape == (1, embedding_model.embed_dim, 1, 1)
    if (
        model_args is not None
        and "num_classes" in model_args
        and not model_name.startswith("torchvision/")
    ):
        assert model.num_classes == model_args["num_classes"]


@pytest.mark.parametrize("embed_dim", [None, 64])
def test_get_embedding_model__custom(embed_dim: int | None) -> None:
    model = package_helpers.get_model(model=DummyCustomModel())
    x = torch.rand(1, 3, 224, 224)
    embedding_model = train_helpers.get_embedding_model(model, embed_dim=embed_dim)
    assert isinstance(embedding_model.feature_extractor, CustomFeatureExtractor)
    embedding = embedding_model.forward(x)
    assert embedding.shape == (1, embedding_model.embed_dim, 1, 1)


def test_get_trainer(tmp_path: Path) -> None:
    model = package_helpers.get_model("torchvision/resnet18")
    embedding_model = train_helpers.get_embedding_model(model, embed_dim=64)
    trainer = train_helpers.get_trainer(
        out=tmp_path,
        model=model,
        embedding_model=embedding_model,
        epochs=1,
        accelerator="cpu",
        strategy="auto",
        devices="auto",
        num_nodes=1,
        precision=32,
        log_every_n_steps=1,
        trainer_args=None,
    )
    assert trainer.max_epochs == 1


def test_get_lightning_logging_interval() -> None:
    assert (
        train_helpers.get_lightning_logging_interval(dataset_size=10, batch_size=10)
        == 1
    )
    assert (
        train_helpers.get_lightning_logging_interval(dataset_size=10, batch_size=2) == 5
    )
    assert (
        train_helpers.get_lightning_logging_interval(dataset_size=1000, batch_size=10)
        == 50
    )
    assert (
        train_helpers.get_lightning_logging_interval(dataset_size=1, batch_size=10) == 1
    )


def test_get_lightning_logging_interval__fails_for_nonpositive_inputs() -> None:
    with pytest.raises(
        ValueError,
        match=r"Dataset size \(0\) and batch size \(10\) must be positive integers.",
    ):
        train_helpers.get_lightning_logging_interval(dataset_size=0, batch_size=10)
    with pytest.raises(
        ValueError,
        match=r"Dataset size \(10\) and batch size \(0\) must be positive integers.",
    ):
        train_helpers.get_lightning_logging_interval(dataset_size=10, batch_size=0)
    with pytest.raises(
        ValueError,
        match=r"Dataset size \(-10\) and batch size \(10\) must be positive integers.",
    ):
        train_helpers.get_lightning_logging_interval(dataset_size=-10, batch_size=10)
    with pytest.raises(
        ValueError,
        match=r"Dataset size \(10\) and batch size \(-10\) must be positive integers.",
    ):
        train_helpers.get_lightning_logging_interval(dataset_size=10, batch_size=-10)


_DDP_STRATEGY = DDPStrategy()


@pytest.mark.parametrize(
    "strategy, accelerator, devices, expected",
    [
        ("ddp", "auto", "auto", "ddp"),
        (_DDP_STRATEGY, "auto", "auto", _DDP_STRATEGY),
        ("auto", "cpu", "auto", "auto"),  # CPU should not use DDP by default
        ("auto", "cpu", 1, "auto"),
        ("auto", "cpu", 2, "ddp_find_unused_parameters_true"),
        ("auto", "gpu", 1, "auto"),
        ("auto", "gpu", 2, "ddp_find_unused_parameters_true"),
    ],
)
def test_get_strategy(
    strategy: str | DDPStrategy,
    accelerator: str,
    devices: str | int,
    expected: str | DDPStrategy,
) -> None:
    if accelerator == "gpu":
        if not torch.cuda.is_available():
            pytest.skip("No GPU available.")
        assert isinstance(devices, int)
        if devices > torch.cuda.device_count():
            pytest.skip("Not enough GPUs available.")

    assert (
        train_helpers.get_strategy(
            strategy=strategy, accelerator=accelerator, devices=devices
        )
        == expected
    )


@pytest.mark.parametrize(
    "optim_args, expected",
    [
        (None, AdamWArgs()),
        ({}, AdamWArgs()),
        ({"lr": 0.1, "betas": [0.2, 0.3]}, AdamWArgs(lr=0.1, betas=(0.2, 0.3))),
    ],
)
def test_get_optimizer_args(
    optim_args: dict[str, Any] | None, expected: AdamWArgs
) -> None:
    method = helpers.get_method()
    assert (
        train_helpers.get_optimizer_args(optim_args=optim_args, method=method)
        == expected
    )


@pytest.mark.parametrize(
    "dataset, expected",
    [
        (FakeData(size=2), ScalingInfo(dataset_size=2)),
        (iter(FakeData(size=2)), ScalingInfo(dataset_size=IMAGENET_SIZE)),
    ],
)
def test_get_scaling_info(dataset: Dataset, expected: ScalingInfo) -> None:
    assert train_helpers.get_scaling_info(dataset=dataset) == expected


def test_get_method() -> None:
    embedding_model = helpers.get_embedding_model()
    method = train_helpers.get_method(
        method="simclr",
        method_args={"temperature": 0.2},
        scaling_info=ScalingInfo(dataset_size=2),
        embedding_model=embedding_model,
        batch_size_per_device=1,
    )
    assert isinstance(method, SimCLR)
    assert method.method_args.temperature == 0.2
    assert method.batch_size_per_device == 1
    assert method.embedding_model == embedding_model
