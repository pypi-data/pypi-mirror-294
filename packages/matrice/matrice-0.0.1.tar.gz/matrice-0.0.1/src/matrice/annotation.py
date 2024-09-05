"""Module to handle annotation-related operations within a project."""
import sys

class Annotation:
    """Class to handle annotation-related operations within a project."""
    def __init__(self, session, dataset_id = None, annotation_id = None, annotation_name = ''):
        """
        Initialize the Annotation class with session details and optional dataset/annotation IDs and names.

        Parameters
        ----------
        session : Session
            The session object that manages the connection to the API.
        dataset_id : str, optional
            The dataset ID associated with the annotation (default is None).
        annotation_id : str, optional
            The annotation ID (default is None).
        annotation_name : str, optional
            The name of the annotation (default is an empty string).
        
        Example
        -------
        >>> session = Session(account_number="account_number")
        >>> annotation = Annotation(session, dataset_id="1234", annotation_id="5678")
        """
        self.project_id = session.project_id
        self.dataset_id = dataset_id
        self.annotation_id = annotation_id
        self.annotation_name = annotation_name
        self.rpc = session.rpc
    
    def handle_response(self, response, success_message, failure_message):
        """
        Handle API response and return a standardized tuple containing the result, error, and message. 
        This method is for internal use within the class to handle API responses.
        
        Parameters
        ----------
        response : dict
            The response returned by the API.
        success_message : str
            Message to return if the API call is successful.
        failure_message : str
            Message to return if the API call fails.

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
        Retrieve details of an annotation based on annotation ID or name.

        This method tries to fetch annotation details by ID if available;
        otherwise, it tries to fetch by name. It raises a ValueError if neither
        identifier is provided.

        Returns
        -------
        dict
            The detailed information of the annotation if found, either by ID or name.

        Raises
        ------
        ValueError
            If neither 'annotation_id' nor 'annotation_name' is provided.

        Examples
        --------
        >>> annotation_details = annotation.get_details()
        >>> if isinstance(annotation_details, dict):
        >>>     print("Annotation Details:", annotation_details)
        >>> else:
        >>>     print("Failed to retrieve annotation details.")

        Notes
        -----
        - `_get_annotation_by_id()` is called if 'annotation_id' is set and retrieves the annotation by its ID.
        - `_get_annotation_by_name()` is used if 'annotation_name' is set and fetches the annotation by its name.
        """
        id = self.annotation_id
        name = self.annotation_name

        if id:
            try:
                return self._get_annotation_by_id()
            except Exception as e:
                print(f"Error retrieving annotation by id: {e}")
        elif name:
            try:
                return self._get_annotation_by_name()
            except Exception as e:
                print(f"Error retrieving annotation by name: {e}")
        else:
            raise ValueError("At least one of 'annotation_id' or 'annotation_name' must be provided.")

        
    #GET REQUESTS
    def _get_annotation_by_id(self):
        """
        Fetch a specific annotation by its ID.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.get_annotation_by_id()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation Details: {resp}")
        """
        path=f"/v1/annotations/{self.annotation_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Annotation fetched successfully",
                                    "Could not fetch annotation")
        
    def get_annotation_by_name(self):
        """
        Fetch a specific annotation by its name.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.get_annotation_by_name()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation Details: {resp}")
        """
        if self.annotation_name == '':
            print("Annotation name not set for this annotation. Cannot perform the operation for annotation without Annotation name")
            sys.exit(0)
        path = f"/v1/annotations/get_annotation_by_name?annotationName={self.annotation_name}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Annotation by name fetched successfully",
                                    "Could not fetch annotation by name")
    
    def get_categories_by_annotation_id(self):
        """
        Fetch categories for a specific annotation by its ID.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.get_categories_by_annotation_id()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Categories: {resp}")
        """
        path=f"/v1/annotations/{self.annotation_id}/categories"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Categories fetched successfully",
                                    "Could not fetch categories")
    
    def get_annotation_files(self):
        """
        Fetch the files associated with the specific annotation.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.get_annotation_files()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation Files: {resp}")
        """
        path=f"/v1/annotations/{self.annotation_id}/files?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Annotation files fetched successfully",
                                    "Could not fetch annotation files")
    
    
    def get_annotation_history(self,annotation_item_id):
        """
        Fetch the annotation history for a specific item.

        Parameters
        ----------
        annotation_item_id : str
            The ID of the annotation item for which history is being fetched.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.get_annotation_history(annotation_item_id="12345")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation History: {resp}")
        """
        path=f"/v1/annotations/{self.annotation_id}/{annotation_item_id}/annotation_history?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Annotation history fetched successfully",
                                    "Could not fetch annotation history")
    
    def get_annotation_summary(self):
        """
        Fetch the summary of a specific annotation.

        Returns
        -------
        tuple
            A tuple containing:
            - The annotation summary (dict) if the request is successful.
            - An error message (str) if an error occurred.
            - A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.get_annotation_summary()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation Summary: {resp}")
        """
        path=f"/v1/annotations/{self.annotation_id}/summary"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Annotation item summary fetched successfully",
                                    "Could not fetch annotation item summary")
    
    def get_annotation_files(self):
        """
        Fetch the summary of a specific annotation item.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.get_annotation_summary()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation Summary: {resp}")
        """
        if self.annotation_id is None:
            print(
                "Annotation id not set for this dataset. Cannot perform the operation for annotation without annotation id"
            )
            sys.exit(0)

        path = f"/v1/annotations/{self.annotation_id}/files?projectId={self.project_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Sucessfully fetched the annotation item files",
                                    "Could not fetch annotation item files")

    def check_for_duplicate(self, name):
        """
        Check if an annotation with the given name already exists.

        Parameters
        ----------
        name : str
            The name of the annotation to check for duplication.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.check_for_duplicate(name="MyAnnotation")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation Duplication Status: {resp}")
        """
        path = f"/v1/annotations/check_for_duplicate?annotationName={name}"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            if resp.get("data") == 'true':
                return self.handle_response(resp, "Annotation with this name already exists", "Could not check for this annotation name")
            else:
                return self.handle_response(resp, "Annotation with this name does not exist", "Could not check for this annotation name")
        else:
            return self.handle_response(resp, "", "Could not check for this annotation name")

   #PUT REQUESTS
    def rename_annotation(self, annotation_title):
        """
        Rename the annotation with the given title.

        Parameters
        ----------
        annotation_title : str
            The new title for the annotation.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.rename_annotation(annotation_title="New Title")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation Renamed: {resp}")
        """
        if self.annotation_id is None:
            print("Dataset id not set for this dataset. Cannot perform the operation for dataset without dataset id")
            sys.exit(0)
        
        path = f"/v1/annotations/{self.annotation_id}"
        headers = {"Content-Type": "application/json"}
        body = {"title": annotation_title}
        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return self.handle_response(resp, "Update data item label in progress",
                                    "Could not update the date item label")


    #POST REQUESTS
    def annotate(
        self,
        file_id,
        annotation_item_id,
        updated_classification_label,
        labeller,
        reviewer,
        status,
        issues,
        label_time,
        review_time,
    ):
        """
        Add annotation data to a specific file.

        Parameters
        ----------
        file_id : str
            The ID of the file being annotated.
        annotation_item_id : str
            The ID of the annotation item.
        updated_classification_label : dict
            The updated classification label for the item.
        labeller : dict
            The labeller's information.
        reviewer : dict
            The reviewer's information.
        status : str
            The status of the annotation.
        issues : str
            Any issues identified during the annotation process.
        label_time : int
            The time taken to label the item.
        review_time : int
            The time taken to review the item.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.annotate(
                file_id="file123", annotation_item_id="item456", 
                updated_classification_label={"_idCategory": "cat1", "categoryName": "Dog"},
                labeller={"_idUser": "user123", "name": "John Doe"},
                reviewer={"_idUser": "user456", "name": "Jane Doe"},
                status="Completed", issues="", label_time=120, review_time=30)
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation added successfully: {resp}")
        """
        path=f"/v1/annotations/{self.annotation_id}/files/{file_id}/annotate?projectId={self.project_id}"
        payload={
             "annotationId":self.annotation_id,
             "annotationItemId":annotation_item_id,
             "labeller":labeller,           
             "reviewer":reviewer,           
             "updatedClassificationLabel":updated_classification_label,  
             "status":status,
             "issues":issues,
             "labelTime":label_time,
             "reviewTime":review_time
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=payload)

        return self.handle_response(resp, "Annotation added successfully",
                                    "An error occured while adding annotation")

    def create_dataset(
        self,
        is_create_new,
        old_dataset_version,
        new_dataset_version,
        new_version_description
    ):
        """
        Create or update a dataset based on annotation data.

        Parameters
        ----------
        is_create_new : bool
            Whether to create a new dataset version or update an existing one.
        old_dataset_version : str
            The version of the old dataset.
        new_dataset_version : str
            The version of the new dataset.
        new_version_description : str
            The description for the new dataset version.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.create_dataset(
                is_create_new=True, old_dataset_version="v1.0", 
                new_dataset_version="v2.0", new_version_description="Updated Version")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Dataset created successfully: {resp}")
        """
        path=f"/v1/annotations/{self.annotation_id}/create_dataset?projectId={self.project_id}"

        payload={
            "annotationId":self.annotation_id,
            "isCreateNew":is_create_new,
            "oldDatasetVersion":old_dataset_version,
            "newDatasetVersion":new_dataset_version,
            "newVersionDescription":new_version_description,  
            "datasetDesc": ""
        }
        headers = {'Content-Type': 'application/json'}
        resp = self.rpc.post(path=path, headers=headers, payload=payload)

        return self.handle_response(resp, "Annotation added successfully",
                                    "An error occured while adding annotation")


    def create_category(self, labelname):
        """
        Create a new category for the annotation.

        Parameters
        ----------
        labelname : str
            The name of the new category.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.create_category(labelname="Animal")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Category created successfully: {resp}")
        """
        if self.annotation_id is None:
            print(
                "Annotation id not set for this annotation. Cannot download without annotation id"
            )
            sys.exit(0)

        body = {
            "_idAnnotation": self.annotation_id,
            "name": labelname
        }
        headers = {"Content-Type": "application/json"}
        path = f"/v1/annotations/{self.annotation_id}/categories?projectId={self.project_id}"

        resp = self.rpc.post(path=path, headers=headers, payload=body)
        return self.handle_response(resp, "Category added successfully",
                                    "An error occured while adding Category")
    
    def delete_annotation(self):
        """
        Delete the entire annotation.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.delete_annotation()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation deleted successfully: {resp}")
        """
        if self.annotation_id is None:
            print(
                "Annotation id not set for this dataset. Cannot perform the deletion for annotation without annotation id"
            )
            sys.exit(0)

        path = f"/v1/annotations/{self.annotation_id}?projectId={self.project_id}" # check

        resp = self.rpc.delete(path=path)
        return self.handle_response(resp, "Annotation deleted successfully",
                                    "An error occured while deleting annotation")
    
    def delete_annotation_item(self, annotation_item_id):
        """
        Delete a specific annotation item.

        Parameters
        ----------
        annotation_item_id : str
            The ID of the annotation item to delete.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = annotation.delete_annotation_item(annotation_item_id="item123")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Annotation item deleted successfully: {resp}")
        """
        if self.annotation_id is None:
            print(
                "Annotation id not set for this dataset. Cannot perform the deletion for annotation without annotation id"
            )
            sys.exit(0)

        path = f"/v1/annotations/{self.annotation_id}/files/{annotation_item_id}?projectId={self.project_id}" # check

        resp = self.rpc.delete(path=path)
        return self.handle_response(resp, "Annotation Item deleted successfully",
                                    "An error occured while deleting annotation item")
    
