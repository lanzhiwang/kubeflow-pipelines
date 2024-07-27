# Using environment variables in pipelines
在管道中使用环境变量

* https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/enviroment_variables/

How to set and use environment variables in Kubeflow pipelines
如何在 Kubeflow 管道中设置和使用环境变量

#### Old Version
旧版

This page is about **Kubeflow Pipelines V1**, please see the [V2 documentation](https://v1-9-branch.kubeflow.org/docs/components/pipelines/) for the latest information.
本页面是关于 Kubeflow Pipelines V1 的，请参阅 V2 文档以获取最新信息。

Note, while the V2 backend is able to run pipelines submitted by the V1 SDK, we strongly recommend [migrating to the V2 SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/user-guides/migration/). For reference, the final release of the V1 SDK was [`kfp==1.8.22`](https://pypi.org/project/kfp/1.8.22/), and its reference documentation is [available here](https://kubeflow-pipelines.readthedocs.io/en/1.8.22/).
请注意，虽然 V2 后端能够运行 V1 SDK 提交的管道，但我们强烈建议迁移到 V2 SDK。作为参考，V1 SDK 的最终版本是 `kfp==1.8.22` ，其参考文档可在此处获取。

This page describes how to pass environment variables to Kubeflow pipeline components.
本页介绍如何将环境变量传递给 Kubeflow 管道组件。

## Before you start
在你开始之前

Set up your environment:
设置您的环境：

- [Install Kubeflow](https://v1-9-branch.kubeflow.org/docs/started/)
  安装 Kubeflow

- [Install the Kubeflow Pipelines SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/install-sdk/)
  安装 Kubeflow Pipelines SDK

## Using environment variables
使用环境变量

In this example, you pass an environment variable to a lightweight Python component, which writes the variable’s value to the log.
在此示例中，您将环境变量传递给轻量级 Python 组件，该组件将变量的值写入日志。

[Learn more about lightweight Python components](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/lightweight-python-components/)
了解有关轻量级 Python 组件的更多信息

To build a component, define a stand-alone Python function and then call [kfp.components.func_to_container_op(func)](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.func_to_container_op) to convert the function to a component that can be used in a pipeline. The following function gets an environment variable and writes it to the log.
要构建组件，请定义一个独立的 Python 函数，然后调用 kfp.components.func_to_container_op(func) 将函数转换为可在管道中使用的组件。以下函数获取环境变量并将其写入日志。

```python
def logg_env_function():
    import os
    import logging
    logging.basicConfig(level=logging.INFO)
    env_variable = os.getenv('example_env')
    logging.info('The environment variable is: {}'.format(env_variable))
```

Transform the function into a component using [kfp.components.func_to_container_op(func)](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.func_to_container_op).
使用 kfp.components.func_to_container_op(func) 将函数转换为组件。

```python
image_name = 'tensorflow/tensorflow:1.11.0-py3'
logg_env_function_op = comp.func_to_container_op(logg_env_function,
                                                 base_image=image_name)
```

Add this component to a pipeline. Use [add_env_variable](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp.container) to pass an environment variable into the component. This code is the same no matter if your using python lightweight components or a [container operation](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp).
将此组件添加到管道中。使用 add_env_variable 将环境变量传递到组件中。无论你使用Python轻量级组件还是容器操作，这段代码都是相同的。

```python
import kfp.dsl as dsl
from kubernetes.client.models import V1EnvVar


@dsl.pipeline(
    name='Env example',
    description='A pipeline showing how to use environment variables')
def environment_pipeline():
    env_var = V1EnvVar(name='example_env', value='env_variable')
    #Returns a dsl.ContainerOp class instance.
    container_op = logg_env_function_op().add_env_variable(env_var)
```

To pass more environment variables into a component, add more instances of [add_env_variable()](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp.container). Use the following command to run this pipeline using the Kubeflow Pipelines SDK.
要将更多环境变量传递到组件中，请添加更多 add_env_variable() 实例。使用以下命令通过 Kubeflow Pipelines SDK 运行此管道。

```python
# Specify pipeline argument values
arguments = {}

# Submit a pipeline run
kfp.Client().create_run_from_pipeline_func(environment_pipeline,
                                           arguments=arguments)
```
