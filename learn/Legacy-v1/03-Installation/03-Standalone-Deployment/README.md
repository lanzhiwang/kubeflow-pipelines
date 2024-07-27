# Standalone Deployment
独立部署

* https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/

Information about Standalone Deployment of Kubeflow Pipelines
有关 Kubeflow Pipelines 独立部署的信息

#### Old Version
旧版

This page is about **Kubeflow Pipelines V1**, please see the [V2 documentation](https://v1-9-branch.kubeflow.org/docs/components/pipelines/) for the latest information.
本页面是关于 Kubeflow Pipelines V1 的，请参阅 V2 文档以获取最新信息。

Note, while the V2 backend is able to run pipelines submitted by the V1 SDK, we strongly recommend [migrating to the V2 SDK](https://v1-9-branch.kubeflow.org/docs/components/pipelines/user-guides/migration/). For reference, the final release of the V1 SDK was [`kfp==1.8.22`](https://pypi.org/project/kfp/1.8.22/), and its reference documentation is [available here](https://kubeflow-pipelines.readthedocs.io/en/1.8.22/).
请注意，虽然 V2 后端能够运行 V1 SDK 提交的管道，但我们强烈建议迁移到 V2 SDK。作为参考，V1 SDK 的最终版本是 `kfp==1.8.22` ，其参考文档可在此处获取。

As an alternative to deploying Kubeflow Pipelines (KFP) as part of the [Kubeflow deployment](https://v1-9-branch.kubeflow.org/docs/started/#installing-kubeflow), you also have a choice to deploy only Kubeflow Pipelines. Follow the instructions below to deploy Kubeflow Pipelines standalone using the supplied kustomize manifests.
作为将 Kubeflow Pipelines (KFP) 作为 Kubeflow 部署的一部分进行部署的替代方案，您还可以选择仅部署 Kubeflow Pipelines。按照以下说明使用提供的 kustomize 清单独立部署 Kubeflow Pipelines。

You should be familiar with [Kubernetes](https://kubernetes.io/docs/home/), [kubectl](https://kubernetes.io/docs/reference/kubectl/overview/), and [kustomize](https://kustomize.io/).
您应该熟悉 Kubernetes、kubectl 和 kustomize。

#### Installation options for Kubeflow Pipelines standalone
Kubeflow Pipelines 独立安装选项

This guide currently describes how to install Kubeflow Pipelines standalone on Google Cloud Platform (GCP). You can also install Kubeflow Pipelines standalone on other platforms. This guide needs updating. See [Issue 1253](https://github.com/kubeflow/website/issues/1253).
本指南当前介绍如何在 Google Cloud Platform (GCP) 上独立安装 Kubeflow Pipelines。您还可以在其他平台上独立安装 Kubeflow Pipelines。本指南需要更新。请参阅问题 1253。

## Before you get started
开始之前

Working with Kubeflow Pipelines Standalone requires a Kubernetes cluster as well as an installation of kubectl.
使用独立的 Kubeflow Pipelines 需要 Kubernetes 集群以及 kubectl 的安装。

### Download and install kubectl
下载并安装 kubectl

Download and install kubectl by following the [kubectl installation guide](https://kubernetes.io/docs/tasks/tools/install-kubectl/).
按照 kubectl 安装指南下载并安装 kubectl。

You need kubectl version 1.14 or higher for native support of kustomize.
您需要 kubectl 版本 1.14 或更高版本才能获得 kustomize 的本机支持。

### Set up your cluster
设置您的集群

If you have an existing Kubernetes cluster, continue with the instructions for [configuring kubectl to talk to your cluster](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#configure-kubectl).
如果您有现有的 Kubernetes 集群，请继续按照说明配置 kubectl 以与您的集群通信。

See the GKE guide to [creating a cluster](https://cloud.google.com/kubernetes-engine/docs/how-to/creating-a-cluster) for Google Cloud Platform (GCP).
请参阅 GKE 指南，了解如何为 Google Cloud Platform (GCP) 创建集群。

Use the [gcloud container clusters create command](https://cloud.google.com/sdk/gcloud/reference/container/clusters/create) to create a cluster that can run all Kubeflow Pipelines samples:
使用 gcloud 容器集群创建命令创建可以运行所有 Kubeflow Pipelines 示例的集群：

```bash
# The following parameters can be customized based on your needs.

CLUSTER_NAME="kubeflow-pipelines-standalone"

ZONE="us-central1-a"

MACHINE_TYPE="e2-standard-2" # A machine with 2 CPUs and 8GB memory.

SCOPES="cloud-platform" # This scope is needed for running some pipeline samples. Read the warning below for its security implication

gcloud container clusters create $CLUSTER_NAME \
--zone $ZONE \
--machine-type $MACHINE_TYPE \
--scopes $SCOPES
```

**Note**: `e2-standard-2` doesn’t support GPU. You can choose machine types that meet your need by referring to guidance in [Cloud Machine families](http://cloud/compute/docs/machine-types).
注意： `e2-standard-2` 不支持GPU。您可以参考云机器系列中的指导，选择符合您需求的机器类型。

**Warning**: Using `SCOPES="cloud-platform"` grants all GCP permissions to the cluster. For a more secure cluster setup, refer to [Authenticating Pipelines to GCP](https://v1-9-branch.kubeflow.org/docs/gke/authentication/#authentication-from-kubeflow-pipelines).
警告：使用 `SCOPES="cloud-platform"` 向集群授予所有 GCP 权限。如需更安全的集群设置，请参阅对 GCP 管道进行身份验证。

Note, some legacy pipeline examples may need minor code change to run on clusters with `SCOPES="cloud-platform"`, refer to [Authoring Pipelines to use default service account](https://v1-9-branch.kubeflow.org/docs/gke/pipelines/authentication-pipelines/#authoring-pipelines-to-use-default-service-account).
请注意，某些旧管道示例可能需要进行少量代码更改才能在具有 `SCOPES="cloud-platform"` 的集群上运行，请参阅创作管道以使用默认服务帐户。

**References**:
参考

- [GCP regions and zones documentation](https://cloud.google.com/compute/docs/regions-zones/#available)
  GCP 区域和专区文档

- [gcloud command-line tool guide](https://cloud.google.com/sdk/gcloud/)
  gcloud 命令行工具指南

- [gcloud command reference](https://cloud.google.com/sdk/gcloud/reference/container/clusters/create)
  gcloud 命令参考

### Configure kubectl to talk to your cluster
配置 kubectl 与您的集群通信

See the Google Kubernetes Engine (GKE) guide to [configuring cluster access for kubectl](https://cloud.google.com/kubernetes-engine/docs/how-to/cluster-access-for-kubectl).
请参阅 Google Kubernetes Engine (GKE) 指南来配置 kubectl 的集群访问。

## Deploying Kubeflow Pipelines
部署 Kubeflow 管道

1. Deploy the Kubeflow Pipelines:
   部署 Kubeflow 管道：

  ```bash
  export PIPELINE_VERSION=2.2.0
  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
  kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
  ```

  The Kubeflow Pipelines deployment requires approximately 3 minutes to complete.
  Kubeflow Pipelines 部署大约需要 3 分钟才能完成。

  **Note**: The above commands apply to Kubeflow Pipelines version 0.4.0 and higher.
  注意：以上命令适用于 Kubeflow Pipelines 0.4.0 及更高版本。

  For Kubeflow Pipelines version 0.2.0 ~ 0.3.0, use:
  对于 Kubeflow Pipelines 版本 0.2.0 ~ 0.3.0，使用：

  ```bash
  export PIPELINE_VERSION=<kfp-version-between-0.2.0-and-0.3.0>
  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/base/crds?ref=$PIPELINE_VERSION"
  kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
  ```

  For Kubeflow Pipelines version < 0.2.0, use:
  对于 Kubeflow Pipelines 版本 < 0.2.0，请使用：

  ```bash
  export PIPELINE_VERSION=<kfp-version-0.1.x>
  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
  ```

  **Note**: `kubectl apply -k` accepts local paths and paths that are formatted as [hashicorp/go-getter URLs](https://github.com/kubernetes-sigs/kustomize/blob/master/examples/remoteBuild.md#url-format). While the paths in the preceding commands look like URLs, the paths are not valid URLs.
  注意： `kubectl apply -k` 接受本地路径和格式为 hashicorp/go-getter URL 的路径。虽然前面命令中的路径看起来像 URL，但这些路径不是有效的 URL。

  #### Deprecation Notice 弃用通知

  Kubeflow Pipelines will change default executor from Docker to Emissary starting KFP backend v1.8, docker executor has been deprecated on Kubernetes 1.20+.
  从 KFP 后端 v1.8 开始，Kubeflow Pipelines 会将默认执行器从 Docker 更改为 Emissary，docker 执行器已在 Kubernetes 1.20+ 上弃用。

  For Kubeflow Pipelines before v1.8, configure to use Emissary executor by referring to [Argo Workflow Executors](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/choose-executor/).
  对于 v1.8 之前的 Kubeflow Pipelines，请参考 Argo Workflow Executors 配置使用 Emissary 执行器。

1. Get the public URL for the Kubeflow Pipelines UI and use it to access the Kubeflow Pipelines UI:
   获取 Kubeflow Pipelines UI 的公共 URL 并使用它来访问 Kubeflow Pipelines UI：

  ```bash
  kubectl describe configmap inverse-proxy-config -n kubeflow | grep googleusercontent.com
  ```

## Upgrading Kubeflow Pipelines
升级 Kubeflow 管道

1. For release notices and breaking changes, refer to [Upgrading Kubeflow Pipelines](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/upgrade/).
   有关发布通知和重大更改，请参阅升级 Kubeflow Pipelines。

1. Check the [Kubeflow Pipelines GitHub repository](https://github.com/kubeflow/pipelines/releases) for available releases.
   检查 Kubeflow Pipelines GitHub 存储库以获取可用版本。

2. To upgrade to Kubeflow Pipelines 0.4.0 and higher, use the following commands:
   要升级到 Kubeflow Pipelines 0.4.0 及更高版本，请使用以下命令：

  ```bash
  export PIPELINE_VERSION=<version-you-want-to-upgrade-to>
  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
  kubectl wait --for condition=established --timeout=60s crd/applications.app.k8s.io
  kubectl apply -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
  ```

  To upgrade to Kubeflow Pipelines 0.3.0 and lower, use the [deployment instructions](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#deploying-kubeflow-pipelines) to upgrade your Kubeflow Pipelines cluster.
  要升级到 Kubeflow Pipelines 0.3.0 及更低版本，请使用部署说明升级 Kubeflow Pipelines 集群。

4. Delete obsolete resources manually.
  手动删除过时的资源。

  Depending on the version you are upgrading from and the version you are upgrading to, some Kubeflow Pipelines resources may have become obsolete.
  根据您要升级的版本以及要升级到的版本，某些 Kubeflow Pipelines 资源可能已过时。

  If you are upgrading from Kubeflow Pipelines < 0.4.0 to 0.4.0 or above, you can remove the following obsolete resources after the upgrade: `metadata-deployment`, `metadata-service`.
  如果您要从 Kubeflow Pipelines < 0.4.0 升级到 0.4.0 或更高版本，则可以在升级后删除以下过时的资源： `metadata-deployment` 、 `metadata-service` 。

  Run the following command to check if these resources exist on your cluster:
  运行以下命令检查集群上是否存在这些资源：

  ```bash
  kubectl -n <KFP_NAMESPACE> get deployments | grep metadata-deployment
  kubectl -n <KFP_NAMESPACE> get service | grep metadata-service
  ```

  If these resources exist on your cluster, run the following commands to delete them:
  如果您的集群上存在这些资源，请运行以下命令删除它们：

  ```bash
  kubectl -n <KFP_NAMESPACE> delete deployment metadata-deployment
  kubectl -n <KFP_NAMESPACE> delete service metadata-service
  ```

  For other versions, you don’t need to do anything.
  对于其他版本，您不需要执行任何操作。

## Customizing Kubeflow Pipelines
自定义 Kubeflow 管道

Kubeflow Pipelines can be configured through kustomize [overlays](https://kubectl.docs.kubernetes.io/references/kustomize/glossary/#overlay).
Kubeflow Pipelines 可以通过 kustomize 覆盖进行配置。

To begin, first clone the [Kubeflow Pipelines GitHub repository](https://github.com/kubeflow/pipelines), and use it as your working directory.
首先，克隆 Kubeflow Pipelines GitHub 存储库，并将其用作您的工作目录。

### Deploy on GCP with Cloud SQL and Google Cloud Storage

使用 Cloud SQL 和 Google Cloud Storage 在 GCP 上部署[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#deploy-on-gcp-with-cloud-sql-and-google-cloud-storage)

**Note**: This is recommended for production environments. For more details about customizing your environment for GCP, see the [Kubeflow Pipelines GCP manifests](https://github.com/kubeflow/pipelines/tree/sdk/release-1.8/manifests/kustomize/env/gcp).  
注意：建议在生产环境中使用此方法。有关为 GCP 自定义环境的更多详细信息，请参阅 Kubeflow Pipelines GCP 清单。

### Change deployment namespace

更改部署命名空间[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#change-deployment-namespace)

To deploy Kubeflow Pipelines standalone in namespace `<my-namespace>`:  
要在命名空间 `<my-namespace>` 中独立部署 Kubeflow Pipelines：

1. Set the `namespace` field to `<my-namespace>` in [dev/kustomization.yaml](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/manifests/kustomize/env/dev/kustomization.yaml) or [gcp/kustomization.yaml](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/manifests/kustomize/env/gcp/kustomization.yaml).  
  在 dev/kustomization.yaml 或 gcp/kustomization.yaml 中将 `namespace` 字段设置为 `<my-namespace>` 。
  
2. Set the `namespace` field to `<my-namespace>` in [cluster-scoped-resources/kustomization.yaml](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/manifests/kustomize/cluster-scoped-resources/kustomization.yaml)  
  在 cluster-scoped-resources/kustomization.yaml 中将 `namespace` 字段设置为 `<my-namespace>`
  
3. Apply the changes to update the Kubeflow Pipelines deployment:  
  应用更改以更新 Kubeflow Pipelines 部署：
  
  ```fallback
  kubectl apply -k manifests/kustomize/cluster-scoped-resources
  kubectl apply -k manifests/kustomize/env/dev
  ```
  
  **Note**: If using GCP Cloud SQL and Google Cloud Storage, set the proper values in [manifests/kustomize/env/gcp/params.env](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/manifests/kustomize/env/gcp/params.env), then apply with this command:  
  注意：如果使用 GCP Cloud SQL 和 Google Cloud Storage，请在 manifests/kustomize/env/gcp/params.env 中设置正确的值，然后使用以下命令应用：
  
  ```fallback
  kubectl apply -k manifests/kustomize/cluster-scoped-resources
  kubectl apply -k manifests/kustomize/env/gcp
  ```
  

### Disable the public endpoint

禁用公共端点[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#disable-the-public-endpoint)

By default, the KFP standalone deployment installs an [inverting proxy agent](https://github.com/google/inverting-proxy) that exposes a public URL. If you want to skip the installation of the inverting proxy agent, complete the following:  
默认情况下，KFP 独立部署会安装公开公共 URL 的反向代理。如果您想跳过反向代理的安装，请完成以下操作：

1. Comment out the proxy components in the base `kustomization.yaml`. For example in [manifests/kustomize/env/dev/kustomization.yaml](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/manifests/kustomize/env/dev/kustomization.yaml) comment out `inverse-proxy`.  
  注释掉基础 `kustomization.yaml` 中的代理组件。例如，在manifests/kustomize/env/dev/kustomization.yaml中注释掉 `inverse-proxy` 。
  
2. Apply the changes to update the Kubeflow Pipelines deployment:  
  应用更改以更新 Kubeflow Pipelines 部署：
  
  ```fallback
  kubectl apply -k manifests/kustomize/env/dev
  ```
  
  **Note**: If using GCP Cloud SQL and Google Cloud Storage, set the proper values in [manifests/kustomize/env/gcp/params.env](https://github.com/kubeflow/pipelines/blob/sdk/release-1.8/manifests/kustomize/env/gcp/params.env), then apply with this command:  
  注意：如果使用 GCP Cloud SQL 和 Google Cloud Storage，请在 manifests/kustomize/env/gcp/params.env 中设置正确的值，然后使用以下命令应用：
  
  ```fallback
  kubectl apply -k manifests/kustomize/env/gcp
  ```
  
3. Verify that the Kubeflow Pipelines UI is accessible by port-forwarding:  
  验证 Kubeflow Pipelines UI 是否可通过端口转发访问：
  
  ```fallback
  kubectl port-forward -n kubeflow svc/ml-pipeline-ui 8080:80
  ```
  
4. Open the Kubeflow Pipelines UI at `http://localhost:8080/`.  
  在 `http://localhost:8080/` 打开 Kubeflow Pipelines UI。
  

## Uninstalling Kubeflow Pipelines

卸载 Kubeflow 管道[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#uninstalling-kubeflow-pipelines)

To uninstall Kubeflow Pipelines, run `kubectl delete -k <manifest-file>`.  
要卸载 Kubeflow Pipelines，请运行 `kubectl delete -k <manifest-file>` 。

For example, to uninstall KFP using manifests from a GitHub repository, run:  
例如，要使用 GitHub 存储库中的清单卸载 KFP，请运行：

```gdscript3
export PIPELINE_VERSION=2.2.0
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=$PIPELINE_VERSION"
kubectl delete -k "github.com/kubeflow/pipelines/manifests/kustomize/cluster-scoped-resources?ref=$PIPELINE_VERSION"
```

To uninstall KFP using manifests from your local repository or file system, run:  
要使用本地存储库或文件系统中的清单卸载 KFP，请运行：

```fallback
kubectl delete -k manifests/kustomize/env/dev
kubectl delete -k manifests/kustomize/cluster-scoped-resources
```

**Note**: If you are using GCP Cloud SQL and Google Cloud Storage, run:  
注意：如果您使用的是 GCP Cloud SQL 和 Google Cloud Storage，请运行：

```fallback
kubectl delete -k manifests/kustomize/env/gcp
kubectl delete -k manifests/kustomize/cluster-scoped-resources
```

## Best practices for maintaining manifests

维护清单的最佳实践[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#best-practices-for-maintaining-manifests)

Similar to source code, configuration files belong in source control. A repository manages the changes to your manifest files and ensures that you can repeatedly deploy, upgrade, and uninstall your components.  
与源代码类似，配置文件属于源代码管理。存储库管理对清单文件的更改，并确保您可以重复部署、升级和卸载组件。

### Maintain your manifests in source control

在源代码管理中维护您的清单[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#maintain-your-manifests-in-source-control)

After creating or customizing your deployment manifests, save your manifests to a local or remote source control repository. For example, save the following `kustomization.yaml`:  
创建或自定义部署清单后，将清单保存到本地或远程源代码控制存储库。例如，保存以下 `kustomization.yaml` ：

```fallback
# kustomization.yaml
apiVersion: kustomize.config.k8s.io/v1beta1
kind: Kustomization
# Edit the following to change the deployment to your custom namespace.
namespace: kubeflow
# You can add other customizations here using kustomize.
# Edit ref in the following link to deploy a different version of Kubeflow Pipelines.
bases:
- github.com/kubeflow/pipelines/manifests/kustomize/env/dev?ref=2.2.0
```

### Further reading 进一步阅读[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#further-reading)

- To learn about kustomize workflows with off-the-shelf configurations, see the [kustomize configuration workflows guide](https://github.com/kubernetes-sigs/kustomize/blob/master/docs/workflows.md#off-the-shelf-configuration).  
  要了解具有现成配置的 kustomize 工作流程，请参阅 kustomize 配置工作流程指南。

## Troubleshooting 故障排除[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#troubleshooting)

- If your pipelines are stuck in ContainerCreating state and it has pod events like  
  如果您的管道陷入 ContainerCreating 状态并且它有 pod 事件，例如

```fallback
MountVolume.SetUp failed for volume "gcp-credentials-user-gcp-sa" : secret "user-gcp-sa" not found
```

You should remove `use_gcp_secret` usages as documented in [Authenticating Pipelines to GCP](https://v1-9-branch.kubeflow.org/docs/distributions/gke/pipelines/authentication-pipelines/#authoring-pipelines-to-use-workload-identity).  
您应该删除 `use_gcp_secret` 用法，如验证 GCP 管道中所述。

## What’s next 下一步是什么[](https://v1-9-branch.kubeflow.org/docs/components/pipelines/legacy-v1/installation/standalone-deployment/#whats-next)

- [Connecting to Kubeflow Pipelines standalone on Google Cloud using the SDK 
  使用 SDK 连接到 Google Cloud 上独立的 Kubeflow Pipelines](https://v1-9-branch.kubeflow.org/docs/distributions/gke/pipelines/authentication-sdk/#connecting-to-kubeflow-pipelines-standalone-or-ai-platform-pipelines)
- [Authenticating Pipelines to GCP](https://v1-9-branch.kubeflow.org/docs/distributions/gke/pipelines/authentication-pipelines/#authoring-pipelines-to-use-workload-identity) if you want to use GCP services in Kubeflow Pipelines.  
  如果您想在 Kubeflow Pipelines 中使用 GCP 服务，请向 GCP 验证 Pipelines。