# Building Python function-based components
构建基于 Python 函数的组件

* https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/

Building your own lightweight pipelines components using Python
使用 Python 构建您自己的轻量级管道组件

#### Old Version
旧版

This page is about **Kubeflow Pipelines V1**, please see the [V2 documentation](https://v1-9-branch.kubeflow.org/docs/components/pipelines/) for the latest information.
本页面是关于 Kubeflow Pipelines V1 的，请参阅 V2 文档以获取最新信息。

Note, while the V2 backend is able to run pipelines submitted by the V1 SDK, we strongly recommend [migrating to the V2 SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/user-guides/migration/). For reference, the final release of the V1 SDK was [`kfp==1.8.22`](https://pypi.org/project/kfp/1.8.22/), and its reference documentation is [available here](https://kubeflow-pipelines.readthedocs.io/en/1.8.22/).
请注意，虽然 V2 后端能够运行 V1 SDK 提交的管道，但我们强烈建议迁移到 V2 SDK。作为参考，V1 SDK 的最终版本是 `kfp==1.8.22` ，其参考文档可在此处获取。

A Kubeflow Pipelines component is a self-contained set of code that performs one step in your ML workflow. A pipeline component is composed of:
Kubeflow Pipelines 组件是一组独立的代码，用于执行 ML 工作流程中的一个步骤。管道组件由以下部分组成：

- The component code, which implements the logic needed to perform a step in your ML workflow.
  组件代码，用于实现在 ML 工作流程中执行步骤所需的逻辑。

- A component specification, which defines the following:
  组件规范，定义以下内容：

  - The component’s metadata, its name and description.
    组件的元数据、名称和描述。

  - The component’s interface, the component’s inputs and outputs.
    组件的接口，组件的输入和输出。

  - The component’s implementation, the Docker container image to run, how to pass inputs to your component code, and how to get the component’s outputs.
    组件的实现、要运行的 Docker 容器映像、如何将输入传递到组件代码以及如何获取组件的输出。

Python function-based components make it easier to iterate quickly by letting you build your component code as a Python function and generating the [component specification](https://v1-9-branch.kubeflow.org/docs/components/pipelines/reference/component-spec/) for you. This document describes how to build Python function-based components and use them in your pipeline.
基于 Python 函数的组件让您可以将组件代码构建为 Python 函数并为您生成组件规范，从而使快速迭代变得更加容易。本文档介绍了如何构建基于 Python 函数的组件并在管道中使用它们。

## Before you begin
在你开始之前

1. Run the following command to install the Kubeflow Pipelines SDK. If you run this command in a Jupyter notebook, restart the kernel after installing the SDK.
  运行以下命令安装 Kubeflow Pipelines SDK。如果您在 Jupyter Notebook 中运行此命令，请在安装 SDK 后重新启动内核。

```bash
pip install kfp==1.8
```

2. Import the `kfp` package.
  导入 `kfp` 包。

```python
import kfp
from kfp.components import create_component_from_func
```

3. Create an instance of the [`kfp.Client` class](https://kubeflow-pipelines.readthedocs.io/en/stable/source/client.html#kfp.Client) following steps in [connecting to Kubeflow Pipelines using the SDK client](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/connect-api).
  按照使用 SDK 客户端连接到 Kubeflow Pipelines 的步骤创建 `kfp.Client` 类的实例。

```python
client = kfp.Client()  # change arguments accordingly
```

For more information about the Kubeflow Pipelines SDK, see the [SDK reference guide](https://kubeflow-pipelines.readthedocs.io/en/stable/index.html).
有关 Kubeflow Pipelines SDK 的更多信息，请参阅 SDK 参考指南。

## Getting started with Python function-based components
基于 Python 函数的组件入门

This section demonstrates how to get started building Python function-based components by walking through the process of creating a simple component.
本节演示如何通过逐步创建简单组件的过程来开始构建基于 Python 函数的组件。

1. Define your component’s code as a [standalone Python function](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/#standalone). In this example, the function adds two floats and returns the sum of the two arguments.
  将组件的代码定义为独立的 Python 函数。在此示例中，该函数将两个浮点数相加并返回两个参数的总和。

```python
def add(a: float, b: float) -> float:
    '''Calculates sum of two arguments'''
    return a + b
```

2. Use `kfp.components.create_component_from_func` to generate the component specification YAML and return a factory function that you can use to create [`kfp.dsl.ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp) class instances for your pipeline. The component specification YAML is a reusable and shareable definition of your component.
  使用 `kfp.components.create_component_from_func` 生成组件规范 YAML 并返回可用于为管道创建 `kfp.dsl.ContainerOp` 类实例的工厂函数。组件规范 YAML 是组件的可重用且可共享的定义。

```python
add_op = create_component_from_func(add,
                                    output_component_file='add_component.yaml')
```

3. Create and run your pipeline. [Learn more about creating and running pipelines](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/component-development/).
  创建并运行您的管道。了解有关创建和运行管道的更多信息。

```python
import kfp.dsl as dsl


@dsl.pipeline(
    name='Addition pipeline',
    description='An example pipeline that performs addition calculations.')
def add_pipeline(
    a='1',
    b='7',
):
    # Passes a pipeline parameter and a constant value to the `add_op` factory
    # function.
    first_add_task = add_op(a, 4)
    # Passes an output reference from `first_add_task` and a pipeline parameter
    # to the `add_op` factory function. For operations with a single return
    # value, the output reference can be accessed as `task.output` or
    # `task.outputs['output_name']`.
    second_add_task = add_op(first_add_task.output, b)


# Specify argument values for your pipeline run.
arguments = {'a': '7', 'b': '8'}

# Create a pipeline run, using the client you initialized in a prior step.
client.create_run_from_pipeline_func(add_pipeline, arguments=arguments)

```

## Building Python function-based components
构建基于 Python 函数的组件

Use the following instructions to build a Python function-based component:
使用以下说明构建基于 Python 函数的组件：

1. Define a standalone Python function. This function must meet the following requirements:
  定义一个独立的 Python 函数。该功能必须满足以下要求：

  - It should not use any code declared outside of the function definition.
    它不应使用在函数定义之外声明的任何代码。

  - Import statements must be added inside the function. [Learn more about using and installing Python packages in your component](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/#packages).
    必须在函数内部添加导入语句。了解有关在组件中使用和安装 Python 包的更多信息。

  - Helper functions must be defined inside this function.
    辅助函数必须在此函数内定义。

2. Kubeflow Pipelines uses your function’s inputs and outputs to define your component’s interface. [Learn more about passing data between components](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/#pass-data). Your function’s inputs and outputs must meet the following requirements:
  Kubeflow Pipelines 使用函数的输入和输出来定义组件的接口。了解有关在组件之间传递数据的更多信息。您的函数的输入和输出必须满足以下要求：

  - If the function accepts or returns large amounts of data or complex data types, you must pass that data as a file. [Learn more about using large amounts of data as inputs or outputs](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/#pass-by-file).
    如果函数接受或返回大量数据或复杂数据类型，则必须将该数据作为文件传递。了解有关使用大量数据作为输入或输出的更多信息。

  - If the function accepts numeric values as parameters, the parameters must have type hints. Supported types are `int` and `float`. Otherwise, parameters are passed as strings.
    如果函数接受数值作为参数，则参数必须具有类型提示。支持的类型是 `int` 和 `float` 。否则，参数将作为字符串传递。

  - If your component returns multiple small outputs (short strings, numbers, or booleans), annotate your function with the [`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) type hint and use the [`collections.namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple) function return your function’s outputs as a new subclass of tuple. For an example, read [Passing parameters by value](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/#pass-by-value).
    如果您的组件返回多个小输出（短字符串、数字或布尔值），请使用 `typing.NamedTuple` 类型提示注释您的函数，并使用 `collections.namedtuple` 函数将函数的输出作为新子类返回元组。有关示例，请阅读按值传递参数。

3. (Optional.) If your function has complex dependencies, choose or build a container image for your Python function to run in. [Learn more about selecting or building your component’s container image](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/#containers).
  （可选。）如果您的函数具有复杂的依赖项，请选择或构建要运行的 Python 函数的容器映像。了解有关选择或构建组件的容器映像的更多信息。

4. Call [`kfp.components.create_component_from_func(func)`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.create_component_from_func) to convert your function into a pipeline component.
  调用 `kfp.components.create_component_from_func(func)` 将您的函数转换为管道组件。

  - **func**: The Python function to convert.
    func：要转换的Python函数。

  - **base_image**: (Optional.) Specify the Docker container image to run this function in. [Learn more about selecting or building a container image](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/#containers).
    base_image：（可选。）指定要在其中运行此函数的 Docker 容器映像。了解有关选择或构建容器映像的更多信息。

  - **output_component_file**: (Optional.) Writes your component definition to a file. You can use this file to share the component with colleagues or reuse it in different pipelines.
    output_component_file：（可选。）将组件定义写入文件。您可以使用此文件与同事共享组件或在不同的管道中重用它。

  - **packages_to_install**: (Optional.) A list of versioned Python packages to install before running your function.
    packages_to_install：（可选。）运行函数之前要安装的版本化 Python 包列表。

### Using and installing Python packages
使用和安装 Python 包

When Kubeflow Pipelines runs your pipeline, each component runs within a Docker container image on a Kubernetes Pod. To load the packages that your Python function depends on, one of the following must be true:
当 Kubeflow Pipelines 运行管道时，每个组件都在 Kubernetes Pod 上的 Docker 容器映像中运行。要加载 Python 函数所依赖的包，必须满足以下条件之一：

- The package must be installed on the container image.
  该包必须安装在容器映像上。

- The package must be defined using the `packages_to_install` parameter of the [`kfp.components.create_component_from_func(func)`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.create_component_from_func) function.
  必须使用 `kfp.components.create_component_from_func(func)` 函数的 `packages_to_install` 参数定义包。

- Your function must install the package. For example, your function can use the [`subprocess` module](https://docs.python.org/3/library/subprocess.html) to run a command like `pip install` that installs a package.
  您的函数必须安装该包。例如，您的函数可以使用 `subprocess` 模块来运行诸如 `pip install` 之类的安装包的命令。

### Selecting or building a container image
选择或构建容器镜像

Currently, if you do not specify a container image, your Python-function based component uses the [`python:3.7` container image](https://hub.docker.com/layers/python/library/python/3.7/images/sha256-7eef781ed825f3b95c99f03f4189a8e30e718726e8490651fa1b941c6c815ad1?context=explore). If your function has complex dependencies, you may benefit from using a container image that has your dependencies preinstalled, or building a custom container image. Preinstalling your dependencies reduces the amount of time that your component runs in, since your component does not need to download and install packages each time it runs.
目前，如果您不指定容器映像，则基于 Python 函数的组件将使用 `python:3.7` 容器映像。如果您的函数具有复杂的依赖项，您可能会受益于使用预安装了依赖项的容器映像，或构建自定义容器映像。预安装依赖项可以减少组件运行的时间，因为组件不需要在每次运行时下载和安装包。

Many frameworks, such as [TensorFlow](https://www.tensorflow.org/install/docker) and [PyTorch](https://hub.docker.com/r/pytorch/pytorch/tags), and cloud service providers offer prebuilt container images that have common dependencies installed.
许多框架（例如 TensorFlow 和 PyTorch）和云服务提供商都提供安装了常见依赖项的预构建容器映像。

If a prebuilt container is not available, you can build a custom container image with your Python function’s dependencies. For more information about building a custom container, read the [Dockerfile reference guide in the Docker documentation](https://docs.docker.com/engine/reference/builder/).
如果预构建的容器不可用，您可以使用 Python 函数的依赖项构建自定义容器映像。有关构建自定义容器的更多信息，请阅读 Docker 文档中的 Dockerfile 参考指南。

If you build or select a container image, instead of using the default container image, the container image must use Python 3.5 or later.
如果您构建或选择容器映像，则容器映像必须使用 Python 3.5 或更高版本，而不是使用默认容器映像。

### Understanding how data is passed between components
了解数据如何在组件之间传递

When Kubeflow Pipelines runs your component, a container image is started in a Kubernetes Pod and your component’s inputs are passed in as command-line arguments. When your component has finished, the component’s outputs are returned as files.
当 Kubeflow Pipelines 运行您的组件时，容器映像将在 Kubernetes Pod 中启动，并且组件的输入将作为命令行参数传入。当您的组件完成后，组件的输出将作为文件返回。

Python function-based components make it easier to build pipeline components by building the component specification for you. Python function-based components also handle the complexity of passing inputs into your component and passing your function’s outputs back to your pipeline.
基于 Python 函数的组件通过为您构建组件规范，使构建管道组件变得更加容易。基于 Python 函数的组件还可以处理将输入传递到组件以及将函数的输出传递回管道的复杂性。

The following sections describe how to pass parameters by value and by file.
以下部分描述如何按值和按文件传递参数。

- Parameters that are passed by value include numbers, booleans, and short strings. Kubeflow Pipelines passes parameters to your component by value, by passing the values as command-line arguments.
  按值传递的参数包括数字、布尔值和短字符串。 Kubeflow Pipelines 通过将值作为命令行参数传递，按值将参数传递给组件。

- Parameters that are passed by file include CSV, images, and complex types. These files are stored in a location that is accessible to your component running on Kubernetes, such as a persistent volume claim or a cloud storage service. Kubeflow Pipelines passes parameters to your component by file, by passing their paths as a command-line argument.
  通过文件传递的参数包括 CSV、图像和复杂类型。这些文件存储在 Kubernetes 上运行的组件可访问的位置，例如持久卷声明或云存储服务。 Kubeflow Pipelines 通过文件将参数传递给您的组件，将其路径作为命令行参数传递。

#### Input and output parameter names
输入和输出参数名称

When you use the Kubeflow Pipelines SDK to convert your Python function to a pipeline component, the Kubeflow Pipelines SDK uses the function’s interface to define the interface of your component in the following ways:
当您使用 Kubeflow Pipelines SDK 将 Python 函数转换为管道组件时，Kubeflow Pipelines SDK 使用函数的接口通过以下方式定义组件的接口：

- Some arguments define input parameters.
  一些参数定义输入参数。

- Some arguments define output parameters.
  一些参数定义输出参数。

- The function’s return value is used as an output parameter. If the return value is a [`collections.namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple), the named tuple is used to return several small values.
  函数的返回值用作输出参数。如果返回值是 `collections.namedtuple` ，则使用命名元组返回几个小值。

Since you can pass parameters between components as a value or as a path, the Kubeflow Pipelines SDK removes common parameter suffixes that leak the component’s expected implementation. For example, a Python function-based component that ingests data and outputs CSV data may have an output argument that is defined as `csv_path: comp.OutputPath(str)`. In this case, the output is the CSV data, not the path. So, the Kubeflow Pipelines SDK simplifies the output name to `csv`.
由于您可以在组件之间以值或路径的形式传递参数，因此 Kubeflow Pipelines SDK 删除了泄露组件预期实现的常见参数后缀。例如，提取数据并输出 CSV 数据的基于 Python 函数的组件可能具有定义为 `csv_path: comp.OutputPath(str)` 的输出参数。在这种情况下，输出是 CSV 数据，而不是路径。因此，Kubeflow Pipelines SDK 将输出名称简化为 `csv` 。

The Kubeflow Pipelines SDK uses the following rules to define the input and output parameter names in your component’s interface:
Kubeflow Pipelines SDK 使用以下规则来定义组件接口中的输入和输出参数名称：

- If the argument name ends with `_path` and the argument is annotated as an [`kfp.components.InputPath`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.InputPath) or [`kfp.components.OutputPath`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.OutputPath), the parameter name is the argument name with the trailing `_path` removed.
  如果参数名称以 `_path` 结尾并且参数注释为 `kfp.components.InputPath` 或 `kfp.components.OutputPath` ，则参数名称是尾随 `_path`

- If the argument name ends with `_file`, the parameter name is the argument name with the trailing `_file` removed.
  如果参数名称以 `_file` 结尾，则参数名称是删除了尾部 `_file` 的参数名称。

- If you return a single small value from your component using the `return` statement, the output parameter is named `output`.
  如果使用 `return` 语句从组件返回单个小值，则输出参数将命名为 `output` 。

- If you return several small values from your component by returning a [`collections.namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple), the Kubeflow Pipelines SDK uses the tuple’s field names as the output parameter names.
  如果您通过返回 `collections.namedtuple` 从组件返回几个小值，Kubeflow Pipelines SDK 将使用元组的字段名称作为输出参数名称。

Otherwise, the Kubeflow Pipelines SDK uses the argument name as the parameter name.
否则，Kubeflow Pipelines SDK 使用参数名称作为参数名称。

#### Passing parameters by value
按值传递参数

Python function-based components make it easier to pass parameters between components by value (such as numbers, booleans, and short strings), by letting you define your component’s interface by annotating your Python function. The supported types are `int`, `float`, `bool`, and `str`. You can also pass `list` or `dict` instances by value, if they contain small values, such as `int`, `float`, `bool`, or `str` values. If you do not annotate your function, these input parameters are passed as strings.
基于 Python 函数的组件让您可以通过注释 Python 函数来定义组件的接口，从而更轻松地按值（例如数字、布尔值和短字符串）在组件之间传递参数。支持的类型有 `int` 、 `float` 、 `bool` 和 `str` 。您还可以按值传递 `list` 或 `dict` 实例（如果它们包含较小的值），例如 `int` 、 `float` 、 `bool` 或 `str` 值。如果您没有注释您的函数，这些输入参数将作为字符串传递。

If your component returns multiple outputs by value, annotate your function with the [`typing.NamedTuple`](https://docs.python.org/3/library/typing.html#typing.NamedTuple) type hint and use the [`collections.namedtuple`](https://docs.python.org/3/library/collections.html#collections.namedtuple) function to return your function’s outputs as a new subclass of `tuple`.
如果您的组件按值返回多个输出，请使用 `typing.NamedTuple` 类型提示注释您的函数，并使用 `collections.namedtuple` 函数将函数的输出作为 `tuple` .

You can also return metadata and metrics from your function.
您还可以从函数返回元数据和指标。

- Metadata helps you visualize pipeline results. [Learn more about visualizing pipeline metadata](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/output-viewer/).
  元数据可帮助您可视化管道结果。了解有关可视化管道元数据的更多信息。

- Metrics help you compare pipeline runs. [Learn more about using pipeline metrics](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/pipelines-metrics/).
  指标可帮助您比较管道运行情况。了解有关使用管道指标的更多信息。

The following example demonstrates how to return multiple outputs by value, including component metadata and metrics.
以下示例演示如何按值返回多个输出，包括组件元数据和指标。

```python
from typing import NamedTuple


def multiple_return_values_example(
    a: float, b: float
) -> NamedTuple('ExampleOutputs', [('sum', float), ('product', float),
                                   ('mlpipeline_ui_metadata', 'UI_metadata'),
                                   ('mlpipeline_metrics', 'Metrics')]):
    """Example function that demonstrates how to return multiple values."""
    sum_value = a + b
    product_value = a * b

    # Export a sample tensorboard
    metadata = {
        'outputs': [{
            'type': 'tensorboard',
            'source': 'gs://ml-pipeline-dataset/tensorboard-train',
        }]
    }

    # Export two metrics
    metrics = {
        'metrics': [{
            'name': 'sum',
            'numberValue': float(sum_value),
        }, {
            'name': 'product',
            'numberValue': float(product_value),
        }]
    }

    from collections import namedtuple
    example_output = namedtuple(
        'ExampleOutputs',
        ['sum', 'product', 'mlpipeline_ui_metadata', 'mlpipeline_metrics'])
    return example_output(sum_value, product_value, metadata, metrics)

```

#### Passing parameters by file
通过文件传递参数

Python function-based components make it easier to pass files to your component, or to return files from your component, by letting you annotate your Python function’s parameters to specify which parameters refer to a file. Your Python function’s parameters can refer to either input or output files. If your parameter is an output file, Kubeflow Pipelines passes your function a path or stream that you can use to store your output file.
基于 Python 函数的组件允许您注释 Python 函数的参数以指定哪些参数引用文件，从而可以更轻松地将文件传递到组件或从组件返回文件。 Python 函数的参数可以引用输入或输出文件。如果您的参数是输出文件，Kubeflow Pipelines 会向您的函数传递可用于存储输出文件的路径或流。

The following example accepts a file as an input and returns two files as outputs.
以下示例接受一个文件作为输入并返回两个文件作为输出。

```python
def split_text_lines(source_path: comp.InputPath(str),
                     odd_lines_path: comp.OutputPath(str),
                     even_lines_path: comp.OutputPath(str)):
    """Splits a text file into two files, with even lines going to one file
    and odd lines to the other."""

    with open(source_path, 'r') as reader:
        with open(odd_lines_path, 'w') as odd_writer:
            with open(even_lines_path, 'w') as even_writer:
                while True:
                    line = reader.readline()
                    if line == "":
                        break
                    odd_writer.write(line)
                    line = reader.readline()
                    if line == "":
                        break
                    even_writer.write(line)

```

In this example, the inputs and outputs are defined as parameters of the `split_text_lines` function. This lets Kubeflow Pipelines pass the path to the source data file and the paths to the output data files into the function.
在此示例中，输入和输出被定义为 `split_text_lines` 函数的参数。这让 Kubeflow Pipelines 将源数据文件的路径和输出数据文件的路径传递到函数中。

To accept a file as an input parameter, use one of the following type annotations:
要接受文件作为输入参数，请使用以下类型注释之一：

- [`kfp.components.InputBinaryFile`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.InputBinaryFile): Use this annotation to specify that your function expects a parameter to be an [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) instance that this function can read.
  `kfp.components.InputBinaryFile` ：使用此注释指定您的函数期望参数是该函数可以读取的 `io.BytesIO` 实例。

- [`kfp.components.InputPath`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.InputPath): Use this annotation to specify that your function expects a parameter to be the path to the input file as a `string`.
  `kfp.components.InputPath` ：使用此注释指定您的函数期望参数作为输入文件的路径，如 `string` 。

- [`kfp.components.InputTextFile`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.InputTextFile): Use this annotation to specify that your function expects a parameter to be an [`io.TextIOWrapper`](https://docs.python.org/3/library/io.html#io.TextIOWrapper) instance that this function can read.
  `kfp.components.InputTextFile` ：使用此注释指定您的函数期望参数是该函数可以读取的 `io.TextIOWrapper` 实例。

To return a file as an output, use one of the following type annotations:
要将文件作为输出返回，请使用以下类型注释之一：

- [`kfp.components.OutputBinaryFile`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.OutputBinaryFile): Use this annotation to specify that your function expects a parameter to be an [`io.BytesIO`](https://docs.python.org/3/library/io.html#io.BytesIO) instance that this function can write to.
  `kfp.components.OutputBinaryFile` ：使用此注释指定您的函数期望参数是该函数可以写入的 `io.BytesIO` 实例。

- [`kfp.components.OutputPath`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.OutputPath): Use this annotation to specify that your function expects a parameter to be the path to store the output file at as a `string`.
  `kfp.components.OutputPath` ：使用此注释指定您的函数需要一个参数作为将输出文件存储为 `string` 的路径。

- [`kfp.components.OutputTextFile`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.OutputTextFile): Use this annotation to specify that your function expects a parameter to be an [`io.TextIOWrapper`](https://docs.python.org/3/library/io.html#io.TextIOWrapper) that this function can write to.
  `kfp.components.OutputTextFile` ：使用此注释指定您的函数期望参数是该函数可以写入的 `io.TextIOWrapper` 。

## Example Python function-based component
基于 Python 函数的组件示例

This section demonstrates how to build a Python function-based component that uses imports, helper functions, and produces multiple outputs.
本节演示如何构建一个基于 Python 函数的组件，该组件使用导入、辅助函数并生成多个输出。

1. Define your function. This example function uses the `numpy` package to calculate the quotient and remainder for a given dividend and divisor in a helper function. In addition to the quotient and remainder, the function also returns metadata for visualization and two metrics.
  定义你的函数。此示例函数使用 `numpy` 包来计算辅助函数中给定被除数和除数的商和余数。除了商和余数之外，该函数还返回用于可视化的元数据和两个指标。

```python
from typing import NamedTuple


def my_divmod(
    dividend: float, divisor: float
) -> NamedTuple('MyDivmodOutput', [('quotient', float), ('remainder', float),
                                   ('mlpipeline_ui_metadata', 'UI_metadata'),
                                   ('mlpipeline_metrics', 'Metrics')]):
    '''Divides two numbers and calculate  the quotient and remainder'''

    # Import the numpy package inside the component function
    import numpy as np

    # Define a helper function
    def divmod_helper(dividend, divisor):
        return np.divmod(dividend, divisor)

    (quotient, remainder) = divmod_helper(dividend, divisor)

    from tensorflow.python.lib.io import file_io
    import json

    # Export a sample tensorboard
    metadata = {
        'outputs': [{
            'type': 'tensorboard',
            'source': 'gs://ml-pipeline-dataset/tensorboard-train',
        }]
    }

    # Export two metrics
    metrics = {
        'metrics': [{
            'name': 'quotient',
            'numberValue': float(quotient),
        }, {
            'name': 'remainder',
            'numberValue': float(remainder),
        }]
    }

    from collections import namedtuple
    divmod_output = namedtuple('MyDivmodOutput', [
        'quotient', 'remainder', 'mlpipeline_ui_metadata', 'mlpipeline_metrics'
    ])
    return divmod_output(quotient, remainder, json.dumps(metadata),
                         json.dumps(metrics))

```

2. Test your function by running it directly, or with unit tests.
  通过直接运行或使用单元测试来测试您的函数。

```python
my_divmod(100, 7)
```

3. This should return a result like the following:
  这应该返回如下结果：

  ```bash
  MyDivmodOutput(
	quotient=14,
	remainder=2,
	mlpipeline_ui_metadata='{"outputs": [{"type": "tensorboard", "source": "gs://ml-pipeline-dataset/tensorboard-train"}]}',
	mlpipeline_metrics='{"metrics": [{"name": "quotient", "numberValue": 14.0}, {"name": "remainder", "numberValue": 2.0}]}'
  )
  ```

4. Use `kfp.components.create_component_from_func` to return a factory function that you can use to create [`kfp.dsl.ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp) class instances for your pipeline. This example also specifies the base container image to run this function in.
  使用 `kfp.components.create_component_from_func` 返回一个工厂函数，您可以使用该函数为管道创建 `kfp.dsl.ContainerOp` 类实例。此示例还指定了运行此函数的基础容器映像。

```python
divmod_op = comp.create_component_from_func(
    my_divmod, base_image='tensorflow/tensorflow:1.11.0-py3')
```

4. Define your pipeline. This example uses the `divmod_op` factory function and the `add_op` factory function from an earlier example.
  定义您的管道。此示例使用前面示例中的 `divmod_op` 工厂函数和 `add_op` 工厂函数。

```python
import kfp.dsl as dsl


@dsl.pipeline(
    name='Calculation pipeline',
    description='An example pipeline that performs arithmetic calculations.')
def calc_pipeline(
    a='1',
    b='7',
    c='17',
):
    # Passes a pipeline parameter and a constant value as operation arguments.
    add_task = add_op(a, 4)  # The add_op factory function returns
    # a dsl.ContainerOp class instance.

    # Passes the output of the add_task and a pipeline parameter as operation
    # arguments. For an operation with a single return value, the output
    # reference is accessed using `task.output` or
    # `task.outputs['output_name']`.
    divmod_task = divmod_op(add_task.output, b)

    # For an operation with multiple return values, output references are
    # accessed as `task.outputs['output_name']`.
    result_task = add_op(divmod_task.outputs['quotient'], c)

```

5. Compile and run your pipeline. [Learn more about compiling and running pipelines](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/component-development/).
  编译并运行您的管道。了解有关编译和运行管道的更多信息。

```python
# Specify pipeline argument values
arguments = {'a': '7', 'b': '8'}

# Submit a pipeline run
client.create_run_from_pipeline_func(calc_pipeline, arguments=arguments)
```
