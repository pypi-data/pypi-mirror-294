# Copyright (c) 2024 Huawei Technologies Co., Ltd.
#
# openMind is licensed under Mulan PSL v2.
# You can use this software according to the terms and conditions of the Mulan PSL v2.
# You may obtain a copy of Mulan PSL v2 at:
#
#          http://license.coscl.org.cn/MulanPSL2
#
# THIS SOFTWARE IS PROVIDED ON AN "AS IS" BASIS, WITHOUT WARRANTIES OF ANY KIND,
# EITHER EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO NON-INFRINGEMENT,
# MERCHANTABILITY OR FIT FOR A PARTICULAR PURPOSE.
# See the Mulan PSL v2 for more details.

import enum
import os
from typing import Mapping, Optional, Sequence, Union

import openmind_hub
from ..hf.datasets_util import load_dataset_with_ctx
from ..utils import replace_invalid_characters
from ..utils.logging import get_logger

OM_DATASETS_CACHE = os.path.join(openmind_hub.OM_HOME, "datasets")

logger = get_logger()


class DownloadMode(enum.Enum):
    """How to treat existing datasets"""

    REUSE_DATASET_IF_EXISTS = "reuse_dataset_if_exists"
    FORCE_REDOWNLOAD = "force_redownload"


class OmDataset:
    @staticmethod
    def load_dataset(
        path: Optional[str] = None,
        name: Optional[str] = None,
        revision: Optional[str] = "main",
        split: Optional[str] = None,
        data_dir: Optional[str] = None,
        data_files: Optional[Union[str, Sequence[str], Mapping[str, Union[str, Sequence[str]]]]] = None,
        download_mode: Optional[DownloadMode] = DownloadMode.REUSE_DATASET_IF_EXISTS,
        cache_dir: Optional[str] = None,
        token: Optional[str] = None,
        dataset_info_only: Optional[bool] = False,
        trust_remote_code: bool = None,
        **config_kwargs,
    ):
        if not isinstance(path, str):
            raise ValueError(replace_invalid_characters(f"path must be `str` , but got {type(path)}"))

        is_local_path = os.path.exists(path)

        if not is_local_path and path.count("/") != 1:
            raise ValueError("The path should be in the form of `namespace/datasetname` or local path")
        elif is_local_path:
            logger.info("Using local dataset")
        else:
            try:
                openmind_hub.repo_info(repo_id=path, repo_type="dataset", token=token)
            except Exception:
                raise ValueError(
                    "The path is not valid `namespace/datasetname`, or not valid local path, or token is necessary for private repo"
                )

        download_mode = DownloadMode(download_mode or DownloadMode.REUSE_DATASET_IF_EXISTS)

        if not cache_dir:
            cache_dir = OM_DATASETS_CACHE

        with load_dataset_with_ctx(
            path=path,
            name=name,
            data_dir=data_dir,
            data_files=data_files,
            split=split,
            cache_dir=cache_dir,
            features=None,
            download_config=None,
            download_mode=download_mode.value,
            revision=revision,
            token=token,
            dataset_info_only=dataset_info_only,
            trust_remote_code=trust_remote_code,
            **config_kwargs,
        ) as dataset_res:
            return dataset_res
