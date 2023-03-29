"""This module implements methods which interact the web API for
the Plenty Workbin Service"""
from urllib import parse
import requests

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, format_url_with_version, str_to_json


class WorkbinServiceClient(BaseClient):
    """Client communicating with the Plenty workbin-service via REST"""

    _service_name = "workbin-service"
    _api_version = "v1"

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return WorkbinServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return WorkbinServiceClient._api_version

    def __init__(self, authenticated_client, url):
        """Create a new workbin service client.
        Args:
            authenticated_client (common.AuthenticatedClient): Plenty service
                client that has credentials.
            url (str): The url to use for the client.

        """
        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version())
        )
        self.__auth_client = authenticated_client
        self.__service_url = url

    def build_commands(self):
        """Builds the commands for this client.
        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        return {}

    def build_cli_subcommand(self):
        """Build the CLI subcommand for this client.
        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return (
            "workbin_service",
            "workbin service client",
            "wbs",
            self.build_commands(),
            lambda s, _: [s[0]],
        )

    # --------------- Health ---------------

    def health(self):
        """
        Returns health status
        @return: Status message is everything ok.
        """
        return self.__auth_client.make_request(requests.get, self.__service_url, ["health"], False, None, None).text

    # --------------- Workbin Definition API ---------------

    def upsert_workbin_task_definition(self, workbin_task_definition: dict):
        """Create workbin task definition.

        @param workbin_task_definition: Dict representing WorkbinTaskDefinition.
        @return: WorkbinTaskDefinition
        """
        body = str_to_json(workbin_task_definition)
        return self.__service_client.post(["workbin", "definition"], req_json=body).json()

    def get_workbin_task_definition_by_id(self, id):
        """Get workbin task definition.

        @param id: id representing WorkbinTaskDefinition UUID
        @return: WorkbinTaskDefinition
        """
        return self.__service_client.get(["workbin", "definition"], query_args={"definitionId": id}).json()

    def filter_workbin_task_definitions(self, filter: dict):
        """Filter workbin task definitions.

        @param filter: Dict representing WorkbinTaskDefinitionFilter object
        @return: List of WorkbinTaskDefinition
        """
        body = str_to_json(filter)
        return self.__service_client.post(["workbin", "definition", "filter"], req_json=body).json()

    def delete_workbin_task_definition_by_id(self, id):
        """Delete workbin task definition.

        @param id: id representing WorkbinTaskDefinition UUID
        @return: WorkbinTaskDefinition
        """
        return self.__service_client.delete(["workbin", "definition"], query_args={"taskId": id}).json()

    # --------------- Workbin Task Instance API ---------------

    def upsert_workbin_task_instance(self, workbin_task_instance: dict):
        """Create workbin task instance.

        @param workbin_task_instance: Dict representing WorkbinTaskInstance.
        @return: UnifiedWorkbinTaskInstance
        """
        body = str_to_json(workbin_task_instance)
        return self.__service_client.post(["workbin", "instance"], req_json=body).json()

    def get_workbin_task_instance_by_id(self, id):
        """Get workbin task instance.

        @param id: id representing WorkbinTaskInstance UUID
        @return: UnifiedWorkbinTaskInstance
        """
        return self.__service_client.get(["workbin", "instance"], query_args={"taskId": id}).json()

    def filter_workbin_task_instances(self, filter: dict):
        """Filter workbin task instances.

        @param filter: Dict representing WorkbinTaskInstanceFilter object
        @return: List of UnifiedWorkbinTaskInstance
        """
        body = str_to_json(filter)
        return self.__service_client.post(["workbin", "instance", "filter"], req_json=body).json()

    def delete_workbin_task_instance_by_id(self, id):
        """Delete workbin task instance.

        @param id: id representing WorkbinTaskInstance UUID
        @return: UnifiedWorkbinTaskInstance
        """
        return self.__service_client.delete(["workbin", "instance"], query_args={"taskId": id}).json()

    # --------------- Workbin Task Comment API ---------------

    def create_workbin_task_comment(self, workbin_task_comment: dict):
        """Create workbin task instance.

        @param workbin_task_comment: Dict representing WorkbinTaskComment.
        @return: UnifiedWorkbinTaskInstance
        """
        body = str_to_json(workbin_task_comment)
        return self.__service_client.post(["workbin", "comment"], req_json=body).json()

    def get_workbin_task_comment_by_id(self, id):
        """Get workbin task comment.

        @param id: id representing WorkbinTaskComment UUID
        @return: WorkbinTaskComment
        """
        return self.__service_client.get(["workbin", "comment"], query_args={"commentId": id}).json()

    def filter_workbin_task_comments(self, filter: dict):
        """Filter workbin task comments.

        @param filter: Dict representing WorkbinTaskCommentFilter object
        @return: List of WorkbinTaskComment
        """
        body = str_to_json(filter)
        return self.__service_client.post(["workbin", "comment", "filter"], req_json=body).json()

    # --------------- Workbin Groups API ---------------
    def create_workbin_task_group(self, workbin_group: dict):
        """Create workbin group instance.

        @param workbin_group: Dict representing WorkbinGroup.
        @return: the JSON representation of the newly created WorkbinGroup"""
        body = str_to_json(workbin_group)
        return self.__service_client.post(["workbin", "group"], req_json=body).json()

    def filter_workbin_task_group(self, filter: dict):
        """Filter workbin groups.

        @param filter: Dict representing WorkbinGroupFilter object.
        @return: List of WorkbinGroup"""
        body = str_to_json(filter)
        return self.__service_client.post(["workbin", "group", "filter"], req_json=body).json()

    def add_definition_to_group(self, farm: str, group_name: str, definition_type: str):
        args = {"farm": farm, "groupName": group_name, "definitionType": definition_type}
        return self.__service_client.get(["workbin", "group", "definition", "add"], query_args=args).json()

    def remove_definition_from_group(self, farm: str, group_name: str, definition_type: str):
        args = {"farm": farm, "groupName": group_name, "definitionType": definition_type}
        return self.__service_client.get(["workbin", "group", "definition", "remove"], query_args=args).json()

    # --------------- Workbin Task Values API ---------------
    def get_valid_workbin_task_groups(self):
        """Get list of valid workbin task group enum values.

        @return: List of WorkbinTaskGroup values
        """
        return self.__service_client.post(["workbin", "values", "groups"]).json()

    def get_valid_workbin_task_priorities(self):
        """Get list of valid workbin task priority enum values.

        @return: List of WorkbinTaskPriority values
        """
        return self.__service_client.post(["workbin", "values", "priority"]).json()

    def get_valid_workbin_task_fields(self):
        """Get list of valid workbin task field enum values.

        @return: List of WorkbinTaskFieldTypeValues values
        """
        return self.__service_client.post(["workbin", "values", "fields"]).json()

    def __url_encode(self, str):
        """
        Returns a URL encoded string, such that forward slashes '/' are properly encoded
        to prevent issues with GET endpoints
        @param str: string to URL encode
        @return: URL encoded string
        """
        return parse.quote(str, safe="")
