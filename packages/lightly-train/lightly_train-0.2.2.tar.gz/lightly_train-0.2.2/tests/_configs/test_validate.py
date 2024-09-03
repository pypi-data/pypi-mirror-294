#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from typing import Any

import pytest
from omegaconf import DictConfig, OmegaConf

from lightly_train._commands.train import TrainConfig
from lightly_train._configs import validate
from lightly_train._methods.simclr import SimCLRArgs
from lightly_train.errors import (
    ConfigError,
    ConfigMissingKeysError,
    ConfigUnknownKeyError,
    ConfigValidationError,
)


def _get_valid_dictconfig() -> DictConfig:
    return OmegaConf.create(_get_valid_dict())


def _get_valid_dict() -> dict[str, Any]:
    return {
        "out": "output",
        "data": "data",
        "model": "model",
        "method": "method",
        "embed_dim": 128,
        "resume": True,
        "overwrite": True,
        "loader_args": {"key": "value"},
        "trainer_args": {"key": "value"},
        "transform_args": {"key": "value"},
        "model_args": {"key": "value"},
    }


@pytest.mark.parametrize(
    "config_fn, validate_fn",
    [
        (_get_valid_dictconfig, validate.validate_dictconfig),
        (_get_valid_dict, validate.validate_dict),
    ],
)
class TestValidate:
    def test_validate(self, config_fn, validate_fn) -> None:
        config = config_fn()
        validated = validate_fn(config=config, default=TrainConfig)
        assert validated.embed_dim == 128

    def test_validate__unknown_key(self, config_fn, validate_fn) -> None:
        config = config_fn()
        config["unknown_key"] = "value"
        with pytest.raises(
            ConfigUnknownKeyError,
            match="Unknown key in config: 'unknown_key'",
        ):
            validate_fn(config=config, default=TrainConfig)

    def test_validate__invalid_type(self, config_fn, validate_fn) -> None:
        config = config_fn()
        config["embed_dim"] = "invalid"  # should be int
        with pytest.raises(
            ConfigValidationError,
            match=(
                "Error for key 'embed_dim' in config: Value 'invalid' of type 'str' could "
                "not be converted to Integer"
            ),
        ):
            validate_fn(config=config, default=TrainConfig)

    def test_validate__config_error(self, config_fn, validate_fn) -> None:
        with pytest.raises(
            ConfigError,
            match="Error in config: Cannot merge DictConfig with ListConfig",
        ):
            # Pass list instead of dict as config.
            validate_fn(config=[], default=TrainConfig)  # type: ignore

    def test_validate__missing_keys(self, config_fn, validate_fn) -> None:
        config = OmegaConf.create({})
        with pytest.raises(ConfigMissingKeysError) as ex_info:
            validate_fn(config=config, default=TrainConfig)

        assert "'out'" in str(ex_info.value)  # Required key
        assert "'embed_dim'" not in str(ex_info.value)  # Optional key


def test_validate_dict__none() -> None:
    # Use SimCLRArgs as default because TrainArgs will always raise an error as it has
    # required keys.
    validated = validate.validate_dict(config=None, default=SimCLRArgs())
    assert validated == SimCLRArgs()
