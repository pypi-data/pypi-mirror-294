"""Module for interacting with backend API to manage experiment."""

class Experiment:
    """A class to manage experiment-related operations within a project."""
    def __init__(self, session, experiment_id = "", experiment_name = ""):
        """
        Initialize a new experiment instance.

        Parameters
        ----------
        session : Session
            The session object that manages the connection to the server.
        experiment_id : str, optional
            The ID of the experiment (default is an empty string).
        experiment_name : str, optional
            The name of the experiment (default is an empty string).

        Example
        -------
        >>> session = Session(account_number="account_number")
        >>> experiment = Experiment(session=session_object, experiment_id=experiment_id, experiment_name=experiment_name)
        """
        self.project_id = session.project_id
        self.project_name = session.project_name
        self.session = session
        self.rpc = session.rpc

        self.models_for_training = []
        self.experiment_id = experiment_id
        self.experiment_name = experiment_name
        resp, error, message = self.get_details()
        experiment_data = resp['data']
        if error:
            print(f"Error fetching project info: {message}")
        else:
            self.experiment_data = experiment_data
            self.experiment_id = experiment_data['_id']
            self.experiment_name = experiment_data['experimentName']
            self.dataset_id = experiment_data['_idDataset']
            self.dataset_name = experiment_data['datasetName']
            self.dataset_version = experiment_data['datasetVersion']
            self.primary_metric = experiment_data['primaryMetric']
            self.model_inputs = experiment_data['modelInputs']
            self.model_outputs = experiment_data['modelOutputs']
            self.target_runtime = experiment_data['targetRuntime']
    
    def handle_response(self, resp, success_message, error_message):
        """
        Handle API response and return a standardized tuple containing the result, error, and message. 
        This method is for internal use within the class to handle API responses.

        Parameters
        ----------
        response : dict
            The response from the API call.
        success_message : str
            Message to return on success.
        failure_message : str
            Message to return on failure.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.
        """
        if resp.get("success"):
            error = None
            message = success_message
        else:
            error = resp.get("message")
            message = error_message

        return resp, error, message
    
    def get_details(self):
        """
        Retrieve details of the experiment based on the experiment ID or name.

        This method fetches experiment details by ID if available; otherwise,
        it attempts to fetch by name. Raises a ValueError if neither identifier is provided.

        Returns
        -------
        tuple
            A tuple containing experiment details, error message (if any), and a status message.

        Raises
        ------
        ValueError
            If neither 'experiment_id' nor 'experiment_name' is provided.

        Example
        -------
        >>> experiment_details = experiment.get_details()
        >>> if isinstance(experiment_details, dict):
        >>>     print("Experiment Details:", experiment_details)
        >>> else:
        >>>     print("Failed to retrieve experiment details.")
        """
        id = self.experiment_id
        name = self.experiment_name
        # if id:
        #     try:
        #         return self._get_experiment_by_id() #TODO
        #     except Exception as e:
        #         print(f"Error retrieving experiment by id: {e}")
        if name:
            try:
                return self._get_experiment_by_name()
            except Exception as e:
                print(f"Error retrieving experiment by name: {e}")
        else:
            raise ValueError("At least one of 'dexperiment_id' or 'experiment_name' must be provided.")
        
    def _get_experiment_by_name(self):
        """
        Retrieve details of the experiment based on the experiment name.

        This method fetches experiment details by name. Raises a ValueError if neither identifier is provided.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises
        ------
        ValueError
            If neither 'experiment_id' nor 'experiment_name' is provided.

        Example
        -------
        >>> resp, err, msg = experiment.get_details()
        >>> if err:
        >>>     print("Failed to retrieve experiment details.")
        >>> else:
        >>>     print("Experiment Details:", experiment_details)  
        """
        if self.experiment_name == '':
            print("Experiment name not set for thiseExperiment. Cannot perform the operation for experiment without experiment name")
        
        path = f"/v1/model/get_experiment_by_name?experimentName={self.experiment_name}"
        resp = self.rpc.get(path=path)
        return self.handle_response(resp, f"Experiment Details Fetched successfully",
                                    "Could not fetch experiment details")

    def _get_experiment_by_id(self):
        pass # TODO: if required

    def add_models_for_training (self, models):
        """
        Add models to the list of models for training within the experiment.

        This method takes a list of model configurations and prepares them for training 
        by adding them to the experiment's training list.

        Parameters
        ----------
        models : list of dict
            A list of dictionaries, each containing the model configurations.

        Example
        -------
        >>> models = [
        >>>     {"model_key": "model_1", "is_autoML": True, "tuning_type": "grid",
        >>>      "model_checkpoint": "checkpoint_1", "checkpoint_type": "best",
        >>>      "id_model_info": "12345", "action_config": {}, "model_config": {},
        >>>      "model_name": "MyModel", "params_millions": 10.2}
        >>> ]
        >>> experiment.add_models_for_training(models)
        """
        for model in models:
            payload = {
                "modelKey": model['model_key'],
                "autoML": model['is_autoML'],
                "tuningType": model['tuning_type'],
                "modelCheckpoint": model['model_checkpoint'],
                "checkpointType": model['checkpoint_type'],
                "_idModelInfo": model['id_model_info'],
                "actionConfig": model['action_config'],
                "modelConfig": model['model_config'],
                "modelName": model['model_name'],
                "paramsMillions": model['params_millions'],
                                                            # TODO: make sure the self. inputs are in the correct format
                "experimentName": self.experiment_name,
                "modelInputs": self.model_inputs,
                "modelOutputs": self.model_outputs,
                "targetRuntime": self.target_runtime,
                "_idDataset": self.dataset_id,
                "datasetVersion": self.dataset_version,
                "_idExperiment": self.experiment_id,
                "primaryMetric": self.primary_metric,
                "datasetName": self.dataset_name,
            }
            self.models_for_training.append(payload)
    
    def list_models_for_training(self):
        """
        List all models that have been added for training within the experiment.

        Returns
        -------
        list of dict
            A list of model configurations that have been added for training.

        Example
        -------
        >>> models_for_training = experiment.list_models_for_training()
        >>> print(models_for_training)
        """
        return self.models_for_training
    
    def start_training(self):
        """
        Start the training of models for the experiment.

        This method sends the list of models to the backend to initiate training
        for the given project.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = experiment.start_training()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Training started: {resp}")
        """
        path = f"/v1/model/add_model_train_list?projectId={self.project_id}"
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=self.models_for_training)
        self.models_for_training = []
        return self.handle_response(resp, "Model training list added successfully",
                                    "An error occurred while adding model training list")
    
    def stop_training(self): # TODO : make sure this is realy stop_training
        """
        Stop the training process for the experiment.

        This method attempts to halt the ongoing training for the experiment by making
        a call to the backend to restrict further progress.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = experiment.stop_training()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Training stopped: {resp}")
        """
        path = f"/v1/model/restrict_experiment/{self.experiment_id}"
        resp = self.rpc.delete(path=path)
        return self.handle_response(resp, f"Experiment restricted successfully",
                                    "Could not restricte the experiment")
    
    def list_experiment_models(self):
        """
        List all models associated with the current experiment.

        This method fetches the list of models linked to the experiment by querying the backend.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = experiment.list_experiment_models()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Experiment models: {resp}")
        """
        path = f"/v1/model/get_models_by_experiment_id/{self.experiment_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(resp, f"Experiment models Fetched successfully",
                                    "Could not fetch experiment models")
    
    # TODO
    def get_best_model(self):
        pass 

    def update_experiment_status(self):
        pass
