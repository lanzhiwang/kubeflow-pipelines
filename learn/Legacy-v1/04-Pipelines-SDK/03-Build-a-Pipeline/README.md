# Build a Pipeline
建立管道

* https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/build-pipeline/

A tutorial on building pipelines to orchestrate your ML workflow
有关构建管道来编排 ML 工作流程的教程

#### Old Version
旧版

This page is about **Kubeflow Pipelines V1**, please see the [V2 documentation](https://v1-9-branch.kubeflow.org/docs/components/pipelines/) for the latest information.
本页面是关于 Kubeflow Pipelines V1 的，请参阅 V2 文档以获取最新信息。

Note, while the V2 backend is able to run pipelines submitted by the V1 SDK, we strongly recommend [migrating to the V2 SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/user-guides/migration/). For reference, the final release of the V1 SDK was [`kfp==1.8.22`](https://pypi.org/project/kfp/1.8.22/), and its reference documentation is [available here](https://kubeflow-pipelines.readthedocs.io/en/1.8.22/).
请注意，虽然 V2 后端能够运行 V1 SDK 提交的管道，但我们强烈建议迁移到 V2 SDK。作为参考，V1 SDK 的最终版本是 `kfp==1.8.22` ，其参考文档可在此处获取。

A Kubeflow pipeline is a portable and scalable definition of a machine learning (ML) workflow. Each step in your ML workflow, such as preparing data or training a model, is an instance of a pipeline component. This document provides an overview of pipeline concepts and best practices, and instructions describing how to build an ML pipeline.
Kubeflow 管道是机器学习 (ML) 工作流程的可移植且可扩展的定义。 ML 工作流程中的每个步骤（例如准备数据或训练模型）都是管道组件的实例。本文档概述了管道概念和最佳实践，以及描述如何构建 ML 管道的说明。

## Before you begin
在你开始之前

1. Run the following command to install the Kubeflow Pipelines SDK. If you run this command in a Jupyter notebook, restart the kernel after installing the SDK.
  运行以下命令安装 Kubeflow Pipelines SDK。如果您在 Jupyter Notebook 中运行此命令，请在安装 SDK 后重新启动内核。

```bash
pip install kfp --upgrade
```

2. Import the `kfp` and `kfp.components` packages.
  导入 `kfp` 和 `kfp.components` 包。

```python
import kfp
import kfp.components as comp
```

## Understanding pipelines
了解管道

A Kubeflow pipeline is a portable and scalable definition of an ML workflow, based on containers. A pipeline is composed of a set of input parameters and a list of the steps in this workflow. Each step in a pipeline is an instance of a component, which is represented as an instance of [`ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp).
Kubeflow 管道是基于容器的 ML 工作流程的可移植且可扩展的定义。管道由一组输入参数和此工作流中的步骤列表组成。管道中的每个步骤都是组件的一个实例，该组件表示为 `ContainerOp` 的实例。

You can use pipelines to:
您可以使用管道来：

- Orchestrate repeatable ML workflows.
  编排可重复的机器学习工作流程。

- Accelerate experimentation by running a workflow with different sets of hyperparameters.
  通过使用不同的超参数集运行工作流程来加速实验。

### Understanding pipeline components
了解管道组件

A pipeline component is a containerized application that performs one step in a pipeline’s workflow. Pipeline components are defined in [component specifications](https://v1-9-branch.kubeflow.org/docs/components/pipelines/reference/component-spec/), which define the following:
管道组件是一种容器化应用程序，它执行管道工作流程中的一个步骤。管道组件在组件规范中定义，其中定义了以下内容：

- The component’s interface, its inputs and outputs.
  组件的接口、输入和输出。
- The component’s implementation, the container image and the command to execute.
  组件的实现、容器镜像和要执行的命令。
- The component’s metadata, such as the name and description of the component.
  组件的元数据，例如组件的名称和描述。

You can build components by [defining a component specification for a containerized application](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/component-development/), or you can [use the Kubeflow Pipelines SDK to generate a component specification for a Python function](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/). You can also [reuse prebuilt components in your pipeline](https://v1-9-branch.kubeflow.org/docs/examples/shared-resources/).
您可以通过为容器化应用程序定义组件规范来构建组件，也可以使用 Kubeflow Pipelines SDK 为 Python 函数生成组件规范。您还可以在管道中重复使用预构建的组件。

### Understanding the pipeline graph
了解管道图

Each step in your pipeline’s workflow is an instance of a component. When you define your pipeline, you specify the source of each step’s inputs. Step inputs can be set from the pipeline’s input arguments, constants, or step inputs can depend on the outputs of other steps in this pipeline. Kubeflow Pipelines uses these dependencies to define your pipeline’s workflow as a graph.
管道工作流程中的每个步骤都是组件的一个实例。定义管道时，您需要指定每个步骤输入的来源。步骤输入可以根据管道的输入参数、常量进行设置，或者步骤输入可以取决于此管道中其他步骤的输出。 Kubeflow Pipelines 使用这些依赖项将管道的工作流程定义为图形。

For example, consider a pipeline with the following steps: ingest data, generate statistics, preprocess data, and train a model. The following describes the data dependencies between each step.
例如，考虑一个具有以下步骤的管道：摄取数据、生成统计数据、预处理数据和训练模型。下面描述各个步骤之间的数据依赖关系。

- **Ingest data**: This step loads data from an external source which is specified using a pipeline argument, and it outputs a dataset. Since this step does not depend on the output of any other steps, this step can run first.
  摄取数据：此步骤从使用管道参数指定的外部源加载数据，并输出数据集。由于此步骤不依赖于任何其他步骤的输出，因此可以先运行此步骤。

- **Generate statistics**: This step uses the ingested dataset to generate and output a set of statistics. Since this step depends on the dataset produced by the ingest data step, it must run after the ingest data step.
  生成统计数据：此步骤使用摄取的数据集生成并输出一组统计数据。由于此步骤取决于摄取数据步骤生成的数据集，因此它必须在摄取数据步骤之后运行。

- **Preprocess data**: This step preprocesses the ingested dataset and transforms the data into a preprocessed dataset. Since this step depends on the dataset produced by the ingest data step, it must run after the ingest data step.
  预处理数据：此步骤对摄取的数据集进行预处理，并将数据转换为预处理数据集。由于此步骤取决于摄取数据步骤生成的数据集，因此它必须在摄取数据步骤之后运行。

- **Train a model**: This step trains a model using the preprocessed dataset, the generated statistics, and pipeline parameters, such as the learning rate. Since this step depends on the preprocessed data and the generated statistics, it must run after both the preprocess data and generate statistics steps are complete.
  训练模型：此步骤使用预处理的数据集、生成的统计数据和管道参数（例如学习率）来训练模型。由于此步骤取决于预处理数据和生成的统计信息，因此必须在预处理数据和生成统计信息步骤完成后运行。

Since the generate statistics and preprocess data steps both depend on the ingested data, the generate statistics and preprocess data steps can run in parallel. All other steps are executed once their data dependencies are available.
由于生成统计数据和预处理数据步骤都取决于摄取的数据，因此生成统计数据和预处理数据步骤可以并行运行。一旦其数据依赖性可用，所有其他步骤都会被执行。

## Designing your pipeline
设计您的管道

When designing your pipeline, think about how to split your ML workflow into pipeline components. The process of splitting an ML workflow into pipeline components is similar to the process of splitting a monolithic script into testable functions. The following rules can help you define the components that you need to build your pipeline.
设计管道时，请考虑如何将 ML 工作流程拆分为管道组件。将 ML 工作流拆分为管道组件的过程类似于将整体脚本拆分为可测试函数的过程。以下规则可以帮助您定义构建管道所需的组件。

- Components should have a single responsibility. Having a single responsibility makes it easier to test and reuse a component. For example, if you have a component that loads data you can reuse that for similar tasks that load data. If you have a component that loads and transforms a dataset, the component can be less useful since you can use it only when you need to load and transform that dataset.
  组件应该有单一的职责。拥有单一职责可以更轻松地测试和重用组件。例如，如果您有一个加载数据的组件，您可以将其重用于加载数据的类似任务。如果您有一个加载和转换数据集的组件，则该组件可能不太有用，因为只有在需要加载和转换该数据集时才能使用它。

- Reuse components when possible. Kubeflow Pipelines provides [components for common pipeline tasks and for access to cloud services](https://v1-9-branch.kubeflow.org/docs/examples/shared-resources/).
  尽可能重用组件。 Kubeflow Pipelines 提供用于常见管道任务和访问云服务的组件。

- Consider what you need to know to debug your pipeline and research the lineage of the models that your pipeline produces. Kubeflow Pipelines stores the inputs and outputs of each pipeline step. By interrogating the artifacts produced by a pipeline run, you can better understand the variations in model quality between runs or track down bugs in your workflow.
  考虑调试管道并研究管道生成的模型的沿袭需要了解哪些内容。 Kubeflow Pipelines 存储每个管道步骤的输入和输出。通过询问管道运行生成的工件，您可以更好地了解运行之间模型质量的变化或跟踪工作流程中的错误。

In general, you should design your components with composability in mind.
一般来说，您在设计组件时应该考虑到可组合性。

Pipelines are composed of component instances, also called steps. Steps can define their inputs as depending on the output of another step. The dependencies between steps define the pipeline workflow graph.
管道由组件实例（也称为步骤）组成。步骤可以将其输入定义为取决于另一个步骤的输出。步骤之间的依赖关系定义了管道工作流程图。

### Building pipeline components
建筑管道组件

Kubeflow pipeline components are containerized applications that perform a step in your ML workflow. Here are the ways that you can define pipeline components:
Kubeflow 管道组件是容器化应用程序，用于执行 ML 工作流程中的步骤。以下是定义管道组件的方法：

- If you have a containerized application that you want to use as a pipeline component, create a component specification to define this container image as a pipeline component.
  如果您有一个想要用作管道组件的容器化应用程序，请创建组件规范以将此容器映像定义为管道组件。

  This option provides the flexibility to include code written in any language in your pipeline, so long as you can package the application as a container image. Learn more about [building pipeline components](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/component-development/).
  此选项提供了在管道中包含以任何语言编写的代码的灵活性，只要您可以将应用程序打包为容器映像即可。了解有关构建管道组件的更多信息。

- If your component code can be expressed as a Python function, [evaluate if your component can be built as a Python function-based component](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/). The Kubeflow Pipelines SDK makes it easier to build lightweight Python function-based components by saving you the effort of creating a component specification.
  如果您的组件代码可以表示为 Python 函数，请评估您的组件是否可以构建为基于 Python 函数的组件。 Kubeflow Pipelines SDK 可以帮助您更轻松地构建轻量级基于 Python 函数的组件，从而节省您创建组件规范的精力。

Whenever possible, [reuse prebuilt components](https://v1-9-branch.kubeflow.org/docs/examples/shared-resources/) to save yourself the effort of building custom components.
只要有可能，就重用预构建的组件，以节省构建自定义组件的精力。

The example in this guide demonstrates how to build a pipeline that uses a Python function-based component and reuses a prebuilt component.
本指南中的示例演示了如何构建使用基于 Python 函数的组件并重用预构建组件的管道。

### Understanding how data is passed between components
了解数据如何在组件之间传递

When Kubeflow Pipelines runs a component, a container image is started in a Kubernetes Pod and your component’s inputs are passed in as command-line arguments. When your component has finished, the component’s outputs are returned as files.
当 Kubeflow Pipelines 运行组件时，容器映像会在 Kubernetes Pod 中启动，组件的输入将作为命令行参数传入。当您的组件完成后，组件的输出将作为文件返回。

In your component’s specification, you define the components inputs and outputs and how the inputs and output paths are passed to your program as command-line arguments. You can pass small inputs, such as short strings or numbers, to your component by value. Large inputs, such as datasets, must be passed to your component as file paths. Outputs are written to the paths that Kubeflow Pipelines provides.
在组件的规范中，您定义组件的输入和输出以及如何将输入和输出路径作为命令行参数传递到程序。您可以按值将小型输入（例如短字符串或数字）传递给组件。大型输入（例如数据集）必须作为文件路径传递到组件。输出写入 Kubeflow Pipelines 提供的路径。

Python function-based components make it easier to build pipeline components by building the component specification for you. Python function-based components also handle the complexity of passing inputs into your component and passing your function’s outputs back to your pipeline.
基于 Python 函数的组件通过为您构建组件规范，使构建管道组件变得更加容易。基于 Python 函数的组件还可以处理将输入传递到组件以及将函数的输出传递回管道的复杂性。

Learn more about how [Python function-based components handle inputs and outputs](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/#understanding-how-data-is-passed-between-components).
详细了解基于 Python 函数的组件如何处理输入和输出。

## Getting started building a pipeline
开始构建管道

The following sections demonstrate how to get started building a Kubeflow pipeline by walking through the process of converting a Python script into a pipeline.
以下部分演示如何通过逐步将 Python 脚本转换为管道的过程来开始构建 Kubeflow 管道。

### Design your pipeline
设计您的管道

The following steps walk through some of the design decisions you may face when designing a pipeline.
以下步骤将介绍您在设计管道时可能面临的一些设计决策。

1. Evaluate the process. In the following example, a Python function downloads a zipped tar file (`.tar.gz`) that contains several CSV files, from a public website. The function extracts the CSV files and then merges them into a single file.
  评估过程。在以下示例中，Python 函数从公共网站下载包含多个 CSV 文件的压缩 tar 文件 ( `.tar.gz` )。该函数提取 CSV 文件，然后将它们合并为一个文件。

```python
import glob
import pandas as pd
import tarfile
import urllib.request


def download_and_merge_csv(url: str, output_csv: str):
    with urllib.request.urlopen(url) as res:
        tarfile.open(fileobj=res, mode="r|gz").extractall('data')
    df = pd.concat([
        pd.read_csv(csv_file, header=None)
        for csv_file in glob.glob('data/*.csv')
    ])
    df.to_csv(output_csv, index=False, header=False)

```

2. Run the following Python command to test the function.
  运行以下Python命令来测试该功能。

```python
download_and_merge_csv(
    url=
    'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz',
    output_csv='merged_data.csv')
```

3. Run the following to print the first few rows of the merged CSV file.
  运行以下命令打印合并的 CSV 文件的前几行。

```bash
head merged_data.csv
```

4. Design your pipeline. For example, consider the following pipeline designs.
  设计您的管道。例如，考虑以下管道设计。

  - Implement the pipeline using a single step. In this case, the pipeline contains one component that works similarly to the example function. This is a straightforward function, and implementing a single-step pipeline is a reasonable approach in this case.
    使用单个步骤实现管道。在这种情况下，管道包含一个与示例函数类似的组件。这是一个简单的函数，在这种情况下实现单步管道是一种合理的方法。

    The down side of this approach is that the zipped tar file would not be an artifact of your pipeline runs. Not having this artifact available could make it harder to debug this component in production.
    这种方法的缺点是压缩的 tar 文件不会成为管道运行的工件。如果没有此工件，可能会导致在生产中调试此组件变得更加困难。

  - Implement this as a two-step pipeline. The first step downloads a file from a website. The second step extracts the CSV files from a zipped tar file and merges them into a single file.
    将其实现为两步管道。第一步从网站下载文件。第二步从压缩的 tar 文件中提取 CSV 文件并将它们合并到单个文件中。

    This approach has a few benefits:
    这种方法有一些好处：

    - You can reuse the [Web Download component](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/components/web/Download/component.yaml) to implement the first step.
      您可以重用Web Download组件来实现第一步。

    - Each step has a single responsibility, which makes the components easier to reuse.
      每个步骤都有一个职责，这使得组件更容易重用。

    - The zipped tar file is an artifact of the first pipeline step. This means that you can examine this artifact when debugging pipelines that use this component.
      压缩的 tar 文件是第一个管道步骤的产物。这意味着您可以在调试使用此组件的管道时检查此工件。

  This example implements a two-step pipeline.
  此示例实现了两步管道。

### Build your pipeline components
构建您的管道组件

1. Build your pipeline components. This example modifies the initial script to extract the contents of a zipped tar file, merge the CSV files that were contained in the zipped tar file, and return the merged CSV file.
  构建您的管道组件。此示例修改初始脚本以提取压缩 tar 文件的内容、合并压缩 tar 文件中包含的 CSV 文件，并返回合并的 CSV 文件。

  This example builds a Python function-based component. You can also package your component’s code as a Docker container image and define the component using a ComponentSpec.
  此示例构建一个基于 Python 函数的组件。您还可以将组件的代码打包为 Docker 容器映像，并使用 ComponentSpec 定义组件。

  In this case, the following modifications were required to the original function.
  在这种情况下，需要对原来的功能进行如下修改。

  - The file download logic was removed. The path to the zipped tar file is passed as an argument to this function.
    文件下载逻辑已被删除。压缩 tar 文件的路径作为参数传递给该函数。

  - The import statements were moved inside of the function. Python function-based components require standalone Python functions. This means that any required import statements must be defined within the function, and any helper functions must be defined within the function. Learn more about [building Python function-based components](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/).
    导入语句已移至函数内部。基于 Python 函数的组件需要独立的 Python 函数。这意味着任何必需的导入语句都必须在函数内定义，并且任何辅助函数都必须在函数内定义。了解有关构建基于 Python 函数的组件的更多信息。

  - The function’s arguments are decorated with the [`kfp.components.InputPath`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html?highlight=inputpath#kfp.components.InputPath) and the [`kfp.components.OutputPath`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html?highlight=outputpath#kfp.components.OutputPath) annotations. These annotations let Kubeflow Pipelines know to provide the path to the zipped tar file and to create a path where your function stores the merged CSV file.
    该函数的参数用 `kfp.components.InputPath` 和 `kfp.components.OutputPath` 注释进行修饰。这些注释让 Kubeflow Pipelines 知道提供压缩 tar 文件的路径并创建函数存储合并的 CSV 文件的路径。

  The following example shows the updated `merge_csv` function.
  以下示例显示更新后的 `merge_csv` 函数。


```python
def merge_csv(file_path: comp.InputPath('Tarball'),
              output_csv: comp.OutputPath('CSV')):
    import glob
    import pandas as pd
    import tarfile

    tarfile.open(name=file_path, mode="r|gz").extractall('data')
    df = pd.concat([
        pd.read_csv(csv_file, header=None)
        for csv_file in glob.glob('data/*.csv')
    ])
    df.to_csv(output_csv, index=False, header=False)
```

2. Use [`kfp.components.create_component_from_func`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html#kfp.components.create_component_from_func) to return a factory function that you can use to create pipeline steps. This example also specifies the base container image to run this function in, the path to save the component specification to, and a list of PyPI packages that need to be installed in the container at runtime.
  使用 `kfp.components.create_component_from_func` 返回可用于创建管道步骤的工厂函数。此示例还指定了运行此函数的基础容器映像、保存组件规范的路径以及运行时需要在容器中安装的 PyPI 包的列表。

```python
create_step_merge_csv = kfp.components.create_component_from_func(
    func=merge_csv,
    output_component_file=
    'merge_csv_component.yaml',  # This is optional. It saves the component spec for future use.
    base_image='python:3.7',
    packages_to_install=['pandas==1.1.4'])
```

### Build your pipeline
建立您的管道

1. Use [`kfp.components.load_component_from_url`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html?highlight=load_component_from_url#kfp.components.load_component_from_url) to load the component specification YAML for any components that you are reusing in this pipeline.
  使用 `kfp.components.load_component_from_url` 加载您在此管道中重用的任何组件的组件规范 YAML。

```python
web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml'
)
```

2. Define your pipeline as a Python function.
  将管道定义为 Python 函数。

  Your pipeline function’s arguments define your pipeline’s parameters. Use pipeline parameters to experiment with different hyperparameters, such as the learning rate used to train a model, or pass run-level inputs, such as the path to an input file, into a pipeline run.
  您的管道函数的参数定义了管道的参数。使用管道参数来试验不同的超参数（例如用于训练模型的学习率），或将运行级别输入（例如输入文件的路径）传递到管道运行中。

  Use the factory functions created by `kfp.components.create_component_from_func` and `kfp.components.load_component_from_url` to create your pipeline’s tasks. The inputs to the component factory functions can be pipeline parameters, the outputs of other tasks, or a constant value. In this case, the `web_downloader_task` task uses the `url` pipeline parameter, and the `merge_csv_task` uses the `data` output of the `web_downloader_task`.
  使用 `kfp.components.create_component_from_func` 和 `kfp.components.load_component_from_url` 创建的工厂函数来创建管道的任务。组件工厂函数的输入可以是管道参数、其他任务的输出或常量值。在本例中， `web_downloader_task` 任务使用 `url` 管道参数， `merge_csv_task` 使用 `web_downloader_task` 输出。

```python
# Define a pipeline and create a task from a component:
def my_pipeline(url):
    web_downloader_task = web_downloader_op(url=url)
    merge_csv_task = create_step_merge_csv(
        file=web_downloader_task.outputs['data'])
    # The outputs of the merge_csv_task can be referenced using the
    # merge_csv_task.outputs dictionary: merge_csv_task.outputs['output_csv']
```

### Compile and run your pipeline
编译并运行您的管道

After defining the pipeline in Python as described in the preceding section, use one of the following options to compile the pipeline and submit it to the Kubeflow Pipelines service.
按照上一节所述在 Python 中定义管道后，使用以下选项之一来编译管道并将其提交到 Kubeflow Pipelines 服务。

#### Option 1: Compile and then upload in UI
选项1：编译然后在UI中上传

1. Run the following to compile your pipeline and save it as `pipeline.yaml`.
  运行以下命令来编译管道并将其保存为 `pipeline.yaml` 。

```python
kfp.compiler.Compiler().compile(pipeline_func=my_pipeline,
                                package_path='pipeline.yaml')
```

2. Upload and run your `pipeline.yaml` using the Kubeflow Pipelines user interface. See the guide to [getting started with the UI](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/overview/quickstart/).
  使用 Kubeflow Pipelines 用户界面上传并运行您的 `pipeline.yaml` 。请参阅 UI 入门指南。

#### Option 2: run the pipeline using Kubeflow Pipelines SDK client
选项 2：使用 Kubeflow Pipelines SDK 客户端运行管道

1. Create an instance of the [`kfp.Client` class](https://kubeflow-pipelines.readthedocs.io/en/stable/source/client.html#kfp.Client) following steps in [connecting to Kubeflow Pipelines using the SDK client](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/connect-api).
  按照使用 SDK 客户端连接到 Kubeflow Pipelines 的步骤创建 `kfp.Client` 类的实例。

```python
client = kfp.Client()  # change arguments accordingly
```

2. Run the pipeline using the `kfp.Client` instance:
  使用 `kfp.Client` 实例运行管道：

```python
client.create_run_from_pipeline_func(
    my_pipeline,
    arguments={
        'url':
        'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz'
    })
```
