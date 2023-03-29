"""This module implements methods which interact the web API for the Plenty
perception object service."""

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, format_url_with_version


class PerceptionObjectServiceClient(BaseClient):
    """Client communicating with the perception object service via REST."""

    _application_name = "PerceptionObjectService"
    _service_name = "perception-object-service"
    _api_version = "v0"

    @staticmethod
    def application_name():
        """Get the application name of the service.
        Returns:
            (str): The application name of the service.
        """
        return PerceptionObjectServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.
        Returns:
            (str): The name of the service.
        """
        return PerceptionObjectServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.
        Returns:
            (str): The api version of this client.
        """
        return PerceptionObjectServiceClient._api_version

    def __init__(self, authenticated_client, url):
        """Create a new perception object store client.
        Args:
            authenticated_client (common.AuthenticatedClient): Plenty service
                client that has credentials.
            url (str): The url to use for the client.
            format_url_with_version
        """
        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version())
        )

    def build_commands(self):
        """Builds the commands for this client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        obj = ["object"], {"help": "the object to ingest"}
        objs = ["object"], {"help": "list of objects to ingest"}
        filters = ["filters"], {"help": "the filters to apply to the query"}
        page_num = (
            ["page"],
            {"help": "the page numer of results to return (100 per page)"},
        )
        obj_uuid = ["uuid"], {"help": "the UUID for the object"}
        label_id = ["label_id"], {"help": "The id for the label"}
        updated_label = ["updated_label"], {"help": "the updated label data"}
        label_sets = (
            ["label_sets"],
            {"help": "the list of label sets to add to the object"},
        )
        label_set_id = ["label_set_id"], {"help": "the id of the label set"}
        updated_label_set = (
            ["updated_label_set"],
            {"help": "The updated label set data"},
        )
        labels = ["labels"], {"help": "the list of labels to add to the label set"}
        tags = ["tags"], {"help": "the list of tags to add to the object"}
        return {
            "ingest": (
                "Ingest objects",
                {
                    "ingest_object": (
                        "ingest passed in object",
                        self.ingest_object,
                        [obj],
                    ),
                    "ingest_list_of_objects": (
                        "ingest list of passed in objects",
                        self.ingest_list_of_objects,
                        [objs],
                    ),
                    "update_object": (
                        "update passed in object",
                        self.update_object,
                        [obj],
                    ),
                },
            ),
            "metadata": (
                "Get object metadata",
                {
                    "get_objects": (
                        "list objects that meet filtering criteria.",
                        self.get_objects,
                        [filters],
                    ),
                    "get_all_objects": (
                        "list all objects.",
                        self.get_all_objects,
                        [page_num],
                    ),
                },
            ),
            "labels": (
                "Manage labels",
                {
                    "get_all_labels": (
                        "Get labels for an object.",
                        self.get_all_labels,
                        [obj_uuid],
                    ),
                    "get_label": (
                        "Get label by id.",
                        self.get_label,
                        [obj_uuid, label_id],
                    ),
                    "update_label": (
                        "Update label by id.",
                        self.update_label,
                        [obj_uuid, label_id, updated_label],
                    ),
                },
            ),
            "label_sets": (
                "Manage label sets",
                {
                    "get_all_label_sets": (
                        "Get all label sets for the object",
                        self.get_all_label_sets,
                        [obj_uuid],
                    ),
                    "add_label_sets": (
                        "Add labels sets to object.",
                        self.add_label_sets,
                        [obj_uuid, label_sets],
                    ),
                    "get_label_set": (
                        "Get label set for object by id.",
                        self.get_label_set,
                        [obj_uuid, label_set_id],
                    ),
                    "update_label_set": (
                        "Update label set for object by id.",
                        self.update_label_set,
                        [obj_uuid, label_set_id, updated_label_set],
                    ),
                    "get_labels_for_label_set": (
                        "Get labels for a label set.",
                        self.get_labels_for_label_set,
                        [obj_uuid, label_set_id],
                    ),
                    "add_labels_to_label_set": (
                        "Add labels to label set.",
                        self.add_labels_to_label_set,
                        [obj_uuid, label_set_id, labels],
                    ),
                },
            ),
            "tags": (
                "Manage tags",
                {
                    "get_tags": ("Get tags for an object.", self.get_tags, [obj_uuid]),
                    "add_tags": (
                        "Add tags to an object.",
                        self.add_tags,
                        [obj_uuid, tags],
                    ),
                },
            ),
        }

    def build_cli_subcommand(self):
        """Bulid the CLI subcommand for this client.
        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return (
            "perception_object",
            "perception object service client",
            "po",
            self.build_commands(),
            lambda s, _: ["".join([p[0] for p in s.split("_")])],
        )

    def ingest_object(self, obj: dict) -> dict:
        """Ingest the object passed in

        Args:
            obj (dict): JSON for object to send in the request

        Returns:
            (dict): Object metadata for ingested object
        """

        return self.__service_client.post(["ingest"], req_json=obj).json()

    def ingest_list_of_objects(self, objs: list) -> list:
        """Ingest the list of objects passed in

        Args:
            objs (list): list of JSON for object to send in the request

        Returns:
            (list): Object metadata for ingested objects
        """

        return self.__service_client.post(["ingest"], req_json=objs).json()

    def update_object(self, obj: dict) -> dict:
        """Update an object passed in updated data

        Args:
            obj (dict): JSON for object to send in the request

        Returns:
            (dict): Object metadata for updated object
        """

        return self.__service_client.put(["ingest"], req_json=obj).json()

    def get_objects(self, filters: dict) -> list:
        """Get a list of objects based on passed in filtering criteria

        Args:
            filters (dict): filters to apply to the returned list of objects

        Returns:
            (list): A list of all objects that meet the filtering criteria.
        """

        return self.__service_client.get(["metadata"], query_args=filters).json()

    def get_all_objects(self, page: int = 1) -> list:
        """list all of the objects in the perception object service

        Args:
            page (int): page of results to return (100 objects per page)

        Returns:
            (list): A list of all objects in the perception object service.
        """
        filters = {"page": page}
        return self.__service_client.get(["metadata"], query_args=filters).json()

    def get_all_labels(self, obj_uuid: str) -> list:
        """Get all labels for object by UUID

        Args:
            obj_uuid (UUID): UUID for object

        Returns:
            labels (list): list of labels for the object
        """
        return self.__service_client.get(["objects", obj_uuid, "labels"]).json()

    def get_label(self, obj_uuid: str, label_id: int) -> dict:
        """Get the label (by id) for an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object
            label_id (int): pk for label

        Returns:
            label (dict): label data
        """
        return self.__service_client.get(["objects", obj_uuid, "labels", label_id]).json()

    def update_label(self, obj_uuid: str, label_id: int, updated_label: dict) -> dict:
        """Update the label (by id) for an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object
            label_id (int): id for label
            updated_label (dict): updated label data

        Returns:
            label (dict): updated label data
        """
        return self.__service_client.put(["objects", obj_uuid, "labels", label_id], req_json=updated_label).json()

    def get_all_label_sets(self, obj_uuid: str) -> list:
        """Get the label sets for an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object

        Returns:
            label sets (list): list of label sets for the object
        """
        return self.__service_client.get(["objects", obj_uuid, "label-sets"]).json()

    def add_label_sets(self, obj_uuid: str, label_sets: list) -> list:
        """Add label sets to an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object
            label_sets (list): label sets to add to object

        Returns:
            label sets (list): label sets added to object
        """
        return self.__service_client.post(["objects", obj_uuid, "label-sets"], req_json=label_sets).json()

    def get_label_set(self, obj_uuid: str, label_set_id: int) -> dict:
        """Get label set (by id) for an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object
            label_set_id (ing): id for label set

        Returns:
            label set (dict): label sets data
        """
        return self.__service_client.get(["objects", obj_uuid, "label-sets", label_set_id]).json()

    def update_label_set(self, obj_uuid: str, label_set_id: int, updated_label_set: dict) -> dict:
        """Update the label set (by id) for an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object
            label_set_id (int): id for label set
            updated_label_set (dict): updated label set data

        Returns:
            label set (dict): updated label set data
        """
        return self.__service_client.put(
            ["objects", obj_uuid, "label-sets", label_set_id],
            req_json=updated_label_set,
        ).json()

    def get_labels_for_label_set(self, obj_uuid: str, label_set_id: int) -> list:
        """Get labels for a label set (by id) for an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object
            label_set_id (int): id for label set

        Returns:
            labels (list): labels in label set for to object
        """
        return self.__service_client.get(["objects", obj_uuid, "label-sets", label_set_id, "labels"]).json()

    def add_labels_to_label_set(self, obj_uuid: str, label_set_id: int, labels: list) -> list:
        """Add labels to label set (by id) for an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object
            label_set_id (int): id for label set
            labels (list): labels to add to label set

        Returns:
            labels (list): labels added to object
        """
        return self.__service_client.post(
            ["objects", obj_uuid, "label-sets", label_set_id, "labels"], req_json=labels
        ).json()

    def get_tags(self, obj_uuid: str) -> list:
        """Get the tags for an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object

        Returns:
            tags (list): list of tags for the object
        """
        return self.__service_client.get(["objects", obj_uuid, "tags"]).json()

    def add_tags(self, obj_uuid: str, tags: list) -> list:
        """Add ltags to an object (by UUID)

        Args:
            obj_uuid (UUID): UUID for object
            tags (list): tags to add to object

        Returns:
            tags (list): tags added to object
        """
        return self.__service_client.post(["objects", obj_uuid, "tags"], req_json=tags).json()
