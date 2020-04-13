# Use a RunConfiguration to specify some additional requirements for this step.
from azureml.core.runconfig import RunConfiguration
from azureml.core.conda_dependencies import CondaDependencies
from azureml.core.runconfig import DEFAULT_CPU_IMAGE
from azureml.core import ComputeTarget
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep


def main(workspace,inputs):

    print("Loading compute target")
    compute_target = ComputeTarget(
        workspace=workspace,
        name=inputs["compute"]
    )
    # create a new runconfig object
    run_config = RunConfiguration()

    # enable Docker 
    run_config.environment.docker.enabled = True

    # set Docker base image to the default CPU-based image
    run_config.environment.docker.base_image = DEFAULT_CPU_IMAGE

    # use conda_dependencies.yml to create a conda environment in the Docker image for execution
    run_config.environment.python.user_managed_dependencies = False

    # specify CondaDependencies obj
    run_config.environment.python.conda_dependencies = CondaDependencies.create(conda_packages=['scikit-learn'])

    # For this step, we use yet another source_directory
    step = PythonScriptStep(name=inputs["step_name"],
                            script_name=inputs["train_script"], 
                            compute_target=compute_target, 
                            source_directory=inputs["source_directory"],
                            runconfig=run_config,
                            allow_reuse=True)
    return step