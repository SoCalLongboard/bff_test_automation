"""This module implements methods which interact the web API for
the Plenty traceability quality 3.0 service"""
from urllib import parse
import requests

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, format_url_with_version, str_to_json


class TraceabilityService3Client(BaseClient):
    """Client communicating with the Plenty traceability-service 3.0 service
    via REST

    """

    _service_name = "traceability-service"
    _api_version = "v0"

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return TraceabilityService3Client._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return TraceabilityService3Client._api_version

    def __init__(self, authenticated_client, url):
        """Create a new traceability service client.
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
            "traceability_service",
            "traceability service client",
            "ts3",
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

    # --------------- Traceability API ---------------

    def run_operation(self, operation):
        """
        Run operation, contains list of parameters, each one represents
        the input state id and state change information.
        @param operation: Dict representing OperationRequest.
        @return: OperationResponse
        """
        operation = str_to_json(operation)
        return self.__service_client.post(["operation", "run"], req_json=operation).json()

    def scrap_material(self, id, process_id, id_type=None):
        """
        Scrap material from container by state ID. Set material status to SCRAPPED,
        and corresponding container's status to DIRTY. Creates new state.
        @param id: Latest state ID of container with material or another state identifier according to id_type, str.
        @param process_id: Current process ID, int.
        @param id_type: Optional string parameter to change type of passed state_id. Allowed values: RESOURCE_STATE_ID, CONTAINER_ID, MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
        @return: OperationResponse
        """
        return self.__service_client.delete(
            ["operation", "material"],
            query_args={"id": id, "processId": process_id, "idType": id_type},
        ).json()

    def wash_container(self, id, process_id, id_type=None):
        """
        Wash Container by latest state ID, change status to CLEAN.
        @param id: Latest state ID of container or another state identifier according to id_type, str.
        @param process_id:
        @param id_type: Optional string parameter to change type of passed state_id. Allowed values: RESOURCE_STATE_ID, CONTAINER_ID, MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
        @return: OperationResponse
        """
        return self.__service_client.post(
            ["operation", "container", "wash"],
            query_args={"id": id, "processId": process_id, "idType": id_type},
            req_json=str_to_json({}),
        ).json()

    def trash_container(self, id, process_id, id_type=None):
        """
        Trash Container by latest state ID, change status to TRASHED.
        @param id: Latest state ID of container or another state identifier according to id_type, str.
        @param process_id:
        @param id_type: Optional string parameter to change type of passed state_id. Allowed values: RESOURCE_STATE_ID, CONTAINER_ID, MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
        @return: OperationResponse
        """
        return self.__service_client.delete(
            ["operation", "container"],
            query_args={"id": id, "processId": process_id, "idType": id_type},
        ).json()

    def untrash_container(self, id, process_id, id_type=None):
        """
        UnTrash Container by latest state ID, change status to DIRTY.
        @param id: Latest state ID of container or another state identifier according to id_type, str.
        @param process_id:
        @param id_type: Optional string parameter to change type of passed state_id. Allowed values: RESOURCE_STATE_ID, CONTAINER_ID, MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
        @return: OperationResponse
        """
        return self.__service_client.post(
            ["operation", "container", "untrash"],
            query_args={"id": id, "processId": process_id, "idType": id_type},
        ).json()

    def move_container(self, id, process_id, location, id_type=None):
        """
        Move container between site, machine, process. Creates new state.
        @param id: Latest state ID or another state identifier according to id_type, str.
        @param location: Location object, dict or json str.
        @param process_id: Current process ID, int.
        @param id_type: Optional string parameter to change type of passed state_id. Allowed values: RESOURCE_STATE_ID, CONTAINER_ID, MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
        @return: OperationResponse
        """
        location = str_to_json(location)
        return self.__service_client.post(
            ["operation", "container", "move"],
            query_args={"id": id, "processId": process_id, "idType": id_type},
            req_json=location,
        ).json()

    def add_label(self, id, label_type, label, process_id, id_type=None):
        """
        Add label to state. Creates new state.
        @param id: Latest state ID or another state identifier according to id_type, str.
        @param label_type: Type of label either CONTAINER or MATERIAL, str.
        @param label: Label to add, str.
        @param process_id: Current process ID, int.
        @param id_type: Optional string parameter to change type of passed state_id. Allowed values: RESOURCE_STATE_ID, CONTAINER_ID, MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
        @return: OperationResponse
        """
        return self.__service_client.post(
            ["operation", "label"],
            query_args={
                "id": id,
                "labelType": label_type,
                "label": label,
                "processId": process_id,
                "idType": id_type,
            },
            req_json=str_to_json({}),
        ).json()

    def remove_label(self, id, label, process_id, id_type=None, operation_type=None):
        """
        Remove labels from both state fields: containerLabels, materialLabels. Creates new state.
        @param id: Latest state ID or another state identifier according to id_type, str.
        @param label: Label to remove, str.
        @param process_id: Current process ID, int.
        @param id_type: Optional string parameter to change type of passed state_id. Allowed values: RESOURCE_STATE_ID, CONTAINER_ID, MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
        @param operation_type: Optional string parameter to change operation type name. Allowed values: REMOVE_LABEL, REWORK
        @return: OperationResponse
        """
        return self.__service_client.delete(
            ["operation", "label"],
            query_args={
                "id": id,
                "label": label,
                "processId": process_id,
                "idType": id_type,
                "operationType": operation_type,
            },
        ).json()

    def update_material(self, material, process_id):
        """
        Updates the Material definition's product and properties field based on
        present changes.

        @param material: Material definition
        @param process_id: Current process ID, int.
        @return: OperationResponse
        """
        material = str_to_json(material)
        return self.__service_client.post(
            ["operation", "material", "update"],
            query_args={"processId": process_id},
            req_json=material,
        ).json()

    def get_add_label_operations(self, id, id_type):
        """
        Get a list of stored add label operations.
        @param id: ID of resource (material ID, container ID, etc).
        @param id_type: Type of resource ID.
                        Valid values are: CONTAINER_ID and MATERIAL_ID.
        @return: List of OperationResponse objects.
        """
        query_args = {"id": id, "idType": id_type}
        return self.__service_client.get(["operation", "label", "list"], query_args=query_args).json()

    # --------------- FarmState API ---------------

    def get_resources_in_use(self, criteria: dict):
        """
        Get all containers and/or materials in use by criteria fields: 'siteName', 'limit', 'offset'.
        @param criteria: Dict of <field>: <value> filter params.
        @return: List of containers and/or materials in use.
        """
        return self.__service_client.post(["farmstate", "in-use"], req_json=criteria).json()

    def filter_containers(self, criteria: dict):
        """
        Filter containers by criteria fields: 'site', 'status', 'type', 'startDt', 'endDt'.
        @param criteria: Dict of <field>: <value> filter params. `site` is required.
        @return: List of containers.
        """
        return self.__service_client.post(["farmstate", "filter", "container"], req_json=criteria).json()

    def filter_materials(self, criteria: dict):
        """
        Filter material by criteria fields: 'site', 'status', 'type', 'product', 'startDt', 'endDt'.
        @param criteria: Dict of <field>: <value> filter params. `site` is required.
        @return: List of materials.
        """
        return self.__service_client.post(["farmstate", "filter", "material"], req_json=criteria).json()

    def filter_states(self, criteria: dict):
        """
        Filter latest states by criteria fields: 'site', 'containerId', 'materialId',
                                                 'machineId', 'startDt'.
        @param criteria: Dict of <field>: <value> filter params. `site` is required.
        @return: List of states.
        """
        return self.__service_client.post(["farmstate", "filter", "state"], req_json=criteria).json()

    def filter_operations(self, criteria: dict):
        """
        Filter operations by criteria fields: 'site', 'status', 'startDt', 'endDt'.
        @param criteria: Dict of <field>: <value> filter params. `site` is required.
                         Both, or neither `startDt` nor `endDt` should be set.
        @return: List of containers.
        """
        return self.__service_client.post(["farmstate", "filter", "operation"], req_json=criteria).json()

    def filter_labels(self, criteria: dict):
        """
        Filter labels by criteria fields: 'id', 'labelType', 'resourceTypes', 'labelCategories'.
        @param criteria: Dict of <field>: <value> filter params. All fields optional.
        @return: List of labels.
        """
        return self.__service_client.post(["farmstate", "filter", "label"], req_json=criteria).json()

    def get_container_by_id(self, container_id):
        """
        Get container by ID.
        @param container_id: ID of container.
        @return: Container or raise error 404 if container not found.
        """
        return self.__service_client.get(["farmstate", "container", self.__url_encode(container_id)]).json()

    def get_material_by_id(self, material_id):
        """
        Get material by ID.
        @param material_id: ID of material.
        @return: Material or raise error 404 if material not found.
        """
        return self.__service_client.get(["farmstate", "material", self.__url_encode(material_id)]).json()

    def get_state_by_id(self, state_id, id_type=None, include_historical=None):
        """
        Get state by ID.
        @param id_type: str. Valid values are: RESOURCE_STATE_ID, CONTAINER_ID,
                        MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
                        If provided, change meaning of `state_id` parameter to ID
                        of corresponding entity.
        @param state_id: Latest state ID, if `id_type` is not passed. Otherwise
                         material ID or container ID.
        @param include_historical: optional boolean. If true is passed, get newest state from historical state
                         if no latest state found for searched resource. If false, restrict lookup
                         for only isLatest=true state.
        @return: State or raise error 404 if latest state not found.
        """
        query_args = {"idType": id_type, "includeHistorical": include_historical}

        if include_historical is not None:
            query_args["includeHistorical"] = include_historical
        if id_type is not None:
            query_args["idType"] = id_type

        return self.__service_client.get(
            ["farmstate", "state", self.__url_encode(state_id)], query_args=query_args
        ).json()

    def get_state_by_historic_id(self, state_id):
        """
        Get state by ID where isLatest = True is not necessarily the case.

        @param state_id: Latest state ID, if `id_type` is not passed. Otherwise
                         material ID or container ID.
        @return: State or raise error 404 if latest state not found.
        """
        return self.__service_client.get(["farmstate", "state", "historic", self.__url_encode(state_id)]).json()

    def get_states_by_ids(self, state_ids, id_type):
        """
        Get state by ID.
        @param id_type: str. Valid values are: RESOURCE_STATE_ID, CONTAINER_ID,
                        MATERIAL_ID, CONTAINER_SERIAL, MATERIAL_LOT.
                        If provided, change meaning of `state_id` parameter to ID
                        of corresponding entity.
        @param state_ids: List of state IDs, if `id_type` is not passed. Otherwise
                         list of material IDs or container IDs.
        @return: List of States or raise error 404 if latest state not found.
        """
        state_ids = str_to_json(state_ids)
        query_args = {"idType": id_type}
        return self.__service_client.post(["farmstate", "states"], query_args=query_args, req_json=state_ids).json()

    def get_states_by_historic_ids(self, state_ids):
        """
        Get state by ID where isLatest = True is not necessarily the case.

        @param state_ids: List of state IDs, if `id_type` is not passed. Otherwise
                         list of material IDs or container IDs.
        @return: List of States or raise error 404 if latest state not found.
        """
        state_ids = str_to_json(state_ids)
        return self.__service_client.post(["farmstate", "states", "historic"], req_json=state_ids).json()

    # --------------- FarmState API (Notes) ---------------

    def create_container_note(self, note):
        """
        Create Note for container. Note should contain `linkId` of referenced container.
        @param note: Dict representing Note.
        @return: Note
        """
        note = str_to_json(note)
        return self.__service_client.post(["farmstate", "container", "note"], req_json=note).json()

    def create_material_note(self, note):
        """
        Create Note for material. Note should contain `linkId` of referenced material.
        @param note: Dict representing Note.
        @return: Note
        """
        note = str_to_json(note)
        return self.__service_client.post(["farmstate", "material", "note"], req_json=note).json()

    def get_container_notes(self, container_id):
        """
        Return notes by container ID.
        @param container_id: ID of container.
        @return: List of Notes.
        """
        return self.__service_client.get(["farmstate", "container", "note", self.__url_encode(container_id)]).json()

    def get_material_notes(self, material_id):
        """
        Return notes by material ID.
        @param material_id: ID of material.
        @return: List of Notes.
        """
        return self.__service_client.get(["farmstate", "material", "note", self.__url_encode(material_id)]).json()

    def get_operation_counts(self, site_name, start_time, end_time):
        """
        Return counts for all operations that were run between the specified
        dates.

        @param site_name: Name of site to get counts for.
        @param start_time: start date time to count operations for.
        @param end_time: end date time to count operations for.
        @return: List of OperationCounts.
        """
        query_args = {"siteName": site_name, "startDateTime": start_time, "endDateTime": end_time}
        return self.__service_client.get(["farmstate", "operation", "counts"], query_args=query_args).json()

    def get_operation_history(self, criteria: dict):
        """
        Return operations for a given containerId or materialId,
        supports pagination with pageSize and pageNumber

        @param criteria: <containerId>, <materialId>, <pageSize>, <pageNumber>. `containerId` or `materialId` is required.
        @return: List of Operations.
        """
        return self.__service_client.post(["operation", "history"], req_json=criteria).json()

    # --------------- FarmState API (Labels) ---------------

    def create_label(self, label: dict):
        """
        Create Label.
        @param label: Dict representing Label.
        @return: Label
        """
        return self.__service_client.post(["farmstate", "label"], req_json=label).json()

    def delete_label(self, label_id: str):
        """
        Delete Label.
        @param label_id: ID of the Label to delete.
        @return: Label
        """
        query_args = {"id": label_id}
        return self.__service_client.delete(["farmstate", "label"], query_args=query_args).json()

    # --------------- FarmState API (Label Categories) ---------------

    def create_label_category(self, label_category: dict):
        """
        Create LabelCategory.
        @param label_category: Dict representing LabelCategory.
        @return: LabelCategory
        """

        return self.__service_client.post(["farmstate", "label-category"], req_json=str_to_json(label_category)).json()

    def delete_label_category(self, label_category_id):
        """
        Delete LabelCategory.
        @param label_category_id: ID of the LabelCategory to delete.
        @return: Label
        """

        return self.__service_client.delete(
            ["farmstate", "label-category"], query_args={"id": label_category_id}
        ).json()

    def filter_label_categories(self, criteria: dict):
        """
        Filter label Categories by criteria fields: 'id', 'name'.
        @param criteria: Dict of <field>: <value> filter params. All fields optional.
        @return: List of labelCategories.
        """
        return self.__service_client.post(
            ["farmstate", "filter", "label-category"], req_json=str_to_json(criteria)
        ).json()

    # --------------- Packaging API ---------------

    def create_packaging_lots(
        self,
        farm_path: str,
        farm_def_machine_id: str,
        start_date: str,
        end_date: str,
        packaging_lot_crop_codes: list = None,
    ):
        """
        Create the packaging lots for the given date range and the farm specified by FarmDef farm path for all crops enabled for the farm.
        @param farm_path: The FarmDef path of the farm.
        @param farm_def_machine_id: The FarmDef machine ID.
        @param start_date: The start of the date range.
        @param end_date: The end of the date range.
        @param packaging_lot_crop_code: The crop code associated with the packaging lot.
        @return: A list of packaging lot objects.
        """
        query_args = {
            "farmPath": farm_path,
            "farmDefMachineId": farm_def_machine_id,
            "startDate": start_date,
            "endDate": end_date,
            "packagingLotCropCode": packaging_lot_crop_codes,
        }
        return self.__service_client.post(["packaging", "lots"], query_args=query_args).json()

    def get_packaging_lots(self, farm_path: str, start_date: str, end_date: str, packaging_lot_crop_codes: list = None):
        """
        Filter the packaging lots by the given date range and the farm specified by FarmDef farm path.
        @param farm_path: The FarmDef path of the farm.
        @param start_date: The start of the date range.
        @param end_date: The end of the date range.
        @return: A list of packaging lot objects matched the criteria.
        """
        query_args = {
            "farmPath": farm_path,
            "startDate": start_date,
            "endDate": end_date,
            "packagingLotCropCode": packaging_lot_crop_codes,
        }
        return self.__service_client.get(["packaging", "lots"], query_args=query_args).json()

    def get_packaging_lot(self, packaging_lot_name: str):
        """
        Get the packaging lot by its lot name.
        @param packaging_lot_name: The packaging lot name.
        @return: Packaging lot object or raise error 404 if packaging lot not found.
        """
        return self.__service_client.get(["packaging", "lots", self.__url_encode(packaging_lot_name)]).json()

    def update_packaging_lot(self, packaging_lot: dict):
        """
        Update the packaging lot.
        @param packaging_lot: The packaging lot object to be updated.
        @return: The updated packaging lot object or raise error 404 if packaging lot not found.
        """
        return self.__service_client.put(["packaging", "lots"], req_json=str_to_json(packaging_lot)).json()

    def delete_packaging_lot(self, packaging_lot_name: str):
        """
        Delete the packaging lot by its lot name.
        @param packaging_lot_name: The packaging lot name.
        @return: The deleted packaging lot object or raise error 404 if packaging lot not found.
        """
        return self.__service_client.delete(["packaging", "lots", self.__url_encode(packaging_lot_name)]).json()

    def release_packaging_lots(
        self, farm_path: str, start_date: str, end_date: str, packaging_lot_crop_codes: list = None
    ):
        """
        Release packaging lots to NetSuite by the given farm specified by FarmDef farm path.
        @param farm_path: The FarmDef path of the farm.
        @param start_date: The start of the date range.
        @param end_date: The end of the date range.
        @return: A list of packaging lots successfully released to NetSuite.
        """
        query_args = {
            "farmPath": farm_path,
            "startDate": start_date,
            "endDate": end_date,
            "packagingLotCropCode": packaging_lot_crop_codes,
        }
        return self.__service_client.post(["packaging", "lots", "release"], query_args=query_args).json()

    def create_finished_goods_case(self, operation_id: str, material: dict, farm_def_machine_id: str, process_id: str):
        """
        Create a new Finished Goods Case material.
        @param operation_id: The operation ID.
        @param material: The Finished Goods Case material object to create.
        @param farm_def_machine_id: The FarmDef machine ID.
        @param process_id: The process ID.
        @return: The created Finished Goods Case material object.
        """
        return self.__service_client.post(
            ["packaging", "finished-goods-cases"],
            query_args={"operationId": operation_id, "farmDefMachineId": farm_def_machine_id, "processId": process_id},
            req_json=str_to_json(material),
        ).json()

    def get_finished_goods_cases(
        self,
        created_at_start: str,
        created_at_end: str,
        packaging_lot_name: str = None,
        package_type: str = None,
        case_id: str = None,
    ):
        """
        Filter the Finished Goods Case materials by the given creation date range, packaging lot name, package type and case ID.
        @param start_date: The start of the creation date range.
        @param end_date: The end of the creation date range.
        @param packaging_lot_name: The packaging lot.
        @param package_type: The package type.
        @param case_id: The case ID.
        @return: A list of Finished Goods Case objects matched the criteria.
        """
        query_args = {
            "createdAtStart": created_at_start,
            "createdAtEnd": created_at_end,
            "lotName": packaging_lot_name,
            "packageType": package_type,
            "caseId": case_id,
        }
        return self.__service_client.get(["packaging", "finished-goods-cases"], query_args=query_args).json()

    def get_finished_goods_case(self, case_id: str):
        """
        Get a Finished Goods Case material by its case ID.
        @param case_id: The case ID of Finished Goods Case material to retrieve.
        @return: The Finished Goods Case material object or raise error 404 if Finished Goods Case material not found.
        """
        return self.__service_client.get(["packaging", "finished-goods-cases", self.__url_encode(case_id)]).json()

    def update_finished_goods_case(self, operation_id: str, material: dict, process_id: str):
        """
        Update a Finished Goods Case material and returns the updated object.
        @param operation_id: The operation ID.
        @param material: The Finished Goods Case material object to update.
        @param process_id: The process ID.
        @return: The updated Finished Goods Case material object.
        """
        return self.__service_client.put(
            ["packaging", "finished-goods-cases"],
            query_args={"operationId": operation_id, "processId": process_id},
            req_json=str_to_json(material),
        ).json()

    def delete_finished_goods_case(self, case_id: str):
        """
        Delete a Finished Goods Case material by its case ID and returns the deleted object.
        @param case_id: The case ID of Finished Goods Case material to delete.
        @return: The deleted Finished Goods Case material object or raise error 404 if Finished Goods Case material not found.
        """
        return self.__service_client.delete(["packaging", "finished-goods-cases", self.__url_encode(case_id)]).json()

    def accumulate_finished_goods_cases(self, case_ids: list):
        """
        Accumulate case IDs of Finished Goods Cases to be later persisted to NetSuite.

        @param case_ids: case IDs of Finished Goods Cases we want to accumulate.
        @return: list of accumulated Finished Goods Case material objects.
        """
        return self.__service_client.post(["packaging", "finished-goods-cases", "accumulate"], req_json=case_ids).json()

    def persist_finished_goods_cases(self, farm_path: str):
        """
        Persist Finished Goods Cases to NetSuite for previously accumulated case IDs.

        @param farm_path: valid farm path in FarmDef.
        @return: list of persisted Finished Goods Case material objects.
        """
        return self.__service_client.post(
            ["packaging", "finished-goods-cases", "persist"], query_args={"farmPath": farm_path}
        ).json()

    # --------------- Testing Utils API ---------------

    def delete_all_data_by_site(self, sites):
        """
        Returns "OK", deletes all data in the database for particular site(s).
        Only works in a staging environment.
        @param sites: either string or list of strings, site names.
        """
        return self.__service_client.delete(
            ["testing", "util", "database", "clear"], query_args={"siteNames": sites}
        ).json()

    def get_summarized_genealogy(self, material_id, max_number_operations, max_number_focused_resource_operations):
        """
        Returns material's genealogy.
        @param material_id: ID of focused material
        @param max_number_operations: max number of operations to return
        @return: List of FocusedGenealogyOperations for material, with Antecedents and Subsequents
        """
        return self.__service_client.get(
            ["operation", "summarized-genealogy", self.__url_encode(material_id)],
            query_args={
                "maxNumberOperations": max_number_operations,
                "maxNumberFocusedResourceOperations": max_number_focused_resource_operations,
            },
        ).json()

    def __url_encode(self, str):
        """
        Returns a URL encoded string, such that forward slashes '/' are properly encoded
        to prevent issues with GET endpoints
        @param str: string to URL encode
        @return: URL encoded string
        """
        return parse.quote(str, safe="")
