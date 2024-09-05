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

import os
import re
from typing import Any, Dict, Optional, Tuple, Union
from ..utils.hub import snapshot_download
from ..utils.patch_utils import _apply_patches
from ..utils.exceptions import FrameworkNotSupportedError
from ..pipelines.pipeline_registry import PipelineRegistry
from ..utils.generic import replace_invalid_characters


SUPPORTED_FRAMEWORKS = ("pt", "ms")
PIPELINE_REGISTRY = PipelineRegistry()


def pipeline_patch(change_dict=None):
    # Pipeline task patch
    import copy
    import transformers
    from transformers import AutoModel
    from transformers.pipelines import SUPPORTED_TASKS, TASK_ALIASES, PIPELINE_REGISTRY
    from transformers.pipelines.base import PipelineRegistry
    from .chatglm_pipeline import ChatGLMPipeline

    ori_supported_tasks = copy.deepcopy(SUPPORTED_TASKS)
    ori_pipeline_registry = copy.deepcopy(PIPELINE_REGISTRY)
    PATCHED_SUPPORTED_TASKS = copy.deepcopy(SUPPORTED_TASKS)
    PATCHED_SUPPORTED_TASKS["chat"] = {"impl": ChatGLMPipeline, "pt": (AutoModel,)}
    for key in PATCHED_SUPPORTED_TASKS.keys():
        if key in change_dict.keys():
            PATCHED_SUPPORTED_TASKS[key]["default"] = change_dict[key]
        else:
            PATCHED_SUPPORTED_TASKS[key]["default"] = {}
    PATCHED_PIPELINE_REGISTRY = PipelineRegistry(supported_tasks=PATCHED_SUPPORTED_TASKS, task_aliases=TASK_ALIASES)
    patch_list = [
        ("SUPPORTED_TASKS", PATCHED_SUPPORTED_TASKS),
        ("PIPELINE_REGISTRY", PATCHED_PIPELINE_REGISTRY),
    ]
    _apply_patches(patch_list, transformers.pipelines)
    return ori_supported_tasks, ori_pipeline_registry


def _get_default_model_and_revision(
    targeted_task: Dict, framework: Optional[str], task_options: Optional[Any]
) -> Union[str, Tuple[str, str]]:
    defaults = targeted_task["default"]
    if task_options:
        if task_options not in defaults:
            raise ValueError(
                replace_invalid_characters(f"The task does not provide any default models for options {task_options}")
            )
        default_models = defaults[task_options]["model"]
    elif "model" in defaults:
        default_models = targeted_task["default"]["model"]
    else:
        raise ValueError('The task defaults can\'t be correctly selected. You probably meant "translation_XX_to_YY"')

    if framework is None:
        framework = "pt"

    if framework not in SUPPORTED_FRAMEWORKS:
        raise FrameworkNotSupportedError(framework=framework)

    return default_models[framework]


def check_task(task: str) -> Tuple[str, Dict, Any]:
    return PIPELINE_REGISTRY.check_task(task)


def download_from_repo(repo_id, revision=None, cache_dir=None, force_download=False):
    if not os.path.exists(repo_id):
        local_path = snapshot_download(
            repo_id,
            revision=revision,
            cache_dir=cache_dir,
            force_download=force_download,
        )
    else:
        local_path = repo_id
    return local_path


def get_task(model_name):
    readme_file = os.path.join(model_name, "README.md")
    if os.path.exists(readme_file):
        with open(readme_file, "r") as file:
            content = file.read()
            pipeline_tag = re.search(r"pipeline_tag:\s?(([a-z]*-)*[a-z]*)", content)
            if pipeline_tag:
                task = pipeline_tag.group(1)
            else:
                raise RuntimeError("Pipeline tag not found in README.md")
    else:
        raise RuntimeError("README.md not found in the model path, please give the task.")
    return task
