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

import argparse
import textwrap

from .subcommand import SubCommand
from .cli_utils import safe_load_yaml, try_to_trans_to_dict
from ..utils.constants import DYNAMIC_ARG, SPECIFIED_ARGS
from ..utils.logging import get_logger, set_verbosity_info
from ..pipelines import pipeline
from ..pipelines.base import SUPPORTED_TASK_PATCH_DICT

logger = get_logger()

set_verbosity_info()


class Run(SubCommand):
    """Holds all the logic for the `openmind-cli run` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "run",
            prog="openmind-cli run repo_id/task_type input/file_path ",
            help="Run models from openMind",
            description="run models from openMind",
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli run PyTorch-NPU/bloom_1b1 --input "Give three tips for staying healthy"

                $ openmind-cli run PyTorch-NPU/bloom_1b1 --input "Give three tips for staying healthy" --task "text-generation"

                $ openmind-cli run text-generation --input "Give three tips for staying healthy" 
            """
            ),
            formatter_class=argparse.RawTextHelpFormatter,
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._run_cmd)

    def _add_arguments(self) -> None:
        """Add arguments to the parser."""
        self._parser.add_argument(
            "--input",
            type=str,
            default=None,
            required=True,
            help="input content or file path",
        )
        self._parser.add_argument(
            "--task",
            type=str,
            default=None,
            help="task type",
        )
        self._parser.add_argument(
            "--framework",
            type=str,
            default=None,
            help="framework type, choosing from pt or ms",
        )
        self._parser.add_argument(
            "--cache_dir",
            type=str,
            default=None,
            help="cache directory of downloaded models",
        )
        self._parser.add_argument(
            "--yaml_path",
            type=str,
            default=None,
            help="path of yaml",
        )

    def _init_pipeline(self, **kwargs):
        return pipeline(**kwargs)

    def _extract_params(self, args):
        if args.yaml_path:
            config_data = safe_load_yaml(args.yaml_path)
        else:
            config_data = dict()
        config_data["repo_or_task"] = vars(args).pop(DYNAMIC_ARG)
        vars(args).pop("func")
        vars(args).pop("yaml_path")

        specified_args = vars(args).pop(SPECIFIED_ARGS)

        for key, value in vars(args).items():
            if key not in config_data:
                config_data[key] = value
            # specified args has a higher priority than yaml
            elif key in config_data and key in specified_args:
                config_data[key] = specified_args[key]
        input_or_path = config_data.pop("input")
        input_or_path = try_to_trans_to_dict(input_or_path)
        config_data["input"] = input_or_path

        return config_data

    def _run_cmd(self, args: argparse.Namespace) -> None:
        params = self._extract_params(args)
        repo_or_task = params.pop("repo_or_task")
        input_or_path = params.pop("input")
        if repo_or_task in SUPPORTED_TASK_PATCH_DICT:
            params["task"] = repo_or_task
        else:
            params["model"] = repo_or_task

        pipe = self._init_pipeline(**params)
        # input_or_path can be str or dict
        if isinstance(input_or_path, dict):
            print(pipe(**input_or_path))
        else:
            print(pipe(input_or_path))
