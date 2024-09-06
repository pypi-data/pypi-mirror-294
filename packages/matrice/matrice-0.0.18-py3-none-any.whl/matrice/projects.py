"""Module for interacting with backend API to manage projects."""

import sys
from matrice.dataset import Dataset
from matrice.annotation import Annotation
from matrice.deployment import Deployment
from matrice.experiment import Experiment
from matrice.models import Model
from matrice.inference_optim import ExportedModel
from matrice.model_store import ModelStore
from matrice.action import Action


class Projects:
    """
    A class for handling project-related operations using the backend API.

    Attributes
    ----------
    session : Session
        The session object used for API interactions.
    account_number : str
        The account number associated with the session.
    project_name : str
        The name of the project.
    project_id : str
        The ID of the project (initialized in the constructor).
    project_input : str
        The input type for the project (initialized in the constructor).
    output_type : str
        The output type for the project (initialized in the constructor).

    Parameters
    ----------
    session : Session
        The session object used for API interactions.
    project_name : str
        The name of the project.
    """

    def __init__(self, session, project_name):
        """
        Initialize a Projects object with project details.

        Parameters
        ----------
        session : Session
            The session object used for API interactions.
        project_name : str
            The name of the project.
        """
        self.session = session
        self.account_number = session.account_number
        self.project_name = project_name
        self.rpc = session.rpc
        project_info, error, message = self._get_project_by_name()
        if error:
            print(f"Error fetching project info: {message}")
        else:
            self.project_id = project_info["data"]["_id"]
            self.project_input = project_info["data"]["inputType"]
            self.output_type = project_info["data"]["outputType"]

    def handle_response(self, resp, success_message, error_message):
        """
        Handle the API response.

        Parameters
        ----------
        resp : dict
            The response dictionary from the API.
        success_message : str
            The message to return if the response indicates success.
        error_message : str
            The message to return if the response indicates an error.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> resp = {"success": True}
        >>> result, error, message = project.handle_response(resp, "Operation successful", "Operation failed")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        if resp.get("success"):
            error = None
            message = success_message
        else:
            error = resp.get("message")
            message = error_message
        return resp, error, message
    
    def _get_service_and_action_ids(self, resp, error, message):
        """
        Extract service and action IDs from the response.

        Parameters
        ----------
        resp : dict
            The response dictionary from the API.
        error : str
            An error message if extraction fails.

        Returns
        -------
        tuple
            A tuple containing:
            - The service ID if extraction is successful, or None if it fails.
            - The action ID if extraction is successful, or None if it fails.
            - An error message if extraction fails, or None if successful.

        Example
        -------
        >>> resp = {"data": {"service_id": "123", "action_id": "456"}}
        >>> service_id, action_id, error = project._get_service_and_action_ids(resp, None)
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Service ID: {service_id}, Action ID: {action_id}")
        """
        if error:
            print(message, error)
            return None, None
        data = resp['data']
        print(data)
        return  data['_id'] , data['_idAction']
    
    def _job_cost_estimate(self, data):
        pass #TODO
    
    def _get_project_by_name(self):
        """
        Fetch project details by project name.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project._get_project_by_name()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        path = f"/v1/project/get_project_by_name?name={self.project_name}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp, "Project details Fetched Successfully", "Could not fetch project details"
        )
    
    def _get_a_project_by_id(self):
        """
        Fetch project information by project ID.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project._get_a_project_by_id()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        path = f"/v1/project/{self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp,
            f"Project info fetched for project with id {self.project_id}",
            f"Could not fetch project info for project with id {self.project_id}",
        )
    
    def get_service_action_logs(self, service_id):
        """
        Fetch action logs for a specific service.

        Parameters
        ----------
        service_id : str
            The ID of the service for which to fetch action logs.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project.get_service_action_logs("service123")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """

        # User can fetch service id using the get method of respective
        # services, eg - to get logs of dataset use get_dataset method
        path = f"/v1/project/service/{service_id}/logs?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp, "Action logs fected succesfully", "Could not fetch action logs"
        )

    def action_logs_from_action_account_number(self, account_number):
        """
        Fetch action logs for a specific action account number.

        Parameters
        ----------
        account_number : str
            The account number associated with the action logs.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project.action_logs_from_action_account_number("account123")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        path = f"/v1/project/actions/action_records/{account_number}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp, "Action logs fected succesfully", "Could not fetch action logs"
        )
    
    def get_latest_action_record(self, service_id):
        """
        Fetch the latest action logs for a specific service ID.

        Parameters
        ----------
        service_id : str
            The ID of the service for which to fetch the latest action logs.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project.get_latest_action_record("service123")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """

        path = f"/v1/project/get_latest_action_record/{service_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp, "Action logs fected succesfully", "Could not fetch action logs"
        )

    def check_for_duplicate(self, name):
        """
        Check if a project with the specified name already exists.

        Parameters
        ----------
        name : str
            The name of the project to check for duplication.

        Returns
        -------
        tuple
            A tuple containing:
            - The response dictionary from the API.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> result, error, message = project.check_for_duplicate("ProjectName")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Status: {message}")
        """
        path = f"/v1/project/check_for_duplicate?name={name}"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            if resp.get("data") == 'true':
                return self.handle_response(resp, "Project with this name already exists", "Could not check for this Project name")
            else:
                return self.handle_response(resp, "Project with this name does not exist", "Could not check for this Project name")
        else:
            return self.handle_response(resp, "", "Could not check for this Project name")

    # POST REQUESTS
    def create_dataset(
        self,
        dataset_name,
        source,
        cloud_provider,
        dataset_type,
        input_type,
        source_url="",
        file_path="",
        credential_alias="",
        bucket_alias="",
        compute_alias="",
        dataset_description="",
        version_description="",
        source_credential_alias="",
        bucket_alias_service_provider="auto",
    ):
        """
        Create a new dataset.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.
        source : str
            The source of the dataset.
        cloud_provider : str
            The cloud provider for the dataset.
        dataset_type : str
            The type of the dataset.
        input_type : str
            The input type for the dataset.
        source_url : str, optional
            The URL of the source (default is an empty string).
        file_path : str, optional
            The path to the file if the source is local (default is an empty string).
        credential_alias : str, optional
            The credential alias for accessing the dataset (default is an empty string).
        bucket_alias : str, optional
            The bucket alias for the dataset (default is an empty string).
        compute_alias : str, optional
            The compute alias (default is an empty string).
        dataset_description : str, optional
            A description of the dataset (default is an empty string).
        version_description : str, optional
            A description of the dataset version (default is an empty string).
        source_credential_alias : str, optional
            The source credential alias (default is an empty string).
        bucket_alias_service_provider : str, optional
            The bucket alias service provider (default is "auto").

        Returns
        -------
        tuple
            A tuple containing:
            - A `Dataset` object for the created dataset.
            - An `Action` object related to the dataset creation process.

        Example
        -------
        >>> dataset, action = project.create_dataset("MyDataset", "local", "", "image", "image", file_path="data.csv")
        >>> if action:
        >>>     print(f"Dataset created: {dataset}")
        >>> else:
        >>>     print(f"Error: {dataset}")
        """
        dataset = Dataset(self)
        if source == "lu":
            response = dataset.upload_file(file_path)
            if response['success']:
                source_url = response['data']
            else:
                return response['data'], "error in uploading file", response['message']
        
        dataset_size, err, msg = dataset.get_dataset_size(source_url)
        if err:
            dataset_size = 0
        path = f"/v1/dataset?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "name": dataset_name,
            "isUnlabeled": False,
            "source": source,
            "sourceUrl": source_url,
            "cloudProvider": cloud_provider,
            "isCreateNew": True,
            "oldDatasetVersion": None,
            "newDatasetVersion": "v1.0",
            "datasetDescription": dataset_description,
            "description": dataset_description,
            "newVersionDescription": version_description,
            "isPublic": False,
            "computeAlias": compute_alias,
            "datasetSize": dataset_size,
            "bucketAliasServiceProvider": bucket_alias_service_provider,
            "_idProject": self.project_id,
            "type": dataset_type,
            "sourceCredentialAlias": source_credential_alias,
            "credentialAlias": credential_alias,
            "bucketAlias": bucket_alias,
            "inputType": input_type
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        resp, error, message = self.handle_response(resp, "Dataset creation in progress",
                                                    "An error occurred while trying to create new dataset")
        service_id, action_id = self._get_service_and_action_ids(resp, error, message)
        return Dataset(self.session, service_id), Action(self.session, action_id)
    
    # TODO : test dataset creates and check what cloud_provider, dataset_type should be in "lu"
    def upload_local_dataset(
        self,
        dataset_name,
        file_path,
        dataset_type,
        source = "lu",
        dataset_description="",
        version_description="",
        input_type="image",
        credential_alias="",
        bucket_alias="",
        compute_alias="",
        source_credential_alias="",
        bucket_alias_service_provider="auto",
    ):
        """
        Upload a local dataset.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.
        file_path : str
            The path to the local file.
        dataset_type : str
            The type of the dataset.
        source : str, optional
            The source of the dataset (default is "lu").
        dataset_description : str, optional
            A description of the dataset (default is an empty string).
        version_description : str, optional
            A description of the dataset version (default is an empty string).
        input_type : str, optional
            The input type for the dataset (default is "image").
        credential_alias : str, optional
            The credential alias for accessing the dataset (default is an empty string).
        bucket_alias : str, optional
            The bucket alias for the dataset (default is an empty string).
        compute_alias : str, optional
            The compute alias (default is an empty string).
        source_credential_alias : str, optional
            The source credential alias (default is an empty string).
        bucket_alias_service_provider : str, optional
            The bucket alias service provider (default is "auto").

        Returns
        -------
        tuple
            A tuple containing:
            - A `Dataset` object for the created dataset.
            - An `Action` object related to the dataset upload process.

        Example
        -------
        >>> dataset, action = project.upload_local_dataset("MyLocalDataset", "path/to/data.csv", "image")
        >>> if action:
        >>>     print(f"Dataset uploaded: {dataset}")
        >>> else:
        >>>     print(f"Error: {dataset}")
        """

        return self.create_dataset(
            dataset_name=dataset_name,
            source=source,
            cloud_provider="",
            dataset_type=dataset_type,
            input_type=input_type,
            file_path=file_path,
            dataset_description=dataset_description,
            version_description=version_description,
            credential_alias=credential_alias,
            bucket_alias=bucket_alias,
            compute_alias=compute_alias,
            source_credential_alias=source_credential_alias,
            bucket_alias_service_provider=bucket_alias_service_provider
        )

    def upload_cloud_dataset(
        self,
        dataset_name,
        source,
        source_url,
        cloud_provider,
        dataset_type,
        input_type="image",
        dataset_description="",
        version_description="",
        credential_alias="",
        bucket_alias="",
        compute_alias="",
        source_credential_alias="",
        bucket_alias_service_provider="auto",
    ):
        """
        Upload a cloud dataset.

        Parameters
        ----------
        dataset_name : str
            The name of the dataset.
        source : str
            The source of the dataset.
        source_url : str
            The URL of the source.
        cloud_provider : str
            The cloud provider for the dataset.
        dataset_type : str
            The type of the dataset.
        input_type : str, optional
            The input type for the dataset (default is "image").
        dataset_description : str, optional
            A description of the dataset (default is an empty string).
        version_description : str, optional
            A description of the dataset version (default is an empty string).
        credential_alias : str, optional
            The credential alias for accessing the dataset (default is an empty string).
        bucket_alias : str, optional
            The bucket alias for the dataset (default is an empty string).
        compute_alias : str, optional
            The compute alias (default is an empty string).
        source_credential_alias : str, optional
            The source credential alias (default is an empty string).
        bucket_alias_service_provider : str, optional
            The bucket alias service provider (default is "auto").

        Returns
        -------
        tuple
            A tuple containing:
            - A `Dataset` object for the created dataset.
            - An `Action` object related to the dataset upload process.

        Example
        -------
        >>> dataset, action = project.upload_cloud_dataset("MyCloudDataset", "cloud_source", "http://source.url", "AWS", "image")
        >>> if action:
        >>>     print(f"Dataset uploaded: {dataset}")
        >>> else:
        >>>     print(f"Error: {dataset}")
        """

        return self.create_dataset(
            dataset_name=dataset_name,
            source=source,
            cloud_provider=cloud_provider,
            dataset_type=dataset_type,
            input_type=input_type,
            source_url=source_url,
            dataset_description=dataset_description,
            version_description=version_description,
            credential_alias=credential_alias,
            bucket_alias=bucket_alias,
            compute_alias=compute_alias,
            source_credential_alias=source_credential_alias,
            bucket_alias_service_provider=bucket_alias_service_provider
        )
    
    def create_annotation(
            self,
            project_type,
            ann_title,
            dataset_id,
            dataset_version,
            labels,
            only_unlabeled,
            is_ML_assisted,
            labellers,
            reviewers,
            guidelines):
        """
        Create a new annotation for a dataset.

        Parameters
        ----------
        project_type : str
            The type of the project for which the annotation is being created.
        ann_title : str
            The title of the annotation.
        dataset_id : str
            The ID of the dataset to annotate.
        dataset_version : str
            The version of the dataset.
        labels : list
            The list of labels for the annotation.
        only_unlabeled : bool
            Whether to annotate only unlabeled data.
        is_ML_assisted : bool
            Whether the annotation is ML-assisted.
        labellers : list
            The list of labellers for the annotation.
        reviewers : list
            The list of reviewers for the annotation.
        guidelines : str
            The guidelines for the annotation.

        Returns
        -------
        tuple
            A tuple containing:
            - An `Annotation` object for the created annotation.
            - An `Action` object related to the annotation creation process.

        Example
        -------
        >>> annotation, action = project.create_annotation("object_detection", "MyAnnotation", "dataset123", "v1.0", ["label1", "label2"], True, False, ["labeller1"], ["reviewer1"], "Follow these guidelines")
        >>> if action:
        >>>     print(f"Annotation created: {annotation}")
        >>> else:
        >>>     print(f"Error: {annotation}")
        """
        path=f"/v1/annotations?projectId={self.project_id}&projectType={project_type}"
        payload={
            "title":ann_title,
            "_idDataset":dataset_id,
            "datasetVersion":dataset_version,
            "labels":labels,
            "onlyUnlabeled":only_unlabeled,
            "isMLAssisted":is_ML_assisted,
            "labellers":labellers,  
            "reviewers":reviewers,
            "guidelines":guidelines,
            "type":project_type,
            "modelType": "",
            "modelId": ""
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=payload)

        resp, error, message = self.handle_response(resp, "Annotation creation in progress",
                                                    "An error occurred while trying to create new annotation")
        service_id, action_id = self._get_service_and_action_ids(resp, error, message)
        return Annotation(self.session, dataset_id, service_id), Action(self.session, action_id)
    
    def create_experiment(
        self,
        name,
        dataset_id,
        target_run_time,
        dataset_version,
        primary_metric,
        matrice_compute = True,
        models_trained=[],
        performance_trade_off=-1,
    ):
        """
        Create a new experiment for model training.

        Parameters
        ----------
        name : str
            The name of the experiment.
        dataset_id : str
            The ID of the dataset to be used in the experiment.
        target_run_time : str
            The target runtime for the experiment.
        dataset_version : str
            The version of the dataset.
        primary_metric : str
            The primary metric to evaluate the experiment.
        matrice_compute : bool, optional
            Flag to indicate whether to use matrix compute (default is True).
        models_trained : list, optional
            List of models that have been trained in the experiment (default is an empty list).
        performance_trade_off : float, optional
            The performance trade-off for the experiment (default is -1).

        Returns
        -------
        tuple
            A tuple containing:
            - An `Experiment` object for the created experiment.
            - An error message if the response indicates an error, or None if successful.
            - A status message describing the result of the operation.

        Example
        -------
        >>> experiment, error, message = project.create_experiment("Experiment1", "dataset123", "runtimeA", "v1.0", "accuracy")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Experiment created: {experiment}")
        """
        dataset = Dataset(self.session, dataset_id = dataset_id)
        model_store = ModelStore(self.session)

        project_info, _, _ = self._get_a_project_by_id()
        if project_info is None:
            print("No project found.")
            return None, "No project found.", None

        dataset_info, _, _ = dataset.get_processed_versions()
        print(dataset_info)
        if dataset_info is None:
            print("No datasets found")
            return None, "No datasets found", None

        model_information = ''
        for data_info in dataset_info:
            if dataset_id == data_info["_id"]:
                if dataset_version in data_info["processedVersions"]:
                    model_information = data_info
                    break

        if model_information == '':
            print("Dataset or Dataset version does not exist. Cannot use this dataset version to create a model.")
            return None, "Dataset or Dataset version does not exist.", None

        model_inputs = [project_info["data"]["inputType"]]
        model_outputs = [project_info["data"]["outputType"]]

        runtime_metrics, _, _ = model_store.fetch_supported_runtimes_metrics(model_inputs, model_outputs, self.project_id)

        if runtime_metrics is None:
            print("No primary metric and target runtime found.")
            return None, "No primary metric and target runtime found.", None

        if target_run_time not in runtime_metrics["data"]["supportedRuntimes"]:
            print("Target runtime provided does not exist.")
            return None, "Target runtime provided does not exist.", None

        if primary_metric not in runtime_metrics["data"]["supportedMetrics"]:
            print("Primary metric not available in the existing runtime Metrics.")
            return None, "Primary metric not available in the existing runtime Metrics.", None

        path = f"/v1/model/create_experiment?projectId={self.project_id}"
        headers = {'Content-Type': 'application/json'}

        if matrice_compute == False:
            model_payload = {
                "experimentName": name,
                "_idProject": self.project_id,
                "matriceCompute": matrice_compute
            }
        else:
            model_payload = {
                "experimentName": name,
                "_idDataset": dataset_id,
                "_idProject": self.project_id,
                "modelInputs": [project_info["data"]["inputType"]],
                "modelOutputs": [project_info["data"]["outputType"]],
                "targetRuntime": [target_run_time],
                "datasetVersion": dataset_version,
                "performanceTradeoff": performance_trade_off,
                "primaryMetric": primary_metric,
                "modelsTrained": models_trained,
                "matriceCompute": matrice_compute,
                "baseModelStoragePath": "",
                "storageCloudCredentials": []
            }

        resp = self.rpc.post(path=path, headers=headers, payload=model_payload)

        resp, error, message = self.handle_response(resp, "Experiment creation success",
                                                    "An error occurred while trying to create new experiment")
        if error:
            print(message, error)
            return None, None
        data = resp['data']
        print(data)
        exp_id =  data['_id'] 
        exp_name = data['experimentName']
    
        return Experiment(self.session, exp_id , exp_name )
    

    def add_model_export(
        self,
        model_train_id,
        export_formats,
        model_config,
        is_gpu_required=False
    ):
        """
        Add export configurations to a trained model.

        Parameters
        ----------
        model_train_id : str
            The ID of the trained model.
        export_formats : list
            The list of formats to export the model.
        model_config : dict
            The configuration settings for the model export.
        is_gpu_required : bool, optional
            Flag to indicate if GPU is required for the export (default is False).

        Returns
        -------
        tuple
            A tuple containing:
            - An `InferenceOptimization` object related to the model export.
            - An `Action` object related to the export process.

        Example
        -------
        >>> inference_opt, action = project.add_model_export("model123", ["format1", "format2"], {"configKey": "configValue"}, is_gpu_required=True)
        >>> if action:
        >>>     print(f"Model export added: {inference_opt}")
        >>> else:
        >>>     print(f"Error: {inference_opt}")
        """
        # Ensure export_formats is a list
        if not isinstance(export_formats, list):
            export_formats = [export_formats]

        M = Model(session=self.session, model_id=model_train_id)
        model_train_id_resp, _, _ = M._get_model_train_by_id()
        if model_train_id_resp["createdAt"] == '0001-01-01T00:00:00Z':
            print("No model exists with the given model train id")
            sys.exit(0)

        path = f"/v1/model/{model_train_id}/add_model_export?projectId={self.project_id}"
        headers = {'Content-Type': 'application/json'}
        model_payload = {
            "_idProject": self.project_id,
            "_idModelTrain": model_train_id,
            "modelName": model_train_id_resp["modelName"],
            "modelInputs": model_train_id_resp["modelInputs"],
            "_idModelInfo": model_train_id_resp["_idModelInfo"],
            "modelOutputs": model_train_id_resp["modelOutputs"],
            "exportFormats": export_formats,
            "_idDataset": model_train_id_resp["_idDataset"],
            "datasetVersion": model_train_id_resp["datasetVersion"],
            "gpuRequired": is_gpu_required,
            "actionConfig": model_train_id_resp["actionConfig"],
            "modelConfig": model_config,
        }

        resp = self.rpc.post(path=path, headers=headers, payload=model_payload)
        resp, error, message = self.handle_response(resp, "Model Export added successfully",
                                                    "An error occurred while adding model export")
        service_id, action_id = self._get_service_and_action_ids(resp, error, message)
        return ExportedModel(self.session, service_id), Action(self.session, action_id)
    
    def create_deployment(
        self,
        deployment_name,
        model_id,
        gpu_required=True,
        auto_scale=False,
        auto_shutdown=True,
        shutdown_threshold=5,
        image_store_confidence_threshold=0.9,
        image_store_count_threshold=50,
        bucket_alias = "",
        compute_alias = "",
        credential_alias = "",
        model_type = "trained",
        runtime_framework = "Pytorch"
    ):
        """
        Create a deployment for a model.
    
        Parameters
        ----------
        deployment_name : str
            The name of the deployment.
        model_id : str
            The ID of the model to be deployed.
        gpu_required : bool, optional
            Flag to indicate if GPU is required for the deployment (default is True).
        auto_scale : bool, optional
            Flag to indicate if auto-scaling is enabled (default is False).
        auto_shutdown : bool, optional
            Flag to indicate if auto-shutdown is enabled (default is True).
        shutdown_threshold : int, optional
            The threshold for auto-shutdown (default is 5).
        image_store_confidence_threshold : float, optional
            The confidence threshold for image store (default is 0.9).
        image_store_count_threshold : int, optional
            The count threshold for image store (default is 50).
        bucket_alias : str, optional
            The alias for the bucket (default is an empty string).
        compute_alias : str, optional
            The alias for the compute (default is an empty string).
        credential_alias : str, optional
            The alias for the credential (default is an empty string).
    
        Returns
        -------
        tuple
            A tuple containing:
            - A `Deployment` object for the created deployment.
            - An `Action` object related to the deployment process.
    
        Example
        -------
        >>> deployment, action = project.create_deployment("Deployment1", "model123", auto_scale=True)
        >>> if action:
        >>>     print(f"Deployment created: {deployment}")
        >>> else:
        >>>     print(f"Error: {deployment}")
        """
        if model_type == "trained":
            model = Model(self.session, model_id=model_id)
            model_info = model.get_details()[0]
        elif model_type == "exported":
            model = ExportedModel(self.session, model_export_id=model_id)
            model_info = model.get_details()[0]['data']
            runtime_framework = model_info['exportFormat']
    
        body = {
            "deploymentName": deployment_name,
            "_idModel": model_id,
            "runtimeFramework": runtime_framework,
            "deploymentType": "regular",
            "modelType": model_type,
            "modelInput": model_info["modelInputs"][0],
            "modelOutput": model_info["modelOutputs"][0],
            "autoShutdown": auto_shutdown,
            "autoScale": auto_scale,
            "gpuRequired": gpu_required,
            "shutdownThreshold": shutdown_threshold,
            "imageStoreConfidenceThreshold": image_store_confidence_threshold,
            "imageStoreCountThreshold": image_store_count_threshold,
            "bucketAlias": bucket_alias,
            "computeAlias": compute_alias,
            "credentialAlias": credential_alias
        }
    
        headers = {'Content-Type': 'application/json'}
        path = f"/v1/deployment?projectId={self.project_id}"
    
        resp = self.rpc.post(path=path, headers=headers, payload=body)
    
        resp, error, message = self.handle_response(resp, "Deployment created successfully.",
                                                    "An error occurred while trying to create deployment.")
        service_id, action_id = self._get_service_and_action_ids(resp, error, message)
        return Deployment(self.session, service_id), Action(self.session, action_id)
    
    def delete_project(self):
        """
        Delete a project by project ID.

        Returns
        -------
        tuple
            A tuple containing:
            - A success message if the project is deleted successfully.
            - An error message if the deletion fails.

        Example
        -------
        >>> success_message, error = project.delete_project()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(success_message)
        """
        _, error, _ = self._get_a_project_by_id()
        if error:
            print("Project is not found")
            sys.exit(1)
        
        path = f"/v1/project/delete_project/{self.project_id}"
        resp = self.rpc.delete(path=path)
        return self.handle_response(
            resp,
            "Project deleted successfully",
            "An error occurred while trying to delete project",
        )
    
    def enable_disable_project(self,type):
        """
        Enable or disable a project.

        Parameters
        ----------
        type : str
            The type of action to perform: "enable" or "disable".

        Returns
        -------
        tuple
            A tuple containing:
            - A success message if the project is enabled or disabled successfully.
            - An error message if the action fails.

        Example
        -------
        >>> success_message, error = project.enable_disable_project("enable")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(success_message)
        """

        _, error, _ = self._get_a_project_by_id()
        if error:
            print("Project is not found")
            sys.exit(1)

        path = f"/v1/project/enable-disable-project/{type}/{self.project_id}"
        resp = self.rpc.put(path=path)

        return self.handle_response(
            resp,
            f"Project {self.project_id} {type}d successfully",
            f"Could not {type} project {self.project_id}",
        )
    
    def get_running_instances(self):
        """
        Fetch the number of running instances.

        Returns
        -------
        tuple
            A tuple containing:
            - The number of running instances if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> instances, error = project.get_running_instances()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Running instances: {instances}")
        """
        path = f"/v1/project/running_instances/{self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp,
            "Running instances fetched successfully",
            "Could not fetch running instances",
        )
    
        
    def get_actions_logs_for_action(self, action_id):
        """
        Fetch action logs for a specific action.

        Parameters
        ----------
        action_id : str
            The ID of the action for which logs are to be fetched.

        Returns
        -------
        tuple
            A tuple containing:
            - The action logs if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> logs, error = project.get_actions_logs_for_action("action123")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Action logs: {logs}")
        """
        path = f"/v1/project/action_logs_from_record_id/{action_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp,
            "Action logs fected succesfully",
            "Could not fetch action logs",
        )
    
    def list_deployments(self):
        """
        List all deployments inside the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of deployments if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> deployments, error = project.list_deployments()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Deployments: {deployments}")
        """
        path = f"/v1/deployment/list_deployments?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
                    resp,
                    "Deployment list fetched successfully",
                    "An error occurred while trying to fetch deployment list.",
                ) 
    
    def list_datasets(self):
        """
        List all datasets in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of datasets if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> datasets, error = project.list_datasets()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Datasets: {datasets}")
        """
        path = f"/v1/dataset?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Dataset list fetched successfully",
                                    "Could not fetch dataset list")

    def list_complete_dataset(self):
        """
        List all completed datasets in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of completed datasets if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> completed_datasets, error = project.list_complete_dataset()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Completed datasets: {completed_datasets}")
        """
        path = f"/v1/dataset/complete?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Completed dataset list fetched successfully",
                                    "Could not fetch completed dataset list")
    def list_annotations(self):
        """
        List all annotations in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of annotations if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> annotations, error = project.list_annotations()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Annotations: {annotations}")
        """
        path=f"/v1/annotations?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Annotations fetched successfully",
                                    "Could not fetch annotations")

    def list_experiments(self):
        """
        List all experiments in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of experiments if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> experiments, error = project.list_experiments()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Experiments: {experiments}")
        """
        path = f"/v1/model/get_experiments?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Experiments summary fetched successfully",
            "An error occurred while trying to fetch experiments summary.",
        )
    
    def list_completed_model_train(self):
        """
        List all completed trained models in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of completed trained models if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> completed_models, error = project.list_completed_model_train()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Completed models: {completed_models}")
        """
        path = f"/v1/model/model_train_completed?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model train list fetched successfully",
                                    "Could not fetch models train list")

    def list_model_train_paginated(self):
        """
        List model training sessions in the project with pagination.

        Returns
        -------
        tuple
            A tuple containing:
            - A paginated list of model training sessions if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> model_train_sessions, error = project.list_model_train_paginated()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model training sessions: {model_train_sessions}")
        """
        path = f"/v1/model/model_train?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model train list fetched successfully",
                                    "Could not fetch models train list")

        
    def list_exported_models(self):
        """
        List all exported models in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - A list of exported models if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> exported_models, error = project.list_exported_models()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Exported models: {exported_models}")
        """
        path = f"/v1/model/model_exported?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Models exported list fetched successfully",
                                    "Could not fetch models exported list")
    
    def get_model_exports(self):       # TODO: check if this is list or get for summary
        """
        Fetch all model exports for the project.

        Returns
        -------
        tuple
            A tuple containing:
            - The model export data if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> model_exports, error = project.get_model_exports()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model exports: {model_exports}")
        """
        path = f"/v1/model/get_model_exports?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model exports fetched successfully",
                                    "Could not fetch model exports")
    
    def get_annotations_summary(self):
        """
        Fetch a summary of annotations in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - The annotation summary if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> annotation_summary, error = project.get_annotations_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Annotation summary: {annotation_summary}")
        """
        path=f"/v1/annotations/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Annotation summary fetched successfully",
                                    "Could not fetch annotation summary")
    
    def get_models_summary(self):
        """
        Fetch a summary of all models in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - The model summary data if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> model_summary, error = project.get_models_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Model summary: {model_summary}")
        """
        path = f"/v1/model/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model Summary fetched successfully",
                                    "Could not fetch models summary")
    def get_exports_summary(self):
        """
        Fetch a summary of all model exports in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - The export summary data if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> export_summary, error = project.get_exports_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Export summary: {export_summary}")
        """
        path = f"/v1/model/summaryExported?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Model Export Summary fetched successfully",
                                    "Could not fetch models export summary")
    
    def get_deployments_summary(self):
        """
        Fetch a summary of all deployments in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - The deployment summary data if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> deployment_summary, error = project.get_deployments_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Deployment summary: {deployment_summary}")
        """
        path = f"/v1/deployment/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp,
            "Deployment summary fetched successfully",
            "An error occurred while trying to fetch deployment summary.",
        )

    def get_experiments_summary(self):
        """
        Fetch a summary of all experiments in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - The experiments summary data if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> experiments_summary, error = project.get_experiments_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Experiments summary: {experiments_summary}")
        """
        pass # TODO: if there is

    def get_datasets_summary(self):
        """
        Fetch a summary of all datasets in the project.

        Returns
        -------
        tuple
            A tuple containing:
            - The datasets summary data if the request is successful.
            - An error message if the request fails.

        Example
        -------
        >>> datasets_summary, error = project.get_datasets_summary()
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Datasets summary: {datasets_summary}")
        """
        pass # TODO if there is

    # Instances Getters
    def get_dataset(self, dataset_id = None, dataset_name = ''):
        """
        Get a Dataset instance.

        Parameters
        ----------
        dataset_id : str, optional
            The ID of the dataset.
        dataset_name : str, optional
            The name of the dataset.

        Returns
        -------
        Dataset
            A Dataset instance with the specified ID and/or name.

        Example
        -------
        >>> dataset = project.get_dataset(dataset_id="dataset123")
        >>> print(dataset)
        """
        return Dataset(self.session, dataset_id, dataset_name)
    
    def get_annotation(self, dataset_id = None, annotation_id = None, annotation_name = ''):
        """
        Get an Annotation instance.

        Parameters
        ----------
        dataset_id : str, optional
            The ID of the dataset associated with the annotation.
        annotation_id : str, optional
            The ID of the annotation.
        annotation_name : str, optional
            The name of the annotation.

        Returns
        -------
        Annotation
            An Annotation instance with the specified dataset ID, annotation ID, and/or name.

        Example
        -------
        >>> annotation = project.get_annotation(annotation_id="annotation123")
        >>> print(annotation)
        """
        return Annotation(self.session, dataset_id, annotation_id, annotation_name)
    
    def get_experiment(self, experiment_id = None, experiment_name = ''):
        """
        Get an Experiment instance.

        Parameters
        ----------
        experiment_id : str, optional
            The ID of the experiment.
        experiment_name : str, optional
            The name of the experiment.

        Returns
        -------
        Experiment
            An Experiment instance with the specified ID and/or name.

        Example
        -------
        >>> experiment = project.get_experiment(experiment_id="experiment123")
        >>> print(experiment)
        """
        return Experiment(self.session, experiment_id, experiment_name)
    
    def get_model(self, model_id = None, model_name = ''):
        """
        Get a Model instance.

        Parameters
        ----------
        model_id : str, optional
            The ID of the model.
        model_name : str, optional
            The name of the model.

        Returns
        -------
        Model
            A Model instance with the specified ID and/or name.

        Example
        -------
        >>> model = project.get_model(model_id="model123")
        >>> print(model)
        """
        return Model(self.session, model_id, model_name)
    
    def get_inference_optimization(self, model_export_id = None, model_export_name = ''):

        """
        Get an InferenceOptimization instance.

        Parameters
        ----------
        model_export_id : str, optional
            The ID of the model export.
        model_export_name : str, optional
            The name of the model export.

        Returns
        -------
        InferenceOptimization
            An InferenceOptimization instance with the specified ID and/or name.

        Example
        -------
        >>> inference_optimization = project.get_inference_optimization(model_export_id="export123")
        >>> print(inference_optimization)
        """

        return ExportedModel(self.session, model_export_id, model_export_name)
    
    def get_deployment(self, deployment_id = None, deployment_name = ''):
        """
        Get a Deployment instance.

        Parameters
        ----------
        deployment_id : str, optional
            The ID of the deployment.
        deployment_name : str, optional
            The name of the deployment.

        Returns
        -------
        Deployment
            A Deployment instance with the specified ID and/or name.

        Example
        -------
        >>> deployment = project.get_deployment(deployment_id="deployment123")
        >>> print(deployment)
        """
        return Deployment(self.session, deployment_id, deployment_name)
    
