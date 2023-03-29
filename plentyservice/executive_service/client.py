"""This module implements methods which interact the web API for the Plenty executive service."""

from typing import Dict, List, Optional

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, format_url_with_version, str_to_json
from uuid import uuid4
import json


class ExecutiveServiceClient(BaseClient):
    """Client communicating with the Plenty executive service via REST."""

    _application_name = "Executive Service"
    _service_name = "executive-service"
    _api_version = "v1"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return ExecutiveServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return ExecutiveServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return ExecutiveServiceClient._api_version

    @staticmethod
    def get_headers(submitter: Optional[str] = None, submission_method: Optional[str] = None):
        """Optional headers to include with "tell" and "request" api calls.

         Args:
            submitter (str): User name of the person submitting the tell/request.
            submission_method (str): Identifies the source of the submission (e.g., FarmOS UI)

        Returns:
            (dict): headers to be sent along with "tell" and "request" api calls.
        """
        additional_headers = {"x-request-id": str(uuid4())}
        if submitter is not None:
            additional_headers["x-submitter"] = submitter
        if submission_method is not None:
            additional_headers["x-submission-method"] = submission_method
        return additional_headers

    def __init__(self, authenticated_client, url):
        """Create a new traceability store client.

        Args:
            authenticated_client (common.AuthenticatedClient): Plenty service
                client that has credentials.
            url (str): The url to use for the client.
        """
        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version())
        )

    def build_commands(self):
        """Stub for building the commands for this client."""
        return {}

    def build_cli_subcommand(self):
        """Bulid the CLI subcommand for this client.

        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return ("executive", "executive service client", "es", self.build_commands(), lambda s, _: [s[0]])

    def get_container_by_lot_name(self, lot_name: str):
        """Get container by material lot name.

        Args:
            lot_name (string): the material lot name of the container

        Returns:
            FarmState JSON
        """
        resp = self.__service_client.get("farm/state/containers/by-lot-name", query_args={"lotName": lot_name})
        return resp.json()

    def upsert_container(self, container_dict: dict):
        """Attempt to create a container.

        Args:
            container_dict (dict): the payload representing the container to be
                                    created as a dictionary, e.g.

        {
            "type": "Tray",
            "resourceState": {
                "location": {
                    "machine": {
                        "traceabilityMachineId": "6acc9369-756a-4ebf-a8eb-3654bc752890",
                        "farmdefMachineId": "63f59464-9754-4c76-a57d-8c5cad398c5d",
                        "siteName": "LAX1",
                        "areaName": "TableAutomation",
                        "lineName": "TrayLoad"
                    }
                },
                "containerObj": {
                    "serial": "P900-0008529A:AAAA-BBBB-47",
                    "containerType": "TRAY"
                },
                "materialObj": {
                    "lotName": "7c4c636f-1b76-47fa-be87-c49f6d61b0e7",
                    "materialType": "LOADED_TRAY",
                    "product": "WHR"
                },
                "quantity": 1.0
            }
        }

        Returns: JSON representing the new container
        """
        resp = self.__service_client.post("farm/state/upsert-container", req_json=container_dict)
        return resp.json()

    def resource_operation(self, operation_dict: dict):
        """Attempt to perform an operation against resources.

        Args:
            operation_dict (dict): the payload representing the operation to be
                                    performed against resources, e.g.

            {
                "type": "LoadContainersIntoContainer",
                "path": "sites/LAX1/areas/TableAutomation/lines/TrayLoad",
                "loadedContainerSerials": [
                    "P900-0008529A:9MRZ-OU8F-GZ"
                ],
                "loadedContainerType": "TRAY",
                "intoContainerSerial": "P900-0008046A:EDYA-2KUA-X6",
                "intoContainerType": "TABLE",
                "loadedContainerPositions": {
                    "P900-0008529A:9MRZ-OU8F-GZ": "A0"
                }
            }

        Returns: JSON representing an HTTP response
        """
        resp = self.__service_client.post("farm/state/resource-operation", req_json=operation_dict)
        return resp.json()

    def tell(self, path: str, args: dict):
        """Make a call to Executive Service asynchronous tell API.

        Args:
            path (str): The path to the tell defined in FarmDef.
            args (dict): The dictionary that contains all arguments needed for the given transaction due to the corresponding proto message defined in FarmDef.

        Returns: Response object
        """

        additional_headers = self.get_headers(args["submitter"], args["submission_method"])
        args.pop("submitter", None)
        args.pop("submission_method", None)

        resp = self.__service_client.post(
            ["tell", path.lstrip("/")], req_json=args, additional_headers=additional_headers
        )

        # "tell" post is asynchronous, so service returns 204 (no content)
        # indicating transaction has been accepted and is processing.
        if resp.status_code == 204:
            return {"status": "processing"}

        return resp.json()

    def create_workbin_instance(self, workbin_task_instance: dict):
        resp = self.__service_client.post("workbins", req_json=workbin_task_instance)
        return resp.json()

    def update_workbin_instance(self, workbin_task_instance: dict):
        resp = self.__service_client.put("workbins", req_json=workbin_task_instance)
        return resp.json()

    def get_workcenter_plan(self, planned_date: str, workcenter: str):
        """Try to get a workcenter plan based on a planned date and a
        workcenter.

        Args:
            planned_date (str): the date we are looking for a WorkcenterPlan in
            workcenter (str): the workcenter we are looking for a
            WorkcenterPlan in

        Returns: a WorkcenterPlan if one exists, None otherwise
        """
        return self.__service_client.get(
            "workcenter-plans", query_args={"plannedDate": planned_date, "workcenter": workcenter}
        ).json()

    def create_workcenter_plan(self, workcenter_plan: dict):
        """Create a WorkcenterPlan based on the plan details.

        Args:
            workcenter_plan (dict): the payload required to create the
        WorkcenterPlan as a dictionary, e.g.
        {"plannedDate": "2021-01-21",
        "workcenter": "sites/LAX1/areas/TrayAutomation",
        "taskOrdering": []}

        Returns: the created WorkcenterPlan
        """
        resp = self.__service_client.post("workcenter-plans", req_json=workcenter_plan)
        return resp.json()

    def update_workcenter_plan(self, workcenter_plan: dict):
        """Update a WorkcenterPlan by modifying the "taskOrdering".

        Args:
            workcenter_plan (dict): the payload to update the plan with, e.g.
        {"plannedDate": "2021-01-21",
        "workcenter": "sites/LAX1/areas/TrayAutomation",
        "taskOrdering": ["bc9671ee-6eed-4863-8f81-7828b433d70f"]}

        Returns: the updated WorkcenterPlan
        """
        resp = self.__service_client.put("workcenter-plans", req_json=workcenter_plan)
        return resp.json()

    def execute_workcenter_plan(self, workcenter_plan: dict):
        """Attempt to execute a WorkcenterPlan.

        Args:
            workcenter_plan (dict): the payload representing the
        WorkcenterPlan details as a dictionary, e.g.
        {"plannedDate": "2021-01-21",
        "workcenter": "sites/LAX1/areas/TrayAutomation"}

        Returns: the WorkcenterPlan after it started execution
        """
        resp = self.__service_client.post("workcenter-plans/execute", req_json=workcenter_plan)
        return resp.json()

    def pause_workcenter_plan(self, workcenter_plan: dict):
        """Attempt to pause a WorkcenterPlan.

        Args:
            workcenter_plan (dict): the payload representing the
        WorkcenterPlan details as a dictionary, e.g.
        {"plannedDate": "2021-01-21",
        "workcenter": "sites/LAX1/areas/TrayAutomation"}

        Returns: the WorkcenterPlan after it started execution
        """
        resp = self.__service_client.post("workcenter-plans/pause", req_json=workcenter_plan)
        return resp.json()

    def resume_workcenter_plan(self, workcenter_plan: dict):
        """Attempt to resume a WorkcenterPlan.

        Args:
            workcenter_plan (dict): the payload representing the
        WorkcenterPlan details as a dictionary, e.g.
        {"plannedDate": "2021-01-21",
        "workcenter": "sites/LAX1/areas/TrayAutomation"}

        Returns: the WorkcenterPlan after it started execution
        """
        resp = self.__service_client.post("workcenter-plans/resume", req_json=workcenter_plan)
        return resp.json()

    def complete_workcenter_plan(self, workcenter_plan: dict):
        """Attempt to complete a WorkcenterPlan.

        Args:
            workcenter_plan (dict): the payload representing the
        WorkcenterPlan details as a dictionary, e.g.
        {"plannedDate": "2021-01-21",
        "workcenter": "sites/LAX1/areas/TrayAutomation"}

        Returns: the WorkcenterPlan after it was completed
        """
        resp = self.__service_client.post("workcenter-plans/complete", req_json=workcenter_plan)
        return resp.json()

    def delete_workcenter_plan(self, workcenter_plan: dict):
        """Delete a given WorkcenterPlan.

        Args:
            workcenter_plan (dict): the plan we want to delete, plannedDate and
        workcenter used to identify the record. E.G.
        {"plannedDate": "2021-01-21",
        "workcenter": "sites/LAX1/areas/TrayAutomation",
        "taskOrdering": ["bc9671ee-6eed-4863-8f81-7828b433d70f"]}

        Returns: the number of records that were deleted (0 or 1)
        """
        resp = self.__service_client.delete("workcenter-plans", req_json=workcenter_plan)
        return resp.json()

    def get_workcenter_task_details(self, task_id: str):
        """Get a WorkcenterTaskDetail based on a given id.

        Args:
            task_id (str): a UUID representing the task id

        Returns: the WorkcenterTaskDetail if one is found, None otherwise
        """
        return self.__service_client.get(f"workcenter-task-details/{task_id}").json()

    def create_workcenter_task_details(self, workcenter_task_details: dict):
        """Create a WorkcenterTaskDetail based on the input payload.

        Args:
            workcenter_task_details (dict): the task payload as a dictionary,
            e.g.
        {
            "id": "bc9671ee-6eed-4863-8f81-7828b433d70f",
            "workcenter": "sites/LAX1/farms/LAX1/workCenters/Seed",
            "planId": "1c114c52-7fc0-4e7b-adae-c196a914aafd",
            "taskPath": "sites/LAX1/farms/LAX1/workCenters/Seed/interfaces/Seed/methods/SeedTraysAndLoadTableToGerm",
            "taskParametersJsonPayload": '{"table_serial": "800-00009336:TBL:000-000-123", "germ_stack_path": {"value": "sites/LAX1/areas/Germination/lines/GerminationLine/machines/GermStack1"}, "seed_trays_and_load_to_table_prescription": {"entry1": {"numberOfTrays": 1, "crop": "WHR"}}}',
        }

        Returns: the created WorkcenterTaskDetail
        """
        resp = self.__service_client.post("workcenter-task-details", req_json=workcenter_task_details)
        return resp.json()

    def update_workcenter_task_details(self, task_id: str, workcenter_task_details: dict):
        """Update the changeable fields of a WorkcenterTaskDetail based on the
        task id.

        Args:
            task_id (str): the id of the  task we want to edit
            workcenter_task_details (dict): the new taskParametersJsonPayload we
        want to set for the task. E.G.
        {
            "taskParametersJsonPayload": '{"table_serial": "800-00009336:TBL:000-000-123", "germ_stack_path": {"value": "sites/LAX1/areas/Germination/lines/GerminationLine/machines/GermStack1"}, "seed_trays_and_load_to_table_prescription": {"entry1": {"numberOfTrays": 2, "crop": "WHR"}}}'
        }

        Returns: the updated WorkcenterTaskDetail
        """
        resp = self.__service_client.put(f"workcenter-task-details/{task_id}", req_json=workcenter_task_details)
        return resp.json()

    def delete_workcenter_task_details(self, task_id: str):
        """Delete a WorkcenterTaskDetail based on the task id.

        Args:
            task_id (str): a UUID that identifies the task we want to delete

        Returns: the number of records that got deleted
        """
        resp = self.__service_client.delete(f"workcenter-task-details/{task_id}")
        return resp.json()

    def get_durative_task_by_id(self, task_id: str):
        """For given task id, get the durative task details.

        Args:
            task_id (str): a UUID that identifies the task.

        Returns: a durative task state.
        """
        resp = self.__service_client.get(["durative-tasks/by-id"], query_args={"taskId": task_id})
        # workaround until this is fixed: https://plentyag.atlassian.net/browse/SD-17570
        try:
            return resp.json()
        except json.decoder.JSONDecodeError:
            return ""

    def get_durative_tasks_by_ids(self, task_ids: List[str]):
        """Bulk method to get list of task from given task ids

        Args:
            task_ids: list of tasks ids

        Returns: list of durative task states
        """
        resp = self.__service_client.post(["durative-tasks/list-of-ids"], req_json=task_ids)
        return resp.json()

    def get_durative_tasks_by_site(self, siteName: str, taskStatus: str):
        """Bulk method to get list of task from given site name with filter support of task status

        Args:
            siteName (str): site name
            taskStatus (enum): one of the statuses i.e. CREATED, QUEUED, RUNNING, COMPLETED, FAILED, CANCELLING, CANCELED

        Returns: list of durative task states
        """
        resp = self.__service_client.get(
            ["durative-tasks/by-site-with-status"], query_args={"siteName": siteName, "taskStatus": taskStatus}
        )
        return resp.json()

    def get_all_durative_leaf_tasks_by_id(self, task_id: str):
        """For a given workcenter page task id, gets all of the durative tasks

        Args:
            task_id (str):a UUID that identifies the workcenter page.

        Returns: an array of durative leaf tasks state.
        """
        resp = self.__service_client.get(["durative-tasks/all-leafs-by-id"], query_args={"taskId": task_id})
        return resp.json()

    def request(self, path: str, args: dict):
        """Make a call to Executive Service synchronous request API.

        Args:
            path (str): The path to the request defined in FarmDef.
            args (dict): The dictionary that contains all arguments needed for the given request due to the corresponding proto message defined in FarmDef.

        Returns: Response object
        """

        additional_headers = self.get_headers(args["submitter"], args["submission_method"])
        args.pop("submitter", None)
        args.pop("submission_method", None)

        resp = self.__service_client.post(
            ["request", path.lstrip("/")],
            req_json=args,
            additional_headers=additional_headers,
        )

        return resp.json()

    def upgrade_firmware(self, data: Dict) -> Dict:
        return self.__service_client.post(["devices/upgrade-firmware"], req_json=str_to_json(data)).json()

    def get_reactor_paths(self, sitePath: str) -> Dict:
        return self.__service_client.get(["reactors/paths"], query_args={"sitePath": sitePath}).json()

    def get_reactor_state(self, reactorPath: str) -> Dict:
        return self.__service_client.get([f"reactors/{reactorPath}/state"]).json()

    def get_reactors_health(self, sitePath: str) -> Dict:
        return self.__service_client.get(["reactors/health"], query_args={"sitePath": sitePath}).json()

    def stop_reactor(self, data: Dict):
        resp = self.__service_client.post(f"reactors/stop/{str_to_json(data)['reactorPath']}")
        return resp.json()

    def start_reactor(self, data: Dict):
        resp = self.__service_client.post(f"reactors/start/{str_to_json(data)['reactorPath']}")
        return resp.json()

    def restart_reactor(self, data: Dict):
        resp = self.__service_client.post(f"reactors/restart/{str_to_json(data)['reactorPath']}")
        return resp.json()

    def cancel_reactor_task(self, data: Dict):
        post_data = str_to_json(data)
        resp = self.__service_client.post(f"reactors/{post_data['reactorPath']}/cancel-task/{post_data['taskId']}")
        return resp.json()
