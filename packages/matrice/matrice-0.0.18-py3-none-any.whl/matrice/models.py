import sys
import requests
from matrice.dataset import Dataset

class Model:
    """
    The `Model` class provides methods for interacting with models in a project,
    including fetching summaries, listing models, and performing evaluations.

    Parameters
    ----------
    session : Session
        A session object containing the project ID and RPC client.
    model_id : str, optional
        The unique identifier for the model (default is None).
    model_name : str, optional
        The name of the model (default is an empty string).

    Example
    -------
    >>> session = Session(project_id="project123")
    >>> model = Model(session, model_id="model789")
    """

    def __init__(self, session, model_id=None, model_name=''):
        self.session = session
        self.project_id = session.project_id
        self.model_id = model_id
        self.model_name = model_name
        self.rpc = session.rpc

    def handle_response(self, response, success_message, failure_message):
        """
        Handle API response and return a standardized tuple.

        Parameters
        ----------
        response : dict
            The response from the API call.
        success_message : str
            The message to return on success.
        failure_message : str
            The message to return on failure.

        Returns
        -------
        tuple
            A tuple containing the result, error message, and status message.

        Example
        -------
        >>> result, error, message = model.handle_response(response, "Success", "Failure")
        """
        if response.get("success"):
            result = response.get("data")
            error = None
            message = success_message
        else:
            result = None
            error = response.get("message")
            message = failure_message

        return result, error, message
    
    def get_details(self):
        """
        Get model details based on the provided ID or name.

        Returns
        -------
        tuple
            A tuple containing the model details, error message, and status message.

        Example
        -------
        >>> details, error, message = model.get_details()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model details: {details}")
        """
        id = self.model_id
        name = self.model_name

        if id:
            try:
                return self._get_model_train_by_id()
            except Exception as e:
                print(f"Error retrieving model train by id: {e}")
        elif name:
            try:
                return self._get_model_train_by_name()
            except Exception as e:
                print(f"Error retrieving model train by name: {e}")
        else:
            raise ValueError("At least one of 'model_id' or 'model_name' must be provided.")
        
    def check_for_duplicate(self, name):
        """
        Check if a trained model with the given name already exists.

        Parameters
        ----------
        name : str
            The name of the model to check for duplication.

        Returns
        -------
        tuple
            A tuple with the duplication check result, error message, and status message.

        Example
        -------
        >>> result, error, message = model.check_for_duplicate("MyModel")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Duplicate check result: {result}")
        """
        path = f"/v1/model/model_train/check_for_duplicate?modelTrainName={name}"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            if resp.get("data") == 'true':
                return self.handle_response(resp, "Model with this name already exists", "Could not check for this model name")
            else:
                return self.handle_response(resp, "Model with this name does not exist", "Could not check for this Model name")
        else:
            return self.handle_response(resp, "", "Could not check for this model name")

    def get_eval_result(self, dataset_id, dataset_version, split_type):
        """
        Fetch the evaluation result of a trained model using a specific dataset version and split type.

        Parameters
        ----------
        dataset_id : str
            The ID of the dataset.
        dataset_version : str
            The version of the dataset.
        split_type : str
            The type of split used for the evaluation.

        Returns
        -------
        tuple
            A tuple with the evaluation result, error message, and status message.

        Example
        -------
        >>> eval_result, error, message = model.get_eval_result("dataset123", "v1.0", "train")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Evaluation result: {eval_result}")
        """
        
        D = Dataset(self.session, dataset_id)
        dataset_info,_,_=D.get_processed_versions()
        if dataset_info is None:
            print("No datasets found")
            sys.exit(0)

        flag = False
        for data_info in dataset_info:
            if dataset_id == data_info["_id"]:
                if dataset_version in data_info["processedVersions"]:
                    flag = True
                    break
        
        if flag == False:
            print("Dataset or Dataset version does not exist. Can not use this dataset version to get/create a eval.")
            sys.exit(0)

        if self.model_id is None:
            print("Model Id is required for this operation")
            sys.exit(0)

        path = "/v1/model/get_eval_result"
        headers = {'Content-Type': 'application/json'}
        model_payload = {
            "_idDataset": dataset_id,
            "_idModel": self.model_id,
            "datasetVersion": dataset_version,
            "splitType": split_type
        }   
        resp = self.rpc.post(path=path, headers=headers, payload=model_payload)

        return self.handle_response(resp, "Eval result fetched successfully",
                                    "An error occurred while fetching Eval result")

    
    def plot_eval_results(self):
        """
        Plot the evaluation results for the model.

        Example
        -------
        >>> model.plot_eval_results()
        """
        import pandas as pd
        import matplotlib.pyplot as plt
        import seaborn as sns
        
        eval_result = self.get_eval_result(dataset_id = Dataset.get("dataset_id"), dataset_version = "v1.0", split_type = ["train", "val","test"])[0]
        df = pd.DataFrame(eval_result)
        # Set up the figure
        plt.figure(figsize=(14, 12))
        
        # List of unique metrics
        metrics = df['metricName'].unique()
        num_metrics = len(metrics)
        
        # Loop through each metric and create a horizontal bar plot
        for i, metric in enumerate(metrics, 1):
            plt.subplot((num_metrics + 1) // 2, 2, i)
            
            # Filter data for the current metric
            metric_data = df[df['metricName'] == metric]
            
            # Create horizontal bar plot
            sns.barplot(data=metric_data, x='metricValue', y='splitType', hue='category', orient='h')
            
            # Set titles and labels
            plt.xlabel(metric)
            plt.xlim(0, 1)  # Assuming metric values are between 0 and 1
            plt.legend(title='Category')
        
        plt.tight_layout()
        plt.show()
        
    def _get_model_train_by_id(self):
        """
        Fetch details of a specific trained model by its ID.

        Returns
        -------
        tuple
            A tuple with the model training data, error message, and status message.

        Example
        -------
        >>> model_data, error, message = model._get_model_train_by_id()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model data: {model_data}")
        """
        path = f"/v1/model/model_train/{self.model_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model train by ID fetched successfully",
                                    "Could not fetch model train by ID")
    
    def _get_model_train_by_name(self):
        """
        Fetch details of a specific trained model by its name.

        Returns
        -------
        tuple
            A tuple with the model training data, error message, and status message.

        Example
        -------
        >>> model_data, error, message = model._get_model_train_by_name()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model data: {model_data}")
        """
        if self.model_name == '':
            print("Model name not set for this Model train. Cannot perform the operation for Model without model name")
            sys.exit(0)
        path = f"/v1/model/model_train/get_model_train_by_name?modelTrainName={self.model_name}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model train by name fetched successfully",
                                    "Could not fetch model train by name")
    
    def add_model_eval(
        self,
        id_dataset,
        dataset_version,
        split_types,
        is_pruned=False,
        is_gpu_required=False,
    ):
        """
    Add a new model evaluation using specified parameters.

    Parameters
    ----------
    id_dataset : str
        The ID of the dataset.
    dataset_version : str
        The version of the dataset.
    split_types : list
        The split types used in the evaluation.
    is_pruned : bool, optional
        Whether the model is pruned (default is False).
    is_gpu_required : bool, optional
        Whether the model requires a GPU (default is False).

    Returns
    -------
    tuple
        A tuple with the evaluation result, error message, and status message.

    Example
    -------
    >>> result, error, message = model.add_model_eval(
    >>>     id_dataset="dataset123",
    >>>     dataset_version="v1.0",
    >>>     split_types=["train", "val"],
    >>> )
    """
        if self.model_id is None:
            print("Set Model Id for model object")
            sys.exit(0)

        model_by_id_resp, _, _ = self._get_model_train_by_id()
        path = "/v1/model/add_model_eval"
        headers = {'Content-Type': 'application/json'}
        model_payload = {
            "_idModel": self.model_id,
            "_idProject": self.project_id,
            "isOptimized": False,
            "isPruned": is_pruned,
            "runtimeFramework": "Pytorch",
            "_idDataset": id_dataset,
            "_idExperiment": model_by_id_resp["_idExperiment"],
            "datasetVersion": dataset_version,
            "gpuRequired": is_gpu_required,
            "splitTypes": split_types,
            "modelType": "trained",
            "exportFormat" : None
        }
        resp = self.rpc.post(path=path, headers=headers, payload=model_payload)

        return self.handle_response(resp, "Model eval added successfully",
                                    "An error occurred while adding model eval")

    def get_model_download_path(self, model_type):
        """
    Get the download path for the specified model type.

    Parameters
    ----------
    model_type : str
        The type of the model to download.

    Returns
    -------
    tuple
        A tuple with the download path, error message, and status message.

    Example
    -------
    >>> download_path, error, message = model.get_model_download_path("ONNX")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Download path: {download_path}")
    """
        if self.model_id is None:
            print("Model id not set for this model. Cannot perform the operation for model without model id")
            sys.exit(0)

        path = "/v1/model/get_model_download_path"
        headers = {'Content-Type': 'application/json'}
        model_payload = {
            "modelID": self.model_id,
            "modelType": model_type,
            "expiryTimeInMinutes": 15
        }  
        resp = self.rpc.post(path=path, headers=headers, payload=model_payload)

        return self.handle_response(resp, "Model download path fetched successfully and it will expire in 15 mins",
                                    "An error occured while downloading the model")

    def update_model_train_name(self, name):
        """
    Update the name of the trained model.

    Parameters
    ----------
    name : str
        The new name for the trained model.

    Returns
    -------
    tuple
        A tuple with the update result, error message, and status message.

    Example
    -------
    >>> result, error, message = model.update_model_train_name("NewModelName")
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Model name updated: {result}")
    """
        if self.model_id is None:
            print("Set Model Id for model object")
            sys.exit(0)
        
        path = f"/v1/model/{self.model_id}/update_modelTrain_name"
        headers = {'Content-Type': 'application/json'}
        model_payload = {"modelTrainId": self.model_id, "name": name}
        resp = self.rpc.put(path=path, headers=headers, payload=model_payload)

        return self.handle_response(resp, "Model train name updated successfully",
                                    "Could not update model train name")

    def delete_model_train(self):
        """
    Delete the trained model.

    Returns
    -------
    tuple
        A tuple with the deletion result, error message, and status message.

    Example
    -------
    >>> result, error, message = model.delete_model_train()
    >>> if error:
    >>>     print(f"Error: {error}")
    >>> else:
    >>>     print(f"Model deleted: {result}")
    """
        if self.model_id is None:
            print("Set Model Id for model object")
            sys.exit(0)
        path = f"/v1/model/delete_model_train/{self.model_id}"
        resp = self.rpc.delete(path=path)

        return self.handle_response(resp, "Model train deleted successfully",
                                    "Could not delete model train")
    
    def download_model(self, file_name):
        """
        Download the specified model type to a local file.

        Parameters
        ----------
        file_name : str
            The name of the file to save the downloaded model.

        Returns
        -------
        tuple
            A tuple with the download status, error message, and status message.

        Example
        -------
        >>> result, error, message = model.download_model("model.pt")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model downloaded: {result}")
        """
        
        presigned_url = self.rpc.post(path=f"/v1/model/get_model_download_path", payload={
                "modelID": self.model_id,
                "modelType": "trained",
                "expiryTimeInMinutes": 59
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
