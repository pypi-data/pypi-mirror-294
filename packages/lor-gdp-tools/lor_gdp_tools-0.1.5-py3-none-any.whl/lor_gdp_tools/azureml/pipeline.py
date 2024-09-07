# AML Core
from azureml.core import Workspace, Experiment, Dataset, Environment
from azureml.core.compute import ComputeTarget, AmlCompute
from azureml.core.compute_target import ComputeTargetException
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import RunConfiguration

# AML pipeline
from azureml.pipeline.core import Pipeline, PipelineData, PipelineParameter
from azureml.pipeline.steps import PythonScriptStep

# AML Data
from azureml.data import OutputFileDatasetConfig
from azureml.data.dataset_consumption_config import DatasetConsumptionConfig
from azureml.data.datapath import DataPath

import pathlib
import logging
from typing import List
import sys


class ProjectPipeline:
    '''
    Class for managing and creating an AML pipeline.
    WARNING: Before instantiating this class make sure that you run:
            python setup.py bdist_wheel
    This is so that the correct dependencies are installed for the
    pipeline's environment.
    Attributes:
        aml_project_name: The name of the project on AML.
        aml_compute_target: The name of the target compute that the pipeline
                            will use.
        project_folder: The directory location of the root of the project.
        ws: The AML workspace of the pipeline
        datastore: The default datastore of ws.
        aml_run_config: The AMl run configuration of the pipeline.
    '''

    def __init__(self, aml_project_name: str, aml_compute_target: str):
        self._logger = logging.getLogger(__name__)
        self._logger.setLevel(logging.DEBUG)
        self._handler = logging.StreamHandler(sys.stdout)
        self._handler.setLevel(logging.DEBUG)
        self._formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self._handler.setFormatter(self._formatter)
        self._logger.addHandler(self._handler)

        self.aml_project_name = aml_project_name
        self.aml_compute_target = aml_compute_target

        # Root folder of repo
        self.project_folder = pathlib.Path(f'{__file__}/../../../').resolve()
        self.ws = Workspace.from_config()
        self.datastore = self.ws.get_default_datastore()

        # Generate pipeline environment
        self._env = Environment(name=self.aml_project_name)
        self._setup_env_dependencies()

        # Provision compute
        self._provision_compute()

        # Create AML run config
        self.aml_run_config = RunConfiguration()
        self.aml_run_config.target = self.aml_compute_target
        self.aml_run_config.environment = self._env

    def _provision_compute(self) -> None:
        '''
        Provision a AML compute for the project pipeline.
        Args:
            None
        
        Returns:
            None
        '''

        try:
            aml_compute = AmlCompute(self.ws, self.aml_compute_target)
            self._logger.info(f'Found existing compute target: {self.aml_compute_target}')
        except ComputeTargetException:
            self._logger.info('No existing compute target found!')
            self._logger.info(f'Creating compute target: {self.aml_compute_target}')
            provisioning_config = AmlCompute.provisioning_configuration(
                vm_size='STANDARD_DS3_V2',
                min_nodes=1,
                max_nodes=4
            )
            self._logger.info('Compute target creation started')
            aml_compute = ComputeTarget.create(
                self.ws,
                self.aml_compute_target,
                provisioning_config
            )
            aml_compute.wait_for_completion(
                show_output=True,
                min_node_count=None,
                timeout_in_minutes=20
            )

        self._logger.info('AML compute attached')

    def _setup_env_dependencies(self) -> None:
        '''
        Set up Conda dependencies of the pipeline environment.
        WARNING: Before running this method make sure that you run:
            python setup.py bdist_wheel
        This will generate a wheel of the src of this project for
        upload to the environment.
        Args:
            None
        Returns:
            None
        '''
        # Upload local wheel to Azure
        whl_loc = list(pathlib.Path(f'{self.project_folder}/dist/').glob('*.whl'))[0]
        whl_url = Environment.add_private_pip_wheel(
            workspace=self.ws,
            file_path=whl_loc,
            exist_ok=True
        )

        conda_dep = CondaDependencies(
            conda_dependencies_file_path=f'{self.project_folder}/environment.yml'
        )
        conda_dep.add_pip_package(whl_url)
        # Remove the src pip package in favour of using the wheel
        conda_dep.remove_pip_package('.')
        self._env.python.conda_dependencies = conda_dep

    def submit_pipeline(self, steps: List[PythonScriptStep]) -> None:
        '''
        Generates a pipeline object from a list of PythonScriptSteps,
        validates the pipeline and then runs the pipeline in an experiment.
        Args:
            steps: A list of PythonScriptSteps
        
        Returns:
            None
        '''
        pipeline = Pipeline(workspace=self.ws, steps=steps)
        # A pipeline must be validated before it can be submitted
        pipeline.validate()

            # Submit pipeline
        pipeline_run = Experiment(
            workspace=self.ws,
            name=f'{self.aml_project_name}-pipeline'
        )
        pipeline_run.submit(pipeline, regenerate_outputs=False)


def main():
    '''Entry point function of script.'''

    aml_project_name = 'gdp-tools'

    pipeline = ProjectPipeline(
        aml_project_name=aml_project_name,
        aml_compute_target=f'{aml_project_name}-pipeline'
    )


if __name__ == '__main__':
    main()
