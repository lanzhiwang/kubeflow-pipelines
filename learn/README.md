## minikube

```bash
gg /root/minikube-linux-amd64 start \
--image-mirror-country='' \
--image-repository='auto' \
--driver='docker' \
--cpus='16' \
--memory='32g' \
--disk-size='30g' \
--logtostderr \
--iso-url=https://github.com/kubernetes/minikube/releases/download/v1.37.0/minikube-v1.37.0-amd64.iso \
--kubernetes-version='v1.34.0' \
--force=true \
--profile='kubeflow-pipelines'

/root/minikube-linux-amd64 profile list

```

## 部署 StorageClass

[local-path-provisioner](https://github.com/rancher/local-path-provisioner)

```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  annotations:
    kubectl.kubernetes.io/last-applied-configuration: |
      {"apiVersion":"storage.k8s.io/v1","kind":"StorageClass","metadata":{"annotations":{"storageclass.kubernetes.io/is-default-class":"true"},"labels":{"addonmanager.kubernetes.io/mode":"EnsureExists"},"name":"standard"},"provisioner":"k8s.io/minikube-hostpath"}
    storageclass.kubernetes.io/is-default-class: "true"
  creationTimestamp: "2025-09-20T12:02:21Z"
  labels:
    addonmanager.kubernetes.io/mode: EnsureExists
  name: standard
  resourceVersion: "275"
  uid: f8680056-da79-46eb-8b6f-c249f909ba2e
provisioner: k8s.io/minikube-hostpath
reclaimPolicy: Delete
volumeBindingMode: Immediate

```

## Deploying Kubeflow Pipelines

```bash
./kustomize version
v5.4.3

./kustomize build manifests/kustomize/cluster-scoped-resources/ > learn/install_01.yaml 2>&1

./kustomize build manifests/kustomize/env/dev/ > learn/install_02.yaml 2>&1

namespace
  kubeflow

customresourcedefinition.apiextensions.k8s.io
  applications.app.k8s.io
  scheduledworkflows.kubeflow.org
  viewers.kubeflow.org
  clusterworkflowtemplates.argoproj.io
  cronworkflows.argoproj.io
  workflowartifactgctasks.argoproj.io
  workfloweventbindings.argoproj.io
  workflows.argoproj.io
  workflowtaskresults.argoproj.io
  workflowtasksets.argoproj.io
  workflowtemplates.argoproj.io

serviceaccount
  kubeflow-pipelines-cache-deployer-sa

clusterrole.rbac.authorization.k8s.io
  kubeflow-pipelines-cache-deployer-clusterrole

clusterrolebinding.rbac.authorization.k8s.io
  kubeflow-pipelines-cache-deployer-clusterrolebinding

serviceaccount
  application
  argo
  kubeflow-pipelines-cache
  kubeflow-pipelines-container-builder
  kubeflow-pipelines-metadata-writer
  kubeflow-pipelines-viewer
  metadata-grpc-server
  ml-pipeline
  ml-pipeline-persistenceagent
  ml-pipeline-scheduledworkflow
  ml-pipeline-ui
  ml-pipeline-viewer-crd-service-account
  ml-pipeline-visualizationserver
  mysql
  pipeline-runner
  proxy-agent-runner

role.rbac.authorization.k8s.io
  application-manager-role
  argo-role
  kubeflow-pipelines-cache-deployer-role
  kubeflow-pipelines-cache-role
  kubeflow-pipelines-metadata-writer-role
  ml-pipeline
  ml-pipeline-persistenceagent-role
  /ml-pipeline-scheduledworkflow-role
  ml-pipeline-ui
  ml-pipeline-viewer-controller-role
  pipeline-runner
  proxy-agent-runner

rolebinding.rbac.authorization.k8s.io
  application-manager-rolebinding
  argo-binding
  kubeflow-pipelines-cache-binding
  kubeflow-pipelines-cache-deployer-rolebinding
  kubeflow-pipelines-metadata-writer-binding
  ml-pipeline
  ml-pipeline-persistenceagent-binding
  ml-pipeline-scheduledworkflow-binding
  ml-pipeline-ui
  ml-pipeline-viewer-crd-binding
  pipeline-runner-binding
  proxy-agent-runner

configmap
  inverse-proxy-config
  kfp-launcher
  metadata-grpc-configmap
  ml-pipeline-ui-configmap
  pipeline-install-config
  workflow-controller-configmap

secret
  mlpipeline-minio-artifact
  mysql-secret

service
  cache-server
  controller-manager-service
  metadata-envoy-service
  metadata-grpc-service
  minio-service
  ml-pipeline
  ml-pipeline-ui
  ml-pipeline-visualizationserver
  mysql

priorityclass.scheduling.k8s.io
  workflow-controller

persistentvolumeclaim
  minio-pvc
  mysql-pv-claim

deployment.apps
  cache-deployer-deployment
  cache-server
  controller-manager
  metadata-envoy-deployment
  metadata-grpc-deployment
  metadata-writer
  minio
  ml-pipeline
  ml-pipeline-persistenceagent
  ml-pipeline-scheduledworkflow
  ml-pipeline-ui
  ml-pipeline-viewer-crd
  ml-pipeline-visualizationserver
  mysql
  proxy-agent
  workflow-controller

application.app.k8s.io
  pipeline

```
