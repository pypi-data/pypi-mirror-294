#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from pathlib import Path

import pytest
from omegaconf import OmegaConf
from pytest_mock import MockerFixture

from lightly_train._commands import embed
from lightly_train._embedding.embedding_format import EmbeddingFormat

from .. import helpers


@pytest.mark.parametrize("num_workers", [0, 2])
def test_embed(tmp_path: Path, num_workers: int) -> None:
    out = tmp_path / "embeddings.csv"
    data = tmp_path / "data"
    checkpoint = tmp_path / "checkpoints" / "last.ckpt"
    helpers.create_images(image_dir=data, n=2)
    helpers.get_checkpoint().save(path=checkpoint)
    embed.embed(
        out=out,
        data=data,
        checkpoint=checkpoint,
        format=EmbeddingFormat.CSV,
        batch_size=1,
        num_workers=num_workers,
        accelerator="cpu",
    )
    lines = out.read_text().splitlines()
    assert lines[0] == "filename,embedding_0,embedding_1"
    assert lines[1].startswith("0.png,")
    assert lines[2].startswith("1.png,")


def test_embed__overwrite_true(tmp_path: Path) -> None:
    out = tmp_path / "embeddings.csv"
    out.touch()
    data = tmp_path / "data"
    checkpoint = tmp_path / "checkpoints" / "last.ckpt"
    helpers.create_images(image_dir=data, n=1)
    helpers.get_checkpoint().save(path=checkpoint)
    embed.embed(
        out=out,
        data=data,
        checkpoint=checkpoint,
        format=EmbeddingFormat.CSV,
        batch_size=1,
        num_workers=0,
        accelerator="cpu",
        overwrite=True,
    )
    # Assert file was overwritten
    assert out.read_text()


def test_embed__varying_image_resolution(tmp_path: Path) -> None:
    out = tmp_path / "embeddings.csv"
    out.touch()

    data = tmp_path / "data"
    data.mkdir(exist_ok=True, parents=True)
    helpers.create_image(path=data / "img.jpg", width=300, height=224)
    helpers.create_image(path=data / "img_2.jpg", width=224, height=300)

    checkpoint = tmp_path / "checkpoints" / "last.ckpt"
    helpers.get_checkpoint().save(path=checkpoint)

    embed.embed(
        out=out,
        data=data,
        checkpoint=checkpoint,
        format=EmbeddingFormat.CSV,
        batch_size=2,
        num_workers=0,
        accelerator="cpu",
        overwrite=True,
    )
    # Assert file was overwritten
    assert out.read_text()


def test_embed__overwrite_false(tmp_path: Path) -> None:
    out = tmp_path / "embeddings.csv"
    out.touch()
    with pytest.raises(ValueError, match=f"Output '{out}' already exists!"):
        embed.embed(
            out=out,
            data=tmp_path / "data",
            checkpoint=tmp_path / "last.ckpt",
            format=EmbeddingFormat.CSV,
            batch_size=1,
            num_workers=0,
            accelerator="cpu",
            overwrite=False,
        )


def test_embed__invalid_format(tmp_path: Path) -> None:
    with pytest.raises(
        ValueError,
        # Wildcard to match the full error message and avoid test failing everytime
        # a new format is added.
        match=(
            r"Invalid embedding format: 'invalid_format'. Valid formats are: "
            r"\['csv', 'lightly_csv', .*\]"
        ),
    ):
        embed.embed(
            out=tmp_path / "embeddings.csv",
            data=tmp_path / "data",
            checkpoint=tmp_path / "last.ckpt",
            format="invalid_format",
        )


def test_embed_from_config(tmp_path: Path) -> None:
    out = tmp_path / "embeddings.csv"
    data = tmp_path / "data"
    checkpoint = tmp_path / "checkpoints" / "last.ckpt"
    helpers.create_images(image_dir=data, n=2)
    helpers.get_checkpoint().save(path=checkpoint)
    embed.embed_from_config(
        OmegaConf.create(
            {
                "out": str(out),
                "data": str(data),
                "checkpoint": str(checkpoint),
                "format": "csv",
                "num_workers": 2,
                "accelerator": "cpu",
            }
        )
    )


@pytest.mark.parametrize(
    "image_size, expected",
    [
        (128, (128, 128)),
        ("[128,224]", (128, 224)),
    ],
)
def test_embed_from_config__image_size(
    image_size: int | str, expected: tuple[int, int], mocker: MockerFixture
) -> None:
    """Tests that image_size is correctly parsed and passed as a tuple[int, int]."""
    config = OmegaConf.from_cli(
        [
            "out=out",
            "data=data",
            "checkpoint=checkpoint",
            f"image_size={image_size}",
            "format=csv",
        ]
    )
    mock_embed = mocker.patch.object(embed, "embed")
    embed.embed_from_config(config)
    assert mock_embed.call_args.kwargs["image_size"] == expected
