# Building Components
建筑构件

* https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/component-development/

A tutorial on how to create components and use them in a pipeline
有关如何创建组件并在管道中使用它们的教程

#### Old Version 旧版

This page is about **Kubeflow Pipelines V1**, please see the [V2 documentation](https://v1-9-branch.kubeflow.org/docs/components/pipelines/) for the latest information.
本页面是关于 Kubeflow Pipelines V1 的，请参阅 V2 文档以获取最新信息。

Note, while the V2 backend is able to run pipelines submitted by the V1 SDK, we strongly recommend [migrating to the V2 SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/user-guides/migration/). For reference, the final release of the V1 SDK was [`kfp==1.8.22`](https://pypi.org/project/kfp/1.8.22/), and its reference documentation is [available here](https://kubeflow-pipelines.readthedocs.io/en/1.8.22/).
请注意，虽然 V2 后端能够运行 V1 SDK 提交的管道，但我们强烈建议迁移到 V2 SDK。作为参考，V1 SDK 的最终版本是 `kfp==1.8.22` ，其参考文档可在此处获取。

A pipeline component is a self-contained set of code that performs one step in your ML workflow. This document describes the concepts required to build components, and demonstrates how to get started building components.
管道组件是一组独立的代码，用于执行 ML 工作流程中的一个步骤。本文档描述了构建组件所需的概念，并演示了如何开始构建组件。

## Before you begin
在你开始之前

Run the following command to install the Kubeflow Pipelines SDK.
运行以下命令安装 Kubeflow Pipelines SDK。

```bash
pip install kfp==1.8
```

For more information about the Kubeflow Pipelines SDK, see the [SDK reference guide](https://kubeflow-pipelines.readthedocs.io/en/stable/index.html).
有关 Kubeflow Pipelines SDK 的更多信息，请参阅 SDK 参考指南。

## Understanding pipeline components
了解管道组件

Pipeline components are self-contained sets of code that perform one step in your ML workflow, such as preprocessing data or training a model. To create a component, you must *build the component’s implementation* and *define the component specification*.
管道组件是一组独立的代码，用于执行 ML 工作流程中的一个步骤，例如预处理数据或训练模型。要创建组件，您必须构建组件的实现并定义组件规范。

Your component’s implementation includes the component’s executable code and the Docker container image that the code runs in. [Learn more about designing a pipeline component](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/component-development/#design).
组件的实现包括组件的可执行代码和运行代码的 Docker 容器映像。了解有关设计管道组件的更多信息。

Once you have built your component’s implementation, you can define your component’s interface as a component specification. A component specification defines:
一旦构建了组件的实现，您就可以将组件的接口定义为组件规范。组件规范定义：

- The component’s inputs and outputs.
  组件的输入和输出。

- The container image that your component’s code runs in, the command to use to run your component’s code, and the command-line arguments to pass to your component’s code.
  组件代码在其中运行的容器映像、用于运行组件代码的命令以及传递给组件代码的命令行参数。

- The component’s metadata, such as the name and description.
  组件的元数据，例如名称和描述。

[Learn more about creating a component specification](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/component-development/#component-spec).
了解有关创建组件规范的更多信息。

If your component’s code is implemented as a Python function, use the Kubeflow Pipelines SDK to package your function as a component. [Learn more about building Python function-based components](https://www.kubeflow.org/docs/pipelines/sdk/python-function-components/).
如果您的组件的代码是作为 Python 函数实现的，请使用 Kubeflow Pipelines SDK 将您的函数打包为组件。了解有关构建基于 Python 函数的组件的更多信息。

## Designing a pipeline component
设计管道组件

When Kubeflow Pipelines executes a component, a container image is started in a Kubernetes Pod and your component’s inputs are passed in as command-line arguments. You can pass small inputs, such as strings and numbers, by value. Larger inputs, such as CSV data, must be passed as paths to files. When your component has finished, the component’s outputs are returned as files.
当 Kubeflow Pipelines 执行组件时，容器映像会在 Kubernetes Pod 中启动，组件的输入将作为命令行参数传入。您可以按值传递小型输入，例如字符串和数字。较大的输入（例如 CSV 数据）必须作为文件路径传递。当您的组件完成后，组件的输出将作为文件返回。

When you design your component’s code, consider the following:
当您设计组件的代码时，请考虑以下事项：

- Which inputs can be passed to your component by value? Examples of inputs that you can pass by value include numbers, booleans, and short strings. Any value that you could reasonably pass as a command-line argument can be passed to your component by value. All other inputs are passed to your component by a reference to the input’s path.
  哪些输入可以按值传递给您的组件？可以按值传递的输入示例包括数字、布尔值和短字符串。您可以合理地作为命令行参数传递的任何值都可以按值传递给您的组件。所有其他输入都通过对输入路径的引用传递到您的组件。

- To return an output from your component, the output’s data must be stored as a file. When you define your component, you let Kubeflow Pipelines know what outputs your component produces. When your pipeline runs, Kubeflow Pipelines passes the paths that you use to store your component’s outputs as inputs to your component.
  要从组件返回输出，输出的数据必须存储为文件。当您定义组件时，您可以让 Kubeflow Pipelines 了解组件产生的输出。当您的管道运行时，Kubeflow Pipelines 会将您用于存储组件输出的路径传递为组件的输入。

- Outputs are typically written to a single file. In some cases, you may need to return a directory of files as an output. In this case, create a directory at the output path and write the output files to that location. In both cases, it may be necessary to create parent directories if they do not exist.
  输出通常写入单个文件。在某些情况下，您可能需要返回文件目录作为输出。在这种情况下，请在输出路径中创建一个目录并将输出文件写入该位置。在这两种情况下，如果父目录不存在，则可能需要创建它们。

- Your component’s goal may be to create a dataset in an external service, such as a BigQuery table. In this case, it may make sense for the component to output an identifier for the produced data, such as a table name, instead of the data itself. We recommend that you limit this pattern to cases where the data must be put into an external system instead of keeping it inside the Kubeflow Pipelines system.
  您的组件的目标可能是在外部服务中创建数据集，例如 BigQuery 表。在这种情况下，组件输出所生成数据的标识符（例如表名称）而不是数据本身可能是有意义的。我们建议您将此模式限制为数据必须放入外部系统而不是将其保留在 Kubeflow Pipelines 系统内的情况。

- Since your inputs and output paths are passed in as command-line arguments, your component’s code must be able to read inputs from the command line. If your component is built with Python, libraries such as [argparse](https://docs.python.org/3/library/argparse.html) and [absl.flags](https://abseil.io/docs/python/guides/flags) make it easier to read your component’s inputs.
  由于输入和输出路径作为命令行参数传入，因此组件的代码必须能够从命令行读取输入。如果您的组件是使用 Python 构建的，则 argparse 和 absl.flags 等库可以更轻松地读取组件的输入。

- Your component’s code can be implemented in any language, so long as it can run in a container image.
  您的组件的代码可以用任何语言实现，只要它可以在容器映像中运行即可。

The following is an example program written using Python3. This program reads a given number of lines from an input file and writes those lines to an output file. This means that this function accepts three command-line parameters:
以下是使用Python3编写的示例程序。该程序从输入文件中读取给定数量的行并将这些行写入输出文件。这意味着该函数接受三个命令行参数：

- The path to the input file.
  输入文件的路径。
- The number of lines to read.
  要读取的行数。
- The path to the output file.
  输出文件的路径。

```python
import argparse
from pathlib import Path


# Function doing the actual work (Outputs first N lines from a text file)
def do_work(input1_file, output1_file, param1):
    for x, line in enumerate(input1_file):
        if x >= param1:
            break
        _ = output1_file.write(line)


# Defining and parsing the command-line arguments
parser = argparse.ArgumentParser(description='My program description')
# Paths must be passed in, not hardcoded
parser.add_argument('--input1-path',
                    type=str,
                    help='Path of the local file containing the Input 1 data.')
parser.add_argument(
    '--output1-path',
    type=str,
    help='Path of the local file where the Output 1 data should be written.')
parser.add_argument(
    '--param1',
    type=int,
    default=100,
    help='The number of lines to read from the input and write to the output.')
args = parser.parse_args()

# Creating the directory where the output file is created (the directory
# may or may not exist).
Path(args.output1_path).parent.mkdir(parents=True, exist_ok=True)

with open(args.input1_path, 'r') as input1_file:
    with open(args.output1_path, 'w') as output1_file:
        do_work(input1_file, output1_file, args.param1)
```

If this program is saved as `program.py`, the command-line invocation of this program is:
如果该程序保存为 `program.py` ，则该程序的命令行调用为：

```bash
python program.py --input1-path /workspaces/kubeflow-pipelines/learn/Legacy-v1/04-Pipelines-SDK/04-Building-Components/program.py \
--param1 5 \
--output1-path /workspaces/kubeflow-pipelines/learn/Legacy-v1/04-Pipelines-SDK/04-Building-Components/out/out.py

```

## Containerize your component’s code
将组件的代码容器化

For Kubeflow Pipelines to run your component, your component must be packaged as a [Docker](https://docs.docker.com/get-started/) container image and published to a container registry that your Kubernetes cluster can access. The steps to create a container image are not specific to Kubeflow Pipelines. To make things easier for you, this section provides some guidelines on standard container creation.
为了让 Kubeflow Pipelines 运行您的组件，您的组件必须打包为 Docker 容器映像并发布到 Kubernetes 集群可以访问的容器注册表。创建容器映像的步骤并非特定于 Kubeflow Pipelines。为了让您更轻松，本节提供了一些有关标准容器创建的指南。

1. Create a [Dockerfile](https://docs.docker.com/engine/reference/builder/) for your container. A Dockerfile specifies:
  为您的容器创建一个 Dockerfile。 Dockerfile 指定：

  - The base container image. For example, the operating system that your code runs on.
    基础容器镜像。例如，您的代码运行的操作系统。

  - Any dependencies that need to be installed for your code to run.
    需要安装代码才能运行的任何依赖项。

  - Files to copy into the container, such as the runnable code for this component.
    要复制到容器中的文件，例如该组件的可运行代码。

  The following is an example Dockerfile.
  以下是 Dockerfile 示例。

  ```Dockerfile
  FROM python:3.7
  RUN python3 -m pip install keras
  COPY ./src /pipelines/component/src
  ```

  In this example:
  在这个例子中：

  - The base container image is [`python:3.7`](https://hub.docker.com/_/python).
    基础容器镜像是 `python:3.7` 。

  - The `keras` Python package is installed in the container image.
    `keras` Python 包安装在容器映像中。

  - Files in your `./src` directory are copied into `/pipelines/component/src` in the container image.
    `./src` 目录中的文件将复制到容器映像中的 `/pipelines/component/src` 中。

2. Create a script named `build_image.sh` that uses Docker to build your container image and push your container image to a container registry. Your Kubernetes cluster must be able to access your container registry to run your component. Examples of container registries include [Google Container Registry](https://cloud.google.com/container-registry/docs/) and [Docker Hub](https://hub.docker.com/).
  创建一个名为 `build_image.sh` 的脚本，该脚本使用 Docker 构建容器映像并将容器映像推送到容器注册表。您的 Kubernetes 集群必须能够访问容器注册表才能运行您的组件。容器注册表的示例包括 Google 容器注册表和 Docker Hub。

  The following example builds a container image, pushes it to a container registry, and outputs the strict image name. It is a best practice to use the strict image name in your component specification to ensure that you are using the expected version of a container image in each component execution.
  以下示例构建容器映像，将其推送到容器注册表，并输出严格的映像名称。最佳实践是在组件规范中使用严格的映像名称，以确保在每个组件执行中使用预期版本的容器映像。

  ```bash
  #!/bin/bash -e
  image_name=gcr.io/my-org/my-image
  image_tag=latest
  full_image_name=${image_name}:${image_tag}

  cd "$(dirname "$0")"
  docker build -t "${full_image_name}" .
  docker push "$full_image_name"

  # Output the strict image name, which contains the sha256 image digest
  docker inspect --format="{{index .RepoDigests 0}}" "${full_image_name}"
  ```

  In the preceding example:
  在前面的示例中：

  - The `image_name` specifies the full name of your container image in the container registry.
    `image_name` 指定容器注册表中容器映像的全名。

  - The `image_tag` specifies that this image should be tagged as **latest**.
    `image_tag` 指定该图像应标记为最新图像。

  Save this file and run the following to make this script executable.
  保存此文件并运行以下命令以使该脚本可执行。

  ```bash
  chmod +x build_image.sh
  ```

3. Run your `build_image.sh` script to build your container image and push it to a container registry.
  运行 `build_image.sh` 脚本来构建容器映像并将其推送到容器注册表。

4. [Use `docker run` to test your container image locally](https://docs.docker.com/engine/reference/commandline/run/). If necessary, revise your application and Dockerfile until your application works as expected in the container.
  使用 `docker run` 在本地测试您的容器映像。如有必要，请修改您的应用程序和 Dockerfile，直到您的应用程序在容器中按预期工作。

## Creating a component specification
创建组件规范

To create a component from your containerized program, you must create a component specification that defines the component’s interface and implementation. The following sections provide an overview of how to create a component specification by demonstrating how to define the component’s implementation, interface, and metadata.
要从容器化程序创建组件，您必须创建定义组件的接口和实现的组件规范。以下部分通过演示如何定义组件的实现、接口和元数据来概述如何创建组件规范。

To learn more about defining a component specification, see the [component specification reference guide](https://v1-9-branch.kubeflow.org/docs/components/pipelines/reference/component-spec/).
要了解有关定义组件规范的更多信息，请参阅组件规范参考指南。

### Define your component’s implementation
定义组件的实现

The following example creates a component specification YAML and defines the component’s implementation.
以下示例创建组件规范 YAML 并定义组件的实现。

1. Create a file named `component.yaml` and open it in a text editor.
  创建一个名为 `component.yaml` 的文件并在文本编辑器中打开它。

2. Create your component’s implementation section and specify the strict name of your container image. The strict image name is provided when you run your `build_image.sh` script.
  创建组件的实现部分并指定容器映像的严格名称。运行 `build_image.sh` 脚本时会提供严格的图像名称。

```yaml
implementation:
  container:
    image: gcr.io/my-org/my-image@sha256:a172..752f
```

1. Define a `command` for your component’s implementation. This field specifies the command-line arguments that are used to run your program in the container.
  为组件的实现定义 `command` 。此字段指定用于在容器中运行程序的命令行参数。

```yaml
implementation:
  container:
    image: gcr.io/my-org/my-image@sha256:a172..752f
    # command is a list of strings (command-line arguments).
    # The YAML language has two syntaxes for lists and you can use either of them.
    # Here we use the "flow syntax" - comma-separated strings inside square brackets.
    command: [
        python3,
        # Path of the program inside the container
        /pipelines/component/src/program.py,
        --input1-path,
        { inputPath: Input 1 },
        --param1,
        { inputValue: Parameter 1 },
        --output1-path,
        { outputPath: Output 1 },
      ]

```

  The `command` is formatted as a list of strings. Each string in the `command` is a command-line argument or a placeholder. At runtime, placeholders are replaced with an input or output. In the preceding example, two inputs and one output path are passed into a Python script at `/pipelines/component/src/program.py`.
  `command` 被格式化为字符串列表。 `command` 中的每个字符串都是命令行参数或占位符。在运行时，占位符被替换为输入或输出。在前面的示例中，两个输入和一个输出路径被传递到 `/pipelines/component/src/program.py` 处的 Python 脚本中。

  There are three types of input/output placeholders:
  输入/输出占位符分为三种类型：

  - `{inputValue: <input-name>}`: This placeholder is replaced with the value of the specified input. This is useful for small pieces of input data, such as numbers or small strings.
    `{inputValue: <input-name>}` ：此占位符将替换为指定输入的值。这对于小块输入数据非常有用，例如数字或小字符串。

  - `{inputPath: <input-name>}`: This placeholder is replaced with the path to this input as a file. Your component can read the contents of that input at that path during the pipeline run.
    `{inputPath: <input-name>}` ：此占位符将替换为此输入文件的路径。您的组件可以在管道运行期间读取该路径上的输入内容。

  - `{outputPath: <output-name>}`: This placeholder is replaced with the path where your program writes this output’s data. This lets the Kubeflow Pipelines system read the contents of the file and store it as the value of the specified output.
    `{outputPath: <output-name>}` ：此占位符将替换为程序写入此输出数据的路径。这让 Kubeflow Pipelines 系统读取文件的内容并将其存储为指定输出的值。

The `<input-name>` name must match the name of an input in the `inputs` section of your component specification. The `<output-name>` name must match the name of an output in the `outputs` section of your component specification.
 `<input-name>` 名称必须与组件规范的 `inputs` 部分中的输入名称匹配。 `<output-name>` 名称必须与组件规范的 `outputs` 部分中的输出名称匹配。

### Define your component’s interface
定义组件的接口

The following examples demonstrate how to specify your component’s interface.
以下示例演示了如何指定组件的接口。

1. To define an input in your `component.yaml`, add an item to the `inputs` list with the following attributes:
  要在 `component.yaml` 中定义输入，请将具有以下属性的项目添加到 `inputs` 列表中：

  - `name`: Human-readable name of this input. Each input’s name must be unique.
    `name` ：此输入的人类可读名称。每个输入的名称必须是唯一的。

  - `description`: (Optional.) Human-readable description of the input.
    `description` ：（可选。）人类可读的输入描述。

  - `default`: (Optional.) Specifies the default value for this input.
    `default` ：（可选。）指定此输入的默认值。

  - `type`: (Optional.) Specifies the input’s type. Learn more about the [types defined in the Kubeflow Pipelines SDK](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/sdk/python/kfp/dsl/types.py) and [how type checking works in pipelines and components](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/static-type-checking/).
    `type` ：（可选。）指定输入的类型。详细了解 Kubeflow Pipelines SDK 中定义的类型以及类型检查在管道和组件中的工作原理。

  - `optional`: Specifies if this input is optional. The value of this attribute is of type `Bool`, and defaults to **False**.
    `optional` ：指定此输入是否可选。该属性的值是 `Bool` 类型，默认为 False。

  In this example, the Python program has two inputs:
  在此示例中，Python 程序有两个输入：

  - `Input 1` contains `String` data.
    `Input 1` 包含 `String` 数据。

  - `Parameter 1` contains an `Integer`.
    `Parameter 1` 包含 `Integer` 。

```yaml
inputs:
  - { name: Input 1, type: String, description: "Data for input 1" }
  - {
      name: Parameter 1,
      type: Integer,
      default: "100",
      description: "Number of lines to copy",
    }

```

  Note: `Input 1` and `Parameter 1` do not specify any details about how they are stored or how much data they contain. Consider using naming conventions to indicate if inputs are expected to be small enough to pass by value.
  注意： `Input 1` 和 `Parameter 1` 未指定有关它们如何存储或包含多少数据的任何详细信息。考虑使用命名约定来指示输入是否足够小以按值传递。

2. After your component finishes its task, the component’s outputs are passed to your pipeline as paths. At runtime, Kubeflow Pipelines creates a path for each of your component’s outputs. These paths are passed as inputs to your component’s implementation.
  组件完成其任务后，组件的输出将作为路径传递到管道。在运行时，Kubeflow Pipelines 为每个组件的输出创建一个路径。这些路径作为输入传递给组件的实现。

  To define an output in your component specification YAML, add an item to the `outputs` list with the following attributes:
  要在组件规范 YAML 中定义输出，请使用以下属性将项目添加到 `outputs` 列表：

  - `name`: Human-readable name of this output. Each output’s name must be unique.
    `name` ：此输出的人类可读名称。每个输出的名称必须是唯一的。

  - `description`: (Optional.) Human-readable description of the output.
    `description` ：（可选。）人类可读的输出描述。

  - `type`: (Optional.) Specifies the output’s type. Learn more about the [types defined in the Kubeflow Pipelines SDK](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/sdk/python/kfp/dsl/types.py) and [how type checking works in pipelines and components](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/static-type-checking/).
    `type` ：（可选。）指定输出的类型。详细了解 Kubeflow Pipelines SDK 中定义的类型以及类型检查在管道和组件中的工作原理。

  In this example, the Python program returns one output. The output is named `Output 1` and it contains `String` data.
  在此示例中，Python 程序返回一个输出。输出名为 `Output 1` 并且包含 `String` 数据。

```yaml
outputs:
  - { name: Output 1, type: String, description: "Output 1 data." }

```

  Note: Consider using naming conventions to indicate if this output is expected to be small enough to pass by value. You should limit the amount of data that is passed by value to 200 KB per pipeline run.
  注意：考虑使用命名约定来指示该输出是否足够小以按值传递。您应该将每次管道运行按值传递的数据量限制为 200 KB。

3. After you define your component’s interface, the `component.yaml` should be something like the following:
  定义组件的接口后， `component.yaml` 应类似于以下内容：

```yaml
inputs:
  - { name: Input 1, type: String, description: "Data for input 1" }
  - {
      name: Parameter 1,
      type: Integer,
      default: "100",
      description: "Number of lines to copy",
    }
outputs:
  - { name: Output 1, type: String, description: "Output 1 data." }
implementation:
  container:
    image: gcr.io/my-org/my-image@sha256:a172..752f
    # command is a list of strings (command-line arguments).
    # The YAML language has two syntaxes for lists and you can use either of them.
    # Here we use the "flow syntax" - comma-separated strings inside square brackets.
    command: [
        python3,
        # Path of the program inside the container
        /pipelines/component/src/program.py,
        --input1-path,
        { inputPath: Input 1 },
        --param1,
        { inputValue: Parameter 1 },
        --output1-path,
        { outputPath: Output 1 },
      ]

```

### Specify your component’s metadata
指定组件的元数据

To define your component’s metadata, add the `name` and `description` fields to your `component.yaml`
要定义组件的元数据，请将 `name` 和 `description` 字段添加到 `component.yaml`

```yaml
name: Get Lines
description: Gets the specified number of lines from the input file.
inputs:
  - { name: Input 1, type: String, description: "Data for input 1" }
  - {
      name: Parameter 1,
      type: Integer,
      default: "100",
      description: "Number of lines to copy",
    }
outputs:
  - { name: Output 1, type: String, description: "Output 1 data." }
implementation:
  container:
    image: gcr.io/my-org/my-image@sha256:a172..752f
    # command is a list of strings (command-line arguments).
    # The YAML language has two syntaxes for lists and you can use either of them.
    # Here we use the "flow syntax" - comma-separated strings inside square brackets.
    command: [
        python3,
        # Path of the program inside the container
        /pipelines/component/src/program.py,
        --input1-path,
        { inputPath: Input 1 },
        --param1,
        { inputValue: Parameter 1 },
        --output1-path,
        { outputPath: Output 1 },
      ]

```

## Using your component in a pipeline
在管道中使用您的组件

You can use the Kubeflow Pipelines SDK to load your component using methods such as the following:
您可以使用 Kubeflow Pipelines SDK 通过以下方法加载组件：

- [`kfp.components.load_component_from_file`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.load_component_from_file): Use this method to load your component from a `component.yaml` path.
  `kfp.components.load_component_from_file` ：使用此方法从 `component.yaml` 路径加载组件。

- [`kfp.components.load_component_from_url`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.load_component_from_url): Use this method to load a `component.yaml` from a URL.
  `kfp.components.load_component_from_url` ：使用此方法从 URL 加载 `component.yaml` 。

- [`kfp.components.load_component_from_text`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.load_component_from_text): Use this method to load your component specification YAML from a string. This method is useful for rapidly iterating on your component specification.
  `kfp.components.load_component_from_text` ：使用此方法从字符串加载组件规范 YAML。此方法对于快速迭代组件规范很有用。

These functions create a factory function that you can use to create [`ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp) instances to use as steps in your pipeline. This factory function’s input arguments include your component’s inputs and the paths to your component’s outputs. The function signature may be modified in the following ways to ensure that it is valid and Pythonic.
这些函数创建一个工厂函数，您可以使用它来创建 `ContainerOp` 实例以用作管道中的步骤。该工厂函数的输入参数包括组件的输入和组件输出的路径。可以通过以下方式修改函数签名，以确保其有效且符合 Python 风格。

- Inputs with default values will come after the inputs without default values and outputs.
  具有默认值的输入将出现在没有默认值的输入和输出之后。

- Input and output names are converted to Pythonic names (spaces and symbols are replaced with underscores and letters are converted to lowercase). For example, an input named `Input 1` is converted to `input_1`.
  输入和输出名称被转换为Pythonic名称（空格和符号被下划线替换，字母被转换为小写）。例如，名为 `Input 1` 的输入将转换为 `input_1` 。

The following example demonstrates how to load the text of your component specification and run it in a two-step pipeline. Before you run this example, update the component specification to use the component specification you defined in the previous sections.
以下示例演示了如何加载组件规范的文本并在两步管道中运行它。在运行此示例之前，请更新组件规范以使用您在前面部分中定义的组件规范。

To demonstrate data passing between components, we create another component that simply uses bash commands to write some text value to an output file. And the output file can be passed to our previous component as an input.
为了演示组件之间的数据传递，我们创建了另一个组件，它仅使用 bash 命令将一些文本值写入输出文件。输出文件可以作为输入传递给我们之前的组件。

```python
import kfp
import kfp.components as comp

create_step_get_lines = comp.load_component_from_text("""
name: Get Lines
description: Gets the specified number of lines from the input file.

inputs:
- {name: Input 1, type: Data, description: 'Data for input 1'}
- {name: Parameter 1, type: Integer, default: '100', description: 'Number of lines to copy'}

outputs:
- {name: Output 1, type: Data, description: 'Output 1 data.'}

implementation:
  container:
    image: gcr.io/my-org/my-image@sha256:a172..752f
    # command is a list of strings (command-line arguments).
    # The YAML language has two syntaxes for lists and you can use either of them.
    # Here we use the "flow syntax" - comma-separated strings inside square brackets.
    command: [
      python3,
      # Path of the program inside the container
      /pipelines/component/src/program.py,
      --input1-path,
      {inputPath: Input 1},
      --param1,
      {inputValue: Parameter 1},
      --output1-path,
      {outputPath: Output 1},
    ]""")

# create_step_get_lines is a "factory function" that accepts the arguments
# for the component's inputs and output paths and returns a pipeline step
# (ContainerOp instance).
#
# To inspect the get_lines_op function in Jupyter Notebook, enter
# "get_lines_op(" in a cell and press Shift+Tab.
# You can also get help by entering `help(get_lines_op)`, `get_lines_op?`,
# or `get_lines_op??`.

# Create a simple component using only bash commands. The output of this component
# can be passed to a downstream component that accepts an input with the same type.
create_step_write_lines = comp.load_component_from_text("""
name: Write Lines
description: Writes text to a file.

inputs:
- {name: text, type: String}

outputs:
- {name: data, type: Data}

implementation:
  container:
    image: busybox
    command:
    - sh
    - -c
    - |
      mkdir -p "$(dirname "$1")"
      echo "$0" > "$1"
    args:
    - {inputValue: text}
    - {outputPath: data}
""")


# Define your pipeline
def my_pipeline():
    write_lines_step = create_step_write_lines(
        text='one\ntwo\nthree\nfour\nfive\nsix\nseven\neight\nnine\nten')

    get_lines_step = create_step_get_lines(
        # Input name "Input 1" is converted to pythonic parameter name "input_1"
        input_1=write_lines_step.outputs['data'],
        parameter_1='5',
    )


# If you run this command on a Jupyter notebook running on Kubeflow,
# you can exclude the host parameter.
# client = kfp.Client()
client = kfp.Client(host='<your-kubeflow-pipelines-host-name>')

# Compile, upload, and submit this pipeline for execution.
client.create_run_from_pipeline_func(my_pipeline, arguments={})

```

## Organizing the component files
组织组件文件

This section provides a recommended way to organize a component’s files. There is no requirement that you must organize the files in this way. However, using the standard organization makes it possible to reuse the same scripts for testing, image building, and component versioning.
本节提供了组织组件文件的推荐方法。不要求您必须以这种方式组织文件。但是，使用标准组织可以重用相同的脚本进行测试、映像构建和组件版本控制。

```zed
components/<component group>/<component name>/

    src/*            # Component source code files
    tests/*          # Unit tests
    run_tests.sh     # Small script that runs the tests
    README.md        # Documentation. If multiple files are needed, move to docs/.

    Dockerfile       # Dockerfile to build the component container image
    build_image.sh   # Small script that runs docker build and docker push

    component.yaml   # Component definition in YAML format
```

See this [sample component](https://github.com/kubeflow/pipelines/tree/sdk/release-1.8/components/sample/keras/train_classifier) for a real-life component example.
请参阅此示例组件以获取现实生活中的组件示例。

