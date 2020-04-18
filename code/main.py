import os

# from azureml.pipeline.steps import PythonScriptStep
# import azureml.core
# from azureml.core import Workspace, Experiment, Datastore
# from azureml.widgets import RunDetails
import inspect
# from azureml.core.compute import ComputeTarget, AmlCompute
# from azureml.core.compute_target import ComputeTargetException

from azureml.pipeline.core import Pipeline
import yamlreader
from workspaceManager import WorkspaceManager
from computeManager import ComputeTargetManager
from experimentManager import ExperimentManager

import sys
import importlib
from utils import *


def getRunSubmissionObject(ws, run_config_file_path, run_config_function, inputs):
    # Load module
    print("::debug::Loading module to receive experiment config")
    root = os.environ.get("GITHUB_WORKSPACE", default="./")
    print("::debug::Adding root to system path")
    sys.path.insert(0, f"{root}")
    run_config_file_path = run_config_file_path
    run_config_file_function_name = run_config_function
    print(root)
    print("::debug::Importing module")
    run_config_file_path = f"{run_config_file_path}.py" if not run_config_file_path.endswith(".py") else run_config_file_path
    try:
        run_config_spec = importlib.util.spec_from_file_location(
            name="runmodule",
            location=run_config_file_path
        )
        run_config_module = importlib.util.module_from_spec(spec=run_config_spec)
        run_config_spec.loader.exec_module(run_config_module)
        run_config_function = getattr(run_config_module, run_config_file_function_name, None)
    except ModuleNotFoundError as exception:
        print(f"::error::Could not load python script in your repository which defines the experiment config (Script: /{run_config_file_path}, Function: {run_config_file_function_name}()): {exception}")
        raise AMLExperimentConfigurationException(f"Could not load python script in your repository which defines the experiment config (Script: /{run_config_file_path}, Function: {run_config_file_function_name}()): {exception}")
    except FileNotFoundError as exception:
        print(f"::error::Could not load python script or function in your repository which defines the experiment config (Script: /{run_config_file_path}, Function: {run_config_file_function_name}()): {exception}")
        raise AMLExperimentConfigurationException(f"Could not load python script or function in your repository which defines the experiment config (Script: /{run_config_file_path}, Function: {run_config_file_function_name}()): {exception}")
    except AttributeError as exception:
        print(f"::error::Could not load python script or function in your repository which defines the experiment config (Script: /{run_config_file_path}, Function: {run_config_file_function_name}()): {exception}")
        raise AMLExperimentConfigurationException(f"Could not load python script or function in your repository which defines the experiment config (Script: /{run_config_file_path}, Function: {run_config_file_function_name}()): {exception}")

    # Load experiment config
    print("::debug::Loading experiment config")
    try:
        run_config = run_config_function(ws, inputs)
    except TypeError as exception:
        print(f"::error::Could not load experiment config from your module (Script: /{run_config_file_path}, Function: {run_config_file_function_name}()): {exception}")
        raise AMLExperimentConfigurationException(f"Could not load experiment config from your module (Script: /{run_config_file_path}, Function: {run_config_file_function_name}()): {exception}")
    return run_config


def handleRunSubmissions(submissions,azure_credentials):
    submittedRuns = []
    for submission in submissions:
        print(submission)
        wsManager = WorkspaceManager(None, azure_credentials, submission["workspace"], False)
        ws = wsManager.executeAction(None, azure_credentials, submission["workspace"], False);
        run_config = getRunSubmissionObject(ws,submission["run_config_file"], submission["run_config_function"], submission["inputs"])
        print(run_config)

        experiment_name = submission["inputs"]["experiment"]
        experiment = ExperimentManager().executeAction(ws,experiment_name)

        run = experiment.submit(run_config);
        submittedRuns.append(run);
        # now submit the run config
    return submittedRuns;

########################### pipeline submissions ##############################

def getpipelineSubmissionObject(ws,submission):
    print("::debug::Loading module to receive experiment config")
    root = os.environ.get("GITHUB_WORKSPACE", default="./")
    print("::debug::Adding root to system path")
    sys.path.insert(0, f"{root}")
    pipeline_yaml_path = submission["pipeline_yamlFile"];

    if pipeline_yaml_path != None and pipeline_yaml_path != "":
        # Load pipeline yaml definition
        print("::debug::Loading pipeline yaml definition")
        try:
            run_config = Pipeline.load_yaml(
                workspace=ws,
                filename=pipeline_yaml_path
                )
            return run_config;  # this is a pipeline run config
        except Exception as exception:
            print(f"::error::Error when loading pipeline yaml definition your repository (Path: /{pipeline_yaml_path}): {exception}")
            raise AMLExperimentConfigurationException(f"Error when loading pipeline yaml definition your repository (Path: /{pipeline_yaml_path}): {exception}")
    
        # means yaml file doesn't exists.
    else:
        # means there are steps which user wants to execute. 
        # steps here
        submissionSteps = [] 
        for step in submission["steps"]:
            pipelineStep = getRunSubmissionObject(ws, step["pipelineStep_run_config_file"], step["run_config_function"], step["inputs"])
            submissionSteps.append(pipelineStep)
        print(submissionSteps)
        pipeline1 = Pipeline(workspace=ws, steps=submissionSteps)
        print ("Pipeline is built")
        print(pipeline1)
        pipeline1.validate();
        print("Pipeline validation complete")
        return pipeline1

def handlePipelineSubmissions(submissions, azure_credentials):
    submittedPipelinesRuns = []
    for submission in submissions:
        print(submission)
        wsManager = WorkspaceManager(None, azure_credentials, submission["workspace"], False)
        ws = wsManager.executeAction(None, azure_credentials, submission["workspace"], False);

        experiment_name = submission["experiment"]
        experiment = ExperimentManager().executeAction(ws,experiment_name)

        submit_pipeline = getpipelineSubmissionObject(ws,submission)
        run = experiment.submit(submit_pipeline, regenerate_outputs=False)
        submittedPipelinesRuns.append(run)

    return submittedPipelinesRuns

def main():
    azure_credentials = os.environ.get("INPUT_AZURECREDENTIALS", default='{}')
    parameters_file = os.environ.get("INPUT_AMLPIPELINEFILE", default="amlpipeline.yaml") 
    # for local debug : pipeline_file_path = os.path.join("..",".ml","azure", parameters_file)
    pipeline_file_path = os.path.join(".ml","azure", parameters_file)
    pipeline_file_path = os.path.abspath(pipeline_file_path)
    pipeline_Config = yamlreader._getPipeLineConfig(pipeline_file_path)
    # print(pipeline_Config)
    # os.chdir('./../') # literal hack to run it locally , should be removed for cloud
    submittedRuns = []

    if "RunSubmissions"  in pipeline_Config:
        if pipeline_Config["RunSubmissions"] != None and len(pipeline_Config["RunSubmissions"]) > 0:
            submittedRuns = handleRunSubmissions(pipeline_Config["RunSubmissions"], azure_credentials)
            print(submittedRuns)
            print(" run submission successful")
            
    submittedPipelines = []
    if "PipelineSubmissions"  in pipeline_Config:
        if pipeline_Config["PipelineSubmissions"] != None and len(pipeline_Config["PipelineSubmissions"]) > 0:
            submittedPipelines = handlePipelineSubmissions(pipeline_Config["PipelineSubmissions"], azure_credentials)
            print(submittedPipelines)
            print(" run submission successful")


if __name__ == "__main__":
    main()
