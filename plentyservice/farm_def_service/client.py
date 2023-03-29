"""This module implements methods which interact the web API for the Plenty
farm def service."""

from typing import Dict, List, Optional

import requests

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, filter_query_args, format_url_with_version, str_to_json


class FarmDefServiceClient(BaseClient):
    """Client communicating with the Plenty farm def service via REST."""

    _application_name = "Farm Def Service"
    _service_name = "farm-def-service"
    _api_version = "v1"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return FarmDefServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return FarmDefServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return FarmDefServiceClient._api_version

    def __init__(self, authenticated_client, url):
        """Create a new traceability store client.

                Args:
                    authenticated_client (common.AuthenticatedClient): Plenty service
                        client that has credentials.
                    url (str): The url to use for the client.
        format_url_with_version
        """

        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version())
        )
        self.__service_client_v2 = AuthenticatedServiceClient(authenticated_client, format_url_with_version(url, "v2"))
        self.__auth_client = authenticated_client
        self.__service_url = url

    def build_commands(self):
        """Stub for building the commands for this client."""

        return {}

    def build_cli_subcommand(self):
        """Bulid the CLI subcommand for this client.

        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return ("farm_def", "farm def service client", "fd", self.build_commands(), lambda s, _: [s[0]])

    #
    # Health endpoint
    #

    def get_health(self) -> Dict:
        """Get farm-def-service health information."""
        return self.__auth_client.make_request(requests.get, self.__service_url, ["health"], False, None, None).json()

    #
    # Objects endpoints
    #

    def search_object(
        self, site: Optional[str] = None, kind: Optional[str] = None, _class: Optional[str] = None
    ) -> List:
        """Search objects

        Search objects by their attributes.

        :param site: Site name
        :type site: str

        :param kind: Object kind (e.g. `machine`)
        :type kind: str

        :param _class: Object class
        :type _class: str

        :return: A list of objects
        """
        return self.__service_client.get(["objects"], query_args={"site": site, "kind": kind, "class": _class}).json()

    def get_object_by_id(self, id, depth: Optional[int] = None) -> Dict:
        """Get an object by ID

        Get an object by its unique ID. You can set the `depth` parameter to return multiple levels of child objects.

        :param object_id: Object ID (required)
        :type object_id: str

        :param depth: depth of hierarchy to return (i.e. # of child levels under this object). Default is 1. (optional)
        :type depth: int

        :return: Returns the result object.
        """
        return self.__service_client.get(
            ["objects", id],
            query_args={
                "depth": depth,
            },
        ).json()

    def get_object_by_path(self, path, depth: Optional[int] = None) -> Dict:
        """Get an object by path

        Get an object by its unique path. You can set the `depth` parameter to return multiple levels of child objects.

        :param path: Site name (required)
        :type path: str

        :param depth: depth of hierarchy to return (i.e. # of child levels under this object) (optional)
        :type depth: int

        :return: Returns the result object.
        """
        return self.__service_client.get(
            ["objects/by-path"],
            query_args={
                "path": path,
                "depth": depth,
            },
        ).json()

    def get_object_by_id_v2(self, id: str, enrich_child_locations: Optional[bool] = None) -> Dict:
        """V2 Get an object by ID.

        :param object_id: Object ID (required)
        :type object_id: str

        :return: Returns the result object and its entire hierarchy.
        """
        query_args = filter_query_args({"enrichChildLocations": enrich_child_locations})
        return self.__service_client_v2.get(["objects", id], query_args=query_args).json()

    def get_object_by_path_v2(self, path: str, enrich_child_locations: Optional[bool] = None) -> Dict:
        """V2 Get an object by path.

        :param path: Site name (required)
        :type path: str

        :return: Returns the result object and its entire hierarchy.
        """
        query_args = filter_query_args({"enrichChildLocations": enrich_child_locations, "path": path})
        return self.__service_client_v2.get(["objects/by-path"], query_args=query_args).json()

    def get_message_descriptor(self, path) -> Dict:
        """Get a Tell or Trigger payload MessageDescriptor

        Returns a google.protobuf.MessageDescriptor for the MethodDescriptor's payload.

        :param method_path: Method descriptor path (required)
        :type method_path: str

        :return: a dictionary containing fields (args) for the tell/trigger.
        """
        return self.__service_client.get(["farmos-rpc/message-descriptor", path]).json()

    def get_message_descriptors(self) -> Dict:
        """Get dictionary containing all proto defns found in farm def.

        :return: a dictionary - key is the proto name and value is the proto defintion.
        """
        return self.__service_client.get(["farmos-rpc/message-descriptors"]).json()

    def get_method_descriptor(self, path) -> Dict:
        """Get a Tell or Trigger payload MethodDescriptor

        Returns the MethodDescriptor's payload that also contain MessageDescriptor data.

        :param method_path: Method descriptor path (required)
        :type method_path: str

        :return: a dictionary containing tell/trigger descriptor fields along with its message descriptor fields.
        """
        return self.__service_client.get(["farmos-rpc/method-descriptor", path]).json()

    #
    # DevicesApi endpoints
    #

    def get_device_by_id(self, device_id: str) -> Dict:
        """
        Get a device.

        Get a device by its unique ID.
        """
        return self.__service_client.get(["devices", device_id]).json()

    def search_devices(
        self,
        device_ids: Optional[List[str]] = None,
        serial: Optional[str] = None,
        serial_contains: Optional[str] = None,
        device_type_name: Optional[str] = None,
        device_type_names: Optional[List[str]] = None,
        placed_parent_id: Optional[str] = None,
        placed_parent_path: Optional[str] = None,
        depth: Optional[int] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> List:
        """
        Search devices.

        Find devices given query parameters. A unique device is defined by the combination of serial and device type.
        """
        query_args = filter_query_args(
            {
                "deviceIds[]": device_ids,
                "serial": serial,
                "serialContains": serial_contains,
                "type": device_type_name,
                "types[]": device_type_names,
                "placedParentId": placed_parent_id,
                "placedParentPath": placed_parent_path,
                "depth": depth,
                "limit": limit,
                "offset": offset,
                "sortBy": sort_by,
                "order": order,
            }
        )

        return self.__service_client.get(["devices"], query_args=query_args).json()

    def search_device_by_location(
        self, device_location_ref: Optional[str] = None, child_device_location_ref: Optional[str] = None
    ) -> List:
        """
        Get device by location.

        Get the device that is placed at a given device location.
        """
        query_args = filter_query_args(
            {"ref": device_location_ref, "childDeviceLocationRef": child_device_location_ref}
        )

        response = self.__service_client.get(["devices/by-location"], query_args=query_args)

        if response.status_code == 204:
            return response

        return response.json()

    def search_devices_by(self, request: Dict) -> List:
        """
        Search Devices using POST endpoint.

        Find devices matching criteria for the given request body.
        """
        return self.__service_client.post(["devices/search"], req_json=str_to_json(request)).json()

    def find_mapped_devices(self, device_id: str) -> List:
        """
        Get Devices mapped to another Device.

        Two devices are mapped together when they are both associated to a Device Location that maps one another.
        """
        return self.__service_client.get(["devices", device_id, "mapped-devices"]).json()

    def create_device(self, device: Dict) -> Dict:
        """
        Create a device.

        Create a new device. A device is defined by a unique combination of serial and device type. If the given serial/type
        already exists, that existing device will be returned.
        """
        return self.__service_client.post(["devices"], req_json=str_to_json(device)).json()

    def update_device(self, device_id: str, device: Dict) -> Dict:
        """
        Update a device.

        Updates the attributes of a device that are modifiable.
        """
        return self.__service_client.put(["devices", device_id], req_json=str_to_json(device)).json()

    def delete_device(self, device_id: str) -> Dict:
        """
        Delete a device.

        Mark the device with given ID as deleted (archived, with history tracked).
        """
        return self.__service_client.delete(["devices", device_id]).json()

    def place_device(self, place_device: Dict) -> Dict:
        """
        Places the device at the given device location.
        """
        return self.__service_client.post(["devices/place-device"], req_json=str_to_json(place_device)).json()

    def unplace_device(self, unplace_device: Dict) -> Dict:
        """
        Unplaces the device from its current device location.
        """
        return self.__service_client.post(["devices/unplace-device"], req_json=str_to_json(unplace_device)).json()

    def replace_device(self, replace_devices: Dict) -> Dict:
        """
        Replace device with another device.

        Swap the placement of one device for another device. This is a handy wrapper that un-places the original
        device from its location and places the new device in the same location.
        """
        return self.__service_client.post(["devices/replace-device"], req_json=str_to_json(replace_devices)).json()

    #
    # TypesApi endpoints
    #

    def brand_types(self) -> List:
        """
        Get array of brand types
        """
        return self.__service_client.get(["types/brand-types"]).json()

    def get_crop_type_by_name(self, crop_type_name: str) -> Dict:
        """
        Get a crop type.

        Get a crop type by its unique name.
        """
        return self.__service_client.get(["types/crop-types", crop_type_name]).json()

    def search_crop_types(self) -> List:
        """
        Search crop types.

        Find crop types.
        """
        return self.__service_client.get(["types/crop-types"]).json()

    def get_device_type_by_name(self, device_type_name: str) -> Dict:
        """
        Get a device type.

        Get a device type by its unique name.
        """
        return self.__service_client.get(["types/device-types", device_type_name]).json()

    def search_device_types(self) -> List:
        """
        Search device types.

        Find device types.
        """
        return self.__service_client.get(["types/device-types"]).json()

    def get_sku_type_by_name(self, sku_type_name: str) -> Dict:
        """
        Get a sku type.

        Get a sku type by its unique name.
        """
        return self.__service_client.get(["types/sku-types", sku_type_name]).json()

    def search_sku_types(self) -> List:
        """
        Search sku types.

        Find sku types.
        """
        return self.__service_client.get(["types/sku-types"]).json()

    def search_measurement_types(self) -> List:
        """
        Search measurement types.

        Find measurement types.
        """
        return self.__service_client.get(["types/measurement-types"]).json()

    #
    # CropsApi endpoints
    #

    def get_crop_by_name(self, name: str) -> Dict:
        """
        Get a crop.

        Get a crop by its unique name.
        """
        return self.__service_client.get(["crops", name]).json()

    def update_crop(self, name: str, crop: Dict) -> Dict:
        """
        Update a crop.

        Updates the attributes of a crop that are modifiable.
        """
        return self.__service_client.put(["crops", name], req_json=str_to_json(crop)).json()

    def delete_crop(self, name: str) -> Dict:
        """
        Delete a crop.

        Mark the crop with given name as deleted (archived, with history tracked).
        """
        return self.__service_client.delete(["crops", name]).json()

    def add_list_of_crops_to_farm(self, crop_list: Dict) -> Dict:
        """
        Add list of crops to farm

        Add existing crops to a farm.
        For each crop, if it is already added to the given farm the existing crop will be returned.
        """
        return self.__service_client.post(["crops/add-to-farm"], req_json=str_to_json(crop_list)).json()

    def remove_list_of_crops_from_farm(self, crop_list: Dict) -> Dict:
        """
        Remove list of crops from farm

        Remove existing crops from a farm.
        Ignores crops not assigned to given farm, throws error if invalid any crop or farm names given.
        """
        return self.__service_client.post(["crops/remove-from-farm"], req_json=str_to_json(crop_list)).json()

    def get_crop_by_farm(self, name: str, farm_path: str) -> Dict:
        """
        Get a crop by farm.

        Returns the crop if it is assigned to the given farm, throws error otherwise.
        """
        return self.__service_client.get(["crops", name, "by-farm"], query_args={"farmPath": farm_path}).json()

    def search_crops(
        self,
        isSeedable: Optional[bool] = None,
        group: Optional[str] = None,
        seedPartNumbers: Optional[str] = None,
        limit: Optional[int] = None,
        isPackable: Optional[bool] = False,
    ) -> Dict:
        """Search for crops

        Returns crops for given search options

        :param isSeedable: if true returns only crops that are seedable.
        :param group: returns only items in given group
        :param seedPartNumbers: comma-separated list of seed part numbers (strings)
        :param limit: max number of crops to return, default is 100
        :param isPackable: if true return crops which are allowed in a SKU, default is false

        :return: list of crop objects
        """
        return self.__service_client.get(
            ["crops"],
            query_args=filter_query_args(
                {
                    "isSeedable": isSeedable,
                    "group": group,
                    "seedPartNumbers": seedPartNumbers,
                    "limit": limit,
                    "isPackable": isPackable,
                }
            ),
        ).json()

    def create_crop(self, crop: Dict) -> Dict:
        """
        Create a crop.

        Create a new crop. A crop is defined by a unique name. If the given name already exists, that existing crop will be returned.
        """
        return self.__service_client.post(["crops"], req_json=str_to_json(crop)).json()

    def search_crops_by_farm_path(
        self,
        farm_path: str,
        limit: Optional[int] = None,
        is_packable_anywhere: Optional[bool] = False,
        is_packable_in_farm: Optional[bool] = False,
    ) -> Dict:
        """Get crops by farm def path

        Returns crops for a given farm identified by its farm def path, ex: sites/SSF2/farms/Tigris

        :param farm_path: path to farm
        :param limit: max number of crops to return, default is 100
        :param is_packable_anywhere: if true return crops that are allowed in any globally-defined SKU, default is false
        :param is_packable_in_farm: if true return crops which are allowed in a SKU which exists in the same farm,
        default is false

        :return: list of crop objects
        """

        return self.__service_client.get(
            ["crops/by-farm"],
            query_args=filter_query_args(
                {
                    "farmPath": farm_path,
                    "limit": limit,
                    "isPackableAnywhere": is_packable_anywhere,
                    "isPackableInFarm": is_packable_in_farm,
                }
            ),
        ).json()

    #
    # SKUApi endpoints
    #

    def get_sku_by_name(self, name: str) -> Dict:
        """
        Get a SKU.

        Get a SKU by its unique name.
        """
        return self.__service_client.get(["skus", name]).json()

    def update_sku(self, name: str, sku: Dict) -> Dict:
        """
        Update a SKU.

        Updates the attributes of a SKU that are modifiable.
        """
        return self.__service_client.put(["skus", name], req_json=str_to_json(sku)).json()

    def delete_sku(self, name: str) -> Dict:
        """
        Delete a SKU.

        Mark the sku with given name as deleted (archived, with history tracked).
        """
        return self.__service_client.delete(["skus", name]).json()

    def add_list_of_skus_to_farm(self, sku_list: Dict) -> Dict:
        """
        Add list of SKUs to farm

        Add existing SKUs to a farm.
        For each SKU, if it is already added to the given farm the existing SKU will be returned.
        """
        return self.__service_client.post(["skus/add-to-farm"], req_json=str_to_json(sku_list)).json()

    def remove_list_of_skus_from_farm(self, sku_list: Dict) -> Dict:
        """
        Remove list of SKUs from farm

        Remove existing SKUs from a farm.
        Ignores SKUs not assigned to given farm, throws error if any invalid SKU or farm names given.
        """
        return self.__service_client.post(["skus/remove-from-farm"], req_json=str_to_json(sku_list)).json()

    def get_sku_by_farm(self, name: str, farm_path: str) -> Dict:
        """
        Get a SKU by farm.

        Returns the SKU if it is assigned to the given farm, throws error otherwise.
        """
        return self.__service_client.get(["skus", name, "by-farm"], query_args={"farmPath": farm_path}).json()

    def search_skus(
        self,
        allowed_crop_names: Optional[str] = None,
        default_crop_name: Optional[str] = None,
        packaging_lot_crop_code: Optional[str] = None,
        netsuite_item: Optional[str] = None,
        sku_type_name: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> Dict:
        """Search for skus

        Returns skus for given search options

        :param allowed_crop_names: comma separated list of crop names; each matched SKU must include all items from this list (order doesn't matter)
        :param default_crop_name: default crop name packed into the SKU
        :param packaging_lot_crop_code: The "crop" portion of the packaging lot code that is used for supply chain + warehouse team
        :param netsuite_item: netsuite item ID
        :param limit: max number of skus to return, default is 100

        :return: list of crop objects
        """
        return self.__service_client.get(
            ["skus"],
            query_args=filter_query_args(
                {
                    "allowedCropNames": allowed_crop_names,
                    "defaultCropName": default_crop_name,
                    "packagingLotCropCode": packaging_lot_crop_code,
                    "netsuiteItem": netsuite_item,
                    "skuTypeName": sku_type_name,
                    "limit": limit,
                }
            ),
        ).json()

    def create_sku(self, sku: Dict) -> Dict:
        """
        Create a SKU.

        Create a new SKU. A SKU is defined by a unique name. If the given name already exists, that existing SKU will be returned.
        """
        return self.__service_client.post(["skus"], req_json=str_to_json(sku)).json()

    def search_skus_by_farm_path(self, farmPath: str, limit: Optional[int] = None) -> Dict:
        """Get skus by farm def path

        Returns skus for a given farm identified by its farm def path, ex: sites/SSF2/farms/Tigris

        :param farmPath: path to farm
        :param limit: max number of skus to return, default is 100

        :return: list of sku objects
        """
        return self.__service_client.get(
            ["skus/by-farm"],
            query_args={
                "farmPath": farmPath,
                "limit": limit,
            },
        ).json()

    #
    # TagsApi endpoints
    #

    def create_tag(self, tag_request: Dict) -> Dict:
        """
        Create a tag.

        Create a path<>tag association.
        """
        return self.__service_client.post(["tags"], req_json=str_to_json(tag_request)).json()

    def update_tag(self, tag_id: str, tag_request: Dict) -> Dict:
        """
        Update a tag.

        Update a path<>tag association with a given id
        """
        return self.__service_client.put(["tags", tag_id], req_json=str_to_json(tag_request)).json()

    def delete_tag(self, tag_id: str) -> Dict:
        """
        Delete a tag.

        Delete a path<>tag association with a given id
        """
        return self.__service_client.delete(["tags", tag_id]).json()

    def search_tags(
        self,
        path: Optional[str] = None,
        tag_provider: Optional[str] = None,
        tag_path: Optional[str] = None,
        measurement_name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict:
        """
        Search tags.

        Search path<>tag association based on farm def path, tag provider, tag path, measurement name
        """
        return self.__service_client.get(
            ["tags"],
            query_args=filter_query_args(
                {
                    "path": path,
                    "tagProvider": tag_provider,
                    "tagPath": tag_path,
                    "measurementName": measurement_name,
                    "limit": limit,
                    "offset": offset,
                    "sort_by": sort_by,
                    "order": order,
                }
            ),
        ).json()
