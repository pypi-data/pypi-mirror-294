class ModelStore:
    
    """
    Class to interact with the model store API to get model configuration info and model related info.
    """
    
    def __init__(self, session): 
        
        """
        Initialize a new ModelStore instance.

        Parameters
        ----------
        session : Session
            The session object containing authentication information.

        Example
        -------
        >>> session = Session(account_number="9625383462734064921642156")
        >>> model_store = ModelStore(session)
        """
        
        self.session = session
        self.account_number = session.account_number
        self.project_id = session.project_id
        self.rpc = session.rpc

    def handle_response(self, resp, success_message, error_message):
        
        """
        Helper function to handle API response.

        Parameters
        ----------
        resp : dict
            The API response.
        success_message : str
            Message to return on success.
        error_message : str
            Message to return on error.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.handle_response(api_response, "Success", "Error occurred")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(message)
        """
        if resp.get("success"):
            error = None
            message = success_message
        else:
            error = resp.get("message")
            message = error_message
        return resp, error, message

    # To fetch a model family
    def get_model_family(self, model_family_id):
        
        """
        Fetch a model family by its ID.

        Parameters
        ----------
        model_family_id : str
            The ID of the model family to fetch.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_model_family("66912342567883074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model family: {resp}")
        """
        
        path = f"/v1/model_store/model_family/{model_family_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Successfully fetched the model family",
                                    "An error occured while fetching the model family")

    # To fetch model info
    def get_model_info(self, model_info_id):
        
        """
        Fetch model information by its ID.

        Parameters
        ----------
        model_info_id : str
            The ID of the model info to fetch.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_model_info("66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model info: {resp}")
        """

        path = f"/v1/model_store/model_info/{model_info_id}"
        resp = self.rpc.get(path=path)
       
        return self.handle_response(resp, "Successfully fetched the model info",
                                    "An error occured while fetching the model info")

    def get_default_model_training_payload(self, model_info_id):
        
        model_info = self.get_model_info(model_info_id = model_info_id)[0]['data']
        model_train_config = self.get_model_train_config(model_info_id = model_info_id)[0]['data']
    
        model_training_payload = [{
                "model_key": model_info['modelKey'],
                "is_autoML": False,
                "tuning_type": "manual",
                "model_checkpoint":"auto",
                "checkpoint_type" : 'predefined',
                "params_millions": model_info['paramsMillions'],
                "model_name": model_info['modelName'],
                "id_model_info": model_info_id,
                "action_config": {},
                "model_config": {param['keyName']: [param['defaultValue']] for param in model_train_config['actionConfig']}
            }]
    
        return model_training_payload

    def get_default_model_export_config(self, model_info_id, export_format):
        model_export_config  = self.get_action_config_for_model_export(model_info_id, export_format)[0]['data']
        default_model_export_config = {param['keyName']: param['defaultValue'] for param in model_export_config['actionConfig']}
        return default_model_export_config
    
    # To fetch model action config
    def get_model_action_config(self, model_action_config_id):
        """
        Fetch model action configuration by its ID.

        Parameters
        ----------
        model_action_config_id : str
            The ID of the model action config to fetch.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_model_action_config("66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model action config: {resp}")
        """

        path = f"/v1/model_store/model_action_config/{model_action_config_id}"
        resp = self.rpc.get(path=path)
        
        return self.handle_response(resp, "Successfully fetched the model action config",
                                    "An error occured while fetching the model action config")

    def get_all_models(self, project_id, project_type = "classification"):
        
        """
        Fetch all models for a given project.

        Parameters
        ----------
        project_id : str
            The ID of the project.
        project_type : str, optional
            The type of the project (default is "classification")(Available types are "detection" and "instance_segmentation").

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_all_models("66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"All models: {resp}")
        """
        path = f"/v1/model_store/get_all_models?projectId={project_id}&projectType={project_type}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Successfully fetched all model infos",
                                    "An error occured while fetching the model family")
    
    def get_all_model_families(self, project_id, project_type = "classification"):
        
        """
        Fetch all model families for a given project.

        Parameters
        ----------
        project_id : str
            The ID of the project.
        project_type : str, optional
            The type of the project (default is "classification").

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_all_model_families("66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"All model families: {resp}")
        """
        path = f"/v1/model_store/get_all_model_families?projectId={project_id}&projectType={project_type}"
        resp = self.rpc.get(path=path)
    
        return self.handle_response(resp, "Successfully fetched all model family",
                                    "An error occured while fetching the model family")
    
    def get_models_by_modelfamily(self, model_family_id):
        
        """
        Fetch all models for a given model family.

        Parameters
        ----------
        model_family_id : str
            The ID of the model family.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_models_by_modelfamily("66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Models by model family: {resp}")
        """
        path = f"/v1/model_store/get_models_by_modelfamily?modelFamilyId={model_family_id}"
        resp = self.rpc.get(path=path)
       
        return self.handle_response(resp, "Successfully fetched all model family",
                                    "An error occured while fetching the model family")
    
    def get_export_formats(self, model_info_id):
        
        """
        Fetch export formats for a given model.

        Parameters
        ----------
        model_info_id : str
            The ID of the model info.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_export_formats("66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Export formats: {resp}")
        """
        path = f"/v1/model_store/get_export_formats?modelInfoId={model_info_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Successfully fetched all model family",
                                    "An error occured while fetching the model family")
   
    def get_action_config_for_model_export(self, model_info_id, export_format):
        """
        Fetch action configuration for model export.

        Parameters
        ----------
        model_info_id : str
            The ID of the model info.
        export_format : str
            The export format.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_action_config_for_model_export("66912342583678074789d", "ONNX")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Action config for model export: {resp}")
        """
        path = f"/v1/model_store/get_action_config_for_model_export?modelInfoId={model_info_id}&exportFormat={export_format}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Successfully fetched all model family",
                                    "An error occured while fetching the model family")
            
    def fetch_supported_runtimes_metrics(self, model_inputs, model_outputs, project_id):
        """
        Fetch supported runtimes and metrics for a given project.

        Parameters
        ----------
        model_inputs : list
            List of model inputs.
        model_outputs : list
            List of model outputs.
        project_id : str
            The ID of the project.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.fetch_supported_runtimes_metrics(["image"], ["classification"], "66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Supported runtimes and metrics: {resp}")
        """
        path = f"/v1/model_store/fetch_supported_runtimes_metrics?projectId={project_id}"
        payload = {
            "modelInputs": model_inputs,
            "modelOutputs": model_outputs,
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=payload)

        return self.handle_response(resp, "Successfully fetched all model family",
                                    "An error occured while fetching the model family")
    
    def get_model_train_config(self, model_info_id):
        """
        Fetch model training configuration by its ID.

        Parameters
        ----------
        model_info_id : str
            The ID of the model info.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_model_train_config("66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model train config: {resp}")
        """
        path = f"/v1/model_store/get_train_config/{model_info_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Successfully fetched model train config",
                                    "An error occured while fetching model train config")

    def get_model_info_by_name_and_key(self, model_name, model_key):
        """
        Fetch model information by name and key.

        Parameters
        ----------
        model_name : str
            The name of the model.
        model_key : str
            The key of the model.

        Returns
        -------
        tuple
            A tuple containing the response data, error (if any), and message.

        Example
        -------
        >>> resp, error, message = model_store.get_model_info_by_name_and_key("ResNet-18", "66912342583678074789d")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model info: {resp}")
        """
        path = f"/v1/model_store/get_model_info_by_name_and_key?modelName={model_name}&modelKey={model_key}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Successfully fetched model info",
                                    "An error occured while fetching model info")


