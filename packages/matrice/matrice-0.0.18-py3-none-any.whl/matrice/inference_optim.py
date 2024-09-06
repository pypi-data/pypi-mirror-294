import sys
import requests

class ExportedModel: 
    """Class to handle model export-related operations within a project."""

    def __init__(self, session, model_export_id=None, model_export_name=''): 
        """
        The `ExportedModel` class provides methods for managing and optimizing model inferences,
        including fetching summaries, listing exported models, and performing evaluations.

        Parameters
        ----------
        session : Session
            A session object containing the project ID and RPC client.
        model_export_id : str, optional
            The unique identifier for the inference optimization (default is None).
        model_export_name : str, optional
            The name of the inference optimization (default is an empty string).

        Example
        -------
        >>> session = Session(account_number="account_number")
        >>> exported_model = ExportedModel(session=session_object, model_export_id="12345",model_export_name="sample_export")
        """
        self.project_id = session.project_id
        self.model_export_id = model_export_id
        self.model_export_name = model_export_name
        self.rpc = session.rpc

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
        Retrieve details of the model export based on the model export ID or name.

        This method fetches details by ID if available; otherwise, it attempts
        to fetch by name. Raises a ValueError if neither identifier is provided.

        Returns
        -------
        tuple
            A tuple containing the model export details, error message (if any), and a status message.

        Raises
        ------
        ValueError
            If neither 'model_export_id' nor 'model_export_name' is provided.

        Example
        -------
        >>> details, err, msg = exported_model.get_details()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Details: {details}")
        """
        id = self.model_export_id
        name = self.model_export_name

        if id:
            try:
                return self._get_model_export_by_id()
            except Exception as e:
                print(f"Error retrieving model_export by id: {e}")
        elif name:
            try:
                return self._get_model_export_by_name()
            except Exception as e:
                print(f"Error retrieving model_export by name: {e}")
        else:
            raise ValueError("At least one of 'model_export_id' or 'model_export_name' must be provided.")
        
    def _get_model_export_by_id(self):
        """
        Fetch details of a specific model export by its ID.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> details, err, msg = exported_model._get_model_export_by_id()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Details: {details}")
        """
        path = f"/v1/model/get_model_export_by_id?modelExportId={self.model_export_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model export by ID fetched successfully",
                                    "Could not fetch model export by ID")
    
    def _get_model_export_by_name(self):
        """
        Fetch details of a specific model export by its name.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> details, err, msg = exported_model._get_model_export_by_name()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Details: {details}")
        """
        if self.model_export_name == '':
            print("Model export name not set for this Model export. Cannot perform the operation for Model export without model export name.")
            sys.exit(0)
        path = f"/v1/model/model_export/get_model_export_by_name?modelExportName={self.model_export_name}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model export by name fetched successfully",
                                    "Could not fetch model export by name")
    
    def get_model_train_of_the_export(self):
        """
        Fetch details of a model training associated with a specific export ID.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> training_data, err, msg = exported_model.get_model_train_of_the_export()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Training Data: {training_data}")
        """
        path = f"/v1/model/get_model_train_by_export_id?exportId={self.model_export_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model train by export ID fetched successfully",
                                    "Could not fetch model train by export ID")


    def check_for_duplicate(self, name):
        """
        Check if a model export with the given name already exists.

        Parameters
        ----------
        name : str
            The name of the model export to check for duplication.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> is_duplicate, err, msg = exported_model.check_for_duplicate(name="ModelExportName")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Duplicate Check Result: {is_duplicate}")
        """
        path = f"/v1/model/model_export/check_for_duplicate?modelExportName={name}"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            if resp.get("data") == 'true':
                return self.handle_response(resp, "Model export with this name already exists", "Could not check for this model export name")
            else:
                return self.handle_response(resp, "Model export with this name does not exist", "Could not check for this model export name")
        else:
            return self.handle_response(resp, "", "Could not check for this model export name")
    
    # POST REQUESTS
    def add_model_eval(
        self,
        id_dataset,
        dataset_version,
        split_types,
        is_gpu_required = True,
        is_pruned = False,
    ):
        """
        Add a new model evaluation using specified parameters.

        Parameters
        ----------
        is_pruned : bool
            Whether the model is pruned.
        id_dataset : str
            The ID of the dataset used for evaluation.
        id_experiment : str
            The ID of the experiment associated with the model.
        dataset_version : str
            The version of the dataset.
        is_gpu_required : bool
            Whether the model requires GPU for inference.
        split_types : list
            A list of split types used in the evaluation.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> eval_result, err, msg = exported_model.add_model_eval(
                is_pruned=False,
                id_dataset="dataset123", id_experiment="experiment123", dataset_version="v1.0",
                is_gpu_required=True, split_types=["train", "test"])
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Evaluation added: {eval_result}")
        """
        model_info = self.get_details()[0]['data']
        runtime_framework = model_info['exportFormat']
        model_train_info = self.get_model_train_of_the_export()[0]['data']

        path = "/v1/model/add_model_eval"
        headers = {'Content-Type': 'application/json'}
        model_payload = {
            "_idModel": self.model_export_id,
            "_idProject": self.project_id,
            "isOptimized": True,
            "isPruned": is_pruned,
            "runtimeFramework": runtime_framework,
            "_idDataset": id_dataset,
            "_idExperiment": model_train_info['_idExperiment'],
            "datasetVersion": dataset_version,
            "gpuRequired": is_gpu_required,
            "splitTypes": split_types,
            "modelType": "exported",
            "computeAlias" : "" 
        }
        resp = self.rpc.post(path=path, headers=headers, payload=model_payload)

        return self.handle_response(resp, "Model eval added successfully",
                                    "An error occurred while adding model eval")
    def get_eval_result(self, dataset_id, dataset_version, split_type):
        """
        Fetch the evaluation result of a trained model using a specific dataset version and split type.

        Parameters
        ----------
        dataset_id : str
            The ID of the dataset.
        dataset_version : str
            The version of the dataset.
        split_type : list
            The types of splits used for the evaluation.

        Returns
        -------
        tuple
            A tuple with the evaluation result, error message, and status message.

        Example
        -------
        >>> eval_result, error, message = model.get_eval_result("dataset123", "v1.0", ["train"])
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Evaluation result: {eval_result}")
        """

        path = "/v1/model/get_eval_result"
        headers = {'Content-Type': 'application/json'}
        model_payload = {
            "_idDataset": dataset_id,
            "_idModel": self.model_export_id,
            "datasetVersion": dataset_version,
            "splitType": split_type
        }   
        resp = self.rpc.post(path=path, headers=headers, payload=model_payload)

        return self.handle_response(resp, "Eval result fetched successfully",
                                    "An error occurred while fetching Eval result")
    # PUT REQUEST
    def update_model_export_name(self, updated_name):
        """
        Update the name of a model export.

        Parameters
        ----------
        updated_name : str
            The new name for the model export.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> result, err, msg = exported_model.update_model_export_name("NewModelExportName")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Name Updated: {result}")
        """
        body = {
            "modelExportId": self.model_export_id,
            "name": updated_name,
            }
        
        headers = {"Content-Type": "application/json"}
        path = f"/v1/model/{self.model_export_id}/update_modelExport_name"
        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return self.handle_response(resp, f"Model export name updated to {updated_name}",
                                    "Could not update the model export name")
    
    # DELETE REQUEST
    def delete_model_export(self):
        """
        Delete a model export.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> result, err, msg = exported_model.delete_model_export()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Model Export Deleted: {result}")
        """
        path = f"/v1/model/model_export/{self.model_export_id}"
        resp = self.rpc.delete(path=path)

        return self.handle_response(resp, f"Model export deleted",
                                    "Could not delete the model export")

    def download_model(self, file_name):
        """
        Download the specified model type to a local file.

        Parameters
        ----------
        model_type : str
            The type of the model to download.
        file_name : str
            The name of the file to save the downloaded model.

        Returns
        -------
        tuple
            A tuple with the download status, error message, and status message.

        Example
        -------
        >>> result, error, message = model.download_model("model.onnx")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model downloaded: {result}")
        """
        
        model_info = self.get_details()[0]['data']
        runtime_framework = model_info['exportFormat']
        if type(runtime_framework) == list:
            runtime_framework = runtime_framework[0]
            
        presigned_url = self.rpc.post(path=f"/v1/model/get_model_download_path", payload={
            "modelID": self.model_export_id,
            "modelType": "exported",
            "expiryTimeInMinutes": 59,
            "exportFormat": runtime_framework,
        })['data']

        response = requests.get(presigned_url)

        if response.status_code == 200:
            with open(file_name, 'wb') as file:
                file.write(response.content)
            print("Model downloaded successfully")
            return file_name
        else:
            print(f"Model download failed with status code: {response.status_code}")
            return ""