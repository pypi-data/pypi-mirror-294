#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
import warnings

# Ignore warning raised by torchvision/convnext models.


def filter_train_warnings() -> None:
    filter_warnings()
    # PytorchLightning warnings.
    warnings.filterwarnings(
        "ignore",
        message=(
            "Consider setting `persistent_workers=True` in 'train_dataloader' to speed "
            "up the dataloader worker initialization."
        ),
    )
    warnings.filterwarnings(
        "ignore",
        message="The verbose parameter is deprecated. Please use get_last_lr()",
    )
    # Ignore warning as we handle it with overwrite flag.
    warnings.filterwarnings(
        "ignore",
        message="Checkpoint directory .* exists and is not empty.",
    )
    # Ignore warning as we handle it with overwrite flag.
    warnings.filterwarnings(
        "ignore",
        message=(
            "Experiment logs directory .* exists and is not empty. Previous log files "
            "in this directory can be modified when the new ones are saved!"
        ),
    )


def filter_embed_warnings() -> None:
    filter_warnings()
    warnings.filterwarnings(
        "ignore", message="Consider setting `persistent_workers=True`"
    )


def filter_export_warnings() -> None:
    filter_warnings()


def filter_warnings() -> None:
    # PyTorch Lighting warnings
    warnings.filterwarnings("ignore", message="pkg_resources is deprecated as an API")
    warnings.filterwarnings("ignore", message="Deprecated call to `pkg_resources")
    warnings.filterwarnings(
        "ignore",
        message=(
            "torch.nn.utils.weight_norm is deprecated in favor of "
            "torch.nn.utils.parametrizations.weight_norm."
        ),
    )

    # Torch ConvNext warning
    warnings.filterwarnings(
        "ignore", message="Grad strides do not match bucket view strides"
    )
