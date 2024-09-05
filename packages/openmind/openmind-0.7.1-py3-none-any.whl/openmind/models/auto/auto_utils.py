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
from enum import Enum
import importlib
from types import ModuleType
from typing import Dict, Tuple, Union

from ...utils.generic import replace_invalid_characters


class AutoClassType(str, Enum):
    CONFIG = "AutoConfig"
    TOKENIZER = "AutoTokenizer"
    MODEL = "AutoModel"
    MODEL_FOR_CAUSAL_LM = "AutoModelForCausalLM"
    MODEL_FOR_PRE_TRAINING = "AutoModelForPreTraining"
    MODEL_FOR_SEQUENCE_CLASSIFICATION = "AutoModelForSequenceClassification"
    MODEL_FOR_TOKEN_CLASSIFICATION = "AutoModelForTokenClassification"
    MODEL_FOR_QUESTION_ANSWERING = "AutoModelForQuestionAnswering"

    @classmethod
    def _missing_(cls, value):
        error_msg = f"{value} is not a valid {cls.__name__}, please select one of {list(cls._value2member_map_.keys())}"
        raise ValueError(replace_invalid_characters(error_msg))


def register_model(module: ModuleType, framework: str, models: Dict[str, Dict[str, Union[str, Tuple]]]):
    config_cls = None

    for model_type, auto_map in models.items():
        if AutoClassType.CONFIG not in auto_map:
            error_msg = (
                f"When registering model type {model_type}, you need to add the mapping "
                f"between {AutoClassType.CONFIG} and model config class"
            )
            raise ValueError(replace_invalid_characters(error_msg))
        model_module = importlib.import_module(f".{model_type}.{framework}", "openmind.models")

        # register config class
        config_cls_name = auto_map[AutoClassType.CONFIG]
        if hasattr(model_module, config_cls_name):
            config_cls = getattr(model_module, config_cls_name)
            getattr(module, "AutoConfig").register(model_type, config_cls, True)
        auto_map.pop(AutoClassType.CONFIG)

        for auto_cls_type, model_cls_name in auto_map.items():
            auto_cls_name = auto_cls_type.value
            if auto_cls_name == "AutoTokenizer":
                if not isinstance(model_cls_name, tuple) or len(model_cls_name) != 2:
                    raise ValueError(
                        "To bind a custom tokenizer to AutoTokenizer, You should provide a tuple with two string, "
                        "which represent the class names for slow tokenizer and fast tokenizer"
                    )
                slow_tokenizer_cls = getattr(model_module, model_cls_name[0], None)
                fast_tokenizer_cls = getattr(model_module, model_cls_name[1], None)
                getattr(module, auto_cls_name).register(config_cls, slow_tokenizer_cls, fast_tokenizer_cls, True)
            else:
                if hasattr(model_module, model_cls_name):
                    model_cls = getattr(model_module, model_cls_name)
                    getattr(module, auto_cls_name).register(config_cls, model_cls, True)
