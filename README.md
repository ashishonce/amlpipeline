# amlpipeline


An action to submit a run to your aml workspace with full flexibility

|Input | Required | Default | Description|
|--|--|--| --|
|azureCredentials| yes | {} | your Service Principle credentials for accessing or creating workspace, if you don't have any exisitng workspace, you must have a workspace.json file in .ml.azure folder in the repository
|amlpipelinefile| yes | None | name of the file which contains the configutaion for setting up aml runs 

### This action assumes you have all the necessary resources already set up before you use this action. if you don't have the resources used , you must first either create them or use
    other actions which support resource creation before using this.
    - Creation of or attachment to an AML Workspace with [azure/aml-workspace](https://github.com/Azure/aml-workspace)
    - Managing Azure compute resources with [azure/aml-compute](https://github.com/Azure/aml-compute): 
    - Managing Azure Machine Learning experimentation and pipeline runs with [azure/aml-run](https://github.com/Azure/aml-run)
    - Model Registration in Azure Machine Learning [azure/aml-registermodel](https://github.com/Azure/aml-registermodel)
    - Deployment to Azure Container Instances or Azure Kubernetes Service with [azure/aml-deploy](https://github.com/Azure/aml-deploy)


The action assumes you have a configuration yaml file at ".ml/azure" folder in your root directory. 
The configuraiton files can have either or both sections

RunSubmissions : # RunSubmissions are non - pipeline submissions which user wants to submit as part of his workflow, these can be simple script run or estimator run etc. 
    a run submission requires following values

    name : example<"amlcomputeTraining">
    workspace: example<'ashkumadevtestwkrspace'>
    run_config_file: example <"/train-on-amlcompute/train1/run_config1.py">  this file represents the file which will return a submission object to submit. it can be anything like ScriptRun, Estimator etc.
    run_config_function : "main" this function will be called by action and must accept two parameters ( workspace , inputs)
    
    inputs : # these values will be sent as input to the runConfig file, user may decide what to do with those params, if he has hardcoded all values then he need not to write these values,list is not restricted to this, user can define infinite list of inpute here  
         
    

PipelineSubmissions


a sample pipeline file can be found at path [amlpipeline.yaml]("./../.ml/azure/amlpipeline.yaml")

