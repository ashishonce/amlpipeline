from azureml.core import ComputeTarget
from azureml.pipeline.core import Pipeline
from azureml.pipeline.steps import PythonScriptStep

def main(workspace,inputs):
    # Loading compute target
    print("Loading compute target")
    compute_target = ComputeTarget(
        workspace=workspace,
        name=inputs["compute"]
    )

    step = PythonScriptStep(name=inputs["step_name"],
                            script_name=inputs["train_script"], 
                            compute_target= compute_target, 
                            source_directory=inputs["source_directory"],
                            allow_reuse=True)
    
    return step



