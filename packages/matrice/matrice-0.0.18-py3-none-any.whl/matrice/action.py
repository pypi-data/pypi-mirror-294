import sys

class Action:
    def __init__(self, session, action_id):
        self.action_id = action_id
        data, error = get_action_details(session, action_id)
        if error is not None:
            print(f"An error occured while fetching action details: \n {error}")
        else:
            self.action_type = data["action"]
            self.project_id = data["_idProject"]
            self.user_id = data["_idUser"]
            self.step_code = data["stepCode"]
            self.status = data["status"]
            self.created_at = data["createdAt"]
            self.service_name = data["serviceName"]




def get_action_details(session, action_id):
    path = f"/v1/project/action/{action_id}/details"
    resp = session.rpc.get(path=path)
    if resp.get("success"):
        return resp.get("data"), None
    else:
        return resp.get("data"), resp.get("message")