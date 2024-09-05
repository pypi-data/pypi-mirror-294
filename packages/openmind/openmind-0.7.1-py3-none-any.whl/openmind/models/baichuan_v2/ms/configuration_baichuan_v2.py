# Copyright 2023 Baichuan Inc. All Rights Reserved.
# Copyright 2022 EleutherAI and the HuggingFace Inc. team. All rights reserved.
# 2024.04.03 - adapt to mindspore
#              Huawei Technologies Co., Ltd.
#
# This code is based on EleutherAI's GPT-NeoX library and the GPT-NeoX
# and OPT implementations in this library. It has been modified from its
# original forms to accommodate minor architectural differences compared
# to GPT-NeoX and OPT used by the Meta AI team that trained the model.
#
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

from typing import Optional, Union

from mindformers.models.configuration_utils import PretrainedConfig
from mindformers.models.utils import convert_mstype
from mindformers.modules.transformer.moe import MoEConfig
from mindformers.modules.transformer.transformer import (
    TransformerOpParallelConfig,
    default_moe_config,
    default_transformer_config,
)
from mindformers.tools.logger import logger
from mindspore._checkparam import args_type_check


class BaichuanV2Config(PretrainedConfig):
    model_type = "baichuan_v2"

    @args_type_check(parallel_config=(dict, TransformerOpParallelConfig))
    def __init__(
        self,
        batch_size: int = 1,
        seq_length: int = 512,
        hidden_size: int = 4096,
        num_layers: int = 32,
        num_heads: int = 32,
        n_kv_heads: Optional[int] = None,
        max_position_embedding: Optional[int] = None,
        intermediate_size: Optional[int] = None,
        vocab_size: int = 125696,  # defined later by tokenizer
        multiple_of: int = 256,  # make SwiGLU hidden layer size multiple of large power of 2
        ffn_dim_multiplier: Optional[int] = None,
        rms_norm_eps: float = 1e-5,
        bos_token_id: int = 1,
        eos_token_id: int = 2,
        pad_token_id: int = 0,
        ignore_token_id: int = -100,
        theta: float = 10000.0,
        compute_dtype: str = "float16",
        layernorm_compute_type: str = "float32",
        softmax_compute_type: str = "float32",
        rotary_dtype: str = "float32",
        param_init_type: str = "float16",
        qkv_has_bias: bool = False,
        qkv_concat: bool = False,
        parallel_config: Union[dict, TransformerOpParallelConfig] = default_transformer_config,
        moe_config: Union[dict, MoEConfig] = default_moe_config,
        use_past: bool = True,
        pretrain_seqlen=None,
        compute_in_2d=None,
        use_past_shard=None,
        extend_method: str = "None",
        scaling_factor: float = 1.0,
        is_dynamic: bool = False,
        use_kvcache_op: bool = False,
        is_flexible_shape: bool = False,
        use_rope_slice: bool = False,
        use_flash_attention: bool = False,
        use_paged_attention: bool = False,
        fine_grain_interleave: int = 1,
        offset: int = 0,
        checkpoint_name_or_path: str = "",
        repetition_penalty: float = 1.0,
        max_decode_length: int = 512,
        block_size: int = 16,
        num_blocks: int = 512,
        top_k: int = 5,
        top_p: float = 1.0,
        do_sample: bool = True,
        **kwargs,
    ):
        if isinstance(parallel_config, dict):
            parallel_config = TransformerOpParallelConfig(**parallel_config)
        if isinstance(moe_config, dict):
            moe_config = MoEConfig(**moe_config)
        self.batch_size = batch_size
        self.seq_length = seq_length
        self.vocab_size = vocab_size
        self.hidden_size = hidden_size
        self.num_layers = num_layers
        self.num_heads = num_heads
        self.max_position_embedding = max_position_embedding if max_position_embedding else seq_length
        self.intermediate_size = intermediate_size
        self.multiple_of = multiple_of
        self.n_kv_heads = n_kv_heads
        self.ffn_dim_multiplier = ffn_dim_multiplier
        self.rms_norm_eps = rms_norm_eps
        self.qkv_concat = qkv_concat
        self.param_init_type = convert_mstype(param_init_type)
        self.qkv_has_bias = qkv_has_bias
        self.layernorm_compute_type = convert_mstype(layernorm_compute_type)
        self.softmax_compute_type = convert_mstype(softmax_compute_type)
        self.rotary_dtype = convert_mstype(rotary_dtype)
        self.compute_dtype = convert_mstype(compute_dtype)
        self.parallel_config = parallel_config
        self.moe_config = moe_config
        self.checkpoint_name_or_path = checkpoint_name_or_path
        self.bos_token_id = bos_token_id
        self.eos_token_id = eos_token_id
        self.pad_token_id = pad_token_id
        self.ignore_token_id = ignore_token_id
        self.use_past = use_past
        if pretrain_seqlen is not None:
            self.pretrain_seqlen = pretrain_seqlen
            logger.warning("Argument `pretrain_seqlen` is deprecated. Use `scaling_factor` instead.")
        if compute_in_2d is not None:
            self.compute_in_2d = compute_in_2d
            logger.warning("Argument `compute_in_2d` is deprecated.")
        if use_past_shard is not None:
            self.use_past_shard = use_past_shard
            logger.warning("Argument `use_past_shard` is deprecated.")
        self.extend_method = extend_method
        self.scaling_factor = scaling_factor
        self.is_dynamic = is_dynamic
        self.use_kvcache_op = use_kvcache_op
        self.is_flexible_shape = is_flexible_shape
        self.use_rope_slice = use_rope_slice
        self.use_flash_attention = use_flash_attention
        self.fine_grain_interleave = fine_grain_interleave
        self.offset = offset
        self.repetition_penalty = repetition_penalty
        self.max_decode_length = max_decode_length
        self.top_k = top_k
        self.top_p = top_p
        self.do_sample = do_sample
        self.theta = theta
        self.use_paged_attention = use_paged_attention
        self.block_size = block_size
        self.num_blocks = num_blocks
        if batch_size * seq_length // self.block_size > self.num_blocks:
            logger.warning(
                "Argument `num blocks` is less than the maximum possible block numbers. "
                "May cause `block pool is out of memory` error"
            )

        super(BaichuanV2Config, self).__init__(
            batch_size=batch_size,
            max_decode_length=max_decode_length,
            top_k=top_k,
            do_sample=do_sample,
            bos_token_id=bos_token_id,
            eos_token_id=eos_token_id,
            pad_token_id=pad_token_id,
            **kwargs,
        )
