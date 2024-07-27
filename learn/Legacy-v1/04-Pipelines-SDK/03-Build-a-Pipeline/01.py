import kfp
import kfp.components as comp
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


download_and_merge_csv(
    url=
    'https://storage.googleapis.com/ml-pipeline-playground/iris-csv-files.tar.gz',
    output_csv='merged_data.csv')
"""
$ ls -al data/
total 20
drwxrwxrwx+ 2 codespace codespace 4096 Jul 27 01:58 .
drwxrwxrwx+ 3 codespace root      4096 Jul 27 01:58 ..
-rw-r--r--  1 codespace codespace 1150 Nov 25  2020 iris-1.csv
-rw-r--r--  1 codespace codespace 1350 Nov 25  2020 iris-2.csv
-rw-r--r--  1 codespace codespace 1300 Nov 25  2020 iris-3.csv
$
$ head merged_data.csv
5.1,3.5,1.4,0.2,setosa
4.9,3.0,1.4,0.2,setosa
4.7,3.2,1.3,0.2,setosa
4.6,3.1,1.5,0.2,setosa
5.0,3.6,1.4,0.2,setosa
5.4,3.9,1.7,0.4,setosa
4.6,3.4,1.4,0.3,setosa
5.0,3.4,1.5,0.2,setosa
4.4,2.9,1.4,0.2,setosa
4.9,3.1,1.5,0.1,setosa
$
"""


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


create_step_merge_csv = kfp.components.create_component_from_func(
    func=merge_csv,
    output_component_file=
    'merge_csv_component.yaml',  # This is optional. It saves the component spec for future use.
    base_image='python:3.7',
    packages_to_install=['pandas==1.1.4'])

web_downloader_op = kfp.components.load_component_from_url(
    'https://raw.githubusercontent.com/kubeflow/pipelines/master/components/contrib/web/Download/component.yaml'
)


# Define a pipeline and create a task from a component:
def my_pipeline(url):
    web_downloader_task = web_downloader_op(url=url)
    merge_csv_task = create_step_merge_csv(
        file=web_downloader_task.outputs['data'])
    # The outputs of the merge_csv_task can be referenced using the
    # merge_csv_task.outputs dictionary: merge_csv_task.outputs['output_csv']


kfp.compiler.Compiler().compile(pipeline_func=my_pipeline,
                                package_path='pipeline.yaml')
