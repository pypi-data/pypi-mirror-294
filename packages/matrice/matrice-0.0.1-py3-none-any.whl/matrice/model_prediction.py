"""Module for interacting with Model Prediction API."""

class ModelPrediction:
    """
    Class for handling model prediction requests and monitoring metrics.

    This class provides methods to interact with the Model Prediction API,
    including monitoring request totals, counts, latencies, and making predictions.

    Attributes:
        project_id (str): The ID of the project.
        deployment_id (str): The ID of the deployment.
        rpc: The RPC client for making API calls.
    """
    def __init__(self, session, deployment_id=None):
        """
        Initialize the ModelPrediction instance.

        Args:
            session: The session object containing project_id.
            deployment_id (str, optional): The ID of the deployment.

        Example:
            >>> session = Session(project_id="project123")
            >>> model_prediction = ModelPrediction(session, deployment_id="deploy456")
        """
        self.project_id = session.project_id
        self.deployment_id=deployment_id
        self.rpc = session.rpc

    def handle_response(self, response, success_message, failure_message):
        """
        Handle API response and return a standardized tuple.

        Args:
            response (dict): The API response.
            success_message (str): Message to return on success.
            failure_message (str): Message to return on failure.

        Returns:
            tuple: (result, error, message)

        Example:
            >>> response = {"success": True, "data": {"count": 100}}
            >>> result, error, message = model_prediction.handle_response(response, "Success", "Failure")
            >>> print(result, error, message)
            {'count': 100} None Success
        """
        if response.get("success"):
            result = response.get("data")
            error = None
            message = success_message
        else:
            result = None
            error = response.get("message")
            message = failure_message
        print(response)
        return result, error, message

    
    #POST REQUESTS
    def request_total_monitor(self,deployment_id=None):
        """
        Monitor the total number of requests for a deployment.

        Args:
            deployment_id (str, optional): The ID of the deployment to monitor.

        Returns:
            tuple: (result, error, message)

        Example:
            >>> result, error, message = model_prediction.request_total_monitor()
            >>> print(result)
            {'total_requests': 1000}
        """
        deployment_id_url=deployment_id if deployment_id else self.deployment_id
        path = f"/v1/model_prediction/monitor/req_total/{deployment_id_url}?projectId={self.project_id}"
        headers = {"Content-Type": "application/json"}
        body={}

        resp = self.rpc.post(path=path, headers=headers, payload=body)  
        return self.handle_response(resp, "Request total monitored successfully",
                                    "An error occured while monitoring the request total.")
        

    def request_count_monitor(self,start_date,end_date,granularity="second",deployment_id=None):
        """
        Monitor request count for a specified time range.

        Args:
            start_date (str): Start date in ISO format.
            end_date (str): End date in ISO format.
            granularity (str, optional): Time granularity. Defaults to "second".
            deployment_id (str, optional): The ID of the deployment to monitor.

        Returns:
            tuple: (result, error, message)

        Example:
            >>> start = "2024-01-28T18:30:00.000Z"
            >>> end = "2024-02-29T10:11:27.000Z"
            >>> result, error, message = model_prediction.request_count_monitor(start, end)
            >>> print(result)
            {'counts': [{'timestamp': '2024-01-28T18:30:00Z', 'count': 50}, ...]}
        """
        path = f"/v1/model_prediction/monitor/request_count"
        headers = {"Content-Type": "application/json"}
        body={
            "granularity":granularity,
            "startDate":start_date,           #"2024-01-28T18:30:00.000Z",
            "endDate":end_date,               #"2024-02-29T10:11:27.000Z",
            "status":"REQ. COUNT",
            "deploymentId": deployment_id if deployment_id else self.deployment_id
            }
        resp = self.rpc.post(path=path, headers=headers, payload=body)  

        return self.handle_response(resp, "Request count monitored successfully",
                                    "An error occured while monitoring the request count.")
    
    def request_latency_monitor(self,start_date,end_date,granularity="second",deployment_id=None):
        """
        Monitor request latency for a specified time range.

        Args:
            start_date (str): Start date in ISO format.
            end_date (str): End date in ISO format.
            granularity (str, optional): Time granularity. Defaults to "second".
            deployment_id (str, optional): The ID of the deployment to monitor.

        Returns:
            tuple: (result, error, message)

        Example:
            >>> start = "2024-01-28T18:30:00.000Z"
            >>> end = "2024-02-29T10:11:27.323Z"
            >>> result, error, message = model_prediction.request_latency_monitor(start, end)
            >>> print(result)
            {'latencies': [{'timestamp': '2024-01-28T18:30:00Z', 'avg_latency': 0.05}, ...]}
        """
        path = f"/v1/model_prediction/monitor/latency"
        headers = {"Content-Type": "application/json"}
        body={
            "granularity":granularity,
             "startDate":start_date,       #"2024-01-28T18:30:00.000Z"
             "endDate":end_date,           #"2024-02-29T10:11:27.323Z"
             "status":"AVG. LATENCY",
             "deploymentId": deployment_id if deployment_id else self.deployment_id
            }
        resp = self.rpc.post(path=path, headers=headers, payload=body)  

        return self.handle_response(resp, "Latency count monitored successfully",
                                    "An error occured while monitoring the latency count.")

    def get_model_prediction(self, image_path, auth_key):
        """
        Fetch model predictions for an image.

        Args:
            image_path (str): Path to the image file.
            auth_key (str): Authentication key for the request.

        Returns:
            tuple: (result, error, message)

        Example:
            >>> result, error, message = model_prediction.get_model_prediction("/path/to/image.jpg", "auth123")
            >>> print(result)
            {'predictions': [{'class': 'cat', 'confidence': 0.95}, ...]}
        """
        url = f"/v1/model_prediction/deployment/{self.deployment_id}/predict"
        files = {'image': open(image_path, 'rb')}
        data = {
            'authKey': auth_key,
        }
        headers = {
            'Authorization': f'Bearer {self.rpc.AUTH_TOKEN.bearer_token}',
        }
        resp = self.rpc.post(url, headers=headers, data=data, files=files)
        return self.handle_response(resp, "Model prediction fetched successfully",
                                    "An error occured while fetching the model prediction.")

    def get_model_test(self,model_train_id,image_path):
        """
        Test a model with a given image.

        Args:
            model_train_id (str): ID of the trained model.
            image_path (str): Path to the image file for testing.

        Returns:
            tuple: (result, error, message)

        Example:
            >>> result, error, message = model_prediction.get_model_test("model123", "/path/to/test_image.jpg")
            >>> print(result)
            {'test_results': {'accuracy': 0.98, 'predictions': [{'class': 'dog', 'confidence': 0.92}, ...]}}
        """
        url=f"/v1/model_prediction/model_test/{model_train_id}?projectId={self.project_id}"
        files={"image": open(image_path, "rb")}
        resp = self.rpc.post(url, files=files)
        return self.handle_response(resp, "Model test successfully",
                                    "An error occured while testing the model.")
    

