"""This module implements methods which interact the web API for the Plenty
device management service."""

from typing import Dict, List, Optional

from ..base_client import BaseClient
from ..common import (
    AuthenticatedServiceClient,
    filter_query_args,
    format_url_with_version,
    str_to_json,
    validate_update_content,
)


class DeviceManagementServiceClient(BaseClient):
    """Client communicating with the device management service via REST."""

    _application_name = "Device Management Service"
    _service_name = "device-management-service"
    _api_version = "v0"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return DeviceManagementServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return DeviceManagementServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return DeviceManagementServiceClient._api_version

    def __init__(self, authenticated_client, url):
        """Create a new traceability store client.

        Args:
            authenticated_client (common.AuthenticatedClient): Plenty service
                client that has credentials.
            url (str): The url to use for the client.
        """
        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version()), True
        )
        self.__service_client_v1 = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, "v1"), True
        )

    def build_commands(self):
        """Builds the commands for this client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        site_arg = ["site"], {"help": "the site to query for"}
        device_arg = ["device_fname"], {"help": "the device's JSON file"}
        serial_arg = ["serial"], {"help": "the serial ID of the device"}
        location_arg = ["location"], {"help": "the new location of the device"}
        capability_list_arg = (
            ["capabilities"],
            {"help": "the new capabiltites list of the device"},
        )
        comm_arg_opt = (
            ["--com"],
            {"help": "the (optional) communication mechanism by which to filter"},
        )
        datetime_arg_opt = ["--date"], {"help": "the datetime at which to get devices"}
        room_arg_opt = ["--room"], {"help": "the room to query for"}
        row_arg_opt = ["--row"], {"help": "the row to query for (e.g --row = D)"}
        tower_arg_opt = (
            ["--tower"],
            {"help": "the tower to query for (e.g --tower = 12)"},
        )
        position_arg_opt = ["--position"], {"help": "the position to query for"}
        capability_arg = (
            ["capability"],
            {"help": "the capability of the device to filter for"},
        )
        model_arg = ["model"], {"help": "the model name of the device to be returned"}
        external_serial_arg = (
            ["external_serial"],
            {"help": "the external serial number of the device to be returned"},
        )
        return {
            "device": (
                "Manage devices.",
                {
                    "list": ("List all devices.", self.list_devices, []),
                    "create": (
                        "Create a new device.",
                        self.create_device,
                        [device_arg],
                    ),
                    "get": ("Get info about a device.", self.get_device, [serial_arg]),
                    "update": (
                        "Update a device.",
                        self.update_device,
                        [serial_arg, device_arg],
                    ),
                    "move": (
                        "Update a device location.",
                        self.update_device_loc,
                        [serial_arg, location_arg],
                    ),
                    "new_capabilities": (
                        "Update the list of device capabilties.",
                        self.update_device_cap,
                        [serial_arg, capability_list_arg],
                    ),
                    "delete": ("Delete a device.", self.delete_device, [serial_arg]),
                    "external": (
                        "Get device information by its external serial number.",
                        self.query_by_external_serial,
                        [model_arg, external_serial_arg],
                    ),
                    "serial_list_of_children": (
                        "list of children of a device.",
                        self.get_children,
                        [serial_arg],
                    ),
                },
            ),
            "key": (
                "Manage device keys.",
                {
                    "check": ("Check info about a key.", self.check_key, [serial_arg]),
                    "generate": ("Generate a key.", self.generate_key, [serial_arg]),
                    "disable": ("Disable a key.", self.disable_key, [serial_arg]),
                },
            ),
            "certificate": (
                "Manage device certificates.",
                {
                    "check": (
                        "Check info about a certificate.",
                        self.check_certificate,
                        [serial_arg],
                    ),
                    "generate": (
                        "Generate a certificate.",
                        self.generate_certificate,
                        [serial_arg],
                    ),
                    "disable": (
                        "Disable a certificate.",
                        self.disable_certificate,
                        [serial_arg],
                    ),
                },
            ),
            "bulk": (
                "Get device information in bulk.",
                {
                    "serials": (
                        "Get a list of all registered device serials.",
                        self.get_all_serials,
                        [comm_arg_opt],
                    ),
                    "location": (
                        "List all devices existing at a location at a datetime.",
                        self.query_by_loc,
                        [
                            site_arg,
                            datetime_arg_opt,
                            room_arg_opt,
                            row_arg_opt,
                            tower_arg_opt,
                            position_arg_opt,
                        ],
                    ),
                    "capability": (
                        "List of all devices with a capability at a location.",
                        self.query_by_loc_and_cap,
                        [
                            site_arg,
                            capability_arg,
                            room_arg_opt,
                            row_arg_opt,
                            tower_arg_opt,
                            position_arg_opt,
                        ],
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
            "device_management",
            "device management service client",
            "d",
            self.build_commands(),
            lambda s, _: [s[0]],
        )

    def list_devices(self):
        """Gets from the /devices endpoint a list of all registered devices.

        Returns:
            (list): A list of all devices stored.
        """
        return self.__service_client.get(["devices"]).json()

    def create_device(self, device=None, device_fname=None):
        """Posts to the /devices endpoint a new device to create.

        Args:
            device (str, optional): A formatted string with the device's
                information. Defaults to None. Either this or device_fname must
                be None.
            device_fname (str, optional): The filename of the file contatining
                the device's information. Defaults to None. Either this or
                device must be None.

        Returns:
            (dict): The original device, updated with server-supplied fields.
        """
        device = validate_update_content(device, device_fname)

        return self.__service_client.post(["devices", "create"], req_json=device).json()

    def create_device_with_serial(self, device=None, device_fname=None):
        """Posts to the /devices endpoint a new device to create with an
        explicit serial.

        Args:
            device (str, optional): A formatted string with the device's
                information. Defaults to None. Either this or device_fname must
                be None.
            device_fname (str, optional): The filename of the file contatining
                the device's information. Defaults to None. Either this or
                device must be None.

        Returns:
            (dict): The original device, updated with server-supplied fields.
        """
        device = validate_update_content(device, device_fname)

        return self.__service_client.post(["devices", "create", "no-serial-generation"], req_json=device).json()

    def get_device(self, serial):
        """Gets from the /device/{serial} endpoint a particular device.

        Args:
            serial (str): The serial ID of the device being requested.

        Returns:
            (dict): The device requested.
        """
        return self.__service_client.get(["device", serial]).json()

    def get_children(self, serial):
        """Gets from the /device/children/{serial} endpoint a particular device.

        Args:
            serial (str): The serial ID of the device being requested.

        Returns:
            (dict): The list of children for the given serial
        """
        return self.__service_client.get(["device", "children", serial]).json()

    def update_device(self, serial, device=None, device_fname=None):
        """Puts to the /device/{serial} endpoint an updated particular device.

        Args:
            serial (str): The serial ID of the device being updated.
            device (str, optional): A formatted string with the device's
                information. Defaults to None. Either this or device_fname must
                be None.
            device_fname (str, optional): The filename of the file contatining
                the device's information. Defaults to None. Either this or
                device must be None.

        Returns:
            (dict): The updated device.
        """
        device = validate_update_content(device, device_fname)

        return self.__service_client.put(["device", serial], req_json=device)

    def update_device_loc(self, serial, location):
        """Puts to the /device/{serial} endpoint an updated particular device.

        Args:
            serial (str): The serial ID of the device being updated.
            location (str|dict): The new location.

        Returns:
            (dict): The updated device.
        """
        return self.__service_client.put(["device", "updateLoc", serial], req_json=location)

    def update_device_cap(self, serial, capabilities):
        """Puts to the /device/{serial} endpoint an updated particular device.

        Args:
            serial (str): The serial ID of the device being updated.
            capabilities (dict): The new list of capabilities.

        Returns:
            (dict): The updated device.
        """
        return self.__service_client.put(["device", "updateCap", serial], req_json=capabilities)

    def delete_device(self, serial):
        """Deletes from the /device/{serial} endpoint a particular device.

        Args:
            serial (str): The serial ID of the device being deleted.
        """
        self.__service_client.delete(["device", serial])

    def check_key(self, serial, device_key):
        """Gets from the /device/{serial}/key endpoint to check whether a key is
        already configured correctly for the specific device.

        Args:
            serial (str): The serial ID of the device in question.
            device_key (str): The device key to be checked.

        Returns:
            (bool): True if a key is configured and ready to go, False
                otherwise.
        """
        return self.__service_client.get(["device", serial, "key"], query_args={"deviceKey": device_key}).json()

    def generate_key(self, serial):
        """Posts to the /device/{serial}/key endpoint to generate a key for the
        specific device.

        Args:
            serial (str): The serial ID of the device in question.

        Returns:
            (string): The key generated for the device.
        """
        return self.__service_client.post(["device", serial, "key"]).json()

    def disable_key(self, serial):
        """Deletes from the /device/{serial}/key endpoint to disable a key for
        the specific device.

        Args:
            serial (str): The serial ID of the device in question.

        Returns:
            (None): None.
        """
        return self.__service_client.delete(["device", serial, "key"]).json()

    def check_certificate(self, serial):
        """Gets from the /device/{serial}/certificate endpoint to check whether
        a certificate is required for the given device--and if so, if it is set
        up.

        Args:
            serial (str): The serial ID of the device in question.

        Returns:
            (str): An object representing whether a certificate is required for
                the given device, and if so, if it is set up.
        """
        return self.__service_client.get(["device", serial, "certificate"]).json()

    def generate_certificate(self, serial):
        """Posts to the /device/{serial}/certificate endpoint to generate a
        certificate for the given device.

        Args:
            serial (str): The serial ID of the device in question.

        Returns:
            (Object): Parsed JSON describing the newly created cert.
        """
        return self.__service_client.post(["device", serial, "certificate"]).json()

    def disable_certificate(self, serial):
        """Deletes from the /device/{serial}/certificate endpoint to disable the
         certificate for the given device.

        Args:
            serial (str): The serial ID of the device in question.
        Returns:
            (None): None.
        """
        return self.__service_client.delete(["device", serial, "certificate"]).json()

    def get_all_serials(self, communication_mechanism=None):
        """Gets a list of all registered device serial numbers.

        Args:
            communication_mechanism (str): The optional string
            indicating the communication mechanism by which to filter.
        Returns:
            (Object): Parsed JSON describing the listing of devices.
        """
        params = {}
        if communication_mechanism:
            params = {"communicationMechanism": communication_mechanism}
        return self.__service_client.get(["devices", "serials"], query_args=params).json()

    def query_by_loc(self, site, date=None, room=None, row=None, tower=None, position=None):
        """Query for devices by those devices' location and date.

        Args:
            date (str): The date for the query. Can be used to query location
                at any time.
            site (str): The name of the site like SouthSF-1 for which devices
                should be returned.
            room (str): The room for which devices should be returned. If empty
                will not filter by room.
            row (str): The row for which devices should be returned. If empty
                will not filter by row.
            tower (str): The tower for which devices should be returned. If
                empty will not filter by tower.
            position (str): The position for which devices should be returned.
                If empty will not filter by position.

        Returns:
            (dict): Parsed JSON describing device listing for the given
                location.
        """
        params = {"site": site}

        if date is not None:
            params["date"] = date
        if room is not None:
            params["room"] = room
        if row is not None:
            params["row"] = row
        if tower is not None:
            params["tower"] = tower
        if position is not None:
            params["position"] = position

        return self.__service_client.get(["devices", "queryByLoc"], query_args=params).json()

    def query_by_loc_and_cap(self, site, room=None, row=None, tower=None, position=None, capability=None):
        """Query for devices by those devices' location and capability.

        Args:
            site (str): The name of the site like SouthSF-1 for which devices
                should be returned.
            room (str): The room for which devices should be returned. If empty
                will not filter by room.
            row (str): The row for which devices should be returned. If empty
                will not filter by row.
            tower (str): The tower for which devices should be returned. If
                empty will not filter by tower.
            position (str): The position for which devices should be returned.
                If empty will not filter by position.
            capability (str): The capability of the device to filter for.

        Returns:
            (dict): Parsed JSON describing device listing for the given
                location.
        """
        params = {"site": site}

        if room:
            params["room"] = room
        if row:
            params["row"] = row
        if tower:
            params["tower"] = tower
        if position:
            params["position"] = position
        if capability:
            params["capability"] = capability

        return self.__service_client.get(["devices", "queryByLocAndCap"], query_args=params).json()

    def query_by_external_serial(self, model, external_serial):
        """Get device information by their external serial.

        Args:
            model (str): The model name of the device to be returned.
            external_serial (str): The external serial number of the device to
                be returned.


        Returns:
            (dict): Parsed JSON describing device for the given external
                serial.
        """
        params = {"modelName": model, "externalSerial": external_serial}

        return self.__service_client.get(["getByExternalSerial"], query_args=params).json()

    #
    # DeviceManagementServiceV2
    #
    def register_device(self, request: dict) -> Dict:
        return self.__service_client_v1.post(["operations/register"], req_json=str_to_json(request)).json()

    def decommission_device(self, request: dict) -> Dict:
        return self.__service_client_v1.post(["operations/decommission"], req_json=str_to_json(request)).json()

    def commission_device(self, request: dict) -> Dict:
        return self.__service_client_v1.post(["operations/commission"], req_json=str_to_json(request)).json()

    def replace_device(self, request: dict) -> Dict:
        return self.__service_client_v1.post(["operations/replace"], req_json=str_to_json(request)).json()

    def get_firmware_history(self, device_id: str) -> Dict:
        return self.__service_client_v1.get(["firmware-history", device_id]).json()

    def get_device_by_id(self, device_id: str) -> Dict:
        return self.__service_client_v1.get(["devices", device_id]).json()

    def search_firmware_images(self, device_type: Optional[str] = None, binary_type: Optional[str] = None) -> List:
        query_args = filter_query_args({"deviceType": device_type, "binaryType": binary_type})
        return self.__service_client_v1.get(["firmware-images"], query_args=query_args).json()

    def get_firmware_upgrade_status(self, process_ids: List[str]) -> Dict:
        query_args = filter_query_args({"processIds[]": process_ids})
        return self.__service_client_v1.get(["firmware-upgrades"], query_args=query_args).json()

    def get_s3_url_for_device_data_download(self, data_type: str, device_id: str) -> Dict:
        return self.__service_client_v1.get(["files", data_type, device_id]).json()

    def get_s3_url_for_device_data_upload(self, request: dict) -> Dict:
        return self.__service_client_v1.post(["files"], req_json=str_to_json(request)).json()

    def ingest_csv_file(self, dataType: str, files: dict) -> Dict:
        return self.__service_client_v1.post(["files", "ingest", dataType], files=files)
