from azureml.core import ComputeTarget
from azureml.train.estimator import Estimator


def main(workspace,inputs):
    # Loading compute target
    print("Loading compute target")
    compute_target = ComputeTarget(
        workspace=workspace,
        name=inputs["compute"]
    )

    # Loading script parameters
    print("Loading script parameters")
    script_params = {
        "--kernel": "linear",
        "--penalty": 0.9
    }

    # Creating experiment config
    print("Creating experiment config")
    estimator = Estimator(
        source_directory=inputs["source_directory"],
        entry_script=inputs["train_script"],
        script_params=script_params,
        compute_target=compute_target,
        conda_dependencies_file="environment.yml"
    )
    return estimator