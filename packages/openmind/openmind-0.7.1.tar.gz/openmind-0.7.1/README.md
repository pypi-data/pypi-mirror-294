# openMind Library

## 简介

openMind Library是一个开源的深度学习开发套件，支持模型训练、推理等流程，兼容PyTorch和MindSpore等主流框架。

## 安装

关于openMind Library的安装步骤，推荐用户参考[《安装》](./docs/zh/install.md)文档，以确保顺利并正确地完成安装过程。

openMind Library的安装过程还依赖于openmind_accelerate与openmind_hub，用户在进行安装时，可以参考[openmind-accelerate环境准备](https://gitee.com/openmind-ai/openmind-accelerate/blob/master/README.md#%E7%8E%AF%E5%A2%83%E5%87%86%E5%A4%87)与[openMind Hub Client安装](https://gitee.com/openmind-ai/openmind-hub#%E5%AE%89%E8%A3%85)来进行操作。

## 快速上手

`pipeline()`提供了使用预训练模型进行推理的全流程，使用`pipeline()`可以轻松实现对文本、图像、音频等多种模态数据的多种任务，如文本情感分析、图像分割、语音识别等。

本章以对文本的情感分析任务为例，展示如何使用`pipeline()`执行一个指定的任务。

首先，实例化一个pipeline对象并指定任务类型，本示例中指定为`sentiment-analysis`（所有支持的任务类型详见 [**pipeline当前支持的推理任务与默认模型**](./docs/zh/basic_tutorial/pipeline.md#pipeline当前支持的推理任务与默认模型)）。此方法未指定模型，pipeline使用任务对应的预定义默认模型进行推理。

```python
from openmind import pipeline

# 当环境中只有一种框架，若不指定framework参数，将默认基于当前框架进行推理
classifier = pipeline("sentiment-analysis")
# 当环境中有多种框架，若指定framework参数为"ms"时，将基于MindSpore框架进行推理
classifier = pipeline("sentiment-analysis", framework="ms")
```

在仅指定任务类型时，`pipeline()`会自动下载预定义默认预训练模型及分词器，本示例中的预训练模型和分词器用于情感分析，随后使用`classifier`对输入文本进行情感分析。

```python
classifier("Welcome to the openMind library!")

'''
输出：
[{'label': 'POSITIVE', 'score': 0.999705970287323}]
'''
```

当输入文本不只一条时，可以把所有输入放入到列表中，一次性传给`pipeline()`，`classifier`也将所有结果存储在一个字典列表内并返回：

```python
results = classifier(["Welcome to the openMind library!", "Have a great experience using it!"])
for result in results:
    print(f"label: {result['label']}, with score: {round(result['score'], 4)}")

'''
输出：
label: POSITIVE, with score: 0.9997
label: POSITIVE, with score: 0.9998
'''
```

其余openMind Library的基础功能可参考[快速入门](./docs/zh/quick_start.md)。

## 贡献

1. 在上传PR之前，请确保所有测试都通过。首先在本地运行如下命令。

```shell
# The scripts below run on system default python version by default. If you want to use other python version, set the env
# PY_VERSION. For example, `PY_VERSION=3.8 ./ci/lint.sh`
# Lint check
./ci/lint.sh
# Unit test
./ci/unit_test.sh
# Functional test, Please generate the HUB_TOKEN from openmind by yourself and use it privatelly.
HUB_TOKEN=your_hub_token ./ci/functional_test.sh
```

2. 当您推送或更新PR（Pull Request）后，系统将自动触发CI（持续集成）构建和测试流程。若所有CI构建和测试均顺利通过，`ci-success`标记将自动添加到您的PR中。然而，若出现CI故障，您可以点击CI日志链接以详细查看失败原因，并在本地进行必要的修复。一旦您完成了修复并希望重新运行CI作业，只需在PR中留下评论`/recheck`即可。

## 安全声明

为保障使用过程安全，推荐用户参考[《安全声明》](./security_statement.md)了解相关安全信息，进行必要的安全加固。

## 许可证

openMind Library使用木兰宽松许可证第2版（MulanPSL v2）。详见[LICENSE](LICENSE)文件。
