import os
import yaml

def _getPipeLineConfig(pipeline_file_path):
    with open(pipeline_file_path) as file:
        # The FullLoader parameter handles the conversion from YAML
        # scalar values to Python the dictionary format
        pipelineConfig = yaml.load(file, Loader=yaml.FullLoader)
        return pipelineConfig;

