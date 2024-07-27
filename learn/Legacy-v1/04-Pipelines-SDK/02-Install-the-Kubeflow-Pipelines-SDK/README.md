# Install the Kubeflow Pipelines SDK
安装 Kubeflow Pipelines SDK

* https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/install-sdk/

Setting up your Kubeflow Pipelines development environment
设置 Kubeflow Pipelines 开发环境

#### Old Version
旧版

This page is about **Kubeflow Pipelines V1**, please see the [V2 documentation](https://v1-9-branch.kubeflow.org/docs/components/pipelines/) for the latest information.
本页面是关于 Kubeflow Pipelines V1 的，请参阅 V2 文档以获取最新信息。

Note, while the V2 backend is able to run pipelines submitted by the V1 SDK, we strongly recommend [migrating to the V2 SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/user-guides/migration/). For reference, the final release of the V1 SDK was [`kfp==1.8.22`](https://pypi.org/project/kfp/1.8.22/), and its reference documentation is [available here](https://kubeflow-pipelines.readthedocs.io/en/1.8.22/).
请注意，虽然 V2 后端能够运行 V1 SDK 提交的管道，但我们强烈建议迁移到 V2 SDK。作为参考，V1 SDK 的最终版本是 `kfp==1.8.22` ，其参考文档可在此处获取。

This guide tells you how to install the [Kubeflow Pipelines SDK](https://github.com/kubeflow/pipelines/tree/sdk/release-1.8/sdk) which you can use to build machine learning pipelines. You can use the SDK to execute your pipeline, or alternatively you can upload the pipeline to the Kubeflow Pipelines UI for execution.
本指南告诉您如何安装 Kubeflow Pipelines SDK，您可以使用它来构建机器学习管道。您可以使用 SDK 来执行管道，也可以将管道上传到 Kubeflow Pipelines UI 来执行。

All of the SDK’s classes and methods are described in the auto-generated [SDK reference docs](https://kubeflow-pipelines.readthedocs.io/en/stable/).
自动生成的 SDK 参考文档中描述了 SDK 的所有类和方法。

**Note:** If you are running [Kubeflow Pipelines with Tekton](https://github.com/kubeflow/kfp-tekton), instead of the default [Kubeflow Pipelines with Argo](https://github.com/kubeflow/pipelines), you should use the [Kubeflow Pipelines SDK for Tekton](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/sdk/pipelines-with-tekton/).
注意：如果您使用 Tekton 运行 Kubeflow Pipelines，而不是使用 Argo 运行默认的 Kubeflow Pipelines，则应使用适用于 Tekton 的 Kubeflow Pipelines SDK。

## Set up Python
设置Python

You need **Python 3.5** or later to use the Kubeflow Pipelines SDK. This guide uses Python 3.7.
您需要 Python 3.5 或更高版本才能使用 Kubeflow Pipelines SDK。本指南使用 Python 3.7。

If you haven’t yet set up a Python 3 environment, do so now. This guide recommends [Miniconda](https://conda.io/miniconda.html), but you can use a virtual environment manager of your choice, such as `virtualenv`.
如果您尚未设置 Python 3 环境，请立即设置。本指南建议使用 Miniconda，但您可以使用您选择的虚拟环境管理器，例如 `virtualenv` 。

Follow the steps below to set up Python using [Miniconda](https://conda.io/miniconda.html):
请按照以下步骤使用 Miniconda 设置 Python：

1. Choose one of the following methods to install Miniconda, depending on your environment:
  根据您的环境，选择以下方法之一来安装 Miniconda：

  - Debian/Ubuntu/[Cloud Shell](https://console.cloud.google.com/cloudshell):
    Debian/Ubuntu/云外壳：

    ```bash
    apt-get update; apt-get install -y wget bzip2
    wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh
    bash Miniconda3-latest-Linux-x86_64.sh
    ```

  - Windows: Download the [installer](https://repo.continuum.io/miniconda/Miniconda3-latest-Windows-x86_64.exe) and make sure you select the option to **Add Miniconda to my PATH environment variable** during the installation.
    Windows：下载安装程序并确保在安装过程中选择“将 Miniconda 添加到我的 PATH 环境变量”选项。

  - MacOS: Download the [installer](https://repo.continuum.io/miniconda/Miniconda3-latest-MacOSX-x86_64.sh) and run the following command:
    MacOS：下载安装程序并运行以下命令：

    ```bash
    bash Miniconda3-latest-MacOSX-x86_64.sh
    ```

2. Check that the `conda` command is available:
  检查 `conda` 命令是否可用：

  ```bash
  which conda
  ```

  If the `conda` command is not found, add Miniconda to your path:
  如果找不到 `conda` 命令，请将 Miniconda 添加到您的路径中：

  ```bash
  export PATH=<YOUR_MINICONDA_PATH>/bin:$PATH
  ```

3. Create a clean Python 3 environment with a name of your choosing. This example uses Python 3.7 and an environment name of `mlpipeline`.:
  使用您选择的名称创建一个干净的 Python 3 环境。此示例使用 Python 3.7 和环境名称 `mlpipeline` ：

  ```bash
  conda create --name mlpipeline python=3.7
  conda activate mlpipeline
  ```

## Install the Kubeflow Pipelines SDK
安装 Kubeflow Pipelines SDK

Run the following command to install the Kubeflow Pipelines SDK:
运行以下命令安装 Kubeflow Pipelines SDK：

```bash
pip install kfp==1.8
```

**Note:** If you are not using a virtual environment, such as `conda`, when installing the Kubeflow Pipelines SDK, you may receive the following error:
注意：如果您没有使用虚拟环境，例如 `conda` ，在安装 Kubeflow Pipelines SDK 时，您可能会收到以下错误：

```bash
ERROR: Could not install packages due to an EnvironmentError: [Errno 13] Permission denied: '/usr/local/lib/python3.5/dist-packages/kfp-<version>.dist-info'
Consider using the `--user` option or check the permissions.
```

If you get this error, install `kfp` with the `--user` option:
如果出现此错误，请使用 `--user` 选项安装 `kfp` ：

```bash
pip install kfp==1.8
```

This command installs the `dsl-compile` and `kfp` binaries under `~/.local/bin`, which is not part of the PATH in some Linux distributions, such as Ubuntu. You can add `~/.local/bin` to your PATH by appending the following to a new line at the end of your `.bashrc` file:
此命令将 `dsl-compile` 和 `kfp` 二进制文件安装在 `~/.local/bin` 下，在某些 Linux 发行版（例如 Ubuntu）中，该二进制文件不是 PATH 的一部分。您可以通过将以下内容附加到 `.bashrc` 文件末尾的新行来将 `~/.local/bin` 添加到您的 PATH：

```bash
export PATH=$PATH:~/.local/bin
```

After successful installation, the command `dsl-compile` should be available. You can use this command to verify it:
成功安装后，命令 `dsl-compile` 应该可用。您可以使用此命令来验证它：

```bash
which dsl-compile
```

The response should be something like this:
响应应该是这样的：

```fallback
/<PATH_TO_YOUR_USER_BIN>/miniconda3/envs/mlpipeline/bin/dsl-compile
```
