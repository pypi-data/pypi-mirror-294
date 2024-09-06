import numpy as np

"""Module for interacting with backend API to manage drift monitoring."""

class DriftMonitoring:
    """Class to handle Drift Monitoring-related operations within a project."""

    def __init__(self, session):
        """
        Class for handling drift monitoring-related operations.

        Parameters
        ----------
        session : object
            The session object containing the RPC interface and project ID.

        Attributes
        ----------
        session : object
            The session object for RPC communication.
        project_id : str
            The project ID associated with the session.
        rpc : object
            The RPC interface used to make API calls.

        Example
        -------
        >>> session = Session(account_number="account_number")
        >>> drift_monitoring = DriftMonitoring(session=session_object)
        """
        
        self.session = session
        self.project_id = session.project_id
        self.rpc = session.rpc

    def handle_response(self, resp, success_message, error_message):
        """
        Handle the API response, checking for success or error.

        Parameters
        ----------
        resp : dict
            The response object returned from the API call.
        success_message : str
            Message to return if the API call was successful.
        error_message : str
            Message to return if the API call failed.

        Returns
        -------
        resp : dict
            The original API response object.
        error : str or None
            The error message if the API call failed, otherwise None.
        message : str
            The success or error message.
        """
        if resp.get("success"):
            error = None
            message = success_message
        else:
            error = resp.get("message")
            message = error_message

        return resp, error, message

    def list_drift_monitorings(self):
        """
        Fetch a list of all drift monitorings.

        Returns
        -------
        tuple
            A tuple containing three elements:
            - API response (dict): The raw response from the API.
            - error_message (str or None): Error message if an error occurred, None otherwise.
            - status_message (str): A status message indicating success or failure.

        Example
        -------
        >>> resp, err, msg = drift_monitoring.list_drift_monitorings()
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Drift Monitoring detail : {resp}")
        """
        path = "/v1/deployment/list_drift_monitorings"
        resp = self.rpc.get(path=path)

        return self.handle_response(
            resp,
            "Drift monitorings fetched successfully",
            "An error occurred while trying to fetch drift monitorings",
        )

    def add_drift_monitoring_params(self, _idDeployment, deploymentName, imageStoreConfidenceThreshold, imageStoreCountThreshold):
        """
        Add drift monitoring parameters.

        Parameters
        ----------
        _idDeployment : str
            The ID of the deployment.
        deploymentName : str
            The name of the deployment.
        imageStoreConfidenceThreshold : float
            Confidence threshold for storing images.
        imageStoreCountThreshold : int
            Count threshold for storing images.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> resp, err, msg = drift_monitoring.add_drift_monitoring_params(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Drift Monitoring detail : {resp}")
        """
        path = "/v1/deployment/drift_monitoring"
        headers = {"Content-Type": "application/json"}
        monitoring_params = {
            "_idDeployment": _idDeployment,
            "deploymentName": deploymentName,
            "imageStoreConfidenceThreshold": imageStoreConfidenceThreshold,
            "imageStoreCountThreshold": imageStoreCountThreshold
        }
        resp = self.rpc.post(path=path, headers=headers, payload=monitoring_params)

        return self.handle_response(
            resp,
            "Drift monitoring parameters added successfully",
            "An error occurred while trying to add drift monitoring parameters",
        )

    def update_drift_monitoring(self, _idDeployment, deploymentName, imageStoreConfidenceThreshold, imageStoreCountThreshold):
        """
        Update drift monitoring parameters.

        Parameters
        ----------
        _idDeployment : str
            The ID of the deployment.
        deploymentName : str
            The name of the deployment.
        imageStoreConfidenceThreshold : float
            Confidence threshold for storing images.
        imageStoreCountThreshold : int
            Count threshold for storing images.

        Returns
        -------
        tuple
            A tuple containing:
            - resp (dict): The API response object.
            - error (str or None): Error message if the API call failed, otherwise None.
            - message (str): Success or error message.

        Example
        -------
        >>> resp, err, msg = drift_monitoring.update_drift_monitoring(dataset_version="v1.0")
        >>> if err:
        >>>     print(f"Error: {err}")
        >>> else:
        >>>     print(f"Updated Drift Monitoring detail : {resp}")
        """
        path = "/v1/deployment/update_drift_monitoring"
        headers = {"Content-Type": "application/json"}
        monitoring_params = {
            "_idDeployment": _idDeployment,
            "deploymentName": deploymentName,
            "imageStoreConfidenceThreshold": imageStoreConfidenceThreshold,
            "imageStoreCountThreshold": imageStoreCountThreshold
        }
        resp = self.rpc.put(path=path, headers=headers, payload=monitoring_params)

        return self.handle_response(
            resp,
            "Drift monitoring parameters updated successfully",
            "An error occurred while trying to update drift monitoring parameters",
        )
