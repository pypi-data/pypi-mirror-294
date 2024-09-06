#
# Copyright (c) Lightly AG and affiliates.
# All rights reserved.
#
# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.
#
from __future__ import annotations

import logging
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path

# Import old types for compatibility with omegaconf.
from typing import Optional

from lightly.data._helpers import VIDEO_EXTENSIONS
from omegaconf import MISSING, DictConfig
from tqdm import tqdm

from lightly_train import _logging
from lightly_train._commands import common_helpers
from lightly_train._configs import omegaconf_utils, validate
from lightly_train._configs.config import Config
from lightly_train.types import PathLike

logger = logging.getLogger(__name__)

FFMPEG_INSTALLATION_EXAMPLES = [
    "Ubuntu: sudo 'apt-get install ffmpeg'",
    "Mac: 'brew install ffmpeg'",
    "Other: visit https://ffmpeg.org/download.html",
]


def ffmpeg_is_installed() -> bool:
    logger.debug("Checking if ffmpeg is installed.")
    try:
        subprocess.run(["ffmpeg", "-version"], check=True, stdout=subprocess.PIPE)
        logger.debug("ffmpeg is installed.")
        return True
    except FileNotFoundError:
        logger.debug("Did not find ffmpeg installation.")
        return False


def assert_ffmpeg_is_installed() -> None:
    if not ffmpeg_is_installed():
        raise RuntimeError(
            f"ffmpeg is not installed! Please install using one of the following "
            f"options: {', '.join(FFMPEG_INSTALLATION_EXAMPLES)}"
        )


def extract_video_frames(
    data: PathLike,
    out: PathLike,
    overwrite: bool = False,
    frame_filename_format: str = "%09d.jpg",
    num_workers: None | int = None,
):
    """
    Extract frames from videos using ffmpeg.

    Args:
        data:
            Path to a directory containing video files.
        out:
            Output directory to save the extracted frames.
        overwrite:
            If True, existing frames are overwritten.
        frame_filename_format:
            Filename format for the extracted frames, passed as it is to ffmpeg.
        num_workers:
            Number of parallel calls to ffmpeg. If None, the number of workers is set to
            the number of available CPU cores.

    """
    # Set up logging.
    _logging.set_up_console_logging()
    logger.info(common_helpers.pretty_format_args(args=locals()))
    logger.info(f"Extracting frames from videos in '{data}'.")

    assert_ffmpeg_is_installed()

    num_workers = os.cpu_count() if num_workers is None else num_workers
    logger.debug(f"Using {num_workers} workers to extract frames.")
    out_dir = common_helpers.get_out_dir(out=out, resume=False, overwrite=overwrite)
    logger.info(f"Saving extracted frames to '{out_dir}'.")

    video_files = list(Path(data).rglob("*"))
    video_files = [f for f in video_files if f.suffix in VIDEO_EXTENSIONS]
    logger.debug(f"Found {len(video_files)} video files in '{data}'.")
    if num_workers is not None:
        num_workers = max(min(len(video_files), num_workers), 1)
    logger.info(
        f"Extracting frames from {len(video_files)} videos with {num_workers} calls to ffmpeg in parallel."
    )
    with ThreadPoolExecutor(max_workers=num_workers) as thread_pool:
        for _ in tqdm(
            thread_pool.map(
                lambda video_file: _extract_video(
                    video_path=video_file,
                    out=out_dir,
                    frame_filename_format=frame_filename_format,
                ),
                video_files,
            ),
            total=len(video_files),
            unit="videos",
        ):
            pass


@dataclass
class ExtactVideoFramesConfig(Config):
    data: str = MISSING
    out: str = MISSING
    overwrite: bool = False
    frame_filename_format: str = "%09d.jpg"
    num_workers: Optional[int] = None


def extract_video_frames_from_config(config: DictConfig) -> None:
    logger.debug(f"Extracting video frames with config: {config}")
    config = _validate_config(config=config)
    config_dict = omegaconf_utils.config_to_dict(config=config)
    extract_video_frames(**config_dict)


def _validate_config(config: DictConfig) -> DictConfig:
    return validate.validate_dictconfig(config=config, default=ExtactVideoFramesConfig)


def _extract_video(video_path: Path, out: Path, frame_filename_format: str):
    """
    Extract frames from a video file using ffmpeg.

    Args:
        video_path:
            Path to the video file.
        out:
            Output directory to save the extracted frames.
        frame_filename_format:
            Filename format for the extracted frames.

    """
    logger.debug(f"Extracting frames from '{video_path}'.")
    out.mkdir(parents=True, exist_ok=True)
    video_output_dir = out / video_path.stem
    video_output_dir.mkdir(parents=True, exist_ok=True)
    logger.debug(f"Saving extracted frames to '{video_output_dir}'.")
    frame_path = video_output_dir / frame_filename_format
    cmd = [
        "ffmpeg",
        "-i",
        str(video_path),
        str(frame_path),
    ]
    try:
        logger.debug(f"Running ffmpeg command: {cmd}")
        subprocess.run(
            cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
        )
    except subprocess.CalledProcessError as e:
        raise RuntimeError(
            f"Error extracting frames from '{video_path}': {e.stderr.decode('utf-8')}"
        )
