"""Module for Session class handling project sessions."""
from matrice.rpc import RPC
from matrice.projects import Projects
import os

class Session:
    """Class to manage sessions."""

    def __init__(self, account_number = "", project_id="", project_name = ""):
        """
        Initialize a new session instance.

        Parameters
        ----------
        account_number : str
            The account number associated with the session.
        project_id : str, optional
            The ID of the project for this session.

        Example
        -------
        >>> session = Session(account_number="9625383462734064921642156")
        """
        # assert project_id, "project_id is empty"
        self.rpc = RPC(project_id=project_id)
        self.account_number = account_number
        self.project_id = project_id
        self.project_name = project_name

        if self.project_name:
            self.project_id = self._get_project_id_by_name()
            self.update_session(self.project_id)

    def _get_project_id_by_name(self):
        path = f"/v1/project/get_project_by_name?name={self.project_name}"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            return resp["data"]["_id"]
        else:
            print("Could not fetch project details", resp.get("message"))
        

    def update_session(self, project_id=""):
        """
        Update the session with new project details.

        Parameters
        ----------
        project_id : str, optional
            The new ID of the project.


        Example
        -------
        >>> session.update_session(project_id="660b96fc019dd5321fd4f8c7")
        """
        self.project_id = project_id
        self.rpc = RPC(project_id=project_id)

    def close(self):
        """
        Close the current session by resetting the RPC and project details.

        Example
        -------
        >>> session.close()
        """
        self.rpc = None
        self.project_id = None

    def _create_project(self, project_name, input_type, output_type):
        """
        Create a new project with specified parameters.

        Parameters
        ----------
        project_name : str
            The name of the project to be created.
        input_type : str
            The type of input for the project (e.g., 'image').
        output_type : str
            The type of output for the project (e.g., 'classification').

        Returns
        -------
        tuple
            A tuple containing the response data, error message (if any).

        Example
        -------
        >>> response, error = session._create_project("New Project", "image", "classification")
        >>> if error:
        >>>     print(f"Error: {error}")
        >>> else:
        >>>     print(f"Project created with ID: {response['_id']}")
        """
        enabled_platforms = {
            'android': False,
            'ios': False,
            'tpu': False,
            'intelCPU': False,
            'gcloudGPU': False
        }
        path = "/v1/project"
        headers = {"Content-Type": "application/json"}
        body = {
            "name": project_name,
            "inputType": input_type,
            "outputType": output_type,
            "enabledPlatforms": enabled_platforms,
            "accountType": "",
            'accountNumber': self.account_number,
        }
        resp = self.rpc.post(path=path, headers=headers, payload=body)
        if resp.get("success"):
            resp_data = resp.get("data")
            return resp_data, None
        else:
            error = resp.get("message")
            return None, error

    def create_classification_project(self, project_name):
        """
        Create a classification project.

        Parameters
        ----------
        project_name : str
            The name of the classification project to be created.

        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.

        Example
        -------
        >>> project = session.create_classification_project("Image Classification Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        resp, error = self._create_project(
            project_name=project_name,
            input_type="image",
            output_type="classification"
        )

        if error is not None:
            print(f'Could not create project: \n {error}')
        else:
            P = Projects(session=Session(self.account_number, project_id=resp["_id"], project_name=resp["name"]) , project_name=resp["name"])
            return P

    def create_detection_project(self, project_name):
        """
        Create a detection project.

        Parameters
        ----------
        project_name : str
            The name of the detection project to be created.

        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.

        Example
        -------
        >>> project = session.create_detection_project("Object Detection Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        resp, error = self._create_project(
            project_name=project_name,
            input_type="image",
            output_type="detection"
        )
        if error is not None:
            print(f'Could not create project: \n {error}')
        else:
            P = Projects(session=Session(self.account_number, project_id=resp["_id"], project_name=resp["name"]) , project_name=resp["name"])
            return P

    def create_segmentation_project(self, project_name):
        """
        Create a segmentation project.

        Parameters
        ----------
        project_name : str
            The name of the segmentation project to be created.

        Returns
        -------
        Projects
            An instance of the Projects class for the created project, or None if an error occurred.

        Example
        -------
        >>> project = session.create_segmentation_project("Instance Segmentation Project")
        >>> if project:
        >>>     print(f"Created project: {project}")
        >>> else:
        >>>     print("Could not create project.")
        """
        resp, error = self._create_project(
            project_name=project_name,
            input_type="image",
            output_type="instance_segmentation"
        )
        if error is not None:
            print(f'Could not create project: \n {error}')
        else:
            P = Projects(session=Session(self.account_number, project_id=resp["_id"], project_name=resp["name"]) , project_name=resp["name"])
            return P

    def list_projects(self, project_type=""):
        """
        List projects based on the specified type.

        Parameters
        ----------
        project_type : str, optional
            The type of projects to list (e.g., 'classification', 'detection'). If empty, all projects are listed.

        Returns
        -------
        tuple
            A tuple containing the list of projects data and a message indicating the result of the fetch operation.

        Example
        -------
        >>> projects, message = session.list_projects("classification")
        >>> print(message)
        Projects fetched successfully
        >>> for project in projects:
        >>>     print(project)
        """
        path = "/v1/project/v2"
        if project_type != "":
            path = path + f"?items[0][field]=outputType&items[0][operator]=is&items[0][value]={project_type}&logicOperator=and"
        resp = self.rpc.get(path=path)
        if resp.get("success"):
            return resp.get("data"), "Projects fetched successfully"
        else:
            message = resp.get("message")
            return None, f"Failed to fetch projects: \n {message}"

def create_session(account_number, access_key, secret_key):
    """
    Create and initialize a new session with specified credentials.

    Parameters
    ----------
    account_number : str
        The account number to associate with the new session.
    access_key : str
        The access key for authentication.
    secret_key : str
        The secret key for authentication.

    Returns
    -------
    Session
        An instance of the Session class initialized with the given credentials.

    Example
    -------
    >>> session = create_session("9625383462734064921642156", "HREDGFXB6KI0TWH6UZEYR", "UY8LP0GQRKLSFPZAW1AUF")
    >>> print(session)
    <Session object at 0x...>
    """
    S = Session(account_number=account_number)
    os.environ['MATRICE_ACCESS_KEY_ID'] = access_key
    os.environ['MATRICE_SECRET_ACCESS_KEY'] = secret_key
    return S
