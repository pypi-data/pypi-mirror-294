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
import json
import os
import stat


class HubName(Enum):
    openmind_hub = "OpenMindHub"


ENV_VARS_TRUE_VALUES = {"1", "ON", "YES", "TRUE"}
FRAMEWORK_ENV_KEY = "OPENMIND_FRAMEWORK"
DEFAULT_FLAGS = os.O_WRONLY | os.O_CREAT
DEFAULT_MODES = stat.S_IWUSR | stat.S_IRUSR
LOG_CONTENT_BLACK_LIST = (
    "\r",
    "\n",
    "\t",
    "\f",
    "\v",
    "\b",
    "\u000A",
    "\u000D",
    "\u000C",
    "\u000B",
    "\u0008",
    "\u007F",
    "\u0009",
)
BLANKS = "    "
DEFAULT_TIMEOUT = 100

file_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
with open(os.path.join(file_path, "public_address_lib.json"), "r") as cfg_file:
    json_file = cfg_file.read()
    MINDSPORE_INSTALL_URL = json.loads(json_file)["mindspore_url"]
    OPENMIND_URL = json.loads(json_file)["openmind_url"]
    OPENMIND_MODEL_URL = json.loads(json_file)["openmind_model_url"]
    OPENMIND_DATASET_DOWNLOAD_URL = json.loads(json_file)["openmind_dataset_download_url"]
    PT_NN_MODULE_URL = json.loads(json_file)["pt_nn_module_url"]
    HUGGINGFACE_CHAT_URL = json.loads(json_file)["huggingface_chat_url"]
    LLAMA_ADDRESS_URL = json.loads(json_file)["llama_address_url"]
    BART_PAPER_URL = json.loads(json_file)["bart_paper_url"]
    LLAMA_TOKENIZER_CONFIG_URL = json.loads(json_file)["llama_tokenizer_config_url"]
    LLAMA_TOKENIZER_MODEL_URL = json.loads(json_file)["llama_tokenizer_model_url"]
    LEGACY_PARAS_URL = json.loads(json_file)["legacy_paras_url"]
    PYTORCH_INSTALL_URL = json.loads(json_file)["pytorch_install_url"]
    MISTRAL_REPO_URL = json.loads(json_file)["mistral_repo_url"]
    URL_PATTERN = rf'^{json.loads(json_file)["openmind_api_url"]}([^/]+)/([^/]+)/([^/]+)/media/(.*)'

GB = 1024**3
GIT = ".git"
GIT_LOGS_HEAD = ".git/logs/HEAD"
OPENMIND_PREFIX = "modelers.cn/"
SNAPSHOTS = "snapshots"
MODEL_CONFIG = "config.json"

# key in args for storing dynamic argument
DYNAMIC_ARG = "_dynamic_arg"

# key in args for storing specified arguments
SPECIFIED_ARGS = "_specified_args"
