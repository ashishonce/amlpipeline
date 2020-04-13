# amlpipeline


An action to submit a run to your aml workspace with full flexibility

|Input | Required | Default | Description|
|--|--|--| --|
|azureCredentials| yes | {} | your Service Principle credentials for accessing or creating workspace, if you don't have any exisitng workspace, you must have a workspace.json file in .ml.azure folder in the repository
|amlpipelinefile| yes | None | name of the file which contains the configutaion for setting up aml runs 

### This action assumes you have all the necessary resources already set up before you use this action. if you don't have the resources used , you must first either create them or use
    other actions which support resource creation before using this.

a sample pipeline file can be found at path [amlpipeline.yaml]("./../.ml/azure/amlpipeline.yaml")

