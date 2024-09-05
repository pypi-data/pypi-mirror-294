from typing import Dict, Optional, Union
import torch
import transformers
from transformers import PretrainedConfig, PreTrainedModel

from ...utils.import_utils import is_torch_npu_available
from .models import LlamaNpuFlashAttention, _update_llama_model_causal_mask


def _patch_check_and_enable_flash_attn_2():
    @classmethod
    def _check_and_enable_flash_attn_2(
        cls,
        config,
        torch_dtype: Optional[torch.dtype] = None,
        device_map: Optional[Union[str, Dict[str, int]]] = None,
        check_device_map: bool = True,
        hard_check_only: bool = False,
    ) -> PretrainedConfig:
        if not hard_check_only:
            config._attn_implementation = "flash_attention_2"
        return config

    PreTrainedModel._check_and_enable_flash_attn_2 = _check_and_enable_flash_attn_2


def adapt_transformers_to_npu():
    if is_torch_npu_available():
        import torch_npu

        torch_npu.npu.config.allow_internal_format = False

    _patch_check_and_enable_flash_attn_2()
    transformers.models.llama.modeling_llama.LLAMA_ATTENTION_CLASSES["flash_attention_2"] = LlamaNpuFlashAttention
    transformers.models.llama.modeling_llama.LlamaModel._update_causal_mask = _update_llama_model_causal_mask