class BYOM:
    
    """
    A class to interact with the BYOM (Bring Your Own Model) API for managing model families, model information, 
    and model action configurations.

    Attributes:
    -----------
    session : Session
        A session object containing account information and RPC (Remote Procedure Call) details.
    account_number : str
        The account number associated with the session.
    rpc : RPC
        The RPC object used to make API calls.

    Methods:
    --------
    handle_response(resp, success_message, error_message)
        Helper function to handle API responses.

    delete_model_family(model_family_id)
        Deletes a model family using its ID.

    delete_model_info(model_info_id)
        Deletes model information using its ID.

    delete_model_action_config(model_action_config_id)
        Deletes a model action configuration using its ID.
        
    add_model_family(...)
        Adds a new model family.

    add_model_info(...)
        Adds new model information.

    add_model_action_config(...)
        Adds a new model action configuration.

    update_model_family(...)
        Updates a model family.

    update_model_info(...)
        Updates model information.

    update_model_action_config(...)
        Updates a model action configuration.

    add_model_family_action_config(...)
        Adds an action configuration to a model family.
    """

    def __init__(self, session):
        """
        Initializes the BYOM class with a session object.

        Parameters:
        -----------
        session : Session
            A session object containing account information and RPC details.
        """
        self.session = session
        self.account_number = session.account_number
        self.rpc = session.rpc

    def handle_response(self, resp, success_message, error_message):
        """
        Handles the API response and returns a tuple containing the response, error message (if any), 
        and a status message.

        Parameters:
        -----------
        resp : dict
            The response dictionary from the API call.
        success_message : str
            The message to return if the API call is successful.
        error_message : str
            The message to return if the API call fails.

        Returns:
        --------
        tuple
            A tuple containing the response dictionary, error message (or None if successful), 
            and a status message.
        """
        if resp.get("success"):
            error = None
            message = success_message
        else:
            error = resp.get("message")
            message = error_message

        return resp, error, message
    
    # To delete a model family
    def delete_model_family(self, model_family_id):
        """
        Deletes a model family using its ID.

        Parameters:
        -----------
        model_family_id : str
            The ID of the model family to delete.

        Returns:
        --------
        tuple
            A tuple containing the API response, error message (or None if successful), and a status message.
        """
        path = f"/v1/model_store/model_family/{model_family_id}"
        resp = self.rpc.delete(path=path)
    
        return self.handle_response(resp, "Successfully deleted the model family",
                                    "An error occured while deleting the model family")
    
    # To delete model info
    def delete_model_info(self, model_info_id):
        """
        Deletes model information using its ID.

        Parameters:
        -----------
        model_info_id : str
            The ID of the model information to delete.

        Returns:
        --------
        tuple
            A tuple containing the API response, error message (or None if successful), and a status message.
        """
        path = f"/v1/model_store/model_info/{model_info_id}"
        resp = self.rpc.delete(path=path)
        
        return self.handle_response(resp, "Successfully deleted the model family",
                                    "An error occured while deleting the model family")
    
    # To delete model action config
    def delete_model_action_config(self, model_action_config_id):
        """
        Deletes a model action configuration using its ID.

        Parameters:
        -----------
        model_action_config_id : str
            The ID of the model action configuration to delete.

        Returns:
        --------
        tuple
            A tuple containing the API response, error message (or None if successful), and a status message.
        """
        path = f"/v1/model_store/model_action_config/{model_action_config_id}"
        resp = self.rpc.delete(path=path)
        
        return self.handle_response(resp, "Successfully deleted the model action config",
                                    "An error occured while deleting the model action config")
    
    # To add a new entry into model family
    def add_model_family(
        self, 
        project_id, 
        model_family, 
        model_inputs, 
        model_outputs, 
        models, 
        description, 
        training_framework, 
        supported_runtimes, 
        benchmark_datasets, 
        supported_metrics, 
        pruning_support, 
        code_repository, 
        training_docker_container, 
        input_format, 
        data_loader_class_definition, 
        data_loader_call_signature, 
        references, 
        is_private
    ):
        """
    Adds a new model family to the model store.

    This function sends a POST request to add a new model family with the provided parameters.

    Parameters:
    -----------
    project_id : str
        The unique identifier for the project.
    model_family : str
        The name of the model family.
    model_inputs : list
        List of input specifications for the model.
    model_outputs : list
        List of output specifications for the model.
    models : list
        List of models in the family.
    description : str
        A detailed description of the model family.
    training_framework : str
        The framework used for training the models.
    supported_runtimes : list
        List of supported runtime environments.
    benchmark_datasets : list
        List of datasets used for benchmarking.
    supported_metrics : list
        List of metrics supported for evaluation.
    pruning_support : bool
        Indicates if the model family supports pruning.
    code_repository : str
        URL or path to the code repository.
    training_docker_container : str
        Docker container used for training.
    input_format : str
        Format of the input data.
    data_loader_class_definition : str
        Definition of the data loader class.
    data_loader_call_signature : str
        Call signature for the data loader.
    references : list
        List of references or citations.
    is_private : bool
        Indicates if the model family is private.

    Returns:
    --------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Raises:
    -------
    May raise exceptions related to network issues or API errors.

    Notes:
    ------
    This function uses the self.rpc.post method to send the request and
    self.handle_response to process the response.
    """

        path = "/v1/model_store/add_model_family"
        model_store_payload = {
            "modelFamily": model_family,
            "modelInputs": model_inputs,
            "modelOutputs": model_outputs,
            "models": models,
            "description": description,
            "trainingFramework": training_framework,
            "supportedRuntimes": supported_runtimes,
            "benchmarkDatasets": benchmark_datasets,
            "supportedMetrics": supported_metrics,
            "pruningSupport": pruning_support,
            "codeRepository": code_repository,
            "trainingDockerContainer": training_docker_container,
            "dataProcessing": {
                "inputFormat": input_format,
                "dataLoaderClassDefinition": data_loader_class_definition,
                "dataLoaderCallSignature": data_loader_call_signature
            },
            "references": references,
            "isPrivate": is_private,
            "projectId": project_id
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=model_store_payload) 

        return self.handle_response(resp, "New model family created",
                                    "An error occured while creating model family")
    
    # To add a new entry into model info
    def add_model_info(
        self,
        model_key,
        model_name,
        model_family_id,
        params_millions,
        recommended_run_time,
        benchmark_results,
        run_time_results
    ):
        """
    Adds information for a specific model to the model store.

    This function sends a POST request to add information about a model with the provided parameters.

    Parameters:
    -----------
    model_key : str
        A unique identifier for the model.
    model_name : str
        The name of the model.
    model_family_id : str
        The identifier of the model family this model belongs to.
    params_millions : float
        The number of parameters in the model, in millions.
    recommended_run_time : list
        List of recommended runtime environments for the model.
    benchmark_results : dict
        Dictionary containing benchmark results for the model.
    run_time_results : dict
        Dictionary containing runtime performance results for the model.

    Returns:
    --------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Raises:
    -------
    May raise exceptions related to network issues or API errors.

    Notes:
    ------
    This function uses the self.rpc.post method to send the request and
    self.handle_response to process the response.
    """

        path = "/v1/model_store/add_model_info"
        model_store_payload = {
            "modelKey": model_key,
            "modelName": model_name,
            "_idModelFamily": model_family_id,
            "paramsMillions": params_millions,
            "recommendedRuntimes": recommended_run_time,
            "benchmarkResults": benchmark_results,
            "runtimeResults": run_time_results
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=model_store_payload)

        return self.handle_response(resp, "New model family created",
                                    "An error occured while creating model info")
    
    # To add a new entry into model action config
    def add_model_action_config(
        self,
        model_info_id,
        action_type,
        action_config,
        docker_container_for_action,
        docker_container_for_evaluation,
        docker_credentials,
        private_docker,
        model_checkpoint,
        action_call_signature,
        export_format
    ):
        """
    Adds a new action configuration for a specific model in the model store.

    This function sends a POST request to add a new action configuration for a model with the provided parameters.

    Parameters:
    -----------
    model_info_id : str
        The identifier of the model info to which this action config belongs.
    action_type : str
        The type of action (e.g., 'train_model', 'export_model').
    action_config : dict
        Configuration details for the action.
    docker_container_for_action : str
        Docker container used for the action.
    docker_container_for_evaluation : str
        Docker container used for evaluation.
    docker_credentials : dict
        Credentials for accessing Docker containers.
    private_docker : bool
        Flag indicating if the Docker containers are private.
    model_checkpoint : str
        Path or identifier for the model checkpoint.
    action_call_signature : str
        Call signature for the action.
    export_format : str
        Format for exporting the model.

    Returns:
    --------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Raises:
    -------
    May raise exceptions related to network issues or API errors.

    Notes:
    ------
    This function uses the self.rpc.post method to send the request and
    self.handle_response to process the response.
    """
        path = "/v1/model_store/add_model_action_config"
        model_store_payload = {
            "_idModelInfo": model_info_id,
            "actionType": action_type,
            "actionConfig": action_config,
            "dockerContainerForAction": docker_container_for_action,
            "dockerContainerForEvaluation": docker_container_for_evaluation,
            "dockerCredentials": docker_credentials,
            "privateDocker": private_docker,
            "modelCheckpoint": model_checkpoint,
            "actionCallSignature": action_call_signature,
            "exportFormat": export_format
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=model_store_payload)

        return self.handle_response(resp, "New model action config created",
                                    "An error occured while creating model action config")
    
    # To update model family
    def update_model_family(
        self,
        model_family_id,
        project_id,
        model_family,
        model_inputs,
        model_outputs,
        model_keys,
        description,
        training_framework,
        supported_runtimes,
        benchmark_datasets,
        supported_metrics,
        pruning_support,
        code_repository,
        training_docker_container,
        input_format, 
        data_loader_class_definition, 
        data_loader_call_signature,
        references,
        is_private
    ):
        """
    Updates an existing model family in the model store.

    This function sends a PUT request to update a model family with the provided parameters.

    Parameters:
    -----------
    model_family_id : str
        The unique identifier of the model family to update.
    project_id : str
        The unique identifier for the project.
    model_family : str
        The updated name of the model family.
    model_inputs : list
        Updated list of input specifications for the model family.
    model_outputs : list
        Updated list of output specifications for the model family.
    model_keys : list
        Updated list of model keys associated with this family.
    description : str
        Updated detailed description of the model family.
    training_framework : str
        Updated framework used for training the models.
    supported_runtimes : list
        Updated list of supported runtime environments.
    benchmark_datasets : list
        Updated list of datasets used for benchmarking.
    supported_metrics : list
        Updated list of metrics supported for evaluation.
    pruning_support : bool
        Updated indicator if the model family supports pruning.
    code_repository : str
        Updated URL or path to the code repository.
    training_docker_container : str
        Updated Docker container used for training.
    input_format : str
        Updated format of the input data.
    data_loader_class_definition : str
        Updated definition of the data loader class.
    data_loader_call_signature : str
        Updated call signature for the data loader.
    references : list
        Updated list of references or citations.
    is_private : bool
        Updated indicator if the model family is private.

    Returns:
    --------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Raises:
    -------
    May raise exceptions related to network issues or API errors.

    Notes:
    ------
    This function uses the self.rpc.put method to send the request and
    self.handle_response to process the response.
    """
        path = f"/v1/model_store/model_family/{model_family_id}"
        model_store_payload = {
            "modelFamily": model_family,
            "modelInputs": model_inputs,
            "modelOutputs": model_outputs,
            "modelKeys": model_keys,
            "description": description,
            "trainingFramework": training_framework,
            "supportedRuntimes": supported_runtimes,
            "benchmarkDatasets": benchmark_datasets,
            "supportedMetrics": supported_metrics,
            "pruningSupport": pruning_support,
            "codeRepository": code_repository,
            "trainingDockerContainer": training_docker_container,
            "dataProcessing": {
                "inputFormat": input_format,
                "dataLoaderClassDefinition": data_loader_class_definition,
                "dataLoaderCallSignature": data_loader_call_signature
            },
            "references": references,
            "isPrivate": is_private
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.put(path=path, headers=headers, payload=model_store_payload)

        return self.handle_response(resp, "Model family successfully updated",
                                    "An error occured while updating model family")
    
    # To update model info
    def update_model_info(
        self,
        model_info_id,
        model_key,
        model_name,
        model_family_id,
        params_millions,
        recommended_runtime,
        benchmark_results,
        runtime_results
    ):
        """
    Updates information for a specific model in the model store.

    This function sends a PUT request to update model information with the provided parameters.

    Parameters:
    -----------
    model_info_id : str
        The unique identifier of the model info to update.
    model_key : str
        The updated unique identifier for the model.
    model_name : str
        The updated name of the model.
    model_family_id : str
        The updated identifier of the model family this model belongs to.
    params_millions : float
        The updated number of parameters in the model, in millions.
    recommended_runtime : list
        Updated list of recommended runtime environments for the model.
    benchmark_results : dict
        Updated dictionary containing benchmark results for the model.
    runtime_results : dict
        Updated dictionary containing runtime performance results for the model.

    Returns:
    --------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Raises:
    -------
    May raise exceptions related to network issues or API errors.

    Notes:
    ------
    This function uses the self.rpc.put method to send the request and
    self.handle_response to process the response.
    """
        path = f"/v1/model_store/model_info/{model_info_id}"
        model_store_payload = {
            "modelKey": model_key,
            "modelName": model_name,
            "_idModelFamily": model_family_id,
            "paramsMillions": params_millions,
            "recommendedRuntimes": recommended_runtime,
            "benchmarkResults": benchmark_results,
            "runtimeResults": runtime_results
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.put(path=path, headers=headers, payload=model_store_payload)

        return self.handle_response(resp, "Model family successfully updated",
                                    "An error occured while updating model family")
    
    # To update model action config
    def update_model_action_config(
        self,
        model_action_config_id,
        model_info_id,
        action_type,
        action_config,
        docker_container_for_action,
        docker_container_for_evaluation,
        docker_credentials,
        private_docker,
        model_checkpoint,
        action_call_signature,
        export_format
    ):
        """
    Updates the action configuration for a specific model in the model store.

    This function sends a PUT request to update model action configuration with the provided parameters.

    Parameters:
    -----------
    model_action_config_id : str
        The unique identifier of the model action config to update.
    model_info_id : str
        The identifier of the model info this action config belongs to.
    action_type : str
        The updated type of action (e.g., 'train_model', 'export_model').
    action_config : dict
        Updated configuration details for the action.
    docker_container_for_action : str
        Updated Docker container used for the action.
    docker_container_for_evaluation : str
        Updated Docker container used for evaluation.
    docker_credentials : dict
        Updated credentials for accessing Docker containers.
    private_docker : bool
        Updated flag indicating if the Docker containers are private.
    model_checkpoint : str
        Updated path or identifier for the model checkpoint.
    action_call_signature : str
        Updated call signature for the action.
    export_format : str
        Updated format for exporting the model.

    Returns:
    --------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Raises:
    -------
    May raise exceptions related to network issues or API errors.

    Notes:
    ------
    This function uses the self.rpc.put method to send the request and
    self.handle_response to process the response.
    """
        path = f"/v1/model_store/model_action_config/{model_action_config_id}"
        model_store_payload = {
            "_idModelInfo": model_info_id,
            "actionType": action_type,
            "actionConfig": action_config,
            "dockerContainerForAction": docker_container_for_action,
            "dockerContainerForEvaluation": docker_container_for_evaluation,
            "dockerCredentials": docker_credentials,
            "privateDocker": private_docker,
            "modelCheckpoint": model_checkpoint,
            "actionCallSignature": action_call_signature,
            "export_format": export_format
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.put(path=path, headers=headers, payload=model_store_payload)

        return self.handle_response(resp, "Model family successfully updated",
                                    "An error occured while updating model family")
    
    def add_model_family_action_config(
        self, 
        model_family_id,
        action_type, 
        action_config, 
        docker_container_for_action,
        docker_container_for_evaluation,
        model_checkpoint,
        docker_credentials, 
        private_docker,
        action_call_signature,
        export_format
        
    ):
        """
    Adds a new action configuration for a model family in the model store.

    This function sends a POST request to add a new model family action configuration with the provided parameters.

    Parameters:
    -----------
    model_family_id : str
        The identifier of the model family to add the action config to.
    action_type : str
        The type of action (e.g., 'train_model', 'export_model').
    action_config : dict
        Configuration details for the action.
    docker_container_for_action : str
        Docker container used for the action.
    docker_container_for_evaluation : str
        Docker container used for evaluation.
    model_checkpoint : str
        Path or identifier for the model checkpoint.
    docker_credentials : dict
        Credentials for accessing Docker containers.
    private_docker : bool
        Flag indicating if the Docker containers are private.
    action_call_signature : str
        Call signature for the action.
    export_format : str
        Format for exporting the model.

    Returns:
    --------
    tuple
        A tuple containing three elements:
        - API response (dict): The raw response from the API.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

    Raises:
    -------
    May raise exceptions related to network issues or API errors.

    Notes:
    ------
    This function uses the self.rpc.post method to send the request and
    self.handle_response to process the response.
    """
        path = f"/v1/model_store/add_model_family_config"
        model_store_payload = {
            "_idModelFamily": model_family_id,
            "actionType": action_type,
            "actionConfigs": action_config,
            "dockerCredentials": docker_credentials,
            "privateDocker": private_docker,
            "actionCallSignature": action_call_signature,
            "dockerContainerForAction": docker_container_for_action,
            "dockerContainerForEvaluation": docker_container_for_evaluation,
            "modelCheckpoint": model_checkpoint,
            "exportFormat": export_format,

        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=model_store_payload)

        return self.handle_response(resp, "Modelfamily action config successfully added",
                                    "An error occured while adding model family action config")
