# Introduction to the Pipelines SDK
管道SDK简介

* https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/sdk-overview/

Overview of using the SDK to build components and pipelines
使用SDK构建组件和管道概述

#### Old Version
旧版

This page is about **Kubeflow Pipelines V1**, please see the [V2 documentation](https://v1-9-branch.kubeflow.org/docs/components/pipelines/) for the latest information.
本页面是关于 Kubeflow Pipelines V1 的，请参阅 V2 文档以获取最新信息。

Note, while the V2 backend is able to run pipelines submitted by the V1 SDK, we strongly recommend [migrating to the V2 SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/user-guides/migration/). For reference, the final release of the V1 SDK was [`kfp==1.8.22`](https://pypi.org/project/kfp/1.8.22/), and its reference documentation is [available here](https://kubeflow-pipelines.readthedocs.io/en/1.8.22/).
请注意，虽然 V2 后端能够运行 V1 SDK 提交的管道，但我们强烈建议迁移到 V2 SDK。作为参考，V1 SDK 的最终版本是 `kfp==1.8.22` ，其参考文档可在此处获取。

The [Kubeflow Pipelines SDK](https://kubeflow-pipelines.readthedocs.io/en/stable/source/html) provides a set of Python packages that you can use to specify and run your machine learning (ML) workflows. A *pipeline* is a description of an ML workflow, including all of the *components* that make up the steps in the workflow and how the components interact with each other.
Kubeflow Pipelines SDK 提供了一组 Python 包，您可以使用它们来指定和运行机器学习 (ML) 工作流程。管道是对 ML 工作流程的描述，包括构成工作流程中步骤的所有组件以及组件之间如何交互。

**Note**: The SDK documentation here refers to [Kubeflow Pipelines with Argo](https://github.com/kubeflow/pipelines) which is the default. If you are running [Kubeflow Pipelines with Tekton](https://github.com/kubeflow/kfp-tekton) instead, please follow the [Kubeflow Pipelines SDK for Tekton](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/pipelines-with-tekton/) documentation.
注意：此处的 SDK 文档指的是带有 Argo 的 Kubeflow Pipelines，这是默认值。如果您使用 Tekton 运行 Kubeflow Pipelines，请遵循适用于 Tekton 的 Kubeflow Pipelines SDK 文档。

## SDK packages
SDK包

The Kubeflow Pipelines SDK includes the following packages:
Kubeflow Pipelines SDK 包含以下软件包：

- [`kfp.compiler`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/compiler.html) includes classes and methods for compiling pipeline Python DSL into a workflow yaml spec Methods in this package include, but are not limited to, the following:
  `kfp.compiler` 包含用于将管道 Python DSL 编译为工作流 yaml 规范的类和方法。此包中的方法包括但不限于以下内容：

  - `kfp.compiler.Compiler.compile` compiles your Python DSL code into a single static configuration (in YAML format) that the Kubeflow Pipelines service can process. The Kubeflow Pipelines service converts the static configuration into a set of Kubernetes resources for execution.
    `kfp.compiler.Compiler.compile` 将 Python DSL 代码编译为 Kubeflow Pipelines 服务可以处理的单个静态配置（YAML 格式）。 Kubeflow Pipelines 服务将静态配置转换为一组 Kubernetes 资源来执行。

- [`kfp.components`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/components.html) includes classes and methods for interacting with pipeline components. Methods in this package include, but are not limited to, the following:
  `kfp.components` 包括用于与管道组件交互的类和方法。该包中的方法包括但不限于以下内容：

  - `kfp.components.func_to_container_op` converts a Python function to a pipeline component and returns a factory function. You can then call the factory function to construct an instance of a pipeline task ([`ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp)) that runs the original function in a container.
    `kfp.components.func_to_container_op` 将Python函数转换为管道组件并返回工厂函数。然后，您可以调用工厂函数来构造管道任务 ( `ContainerOp` ) 的实例，该实例在容器中运行原始函数。

  - `kfp.components.load_component_from_file` loads a pipeline component from a file and returns a factory function. You can then call the factory function to construct an instance of a pipeline task ([`ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp)) that runs the component container image.
    `kfp.components.load_component_from_file` 从文件加载管道组件并返回工厂函数。然后，您可以调用工厂函数来构造运行组件容器映像的管道任务 ( `ContainerOp` ) 的实例。

  - `kfp.components.load_component_from_url` loads a pipeline component from a URL and returns a factory function. You can then call the factory function to construct an instance of a pipeline task ([`ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp)) that runs the component container image.
    `kfp.components.load_component_from_url` 从 URL 加载管道组件并返回工厂函数。然后，您可以调用工厂函数来构造运行组件容器映像的管道任务 ( `ContainerOp` ) 的实例。

- [`kfp.dsl`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html) contains the domain-specific language (DSL) that you can use to define and interact with pipelines and components. Methods, classes, and modules in this package include, but are not limited to, the following:
  `kfp.dsl` 包含可用于定义管道和组件并与之交互的特定于域的语言 (DSL)。此包中的方法、类和模块包括但不限于以下内容：

  - `kfp.dsl.PipelineParam` represents a pipeline parameter that you can pass from one pipeline component to another. See the guide to [pipeline parameters](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/parameters/).
    `kfp.dsl.PipelineParam` 表示可以从一个管道组件传递到另一个管道组件的管道参数。请参阅管道参数指南。

  - `kfp.dsl.component` is a decorator for DSL functions that returns a pipeline component. ([`ContainerOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ContainerOp)).
    `kfp.dsl.component` 是返回管道组件的 DSL 函数的装饰器。 （ `ContainerOp` ）。

  - `kfp.dsl.pipeline` is a decorator for Python functions that returns a pipeline.
    `kfp.dsl.pipeline` 是返回管道的 Python 函数的装饰器。

  - `kfp.dsl.python_component` is a decorator for Python functions that adds pipeline component metadata to the function object.
    `kfp.dsl.python_component` 是 Python 函数的装饰器，它将管道组件元数据添加到函数对象。

  - [`kfp.dsl.types`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.types.html) contains a list of types defined by the Kubeflow Pipelines SDK. Types include basic types like `String`, `Integer`, `Float`, and `Bool`, as well as domain-specific types like `GCPProjectID` and `GCRPath`. See the guide to [DSL static type checking](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/static-type-checking/).
    `kfp.dsl.types` 包含 Kubeflow Pipelines SDK 定义的类型列表。类型包括 `String` 、 `Integer` 、 `Float` 和 `Bool` 等基本类型，以及 `GCPProjectID` 。请参阅 DSL 静态类型检查指南。

  - [`kfp.dsl.ResourceOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ResourceOp) represents a pipeline task (op) which lets you directly manipulate Kubernetes resources (`create`, `get`, `apply`, …).
    `kfp.dsl.ResourceOp` 表示管道任务 (op)，可让您直接操作 Kubernetes 资源（ `create` 、 `get` 、 `apply` 等）。

  - [`kfp.dsl.VolumeOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.VolumeOp) represents a pipeline task (op) which creates a new `PersistentVolumeClaim` (PVC). It aims to make the common case of creating a `PersistentVolumeClaim` fast.
    `kfp.dsl.VolumeOp` 表示创建新 `PersistentVolumeClaim` (PVC) 的管道任务 (op)。它的目的是使创建 `PersistentVolumeClaim` 的常见情况变得更快。

  - [`kfp.dsl.VolumeSnapshotOp`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.VolumeSnapshotOp) represents a pipeline task (op) which creates a new `VolumeSnapshot`. It aims to make the common case of creating a `VolumeSnapshot` fast.
    `kfp.dsl.VolumeSnapshotOp` 表示创建新 `VolumeSnapshot` 的管道任务 (op)。它的目的是使创建 `VolumeSnapshot` 的常见情况变得更快。

  - [`kfp.dsl.PipelineVolume`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.PipelineVolume) represents a volume used to pass data between pipeline steps. `ContainerOp`s can mount a `PipelineVolume` either via the constructor’s argument `pvolumes` or `add_pvolumes()` method.
    `kfp.dsl.PipelineVolume` 表示用于在管道步骤之间传递数据的卷。 `ContainerOp` 可以通过构造函数的参数 `pvolumes` 或 `add_pvolumes()` 方法挂载 `PipelineVolume` 。

  - [`kfp.dsl.ParallelFor`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ParallelFor) represents a parallel for loop over a static or dynamic set of items in a pipeline. Each iteration of the for loop is executed in parallel.
    `kfp.dsl.ParallelFor` 表示管道中静态或动态项目集的并行 for 循环。 for 循环的每次迭代都是并行执行的。

  - [`kfp.dsl.ExitHandler`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.ExitHandler) represents an exit handler that is invoked upon exiting a pipeline. A typical usage of `ExitHandler` is garbage collection.
    `kfp.dsl.ExitHandler` 表示退出管道时调用的退出处理程序。 `ExitHandler` 的典型用法是垃圾回收。

  - [`kfp.dsl.Condition`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/dsl.html#kfp.dsl.Condition) represents a group of ops, that will only be executed when a certain condition is met. The condition specified need to be determined at runtime, by incorporating at least one task output, or PipelineParam in the boolean expression.
    `kfp.dsl.Condition` 代表一组操作，只有在满足特定条件时才会执行。指定的条件需要在运行时确定，方法是在布尔表达式中合并至少一个任务输出或 PipelineParam。

- [`kfp.Client`](https://kubeflow-pipelines.readthedocs.io/en/stable/source/client.html) contains the Python client libraries for the [Kubeflow Pipelines API](https://v1-9-branch.kubeflow.org/docs/components/pipelines/reference/api/kubeflow-pipeline-api-spec/). Methods in this package include, but are not limited to, the following:
  `kfp.Client` 包含 Kubeflow Pipelines API 的 Python 客户端库。该包中的方法包括但不限于以下内容：

  - `kfp.Client.create_experiment` creates a pipeline [experiment](https://v1-9-branch.kubeflow.org/docs/components/pipelines/concepts/experiment/) and returns an experiment object.
    `kfp.Client.create_experiment` 创建管道实验并返回实验对象。

  - `kfp.Client.run_pipeline` runs a pipeline and returns a run object.
    `kfp.Client.run_pipeline` 运行管道并返回运行对象。

  - `kfp.Client.create_run_from_pipeline_func` compiles a pipeline function and submits it for execution on Kubeflow Pipelines.
    `kfp.Client.create_run_from_pipeline_func` 编译管道函数并将其提交到 Kubeflow Pipelines 上执行。

  - `kfp.Client.create_run_from_pipeline_package` runs a local pipeline package on Kubeflow Pipelines.
    `kfp.Client.create_run_from_pipeline_package` 在 Kubeflow Pipelines 上运行本地管道包。

  - `kfp.Client.upload_pipeline` uploads a local file to create a new pipeline in Kubeflow Pipelines.
    `kfp.Client.upload_pipeline` 上传本地文件以在 Kubeflow Pipelines 中创建新管道。

  - `kfp.Client.upload_pipeline_version` uploads a local file to create a pipeline version. [Follow an example to learn more about creating a pipeline version](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/tutorials/sdk-examples/).
    `kfp.Client.upload_pipeline_version` 上传本地文件以创建管道版本。按照示例了解有关创建管道版本的更多信息。

- [Kubeflow Pipelines extension modules](https://kubeflow-pipelines.readthedocs.io/en/stable/source/kfp.extensions.html) include classes and functions for specific platforms on which you can use Kubeflow Pipelines. Examples include utility functions for on premises, Google Cloud Platform (GCP), Amazon Web Services (AWS), and Microsoft Azure.
  Kubeflow Pipelines 扩展模块包括适用于您可以使用 Kubeflow Pipelines 的特定平台的类和函数。示例包括本地、Google Cloud Platform (GCP)、Amazon Web Services (AWS) 和 Microsoft Azure 的实用程序函数。

- [Kubeflow Pipelines diagnose_me modules](https://github.com/kubeflow/pipelines/tree/sdk/release-1.8/sdk/python/kfp/cli/diagnose_me) include classes and functions that help with environment diagnostic tasks.
  Kubeflow Pipelinesdiagnose_me 模块包含有助于完成环境诊断任务的类和函数。

  - `kfp.cli.diagnose_me.dev_env` reports on diagnostic metadata from your development environment, such as your python library version.
    `kfp.cli.diagnose_me.dev_env` 报告来自您的开发环境的诊断元数据，例如您的 python 库版本。

  - `kfp.cli.diagnose_me.kubernetes_cluster` reports on diagnostic data from your Kubernetes cluster, such as Kubernetes secrets.
    `kfp.cli.diagnose_me.kubernetes_cluster` 报告来自 Kubernetes 集群的诊断数据，例如 Kubernetes 密钥。

  - `kfp.cli.diagnose_me.gcp` reports on diagnostic data related to your GCP environment.
    `kfp.cli.diagnose_me.gcp` 报告与您的 GCP 环境相关的诊断数据。

## Kubeflow Pipelines CLI tool
Kubeflow Pipelines CLI 工具

The Kubeflow Pipelines CLI tool enables you to use a subset of the Kubeflow Pipelines SDK directly from the command line. The Kubeflow Pipelines CLI tool provides the following commands:
Kubeflow Pipelines CLI 工具使您能够直接从命令行使用 Kubeflow Pipelines SDK 的子集。 Kubeflow Pipelines CLI 工具提供以下命令：

- `kfp diagnose_me` runs environment diagnostic with specified parameters.
  `kfp diagnose_me` 使用指定参数运行环境诊断。

  - `--json` - Indicates that this command must return its results as JSON. Otherwise, results are returned in human readable format.
    `--json` - 指示此命令必须以 JSON 形式返回其结果。否则，结果将以人类可读的格式返回。

  - `--namespace TEXT` - Specifies the Kubernetes namespace to use. all-namespaces is the default value.
    `--namespace TEXT` - 指定要使用的 Kubernetes 命名空间。 all-namespaces 是默认值。

  - `--project-id TEXT` - For GCP deployments, this value specifies the GCP project to use. If this value is not specified, the environment default is used.
    `--project-id TEXT` - 对于 GCP 部署，此值指定要使用的 GCP 项目。如果未指定该值，则使用环境默认值。

- `kfp pipeline <COMMAND>` provides the following commands to help you manage pipelines.
  `kfp pipeline <COMMAND>` 提供以下命令来帮助您管理管道。

  - `get` - Gets detailed information about a Kubeflow pipeline from your Kubeflow Pipelines cluster.
    `get` - 从 Kubeflow Pipelines 集群获取有关 Kubeflow pipeline 的详细信息。

  - `list` - Lists the pipelines that have been uploaded to your Kubeflow Pipelines cluster.
    `list` - 列出已上传到 Kubeflow Pipelines 集群的管道。

  - `upload` - Uploads a pipeline to your Kubeflow Pipelines cluster.
    `upload` - 将管道上传到 Kubeflow Pipelines 集群。

- `kfp run <COMMAND>` provides the following commands to help you manage pipeline runs.
  `kfp run <COMMAND>` 提供以下命令来帮助您管理管道运行。

  - `get` - Displays the details of a pipeline run.
    `get` - 显示管道运行的详细信息。

  - `list` - Lists recent pipeline runs.
    `list` - 列出最近的管道运行。

  - `submit` - Submits a pipeline run.
    `submit` - 提交管道运行。

- `kfp --endpoint <ENDPOINT>` - Specifies the endpoint that the Kubeflow Pipelines CLI should connect to.
  `kfp --endpoint <ENDPOINT>` - 指定 Kubeflow Pipelines CLI 应连接到的端点。

## Installing the SDK
安装SDK

Follow the guide to [installing the Kubeflow Pipelines SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/install-sdk/).
按照指南安装 Kubeflow Pipelines SDK。

## Building pipelines and components
构建管道和组件

This section summarizes the ways you can use the SDK to build pipelines and components.
本节总结了使用 SDK 构建管道和组件的方法。

A Kubeflow *pipeline* is a portable and scalable definition of an ML workflow. Each step in your ML workflow, such as preparing data or training a model, is an instance of a pipeline component.
Kubeflow 管道是 ML 工作流程的可移植且可扩展的定义。 ML 工作流程中的每个步骤（例如准备数据或训练模型）都是管道组件的实例。

[Learn more about building pipelines](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/build-pipeline/).
了解有关构建管道的更多信息。

A pipeline *component* is a self-contained set of code that performs one step in your ML workflow. Components are defined in a component specification, which defines the following:
管道组件是一组独立的代码，用于执行 ML 工作流程中的一个步骤。组件在组件规范中定义，该规范定义了以下内容：

- The component’s interface, its inputs and outputs.
  组件的接口、输入和输出。

- The component’s implementation, the container image and the command to execute.
  组件的实现、容器镜像和要执行的命令。

- The component’s metadata, such as the name and description of the component.
  组件的元数据，例如组件的名称和描述。

Use the following options to create or reuse pipeline components.
使用以下选项创建或重用管道组件。

- You can build components by defining a component specification for a containerized application.
  您可以通过为容器化应用程序定义组件规范来构建组件。

  [Learn more about building pipeline components](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/component-development/).
  了解有关构建管道组件的更多信息。

- Lightweight Python function-based components make it easier to build a component by using the Kubeflow Pipelines SDK to generate the component specification for a Python function.
  基于轻量级 Python 函数的组件可以通过使用 Kubeflow Pipelines SDK 生成 Python 函数的组件规范来更轻松地构建组件。

  [Learn how to build a Python function-based component](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/python-function-components/).
  了解如何构建基于 Python 函数的组件。

- You can reuse prebuilt components in your pipeline.
  您可以在管道中重复使用预构建的组件。

  [Learn more about reusing prebuilt components](https://v1-9-branch.kubeflow.org/docs/examples/shared-resources/).
  了解有关重用预构建组件的更多信息。
