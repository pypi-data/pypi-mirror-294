import sys


class Deployment:

    def __init__(self, session, deployment_id=None, deployment_name=''):
        """
        Initialize Deployment instance with the given session and optional deployment_id.

        Parameters
        ----------
        session : object
            The session object containing project and RPC information.
        deployment_id : str, optional
            The ID of the deployment to be managed. Default is None.
        deployment_name : str, optional
            The name of the deployment. Default is an empty string.

        Example
        -------
        >>> session = Session(account_number="account_number")
        >>> deployment = Deployment(session=session_object,deployment_id=deployment_id,deployment_name=deployment_name)
        """
        self.project_id = session.project_id
        self.deployment_id = deployment_id
        self.deployment_name = deployment_name
        self.rpc = session.rpc

    def handle_response(self, resp, success_message, error_message):
        """
        Helper function to handle API response.

        Parameters
        ----------
        resp : dict
            The response from the API call.
        success_message : str
            The message to be returned if the API call is successful.
        error_message : str
            The message to be returned if the API call fails.

        Returns
        -------
        tuple
            A tuple containing the API response, error message (if any), and the corresponding message.
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
        Fetch deployment details based on either the deployment ID or deployment name.

        This method tries to fetch deployment details by ID if available;
        otherwise, it tries to fetch by name. It raises a ValueError if neither
        identifier is provided.

        Returns
        -------
        dict
            A dictionary containing the deployment details.

        Raises
        ------
        ValueError
            If neither deployment ID nor deployment name is provided.

        Example
        -------
        >>> deployment_details = deployment.get_details()
        >>> if isinstance(deployment_details, dict):
        >>>     print("deployment Details:", deployment_details)
        >>> else:
        >>>     print("Failed to retrieve deployment details.")        
        """
        id = self.deployment_id
        name = self.deployment_name

        if id:
            try:
                return self._get_deployment_by_id()
            except Exception as e:
                print(f"Error retrieving deployment by id: {e}")
        elif name:
            try:
                return self._get_deployment_by_name()
            except Exception as e:
                print(f"Error retrieving deployment by name: {e}")
        else:
            raise ValueError("At least one of 'deployment_id' or 'deployment_name' must be provided.")
        
    #GET REQUESTS
    def _get_deployment_by_id(self):
        """
        Fetch details of the specified deployment.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Examples
        --------
        >>> deployment = Deployment(session, deployment_id="1234")
        >>> deployment._get_deployment_by_id()
        """
        path = f"/v1/deployment/{self.deployment_id}"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp,
            "Deployment fetched successfully",
            "An error occurred while trying to fetch deployment.",
        )
        
    def _get_deployment_by_name(self):
        """
        Fetch deployment details using the deployment name.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the deployment name is not set.

        Examples
        --------
        >>> deployment = Deployment(session, deployment_name="MyDeployment")
        >>> resp, err, msg = deployment.get_deployment_by_name()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Deployment details : {resp}")
        """
        if self.deployment_name == '':
            print("Deployment name not set for this Deployment. Cannot perform the operation for Deployment without deployment name")
            sys.exit(0)
        path = f"/v1/deployment/get_deployment_by_name?deploymentName={self.deployment_name}"
        resp = self.rpc.get(path=path)

        return self.handle_response(resp, "Deployment by name fetched successfully",
                                    "Could not fetch Deployment by name")

    def get_deployment_server(self, model_train_id, model_type):
        """
        Fetch information about the deployment server for a specific model.

        Parameters
        ----------
        model_train_id : str
            The ID of the model training instance.
        model_type : str
            The type of model (e.g., 'YOLO', 'EfficientNet').

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Examples
        --------
        >>> deployment = Deployment(session)
        >>> resp, err, msg = deployment.get_deployment_server("train123", "YOLO")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Deployment server details : {resp}")
        """
        path = f"/v1/deployment/get_deploy_server/{model_train_id}/{model_type}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Deployment server fetched successfully",
            "An error occurred while trying to fetch deployment server.",
        )

    def wakeup_deployment_server(self):
        """
        Wake up the deployment server associated with the current deployment.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Examples
        --------
        >>> deployment = Deployment(session, deployment_id="1234")
        >>> resp, err, msg = deployment.wakeup_deployment_server()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Response : {resp}")
        """
        path = f"/v1/deployment/wake_up_deploy_server/{self.deployment_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Deployment server has been successfully awakened",
            "An error occurred while attempting to wake up the deployment server.",
        )

    def get_deployment_status_cards(self):
        """
        Fetch status cards for the current project's deployments.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Examples
        --------
        >>> deployment = Deployment(session)
        >>> resp, err, msg = deployment.get_deployment_status_cards()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Response : {resp}")
        """
        path = f"/v1/deployment/status_cards?projectId={self.project_id}"
        resp = self.rpc.get(path=path)
        return self.handle_response(
            resp,
            "Deployment status cards fetched successfully.",
            "An error occurred while trying to fetch deployment status cards.",
        )


    def check_for_duplicate(self, name):
        """
        Check for duplicate deployment names.

        Parameters
        ----------
        name : str
            The deployment name to check for duplicates.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Examples
        --------
        >>> deployment = Deployment(session)
        >>> resp, err, msg = deployment.check_for_duplicate("MyDeployment")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Response : {resp}")
        """
        path = f"/v1/deployment/check_for_duplicate?deploymentName={name}"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            if resp.get("data") == 'true':
                return self.handle_response(resp, "Deployment with this name already exists", "Could not check for this Deployment name")
            else:
                return self.handle_response(resp, "Deployment with this name does not exist", "Could not check for this Deployment name")
        else:
            return self.handle_response(resp, "", "Could not check for this Deployment name")

    def create_auth_key(self, expiry_days):
        """
        Create a new authentication key for the deployment that is valid for the specified number.

        Parameters
        ----------
        expiry_days : int
            The number of days before the authentication key expires.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Examples
        --------
        >>> deployment = Deployment(session, deployment_id="1234")
        >>> resp, err, msg = deployment.create_auth_key(30)
        """
        body = {"expiryDays": expiry_days,
                "authType": "external"}

        headers = {'Content-Type': 'application/json'}
        path = f"/v1/deployment/add_auth_key/{self.deployment_id}?projectId={self.project_id}"

        resp = self.rpc.post(path=path, headers=headers, payload=body)
        return self.handle_response(
            resp,
            "Auth Key created successfully.",
            "An error occurred while trying to create auth key.",
        )

    def update_deployment_name(self, updated_name):
        """
        Update the deployment name for the current deployment.

        Parameters
        ----------
        updated_name : str
            The new name for the deployment.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the deployment ID is not set.

        Examples
        --------
        >>> deployment = Deployment(session, deployment_id="1234")
        >>> resp, err, msg = deployment.update_deployment_name("NewDeploymentName")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Response : {resp}")
        """
        if self.deployment_id is None:
            print("Deployment id not set for this model.")
            sys.exit(0)

        body = {"deploymentName": updated_name}

        headers = {"Content-Type": "application/json"}
        path = f"/v1/deployment/update_deployment_name/{self.deployment_id}"
        resp = self.rpc.put(path=path, headers=headers, payload=body)

        return self.handle_response(resp, f"Deployment name updated to {updated_name}",
                                    "Could not update the deployment name")

    def delete_deployment(self):
        """
        Delete the specified deployment.

        Parameters
        ----------
        deployment_id : str
            The ID of the deployment to be deleted.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Examples
        --------
        >>> deployment = Deployment(session)
        >>> resp, err, msg = deployment.delete_deployment("1234")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Response : {resp}")
        """
        path = f"/v1/deployment/delete_deployment/{self.deployment_id}"

        resp = self.rpc.delete(path=path)
        return self.handle_response(
            resp,
            "Deployment deleted successfully.",
            "An error occurred while trying to delete the deployment.",
        )

    def delete_auth_key(self, auth_key):
        """
        Delete the specified authentication key.

        Parameters
        ----------
        auth_key : str
            The authentication key to be deleted.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Raises
        ------
        SystemExit
            If the deployment ID is not set.

        Examples
        --------
        >>> deployment = Deployment(session, deployment_id="1234")
        >>> resp, err, msg = deployment.delete_auth_key("abcd1234")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Response : {resp}")
        """
        if self.deployment_id is None:
            print(
                "Deployment id not set for this deployment."
            )
            sys.exit(0)

        path = f"/v1/deployment/delete_auth_key/{self.deployment_id}/{auth_key}"

        resp = self.rpc.delete(path=path)
        return self.handle_response(
            resp,
            "Auth key deleted successfully.",
            "An error occurred while trying to delete the auth key.",
        )
