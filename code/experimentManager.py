

from azureml.core import Experiment

class ExperimentManager(object):
    def __init__(self):
        pass
    def executeAction(self,ws, experiment_name = None):
        experiment = None;
        if experiment_name != None:
            experiment = Experiment(workspace = ws, name = experiment_name)

        return experiment;
