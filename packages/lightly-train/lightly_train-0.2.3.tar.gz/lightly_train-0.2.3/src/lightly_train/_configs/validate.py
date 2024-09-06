#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

from omegaconf import DictConfig, OmegaConf
from omegaconf import errors as omegaconf_errors
from typing_extensions import Any, Type, TypeVar

from lightly_train._configs import omegaconf_utils
from lightly_train._configs.config import Config
from lightly_train.errors import (
    ConfigError,
    ConfigMissingKeysError,
    ConfigUnknownKeyError,
    ConfigValidationError,
)


def validate_dictconfig(
    config: DictConfig,
    default: Type[Config] | Config,
) -> DictConfig:
    """Validates a config against a default config.

    Returns:
        The default config merged with the input config.
    """
    # Create a structured config object from the default class.
    default = OmegaConf.structured(default)

    # Validate that the config object conforms to the default config.
    try:
        merged = OmegaConf.merge(default, config)
    except omegaconf_errors.ConfigKeyError as ex:
        raise ConfigUnknownKeyError(f"Unknown key in config: '{ex.full_key}'")
    except omegaconf_errors.ValidationError as ex:
        raise ConfigValidationError(
            f"Error for key '{ex.full_key}' in config: {_error_msg(ex)}"
        )
    except omegaconf_errors.OmegaConfBaseException as ex:
        # Catch all other OmegaConf exceptions
        raise ConfigError(f"Error in config: {ex}")

    # Make mypy happy.
    assert isinstance(merged, DictConfig)

    # Check for missing keys.
    missing_keys = OmegaConf.missing_keys(merged)
    if missing_keys:
        raise ConfigMissingKeysError(f"Missing keys in config: {missing_keys}")
    return merged


_Config = TypeVar("_Config", bound=Config)


def validate_dict(
    config: dict[str, Any] | None,
    default: Type[_Config] | _Config,
) -> _Config:
    """Validates a config against a default config.

    Returns:
        The default config merged with the input config.
    """
    config = {} if config is None else config
    validated = validate_dictconfig(config=OmegaConf.create(config), default=default)
    assert isinstance(validated, DictConfig)  # make mypy happy
    # Create Config object from DictConfig.
    kwargs = omegaconf_utils.config_to_dict(config=validated)
    config_cls = default if isinstance(default, type) else default.__class__
    return config_cls(**kwargs)


def _error_msg(ex: omegaconf_errors.OmegaConfBaseException) -> str:
    if ex.msg is None:
        return ""

    # Omegaconf error messages are multiline and look like this:
    #
    # Value 'invalid' of type 'str' could not be converted to Integer
    #   full_key: embed_dim
    #   object_type=TrainConfig
    #
    # We only want to show the first line as the other lines are not useful for the
    # user.
    lines = ex.msg.splitlines()
    if lines:
        return lines[0]
    else:
        return ""
