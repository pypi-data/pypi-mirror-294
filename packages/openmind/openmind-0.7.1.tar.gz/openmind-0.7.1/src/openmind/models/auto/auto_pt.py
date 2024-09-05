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
import sys

# ruff: noqa: F401
from ...hf.hf_utils import (
    AutoConfig,
    AutoFeatureExtractor,
    AutoImageProcessor,
    AutoModel,
    AutoModelForCausalLM,
    AutoModelForPreTraining,
    AutoModelForQuestionAnswering,
    AutoModelForSequenceClassification,
    AutoModelForTokenClassification,
    AutoProcessor,
    AutoTokenizer,
)

from .auto_utils import AutoClassType, register_model


# register model here
register_model(
    module=sys.modules[__name__],
    framework="pt",
    models={
        # register model here
        # "<model_type>": {
        #     AutoClassType.CONFIG: "CustomModelConfig",
        #     AutoClassType.TOKENIZER: ("CustomTokenizerSlow", "CustomTokenizerFast"),
        #     AutoClassType.MODEL_FOR_CAUSAL_LM: "CustomModelForCausalLM",
        # },
        "bloom": {
            AutoClassType.CONFIG: "BloomConfig",
            AutoClassType.TOKENIZER: ("", "BloomTokenizerFast"),
            AutoClassType.MODEL: "BloomModel",
            AutoClassType.MODEL_FOR_CAUSAL_LM: "BloomForCausalLM",
            AutoClassType.MODEL_FOR_PRE_TRAINING: "BloomPreTrainedModel",
            AutoClassType.MODEL_FOR_SEQUENCE_CLASSIFICATION: "BloomForSequenceClassification",
            AutoClassType.MODEL_FOR_TOKEN_CLASSIFICATION: "BloomForTokenClassification",
            AutoClassType.MODEL_FOR_QUESTION_ANSWERING: "BloomForQuestionAnswering",
        },
        "mistral": {
            AutoClassType.CONFIG: "MistralConfig",
            AutoClassType.TOKENIZER: ("LlamaTokenizer", "LlamaTokenizerFast"),
            AutoClassType.MODEL: "MistralModel",
            AutoClassType.MODEL_FOR_CAUSAL_LM: "MistralForCausalLM",
            AutoClassType.MODEL_FOR_SEQUENCE_CLASSIFICATION: "MistralForSequenceClassification",
            AutoClassType.MODEL_FOR_PRE_TRAINING: "MistralPreTrainedModel",
        },
        "qwen2": {
            AutoClassType.CONFIG: "Qwen2Config",
            AutoClassType.TOKENIZER: ("Qwen2Tokenizer", "Qwen2TokenizerFast"),
            AutoClassType.MODEL_FOR_CAUSAL_LM: "Qwen2ForCausalLM",
            AutoClassType.MODEL_FOR_PRE_TRAINING: "Qwen2PreTrainedModel",
            AutoClassType.MODEL: "Qwen2Model",
            AutoClassType.MODEL_FOR_SEQUENCE_CLASSIFICATION: "Qwen2ForSequenceClassification",
        },
    },
)
