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

from typing import Literal, Optional

from ..models.auto import AutoTokenizer
from ..utils import is_transformers_available, is_mindformers_available, get_framework
from ..utils.exceptions import FrameworkNotSupportedError, PipelinePackageNotFoundError
from ..pipelines.pipeline_registry import PipelineRegistry
from .pipeline_utils import (
    download_from_repo,
    pipeline_patch,
    _get_default_model_and_revision,
    check_task,
    get_task,
)
from ..utils.patch_utils import _apply_patches
from ..utils.generic import replace_invalid_characters


SUPPORTED_TASK_PATCH_DICT = {
    "text-classification": {
        "model": {"pt": ("PyTorch-NPU/distilbert_base_uncased_finetuned_sst_2_english", "5a5cb27")}
    },
    "question-answering": {"model": {"pt": ("PyTorch-NPU/roberta_base_squad2", "ba973aa")}},
    "table-question-answering": {"model": {"pt": ("PyTorch-NPU/tapas_base_finetuned_wtq", "17e5ded")}},
    "fill-mask": {"model": {"pt": ("PyTorch-NPU/bert_base_uncased", "42ad83b")}},
    "summarization": {"model": {"pt": ("PyTorch-NPU/bart_large_cnn", "b39bb57")}},
    "text-generation": {"model": {"pt": ("Baichuan/Baichuan2_7b_chat_pt", "ca161b7")}},
    "zero-shot-image-classification": {"model": {"pt": ("PyTorch-NPU/siglip_so400m_patch14_384", "b4099dd")}},
    "chat": {"model": {"pt": ("PyTorch-NPU/chatglm2_6b", "8e0fda5")}},
}

SUPPORTED_FRAMEWORKS = ("pt", "ms")
PIPELINE_REGISTRY = PipelineRegistry()


