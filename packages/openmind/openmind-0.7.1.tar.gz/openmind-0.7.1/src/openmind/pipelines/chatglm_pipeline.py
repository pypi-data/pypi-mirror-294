# Copyright 2023 Baichuan Inc. All Rights Reserved.
# Copyright 2022 EleutherAI and the HuggingFace Inc. team. All rights reserved.
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

from typing import List, Optional, Tuple

import torch
from transformers import Pipeline
from transformers.generation.logits_process import LogitsProcessor
from transformers.generation.utils import LogitsProcessorList


class InvalidScoreLogitsProcessor(LogitsProcessor):
    """
    Process the input scores tensor, replacing infinite values with 0 and setting the value at the 5th position 50000,
    ensureing that the output scores tensor does not contain any invalid values.
    """

    def __call__(self, input_ids: torch.LongTensor, scores: torch.FloatTensor) -> torch.FloatTensor:
        if torch.isnan(scores).any() or torch.isinf(scores).any():
            scores.zero_()
            scores[..., 5] = 5e4
        return scores


class ChatGLMPipeline(Pipeline):
    """
    Language generation pipeline of chatglm2-6b. This pipeline predicts the words that will follow a specified text
    prompt.

    Example:

    ```python
    >>> from openmind import AutoTokenizer, AutoModel, pipelines

    >>> tokenizer = AutoTokenizer.from_pretrained("PyTorch-NPU/chatglm2_6b", trust_remote_code=True)
    >>> model = AutoModel.from_pretrained("PyTorch-NPU/chatglm2_6b", device_map="npu:0", trust_remote_code=True).half()

    >>> pipe = pipelines.pipeline(task="chat", model=model, tokenizer=tokenizer, framework="pt")
    >>> outputs, history = pipe("人工智能是什么", do_sample=False)
    outputs: 人工智能(Artificial Intelligence, AI)是一种涵盖了多个学科领域的科技领域，旨在创造出可以执行与人类智能类相似的任务的计算机
    程序和系统。AI通常包括机器学习、自然语言处理、计算机视觉、知识表示、推理、规划和决策等技术。其目标是使计算机能够自主地处理复杂的任务，例如
    识别图像和语音、自动驾驶、智能机器人、自然语言交互等。AI是一个快速发展的领域，涉及到数学、统计学、计算机科学、认知心理学、哲学等多个学科
    的知识。
    ```
    """

    def __call__(self, inputs, **kwargs):
        """
        Args:
            inputs:
                The text prompt or text sequence
            kwargs:
                Additional keyword arguments that users can customize.
        """
        return super().__call__(inputs, **kwargs)

    def preprocess(self, inputs, history):
        prompt = self.tokenizer.build_prompt(inputs, history=history)
        inputs = self.tokenizer([prompt], return_tensors="pt")
        inputs = inputs.to(self.device)
        return inputs

    def postprocess(self, model_outputs, **postprocess_kwargs):
        response = self.tokenizer.decode(model_outputs)
        response = response.strip()
        response = response.replace("[[训练时间]]", "2023年")
        try:
            history = postprocess_kwargs["history"] + [(postprocess_kwargs["inputs"], response)]
        except KeyError as e:
            raise KeyError("history or inputs is invalid") from e
        return response, history

    def _forward(self, model_inputs, **generate_kwargs):
        outputs = self.model.generate(**model_inputs, **generate_kwargs)
        return outputs.tolist()[0][len(model_inputs["input_ids"][0]) :]

    def _sanitize_parameters(
        self,
        inputs: Optional[str] = None,
        history: List[Tuple[str, str]] = None,
        max_length: int = 8192,
        num_beams=1,
        do_sample=True,
        top_p=0.8,
        temperature=0.8,
        logits_processor=None,
        **kwargs,
    ):
        preprocess_keys = {}
        if history is None:
            history = []
        preprocess_keys["history"] = history

        forward_kwargs = {
            "max_length": max_length,
            "num_beams": num_beams,
            "do_sample": do_sample,
            "temperature": temperature,
        }

        if logits_processor is None:
            logits_processor = LogitsProcessorList()
        logits_processor.append(InvalidScoreLogitsProcessor())
        forward_kwargs["logits_processor"] = logits_processor

        postprocess_kwargs = {
            "inputs": inputs,
            "history": history,
        }

        return preprocess_keys, forward_kwargs, postprocess_kwargs
