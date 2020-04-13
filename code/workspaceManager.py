
import os
import json

from azureml.core import Workspace
from azureml.exceptions import WorkspaceException, AuthenticationException, ProjectSystemException
from azureml.core.authentication import ServicePrincipalAuthentication
from azureml.core.authentication import AzureCliAuthentication
from adal.adal_error import AdalError
from msrest.exceptions import AuthenticationError
from json import JSONDecodeError
from utils import required_parameters_provided, AMLConfigurationException


class WorkspaceManager(object):
    def __init__(self,parameters_file = None, azure_credentials = None, azureml_workSpaceName=None, azureml_createWSIfNotExist =False):

        pass


    def executeAction(self,parameters_file,azure_credentials,azureml_workSpaceName,azureml_createWSIfNotExist):
        try:
            azure_credentials = json.loads(azure_credentials)
        except JSONDecodeError:
            print("::error::Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS. The JSON should include the following keys: 'tenantId', 'clientId', 'clientSecret' and 'subscriptionId'.")
            raise AMLConfigurationException(f"Incorrect or poorly formed output from azure credentials saved in AZURE_CREDENTIALS secret. See setup in https://github.com/Azure/aml-workspace/blob/master/README.md")
        
        # Checking provided parameters
        print("::debug::Checking provided parameters")
        required_parameters_provided(
            parameters=azure_credentials,
            keys=["tenantId", "clientId", "clientSecret", "subscriptionId"],
            message="Required parameter(s) not found in your azure credentials saved in AZURE_CREDENTIALS secret for logging in to the workspace. Please provide a value for the following key(s): "
        )
        
        if (azureml_workSpaceName == None) or len(azureml_workSpaceName) == 0:
            raise AMLConfigurationException("WorkSpace Name must be provided")

        # Loading Workspace
        sp_auth = ServicePrincipalAuthentication(
            tenant_id=azure_credentials.get("tenantId", ""),
            service_principal_id=azure_credentials.get("clientId", ""),
            service_principal_password=azure_credentials.get("clientSecret", "")
        )
        try:
            print("::debug::Loading existing Workspace")
            ws = Workspace.get(
                name=azureml_workSpaceName,
                subscription_id=azure_credentials.get("subscriptionId", ""),
                auth=sp_auth
            )
            print("::debug::Successfully loaded existing Workspace")
            print(ws)
        except AuthenticationException as exception:
            print(f"::error::Could not retrieve user token. Please paste output of `az ad sp create-for-rbac --name <your-sp-name> --role contributor --scopes /subscriptions/<your-subscriptionId>/resourceGroups/<your-rg> --sdk-auth` as value of secret variable: AZURE_CREDENTIALS: {exception}")
            raise AuthenticationException
        except AuthenticationError as exception:
            print(f"::error::Microsoft REST Authentication Error: {exception}")
            raise AuthenticationException
        except AdalError as exception:
            print(f"::error::Active Directory Authentication Library Error: {exception}")
            raise AdalError
        except ProjectSystemException as exception:
            print(f"::error::Workspace authorizationfailed: {exception}")
            raise ProjectSystemException
        except WorkspaceException as exception:
            print(f"::debug::Loading existing Workspace failed: {exception}")
            
        return ws;



