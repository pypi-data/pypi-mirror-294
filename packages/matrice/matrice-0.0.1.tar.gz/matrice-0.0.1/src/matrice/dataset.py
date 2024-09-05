"""Module to handle dataset-related operations within a project."""
import sys
import os
import requests

class Dataset:
    """Class to handle dataset-related operations within a project."""
    def __init__(self, session, dataset_id=None, dataset_name=''):
        """
        Initialize a new dataset instance.

        Parameters
        ----------
        session : Session
            The session object that manages the connection to the server.
        dataset_id : str, optional
            The ID of the dataset (default is None).
        dataset_name : str
            The name of the dataset (default is an empty string).

        Example
        -------
        >>> session = Session(account_number="account_number")
        >>> dataset = Dataset(session=session_object,dataset_id=dataset_id,dataset_name=dataset_name)
        """
        self.project_id = session.project_id
        self.dataset_id = dataset_id
        self.dataset_name = dataset_name
        self.rpc = session.rpc

    def handle_response(self, response, success_message, failure_message):
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
        Retrieve details of the dataset based on dataset ID or name.

        This method attempts to fetch dataset details by ID if available;
        otherwise, it tries to fetch by name. It raises a ValueError if neither
        identifier is provided.

        Returns
        -------
        dict
            The detailed information of the dataset if found, either by ID or name.

        Raises
        ------
        ValueError
            If neither 'dataset_id' nor 'dataset_name' is provided.

        Examples
        --------
        >>> dataset_details = dataset.get_details()
        >>> if isinstance(dataset_details, dict):
        >>>     print("Dataset Details:", dataset_details)
        >>> else:
        >>>     print("Failed to retrieve dataset details.")

        Notes
        -----
        - `get_dataset()` is called if 'dataset_id' is set and retrieves the dataset by its ID.
        - `get_dataset_by_name()` is used if 'dataset_name' is set and fetches the dataset by its name.
        """
        id = self.dataset_id
        name = self.dataset_name

        if id:
            try:
                return self.get_dataset()
            except Exception as e:
                print(f"Error retrieving dataset by id: {e}")
        elif name:
            try:
                return self.get_dataset_by_name()
            except Exception as e:
                print(f"Error retrieving dataset by name: {e}")
        else:
            raise ValueError("At least one of 'dataset_id' or 'dataset_name' must be provided.")
        
    def get_summary(self, dataset_version):
        """
        Get the summary for a specific version of the dataset.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to fetch the summary for.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.get_summary(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset summary: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/summary?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Dataset summary fetched successfully",
                                    "Could not fetch dataset summary")

    def get_dataset(self):
        """
        Fetch the details of the dataset.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.
             
        Example
        -------
        >>> resp, err, msg = dataset.get_dataset()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset details: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Dataset fetched successfully",
                                    "Could not fetch dataset")

    def get_categories(self, dataset_version):
        """
        Get the categories for a specific dataset version.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset for which to fetch categories.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.get_categories(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Categories: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/categories?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, f"Dataset categories for version - {dataset_version} fetched successfully",
                                    "Could not fetch dataset categories")

    def list_items_V2(self, dataset_version):
        """
        List all items for a specific version of the dataset.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset for which to list items.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.list_items_V2(dataset_version="v2.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset items: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/v2/item?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, f"Dataset items for version - {dataset_version} fetched successfully",
                                    "Could not fetch dataset items")

    def list_items(self, dataset_version):
        """
        List all items for a specific version of the dataset.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset for which to list items.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.list_items(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Items: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/item?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, f"Dataset items for version - {dataset_version} fetched successfully",
                                    "Could not fetch dataset items")

    def get_processed_versions(self):
        """
        Get all processed versions of the dataset.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.get_processed_versions()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Processed Versions: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/get_processed_versions?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, f"Processed versions fetched successfully",
                                    "Could not fetch processed versions")
    
    def check_valid_spilts(self, dataset_version):
        """
        Check if the splits are valid for a specific dataset version.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to check for valid splits.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.check_valid_splits(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Splits Valid: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/check_valid_spilts/{self.dataset_id}/{dataset_version}?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, f"Splits are valid",
                                    "Splits are invalid")

    def get_dataset_analysis(self, dataset_version):
        """
        Fetch the analysis for a specific dataset version.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to fetch the analysis for.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.get_dataset_analysis(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset Analysis: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/get_dataset_analysis/{self.dataset_id}/version/{dataset_version}?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, f"Dataset Analysis Fetched successfully",
                                    "Could not fetch dataset Analysis")

    def get_dataset_by_name(self):
        """
        Fetch the dataset details by name.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.get_dataset_by_name()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset Details: {resp}")
        """
        if self.dataset_name == '':
            print("Dataset name not set for this dataset. Cannot perform the operation for dataset without dataset name")
            sys.exit(0)
        
        path = f"/v1/dataset/get_dataset_by_name?datasetName={self.dataset_name}"
        resp = self.rpc.get(path=path)
        return self.handle_response(resp, f"Dataset Details Fetched successfully",
                                    "Could not fetch dataset details")

    def check_for_duplicate(self, name):
        """
        Check if a dataset with the given name already exists.

        Parameters
        ----------
        name : str
            The name of the dataset to check for duplication.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.check_for_duplicate(name="Dataset Name")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Duplicate check result: {resp}")
        """
        path = f"/v1/dataset/check_for_duplicate?datasetName={name}"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            if resp.get("data") == 'true':
                return self.handle_response(resp, "Dataset with this name already exists", "Could not check for this dataset name")
            else:
                return self.handle_response(resp, "Dataset with this name does not exist", "Could not check for this dataset name")
        else:
            return self.handle_response(resp, "", "Could not check for this dataset name")
    
    def get_upload_path(self, file_name):
        """
        Get the upload path for a given file name.

        Parameters
        ----------
        file_name : str
            The name of the file to get the upload path for.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.get_upload_path(file_name="data.zip")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Upload Path: {resp}")
        """
        path = f"/v1/dataset/upload-path?fileName={file_name}"
        resp = self.rpc.get(path=path)
        return self.handle_response(resp, "Upload Path fetched successfully", "Could not fetch upload path")

    # PUT REQUESTS

    def update_dataset(self, updated_name):
        """
        Update the dataset name.

        Parameters
        ----------
        updated_name : str
            The new name of the dataset.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.update_dataset(updated_name="Updated Dataset Name")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset updated successfully: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {"name": updated_name}
        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return self.handle_response(resp, f"Successfully updated dataset name to {updated_name}",
                                    "Could not update datename")

    def update_data_item_label(self, dataset_version, item_id, label_id):
        """
        Update the label of a specific dataset item.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset.
        item_id : str
            The ID of the dataset item.
        label_id : str
            The ID of the new label to assign to the dataset item.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.update_data_item_label(dataset_version="v1.0", item_id="12345", label_id="67890")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Label updated successfully: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}/item/{item_id}/label?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {"labelId": label_id}
        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return self.handle_response(resp, "Update data item label in progress",
                                    "Could not update the date item label")

    # POST REQUESTS
    def create_dataset_import(
        self,
        source,
        source_url,
        new_dataset_version,
        old_dataset_version,
        dataset_description="",
        version_description="",
        compute_alias="",
    ):
        """
        Import a new version of the dataset from an external source.

        Parameters
        ----------
        source : str
            The source of the dataset.
        source_url : str
            The URL of the dataset to import.
        new_dataset_version : str
            The version number for the new dataset.
        old_dataset_version : str
            The version number of the existing dataset.
        dataset_description : str, optional
            The description of the dataset (default is an empty string).
        version_description : str, optional
            The description of the new dataset version (default is an empty string).
        compute_alias : str, optional
            The alias for the compute instance to be used (default is an empty string).

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.create_dataset_import(source="url", source_url="https://example.com/dataset.zip", new_dataset_version="v2.0", old_dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset import in progress: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        dataset_resp, err, message = self.get_dataset()
        if err is not None:
            return dataset_resp, err, message

        stats = dataset_resp["stats"]
        if dataset_description == "":
            dataset_description = dataset_resp["datasetDesc"]

        for stat in stats:
            if stat["version"] != old_dataset_version:
                continue
            if stat["versionStatus"] != "processed":
                resp = {}
                err = None
                message = f"Only the dataset versions with complete status can be updated.Version {old_dataset_version} of the dataset doesn't have status complete."
                return resp, err, message

            if version_description == "" and old_dataset_version == new_dataset_version:
                version_description = stat["versionDescription"]
            break
        
        is_created_new = new_dataset_version == old_dataset_version
        path = f"v1/dataset/{self.dataset_id}/import?project={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "source": source,
            "sourceUrl": source_url,
            "isCreateNew": is_created_new,
            "isUnlabeled": False,
            "newDatasetVersion": new_dataset_version,
            "oldDatasetVersion": old_dataset_version,
            "newVersionDescription": version_description,
            "datasetDesc": dataset_description,
            "computeAlias": compute_alias,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        return self.handle_response(resp, "New data item addition in progress",
                                    "An error occured while trying to add new data item.")

    def split_data(
        self,
        old_dataset_version,
        new_dataset_version,
        is_random_split,
        train_num=0,
        val_num=0,
        test_num=0,
        transfers=[{"source": "", "destination": "", "transferAmount": 1}],
        dataset_description="",
        version_description="",
        new_version_description="",
        compute_alias="",
    ):
        """
        Split or transfer images between training, validation, and test sets in the datasets.

        Parameters
        ----------
        old_dataset_version : str
            The version of the existing dataset.
        new_dataset_version : str
            The version of the new dataset.
        is_random_split : bool
            Whether to perform a random split.
        train_num : int, optional
            Number of training samples (default is 0).
        val_num : int, optional
            Number of validation samples (default is 0).
        test_num : int, optional
            Number of test samples (default is 0).
        transfers : list, 
            A list of transfer details .
        dataset_description : str, optional
            Description of the dataset (default is an empty string).
        version_description : str, optional
            Description of the dataset version (default is an empty string).
        new_version_description : str, optional
            Description of the new dataset version (default is an empty string).
        compute_alias : str, optional
            Compute instance alias (default is an empty string).

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.split_data(
                old_dataset_version="v1.0", new_dataset_version="v2.0", 
                is_random_split=True, train_num=100, val_num=20, test_num=30, transfers=[{"source": "train", "destination": "test", "transferAmount": 100}] )
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Data split in progress: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        dataset_resp, err, message = self.get_dataset()
        if err is not None:
            return dataset_resp, err, message

        stats = dataset_resp["stats"]
        if dataset_description == "":
            dataset_description = dataset_resp["datasetDesc"]

        for stat in stats:
            if stat["version"] != old_dataset_version:
                continue
            if stat["versionStatus"] != "processed":
                resp = {}
                err = None
                message = f"Only the dataset versions with complete status can be updated.Version {old_dataset_version} of the dataset doesn't have status complete."
                return resp, err, message

            if version_description == "" and old_dataset_version == new_dataset_version:
                version_description = stat["versionDescription"]
            break

        path = f"/v1/dataset/{self.dataset_id}/split_data?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "trainNum": train_num,
            "testNum": test_num,
            "valNum": val_num,
            "unassignedNum": 0,
            "oldDatasetVersion": old_dataset_version,
            "newDatasetVersion": new_dataset_version,
            "isRandomSplit": is_random_split,
            "datasetDesc": dataset_description,
            "newVersionDescription": new_version_description,
            "transfers": transfers,
            "computeAlias": compute_alias,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        return self.handle_response(resp, "Dataset spliting in progress",
                                    "An error occured while trying to split the data.")
        
    def create_dataset_from_deployment(
            self,
            dataset_name,
            is_unlabeled,
            source,
            source_url,
            deployment_id,
            is_public,
            dataset_type,
            project_type,
            dataset_description="",
            version_description="",
    ):
        """
        Create a dataset from deployment.

        Parameters
        ----------
        dataset_name : str
            The name of the new dataset.
        is_unlabeled : bool
            Indicates whether the dataset is unlabeled.
        source : str
            The source of the dataset.
        source_url : str
            The URL of the dataset to be created.
        deployment_id : str
            The deployment ID from which to create the dataset.
        is_public : bool
            Indicates whether the dataset is public.
        project_type : str
            The type of project for the dataset.
        dataset_description : str, optional
            The description of the dataset (default is an empty string).
        version_description : str, optional
            The description of the dataset version (default is an empty string).

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.create_dataset_from_deployment(
                dataset_name="New Dataset", is_unlabeled=False, source="source",
                source_url="https://example.com/dataset.zip", deployment_id="123",
                is_public=True, project_type="classification")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset creation in progress: {resp}")
        """
        dataset_size,err,msg=self.get_dataset_size(source_url)
        print(f'dataset size is = {dataset_size}')
        path = f"/v1/dataset/deployment?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body = {
            "name":dataset_name,
            "isUnlabeled": is_unlabeled, #false,
            "source": source, #"lu",
            "sourceUrl": source_url, #"https://s3.us-west-2.amazonaws.com/dev.dataset/test%2Fb34ea15a-1f52-48a3-9a70-d43688084441.zip",
            "_idDeployment": deployment_id,
            "cloudProvider":"AWS",
            "isCreateNew": True,
            "oldDatasetVersion": None,
            "newDatasetVersion": "v1.0",
            "datasetDescription": dataset_description,
            "newVersionDescription": version_description,
            "isPublic": is_public, #false,
            "computeAlias": "",
            "targetCloudStorage": "GCP",
            "inputType": "MSCOCO",
            "copyData": False,
            "isPrivateStorage": False,
            "cloudStoragePath": "",
            "urlType": "",
            "datasetSize": 0,
            "deleteDeploymentDataset": False,
            "_idProject": self.project_id,
            "type": project_type
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)

        print(resp)

        return self.handle_response(resp, "Dataset creation in progress",
                                    "An error occured while trying to create new dataset")

    # DELETE REQUESTS
    def delete_dataset_item_classification(self, dataset_version, dataset_item_ids):
        """
        Delete classification dataset items.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset from which to delete items.
        dataset_item_ids : list
            A list of dataset item IDs to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_dataset_item_classification(
                dataset_version="v1.0", dataset_item_ids=["123", "456"])
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Items deleted successfully: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/version/{dataset_version}/dataset_item_classification?projectId={self.project_id}&datasetId={self.dataset_id}"
        requested_payload = {"datasetItemIds": dataset_item_ids}
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.delete(path=path, headers=headers,
                               payload=requested_payload)

        return self.handle_response(resp, f"Given dataset items deleted successfully",
                                    "Could not delete the given dataset items")

    def delete_dataset_item_detection(self, dataset_version, dataset_item_ids):
        """
        Delete detection dataset items.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset from which to delete items.
        dataset_item_ids : list
            A list of dataset item IDs to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_dataset_item_detection(
                dataset_version="v1.0", dataset_item_ids=["123", "456"])
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Items deleted successfully: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/version/{dataset_version}/dataset_item_detection?projectId={self.project_id}&datasetId={self.dataset_id}"
        requested_payload = {"datasetItemIds": dataset_item_ids}
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.delete(path=path, headers=headers,
                               payload=requested_payload)

        return self.handle_response(resp, f"Given dataset items deleted successfully",
                                    "Could not delete the given dataset items")

    def delete_version(self, dataset_version):
        """
        Delete a specific version of the dataset.

        Parameters
        ----------
        dataset_version : str
            The version of the dataset to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_version(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Version deleted successfully: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}/version/{dataset_version}?projectId={self.project_id}"
        resp = self.rpc.delete(path=path)

        return self.handle_response(resp, f"Successfully deleted version - {dataset_version}",
                                    "Could not delete the said version")

    def delete_dataset(self):
        """
        Delete the entire dataset.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = dataset.delete_dataset()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset deleted successfully: {resp}")
        """
        if self.dataset_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)

        path = f"/v1/dataset/{self.dataset_id}?projectId={self.project_id}"
        resp = self.rpc.delete(path=path)

        return self.handle_response(resp, f"Successfully deleted the dataset",
                                    "Could not delete the dataset")

    def get_dataset_size(self, url):
        """
        Fetch the size of the dataset from the given URL.

        Parameters
        ----------
        url : str
            The URL of the dataset to fetch the size for.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> size, err, msg = dataset.get_dataset_size(url="")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset size: {size} MB")
        """
        path = f"/v1/dataset/get_dataset_size_in_mb_from_url?projectId={self.project_id}"
        requested_payload = {"datasetUrl": url}
        headers = {"Content-Type": "application/json"}
        resp = self.rpc.post(path=path, headers=headers,
                             payload=requested_payload)

        return self.handle_response(resp, f"Dataset size fetched successfully",
                                    "Could not fetch dataset size")

    def upload_file(self, file_path):
        """
        Upload a file to the dataset.

        Parameters
        ----------
        file_path : str
            The local file path of the file to upload.

        Returns
        -------
        dict
        A dicttionary containing three elements:
        - API response (data): The URL of the uploaded file if successful, otherwise an empty string.
        - error_message (str or None): Error message if an error occurred, None otherwise.
        - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> result = dataset.upload_file(file_path="path/to/data.zip")
        >>> if result['success']:
        >>>     print(f"File uploaded successfully: {result['data']}")
        >>> else:
        >>>     print(f"Error: {result['message']}")
        """
        file_name = os.path.basename(file_path)  
        upload_url, error, message = self.get_upload_path(file_name)
        
        if error is not None:
            return {
                'success': False,
                'data': '',
                'message': message
            }
        
        file = open(file_path, 'rb')
        response = requests.put(upload_url, data=file)
        file.close()

        if response.status_code == 200:
            return {
                'success': True,
                'data': upload_url.split('?')[0],
                'message': 'File uploaded successfully'
            }
        else:
            return {
                'success': False,
                'data': '',
                'message': response.json().get('message', 'Network Error')
            }
