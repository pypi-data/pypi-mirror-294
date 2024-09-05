# Copyright 2018 The HuggingFace Inc. team.
# Copyright (c) Huawei Technologies Co., Ltd. 2023-2023, All rights reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" Class Register Module For Pipeline."""
from typing import Any, Dict, List, Optional, Tuple, Union

from ..utils.import_utils import get_framework
from ..utils.generic import replace_invalid_characters


class PipelineRegistry:
    """When user customizes the pipeline object, call this interface to register."""

    def __init__(self) -> None:
        self.pipeline_register = None

    def check_framework(self):
        """set the framework used by the pipeline registration method"""
        framework = get_framework()
        if framework == "ms":
            from mindformers.pipeline.registry_constant import PIPELINE_REGISTRY

            self.pipeline_register = PIPELINE_REGISTRY
        elif framework == "pt":
            from transformers.pipelines import PIPELINE_REGISTRY

            self.pipeline_register = PIPELINE_REGISTRY
        else:
            raise RuntimeError("The current environment does not have a framework installed.")

    def get_supported_tasks(self) -> List[str]:
        """return the supported tasks"""
        if self.pipeline_register is None:
            self.check_framework()
        return self.pipeline_register.get_supported_tasks()

    def check_task(self, task: str) -> Tuple[str, Dict, Any]:
        """check whether the taks is in the supported_task list or not"""
        if self.pipeline_register is None:
            self.check_framework()
        return self.pipeline_register.check_task(task)

    def register_pipeline(
        self,
        task: str,
        pipeline_class: type,
        pt_model: Optional[Union[type, Tuple[type]]] = None,
        ms_model: Optional[Union[type, Tuple[type]]] = None,
        default: Optional[Dict] = None,
        task_type: Optional[str] = None,
    ) -> None:
        """Register custom pipeline objects"""
        framework = get_framework()
        if self.pipeline_register is None:
            self.check_framework()
        if framework == "ms" and ms_model is not None:
            self.pipeline_register.register_pipeline(
                task=task, pipeline_class=pipeline_class, ms_model=ms_model, default=default, task_type=task_type
            )
        elif framework == "pt" and pt_model is not None:
            self.pipeline_register.register_pipeline(
                task=task, pipeline_class=pipeline_class, pt_model=pt_model, default=default, type=task_type
            )
        else:
            error_msg = f"Please provide the {framework}_model that is supported by the framework {framework}"
            raise RuntimeError(replace_invalid_characters(error_msg))

    def to_dict(self):
        if self.pipeline_register is None:
            self.check_framework()
        return self.pipeline_register.to_dict()
