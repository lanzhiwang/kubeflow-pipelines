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

./kustomize build manifests/kustomize/cluster-scoped-resources > learn/install_01.yaml 2>&1

./kustomize build manifests/kustomize/env/platform-agnostic-multi-user > learn/install_02.yaml 2>&1

```
