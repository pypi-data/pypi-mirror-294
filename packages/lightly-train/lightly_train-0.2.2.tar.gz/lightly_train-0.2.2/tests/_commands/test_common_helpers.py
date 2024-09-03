#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from pathlib import Path

import pytest
from omegaconf import MISSING
from pytest_mock import MockerFixture
from pytorch_lightning.accelerators.cpu import CPUAccelerator

from lightly_train._commands import common_helpers


def test_get_checkpoint_path(tmp_path: Path) -> None:
    out_file = tmp_path / "file.ckpt"
    out_file.touch()
    assert common_helpers.get_checkpoint_path(checkpoint=out_file) == out_file


def test_get_checkpoint_path__non_existing(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    with pytest.raises(FileNotFoundError):
        common_helpers.get_checkpoint_path(checkpoint=out_dir)


def test_get_checkpoint_path__non_file(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    out_dir.mkdir()
    with pytest.raises(ValueError):
        common_helpers.get_checkpoint_path(checkpoint=out_dir)


def test_get_out_path__nonexisting(tmp_path: Path) -> None:
    out_dir = tmp_path / "out"
    assert common_helpers.get_out_path(out=out_dir, overwrite=False) == out_dir


def test_get_out_path__existing__no_overwrite(tmp_path: Path) -> None:
    out_file = tmp_path / "file.txt"
    out_file.touch()
    with pytest.raises(ValueError):
        common_helpers.get_out_path(out=out_file, overwrite=False)


def test_get_out_path__existing_file__overwrite(tmp_path: Path) -> None:
    out_file = tmp_path / "file.txt"
    out_file.touch()
    assert common_helpers.get_out_path(out=out_file, overwrite=True) == out_file


def test_get_out_path__existing_dir__overwrite(tmp_path: Path) -> None:
    out_dir = tmp_path / "dir"
    out_dir.mkdir()
    with pytest.raises(ValueError):
        common_helpers.get_out_path(out=out_dir, overwrite=True)


def test_get_accelerator__set() -> None:
    """Test that same accelerator is returned if it is set."""
    assert common_helpers.get_accelerator(accelerator="cpu") == "cpu"
    accelerator = CPUAccelerator()
    assert common_helpers.get_accelerator(accelerator=accelerator) == accelerator


def test_get_default_out() -> None:
    assert common_helpers.get_default_out() == MISSING


def test_get_default_out__docker(mocker: MockerFixture) -> None:
    mocker.patch("os.environ", {"LIGHTLY_TRAIN_IS_DOCKER": "True"})
    assert common_helpers.get_default_out() == "/out"


def test_get_default_data() -> None:
    assert common_helpers.get_default_data() == MISSING


def test_get_default_data__docker(mocker: MockerFixture) -> None:
    mocker.patch("os.environ", {"LIGHTLY_TRAIN_IS_DOCKER": "True"})
    assert common_helpers.get_default_data() == "/data"


def test_get_out_dir(tmp_path: Path) -> None:
    assert (
        common_helpers.get_out_dir(out=tmp_path, resume=False, overwrite=False)
        == tmp_path
    )


def test_get_out_dir_nonexisting(tmp_path: Path) -> None:
    out_dir = tmp_path / "nonexisting"
    assert (
        common_helpers.get_out_dir(out=out_dir, resume=False, overwrite=False)
        == out_dir
    )


def test_get_out_dir__nondir(tmp_path: Path) -> None:
    out_dir = tmp_path / "file.txt"
    out_dir.touch()
    with pytest.raises(ValueError):
        common_helpers.get_out_dir(out=out_dir, resume=False, overwrite=False)


@pytest.mark.parametrize("resume", [True, False])
@pytest.mark.parametrize("overwrite", [True, False])
def test_get_out_dir__nonempty(tmp_path: Path, resume: bool, overwrite: bool) -> None:
    (tmp_path / "some_file.txt").touch()
    if resume or overwrite:
        assert (
            common_helpers.get_out_dir(out=tmp_path, resume=resume, overwrite=overwrite)
            == tmp_path
        )
    else:
        with pytest.raises(ValueError):
            common_helpers.get_out_dir(out=tmp_path, resume=resume, overwrite=overwrite)
