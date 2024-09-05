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
import argparse
import textwrap
from pathlib import Path
from collections import OrderedDict

from ...utils.logging import get_logger
from ...utils import replace_invalid_characters
from ...omdatasets.om_datasets import OmDataset
from ...hf.hf_utils import (
    AutoConfig,
    AutoModelForCausalLM,
    AutoModelForSeq2SeqLM,
    AutoTokenizer,
)

from ..subcommand import SubCommand


logger = get_logger(__name__)
TASK_DATASET_MAPPING = OrderedDict(
    [
        # task, {dataset repo id on hf: dataset repo id on om}
        # You can find the repo id of the corresponding dataset in the `dataset_path` field of
        # lm-evaluation-harness/lm_eval/tasks/<specific task>/<task_name.yaml>.
        # For example, the repo id of the arithmetic dataset can be found here:
        # https://github.com/EleutherAI/lm-evaluation-harness/blob/2a6acc88a0c31be7734aec85b17555323b70c049/lm_eval/tasks/arithmetic/arithmetic_1dc.yaml#L4
        ("arithmetic", {"EleutherAI/arithmetic": "humphrey007/arithmetic"}),
    ]
)


class LMEVAL(SubCommand):
    """Holds all the logic for the `openmind-cli lmeval` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "lmeval",
            prog="openmind-cli lmeval",
            help="EleutherAI LLM Evaluation Harness.",
            description="EleutherAI LLM Evaluation Harness.",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli lmeval --model Baichuan/Baichuan2_7b_chat_pt --device npu:0 --tasks arithmetic --batch_size 8
                ...
            """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._lmeval_cmd)

    def _add_arguments(self) -> None:
        """Add arguments to the parser."""
        self._parser.add_argument(
            "--model",
            type=str,
            default=None,
            help=(
                "The pre-trained or finetuned language model to evaluate. "
                "Can be either a string, the model id of a model hosted inside a model repo on openMind Hub, "
                "or a path to a directory containing pre-trained model"
            ),
        )
        self._parser.add_argument(
            "--tasks",
            type=str,
            default=None,
            metavar="task1,task2",
            help="List lm-eluther tasks to evaluate usage: --tasks task1,task2",
        )
        self._parser.add_argument(
            "--batch_size",
            type=str,
            default=1,
            metavar="auto|auto:N|N",
            help="Acceptable values are 'auto', 'auto:N' or N, where N is an integer. Default 1.",
        )
        self._parser.add_argument(
            "--device",
            type=str,
            default="npu:0",
            help="Device to use (e.g. npu:0, cpu).",
        )
        self._parser.add_argument(
            "--limit",
            type=int,
            default=None,
            help="Limit the number of examples per task.",
        )
        self._parser.add_argument(
            "--trust_remote_code",
            type=int,
            default=None,
            help=(
                "Whether or not to allow for custom models defined on the Hub in their own modeling files. "
                "This option should only be set to 1 for repositories you trust and in which you have read the code, "
                "as it will execute code present on the Hub on your local machine.",
            ),
        )

    def _supported_tasks(self) -> str:
        result = "Available tasks:"
        for task in TASK_DATASET_MAPPING.keys():
            result += f"\n - {task}"
        return result

    def _evaluate(self, args: argparse.Namespace):
        try:
            from lm_eval import evaluator, utils
            from lm_eval.tasks import TaskManager
            from lm_eval.models.huggingface import HFLM
            from lm_eval.utils import make_table
        except ImportError:
            raise ImportError(
                "openmind-cli lmeval requires lm-evaluation-harness. Please install with `pip install openmind[pt]"
            )

        # patch some function in lm-evaluation-harness to unncecessary alerts
        origin_get_model_info = HFLM.get_model_info
        origin_get_git_commit_hash = evaluator.get_git_commit_hash
        HFLM.get_model_info = lambda x: ""
        evaluator.get_git_commit_hash = lambda: ""

        task_manager = TaskManager()
        task_list = args.tasks.split(",")
        task_names = task_manager.match_tasks(task_list)
        for task in [task for task in task_list if task not in task_names]:
            if os.path.isfile(task):
                config = utils.load_yaml_config(task)
                task_names.append(config)
        task_missing = [task for task in task_list if task not in task_names and "*" not in task]

        if task_missing:
            missing = ", ".join(task_missing)
            logger.error(
                f"Tasks were not found: {missing}\n"
                f"Try `openmind-cli lmeval --tasks list` for list of available tasks",
            )
            raise ValueError(
                f"Tasks not found: {missing}. Try `openmind-cli lmeval --tasks list` for list of available tasks."
            )
        logger.info(f"Selected Tasks: {task_names}")

        model_args = f"pretrained={args.model}"
        if args.trust_remote_code:
            model_args = model_args + ",trust_remote_code=True"

        results = evaluator.simple_evaluate(
            model="hf",
            model_args=model_args,
            tasks=task_names,
            batch_size=args.batch_size,
            device=args.device,
            limit=args.limit,
        )
        print(make_table(results))
        if "groups" in results:
            print(make_table(results, "groups"))

        # rollback patches
        HFLM.get_model_info = origin_get_model_info
        evaluator.get_git_commit_hash = origin_get_git_commit_hash

    def _lmeval_cmd(self, args: argparse.Namespace) -> None:
        """Evaluate LLM with EleutherAI's llm evaluation harness."""
        # monkey patch parts of datasets/evaluate/transformeres' APIs to adapter to openMind Hub.
        try:
            import datasets
            import evaluate
            import transformers
        except ImportError:
            raise ImportError(
                "openmind-cli lmeval requires datasets, evaluate and transforemrs. \
                    Please install with `pip install openmind[pt]"
            )

        if args.tasks == "list":
            print(self._supported_tasks())
            return

        # disable tokenizers parallelism
        origin_env_tokenizers_parallelism = os.environ.get("TOKENIZERS_PARALLELISM")
        os.environ["TOKENIZERS_PARALLELISM"] = "0"

        # load `exact_match` metric locally, the actual patch takes effect here:
        # https://github.com/EleutherAI/lm-evaluation-harness/blob/4600d6bf73ba2cf7037ae7feada03315839ef185/lm_eval/api/metrics.py#L168
        origin_evaluate_load = evaluate.load

        def _patch_evaluate_load(path, *args, **kwargs):
            if path == "exact_match":
                path = os.path.join(Path(__file__).resolve().parent, "exact_match")
            return origin_evaluate_load(path, *args, **kwargs)

        evaluate.load = _patch_evaluate_load

        # patch load_dataset
        origin_load_dataset = datasets.load_dataset

        def _patch_load_dataset(args: argparse.Namespace):
            if args.tasks is None:
                error_msg = replace_invalid_characters(
                    f"The task to be evaluated must be specified, but got None. \
                                Supported tasks include {list(TASK_DATASET_MAPPING.keys())}"
                )
                raise ValueError(error_msg)
            tasks = args.tasks.split(",")
            for task in tasks:
                if task not in TASK_DATASET_MAPPING:
                    error_msg = replace_invalid_characters(
                        f"{task} is invalid or not supported now. \
                            Supported tasks include {list(TASK_DATASET_MAPPING.keys())}"
                    )
                    raise KeyError(error_msg)
            # Don't use generators!
            dataset_maps = [TASK_DATASET_MAPPING[task] for task in tasks]

            def wrapper(path, *args, **kwargs):
                for dataset_map in dataset_maps:
                    if path in dataset_map:
                        path = dataset_map[path]
                        break
                return OmDataset.load_dataset(path, *args, **kwargs)

            return wrapper

        datasets.load_dataset = _patch_load_dataset(args)

        # patch auto-classes
        origin_AutoConfig = transformers.AutoConfig
        origin_AutoTokenizer = transformers.AutoTokenizer
        origin_AutoModelForCausalLM = transformers.AutoModelForCausalLM
        origin_AutoModelForSeq2SeqLM = transformers.AutoModelForSeq2SeqLM
        transformers.AutoConfig = AutoConfig
        transformers.AutoTokenizer = AutoTokenizer
        transformers.AutoModelForCausalLM = AutoModelForCausalLM
        transformers.AutoModelForSeq2SeqLM = AutoModelForSeq2SeqLM

        self._evaluate(args)

        # rollback patches
        if origin_env_tokenizers_parallelism is not None:
            os.environ["TOKENIZERS_PARALLELISM"] = origin_env_tokenizers_parallelism
        else:
            del os.environ["TOKENIZERS_PARALLELISM"]
        evaluate.load = origin_evaluate_load
        datasets.load_dataset = origin_load_dataset
        transformers.AutoConfig = origin_AutoConfig
        transformers.AutoTokenizer = origin_AutoTokenizer
        transformers.AutoModelForCausalLM = origin_AutoModelForCausalLM
        transformers.AutoModelForSeq2SeqLM = origin_AutoModelForSeq2SeqLM
