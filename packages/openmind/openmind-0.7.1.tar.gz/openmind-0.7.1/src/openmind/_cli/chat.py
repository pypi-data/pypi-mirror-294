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

from .cli_utils import safe_load_yaml
from ..pipelines import pipeline
from .subcommand import SubCommand
from ..utils.hub import OPENMIND_CACHE
from ..pipelines.base import SUPPORTED_TASK_PATCH_DICT
from ..utils.constants import DYNAMIC_ARG, SPECIFIED_ARGS
from ..models.auto import AutoModel, AutoConfig, AutoTokenizer
from ..utils import get_framework, logging, replace_invalid_characters

logger = logging.get_logger()
logging.set_verbosity_info()


class Chat(SubCommand):
    """Holds all the logic for the `openmind-cli chat` subcommand."""

    def __init__(self, subparsers: argparse._SubParsersAction):
        super().__init__()
        self._parser = subparsers.add_parser(
            "chat",
            prog="openmind-cli chat",
            help="start a multi-turn conversation.",
            description="start a multi-turn conversation.",
            formatter_class=argparse.RawTextHelpFormatter,
            epilog=textwrap.dedent(
                """\
            examples:
                $ openmind-cli chat text-generation
                [User]>>> hello
                [Model]>>> [{'generated_text': 'hello'}]
            """
            ),
        )
        self._add_arguments()
        self._parser.set_defaults(func=self._start_chat)

    def _add_arguments(self) -> None:
        """Add arguments to the parser"""
        self._parser.add_argument(
            "--framework",
            type=str,
            default=None,
            choices=["pt", "ms"],
            help="framework for chat.",
        )
        self._parser.add_argument("--cache_dir", type=str, default=None, help="local directory for caching models.")
        self._parser.add_argument("--model", type=str, default=None, help="model id for chat.")
        self._parser.add_argument("--config", type=str, default=None, help="config model id for chat.")
        self._parser.add_argument("--tokenizer", type=str, default=None, help="tokenizer model id for chat.")
        self._parser.add_argument("--yaml_path", type=str, default=None, help="local path of yaml config file.")

    def _prepare_arguments(self, args: argparse.Namespace) -> dict:
        args_dict = vars(args)
        args_dict.pop("func")

        # assemble arguments according to priority
        if args_dict.get(DYNAMIC_ARG) is None:
            raise ValueError("command `openmind-cli chat [arg] --xx xx`, [arg] is required but not found.")

        if args_dict.get("yaml_path") is not None:
            yaml_content_dict = safe_load_yaml(args_dict.pop("yaml_path"))
            args_dict.update(yaml_content_dict)

        args_dict.update(args_dict.pop(SPECIFIED_ARGS))

        # determine whether the dynamic argument is a task name or model id
        dynamic_model_id = args_dict.pop(DYNAMIC_ARG)

        if dynamic_model_id in SUPPORTED_TASK_PATCH_DICT:
            task_name = dynamic_model_id
            model = None
        else:
            task_name = None
            model = dynamic_model_id

        if args_dict.get("model") is not None:
            if model is not None:
                warn_msg = (
                    f"a new model name `{args_dict.get('model')}` is found from `--model`, "
                    f"which will override previously specified model `{model}`"
                )
                logger.warning(replace_invalid_characters(warn_msg))

            model = args_dict.get("model")

        args_dict.update({"task": task_name, "model": model})

        # set default value
        if args_dict.get("framework") is None:
            args_dict.update({"framework": get_framework()})

        if args_dict.get("cache_dir") is None:
            args_dict.update({"cache_dir": OPENMIND_CACHE})

        if args_dict.get("trust_remote_code") is None:
            logger.info(
                "`trust_remote_code` is not specified, default value is `False`, "
                "set to `True` when loading object from repo."
            )
            args_dict.update({"trust_remote_code": False})

        # initialize config/model/tokenizer if not model id
        if isinstance(args_dict.get("config"), dict):
            args_dict.update({"config": AutoConfig.from_pretrained(**args_dict.get("config"))})

        if isinstance(args_dict.get("model"), dict):
            args_dict.update({"model": AutoModel.from_pretrained(**args_dict.get("model"))})

        if isinstance(args_dict.get("tokenizer"), dict):
            args_dict.update({"tokenizer": AutoTokenizer.from_pretrained(**args_dict.get("tokenizer"))})

        return args_dict

    def _start_chat(self, args: argparse.Namespace) -> None:
        args_dict = self._prepare_arguments(args)

        chat_pipeline = pipeline(**args_dict)

        logger.info("welcome to use openmind chat")

        while True:
            try:
                user_query = input("\n[User]>>> ")
            except UnicodeDecodeError:
                logger.error(
                    "decoding error occurred when processing user inputs, please set the terminal encoding " "to utf-8."
                )
                continue
            except Exception as ex:
                err_msg = f"exception occurred when processing user inputs, detail error message: {str(ex)}"
                raise RuntimeError(replace_invalid_characters(err_msg))

            if user_query.strip() == "exit":
                break

            model_rsp = chat_pipeline(user_query)

            print(f"\n[Model]>>> {model_rsp}")
