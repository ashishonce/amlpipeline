import os
import json

from azureml.core import Workspace
from azureml.core.compute import ComputeTarget
from azureml.exceptions import ComputeTargetException, AuthenticationException, ProjectSystemException
from azureml.core.authentication import ServicePrincipalAuthentication
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError
from utils import AMLConfigurationException, required_parameters_provided, create_aml_cluster, create_aks_cluster


class ComputeTargetManager(object):
    def __init__(self):
        pass
    
    def executeAction(self, parameters_file =None, ws = None, azure_credentials = None , azure_computeTarget = None):
        try:
            azure_credentials = json.loads(azure_credentials)
        except JSONDecodeError:
            print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS")
            raise AMLConfigurationException(f"Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-compute/blob/master/README.md")

        # Checking provided parameters
        print("::debug::Checking provided parameters")
        required_parameters_provided(
            parameters=azure_credentials,
            keys=["tenantId", "clientId", "clientSecret"],
            message="Required parameter(s) not found in your azure credentials saved in AZURE_CREDENTIALS secret for logging in to the workspace. Please provide a value for the following key(s): "
        )
       
        compute_target = ComputeTarget(
            workspace=ws,
            name=azure_computeTarget
        )

        print(f"::debug::Found compute target with same name. Not updating the compute target: {compute_target.serialize()}")
        print("::debug::Successfully finished Azure Machine Learning Compute Action")
        return compute_target;