def pipeline(
    task: Optional[str] = None,
    model=None,
    config=None,
    tokenizer=None,
    feature_extractor=None,
    image_processor=None,
    framework: Optional[Literal["pt", "ms"]] = None,
    **kwargs,
):
    """
    Build a pipeline instance.
    Belowing docstring is mostly adapted from transformers.pipelines.pipeline

    Args:
        task:
            The task defining which pipeline will be returned.
        model:
            The model that will be used by the pipeline to make predictions.
            This can be a model identifier or an actual instance of a pretrained model.
            If not provided, the default for the `task` will be loaded.
        config:
            The configuration that will be used by the pipeline to instantiate
            the model. This can be a model identifier or an actual pretrained model
            configuration.
        tokenizer:
            The tokenizer that will be used by the pipeline to encode data for
            the model. This can be a model identifier or an actual pretrained tokenizer.
        feature_extractor:
            The feature extractor that will be used by the pipeline to encode data for
            the model. This can be a model identifier or an actual pretrained
             feature extractor.
        image_processor:
            The image_processor that will be used by the pipeline.
        framework (`str`, *optional*):
            The framework to use, either `"pt"` for PyTorch or "ms" for mindspore.
            The specified framework must be installed.
        kwargs:
            Additional keyword arguments passed along to the specific pipeline init.
            e.g. for transformers pipeline:
                revision (`str`, *optional*, defaults to `"main"`):
                    When passing a task name or a string model identifier:
                    The specific model version to use. It can be a branch name,
                    a tag name, or a commit id, since we use a git-based system for
                    storing models and other artifacts on openmind hub, so `revision`
                     can be any identifier allowed by git.
                use_fast (`bool`, *optional*, defaults to `True`):
                    Whether to use a Fast tokenizer if possible
                    (a [`PreTrainedTokenizerFast`]).
                device (`int` or `str` or `torch.device`):
                    Defines the device (*e.g.*, `"cpu"`, `"npu:0"`) on which this pipeline will be allocated.
                device_map (`str` or `Dict[str, Union[int, str, torch.device]`,
                *optional*):
                    Sent directly as `model_kwargs` (just a simpler shortcut).
                    When `accelerate` library is present, set `device_map="auto"` to
                    compute the most optimized `device_map` automatically.
                    Do not use `device_map` AND `device` at the same time as they will
                    conflict.
                torch_dtype (`str` or `torch.dtype`, *optional*):
                    Sent directly as `model_kwargs` (just a simpler shortcut) to use
                    the available precision for this model
                    (`torch.float16`, `torch.bfloat16`, ... or `"auto"`).
                trust_remote_code (`bool`, *optional*, defaults to `False`):
                    Whether to allow for custom code defined on the Hub in their own
                    modeling, configuration, tokenization or even pipeline files.
                    This option should only be set to `True` for repositories you trust
                    and in which you have read the code, as it will execute code present
                     on the Hub on your local machine.
                model_kwargs (`Dict[str, Any]`, *optional*):
                    Additional dictionary of keyword arguments passed along to the
                    model's `from_pretrained(...,**model_kwargs)` function.

    Returns:
        A suitable pipeline for the task.

    Examples:

    ```python
    >>> from openmind import pipeline

    >>> # will use transformers pipeline if not specified
    >>> pipeline_ins = pipeline("sentiment-analysis")

    >>> # if you want to use mindspore pipeline
    >>> pipeline_ins = pipeline("sentiment-analysis", framework="ms")
    ```
    """
    ORI_SUPPORTED_TASKS = None
    ORI_PIPELINE_REGISTRY = None
    if is_transformers_available():
        ORI_SUPPORTED_TASKS, ORI_PIPELINE_REGISTRY = pipeline_patch(change_dict=SUPPORTED_TASK_PATCH_DICT)

    try:
        if task is None and model is None:
            raise RuntimeError(
                "Impossible to instantiate a pipeline without either a task or a model being specified. "
                "Please provide a task class or a model"
            )

        if model is None and tokenizer is not None:
            raise RuntimeError(
                "Impossible to instantiate a pipeline with tokenizer specified but not the model as the provided tokenizer"
                " may not be compatible with the default model. Please provide a PreTrainedModel class or a"
                " path/identifier to a pretrained model when providing tokenizer."
            )

        if model is None and feature_extractor is not None:
            raise RuntimeError(
                "Impossible to instantiate a pipeline with feature_extractor specified but not the model as the provided"
                " feature_extractor may not be compatible with the default model. Please provide a PreTrainedModel class"
                " or a path/identifier to a pretrained model when providing feature_extractor."
            )

        revision = kwargs.get("revision", None)
        cache_dir = kwargs.get("cache_dir", None)
        force_download = kwargs.get("force_download", False)
        use_auth_token = kwargs.get("use_auth_token", None)
        trust_remote_code = kwargs.get("trust_remote_code", None)
        _commit_hash = kwargs.get("_commit_hash", None)
        torch_dtype = kwargs.get("torch_dtype", None)

        if task is not None and model is None:
            normalized_task, targeted_task, task_options = check_task(task)
            model, default_revision = _get_default_model_and_revision(targeted_task, framework, task_options)

        if isinstance(model, str):
            model_name_or_path = download_from_repo(
                model, revision=revision, cache_dir=cache_dir, force_download=force_download
            )
        else:
            model_name_or_path = model

        if task is None:
            if isinstance(model, str):
                if is_transformers_available():
                    task = get_task(model_name_or_path)
                elif is_mindformers_available():
                    raise RuntimeError("Must provide task and model under the mindspore framework.")
            else:
                raise RuntimeError(
                    replace_invalid_characters(
                        "Inferring the task automatically requires to check the hub with a repo_id defined as a `str`. "
                        f"{model} is not a valid model_id."
                    )
                )

        if tokenizer is not None:
            if isinstance(tokenizer, str):
                tokenizer_name_or_path = download_from_repo(
                    tokenizer, revision=revision, cache_dir=cache_dir, force_download=force_download
                )
            else:
                tokenizer_name_or_path = tokenizer
        else:
            if (task == "text-generation" or task == "text_generation") and isinstance(model, str):
                tokenizer_kwargs = {
                    "revision": revision,
                    "token": use_auth_token,
                    "trust_remote_code": trust_remote_code,
                    "_commit_hash": _commit_hash,
                    "torch_dtype": torch_dtype,
                }
                tokenizer_name_or_path = AutoTokenizer.from_pretrained(model, **tokenizer_kwargs)
            else:
                tokenizer_name_or_path = tokenizer

        if isinstance(config, str):
            config_name_or_path = download_from_repo(
                config, revision=revision, cache_dir=cache_dir, force_download=force_download
            )
        else:
            config_name_or_path = config

        if isinstance(feature_extractor, str):
            feature_extractor_name_or_path = download_from_repo(
                feature_extractor, revision=revision, cache_dir=cache_dir, force_download=force_download
            )
        else:
            feature_extractor_name_or_path = feature_extractor

        if isinstance(image_processor, str):
            image_processor_name_or_path = download_from_repo(
                image_processor, revision=revision, cache_dir=cache_dir, force_download=force_download
            )
        else:
            image_processor_name_or_path = image_processor

        if framework is not None:
            if framework not in SUPPORTED_FRAMEWORKS:
                raise FrameworkNotSupportedError(framework=framework)
        else:
            framework = get_framework()

        if framework == "ms":
            if not is_mindformers_available():
                raise PipelinePackageNotFoundError(pipeline="mindspore", package="mindformers")
            from mindformers.pipeline import pipeline as pipeline_func

            kwargs.pop("revision", None)
            kwargs.pop("cache_dir", None)
            kwargs.pop("force_download", False)

            pipe = pipeline_func(
                task=task,
                model=model_name_or_path,
                config=config_name_or_path,
                tokenizer=tokenizer_name_or_path,
                feature_extractor=feature_extractor_name_or_path,
                image_processor=image_processor_name_or_path,
                framework=framework,
                **kwargs,
            )

        elif framework == "pt":
            if not is_transformers_available():
                raise PipelinePackageNotFoundError(pipeline="transformers", package="transformers")
            from transformers.pipelines import pipeline as pipeline_func

            model_kwargs = {
                "cache_dir": kwargs.pop("cache_dir", None),
                "force_download": kwargs.pop("force_download", False),
            }

            pipe = pipeline_func(
                task=task,
                model=model_name_or_path,
                config=config_name_or_path,
                tokenizer=tokenizer_name_or_path,
                feature_extractor=feature_extractor_name_or_path,
                image_processor=image_processor_name_or_path,
                framework=framework,
                model_kwargs=model_kwargs,
                **kwargs,
            )

        return pipe
    finally:
        # Rollback the patch operation of transformers
        if is_transformers_available():
            import transformers

            patch_list = [
                ("SUPPORTED_TASKS", ORI_SUPPORTED_TASKS),
                ("PIPELINE_REGISTRY", ORI_PIPELINE_REGISTRY),
            ]
            _apply_patches(patch_list, transformers.pipelines)
