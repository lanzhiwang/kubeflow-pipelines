# Kubeflow Pipelines SDK API

- kfp package

  - kfp.Client class
    - Generated APIs

  - kfp.compiler package

  - kfp.components package
    - kfp.components.structures subpackage

  - kfp.containers package

  - kfp.dsl package
    - kfp.dsl.types module

  - KFP extension modules
    - kfp.onprem module
    - kfp.gcp module
    - kfp.aws module
    - kfp.azure module

```bash
docker run -ti --rm \
-v ~/work/code/go_code/ai/kubeflow/pipelines:/pipelines \
-w /pipelines \
docker-mirrors.alauda.cn/library/python:3.10.12-bullseye \
bash

pip install -i https://pypi.tuna.tsinghua.edu.cn/simple yapf

find ./learn/ -name "*.py" -exec yapf -i {} \;

python -m venv .env

source .env/bin/activate

(.env) @lanzhiwang ➜ /workspaces/kubeflow-pipelines (learn-1.8.22) $ python
Python 3.10.13 (main, Jul 11 2024, 16:23:02) [GCC 9.4.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
>>>

```
