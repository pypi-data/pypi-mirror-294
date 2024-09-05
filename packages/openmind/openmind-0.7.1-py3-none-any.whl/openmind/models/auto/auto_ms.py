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

from mindformers import (
    AutoConfig,  # noqa: F401
    AutoImageProcessor,  # noqa: F401
    AutoModel,  # noqa: F401
    AutoModelForCausalLM,  # noqa: F401
    AutoModelForSequenceClassification,  # noqa: F401
    AutoProcessor,  # noqa: F401
    AutoTokenizer,  # noqa: F401
)

from .auto_utils import AutoClassType, register_model


# register model here
register_model(
    module=sys.modules[__name__],
    framework="ms",
    models={
        # register model here
        # "<model_type>": {
        #     AutoClassType.CONFIG: "CustomModelConfig",
        #     AutoClassType.TOKENIZER: ("CustomTokenizerSlow", "CustomTokenizerFast"),
        #     AutoClassType.MODEL_FOR_CAUSAL_LM: "CustomModelForCausalLM",
        # },
        "baichuan_v2": {
            AutoClassType.CONFIG: "BaichuanV2Config",
            AutoClassType.TOKENIZER: ("BaichuanV2Tokenizer", ""),
            AutoClassType.MODEL_FOR_CAUSAL_LM: "BaichuanV2ForCausalLM",
        },
        "glm2": {
            AutoClassType.CONFIG: "ChatGLM2Config",
            AutoClassType.TOKENIZER: ("ChatGLM2Tokenizer", ""),
            AutoClassType.MODEL_FOR_CAUSAL_LM: "ChatGLM2ForConditionalGeneration",
        },
        "open_llama_7b": {
            AutoClassType.CONFIG: "LlamaConfig",
            AutoClassType.TOKENIZER: ("LlamaTokenizer", "LlamaTokenizerFast"),
            AutoClassType.MODEL_FOR_CAUSAL_LM: "LlamaForCausalLM",
        },
        "qwen": {
            AutoClassType.CONFIG: "QwenConfig",
            AutoClassType.TOKENIZER: ("QwenTokenizer", ""),
            AutoClassType.MODEL_FOR_CAUSAL_LM: "QwenForCausalLM",
        },
        "internlm": {
            AutoClassType.CONFIG: "InternLMConfig",
            AutoClassType.TOKENIZER: ("InternLMTokenizer", ""),
            AutoClassType.MODEL_FOR_CAUSAL_LM: "InternLMForCausalLM",
        },
    },
)
