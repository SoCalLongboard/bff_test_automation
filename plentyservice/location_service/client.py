"""This module implements methods which interact the web API for the Plenty
location service."""

from ..base_client import BaseClient
from ..common import (
    validate_update_content,
    AuthenticatedServiceClient,
    format_url_with_version,
)


class LocationServiceClient(BaseClient):
    """Client communicating with the Plenty location service via REST."""

    _application_name = "Location Service"
    _service_name = "location-service"
    _api_version = "v0"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return LocationServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return LocationServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return LocationServiceClient._api_version

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

    def build_commands(self):
        """Builds the commands for this client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """

        site_name_arg = ["site_name"], {"help": "the site's name"}
        site_fname_arg = (
            ["site_fname"],
            {"help": "a file specifying a site in JSON format"},
        )
        room_name_arg = ["room_name"], {"help": "the room's name"}
        room_fname_arg = (
            ["room_fname"],
            {"help": "a file specifying a room in JSON format"},
        )
        omit_items_arg = (
            ["omit_items"],
            {
                "type": bool,
                "help": "whether or not to omit the rooms' items",
            },
        )
        items_arg = (
            ["items"],
            {
                "nargs": "*",
                "help": "a file specifying a list of items in JSON format",
            },
        )
        dashboard_metrics_arg = (
            ["dashboard_metrics"],
            {
                "nargs": "*",
                "help": "a file specifying a serialized DashboardMetricModelListing",
            },
        )
        controls_arg = (
            ["controls"],
            {
                "nargs": "*",
                "help": "a file specifying a serialized ControlModelListing",
            },
        )
        control_names_arg = (
            ["control_names"],
            {
                "nargs": "*",
                "help": "a list of controls' names",
            },
        )

        return {
            "site": (
                "Manage sites.",
                {
                    "list": ("List all sites.", self.list_sites, []),
                    "get": ("Get info about a site.", self.get_site, [site_name_arg]),
                    "update": (
                        "Update or create a site",
                        self.update_site,
                        [site_name_arg, site_fname_arg],
                    ),
                },
            ),
            "room": (
                "Manage rooms.",
                {
                    "list": (
                        "List all rooms in the specified site.",
                        self.list_rooms,
                        [site_name_arg, omit_items_arg],
                    ),
                    "get": (
                        "Get info about a room in the specified site.",
                        self.get_room,
                        [site_name_arg, room_name_arg],
                    ),
                    "update": (
                        "Update or create a room in the specified site.",
                        self.update_room,
                        [site_name_arg, room_name_arg, room_fname_arg],
                    ),
                },
            ),
            "item": (
                "Manage room items.",
                {
                    "update": (
                        "Update or create particular items in a specified room.",
                        self.update_items,
                        [site_name_arg, room_name_arg, items_arg],
                    ),
                    "delete": (
                        "Delete particular items in a specified room.",
                        self.delete_items,
                        [site_name_arg, room_name_arg, items_arg],
                    ),
                },
            ),
            "dashboard_metric": (
                "Manage room environment dashboard metrics.",
                {
                    "list": (
                        "Get info about the environment dashboard metrics for the" "specified room.",
                        self.list_dashboard_metrics,
                        [site_name_arg, room_name_arg],
                    ),
                    "update": (
                        "Update or create particular environment dashboard metrics " "for a specified room.",
                        self.update_dashboard_metrics,
                        [site_name_arg, room_name_arg, dashboard_metrics_arg],
                    ),
                    "delete": (
                        "Delete particular environment dashboard metrics for a " "specified room.",
                        self.delete_dashboard_metrics,
                        [site_name_arg, room_name_arg, dashboard_metrics_arg],
                    ),
                },
            ),
            "control": (
                "Manage room controls.",
                {
                    "update": (
                        "Update or create particular controls for a room.",
                        self.update_controls,
                        [site_name_arg, room_name_arg, controls_arg],
                    ),
                    "delete": (
                        "Delete particular controls for a specified room.",
                        self.delete_controls,
                        [site_name_arg, room_name_arg, control_names_arg],
                    ),
                },
            ),
            "sensor": (
                "Manage room sensors.",
                {
                    "list": (
                        "Get info about all sensors in the specified room.",
                        self.list_sensors,
                        [site_name_arg, room_name_arg],
                    )
                },
            ),
            "tower_location": (
                "Manage room tower locations.",
                {
                    "list": (
                        "Get info about all tower locations in the specified room.",
                        self.list_tower_locations,
                        [site_name_arg, room_name_arg],
                    )
                },
            ),
            "tray_location": (
                "Manage tray locations sensors.",
                {
                    "list": (
                        "Get info about all tray locations in the specified room.",
                        self.list_tray_locations,
                        [site_name_arg, room_name_arg],
                    )
                },
            ),
            "miscellaneous_item": (
                "Manage room miscellaneous items.",
                {
                    "list": (
                        "Get info about all miscellaneous items in a room.",
                        self.list_miscellaneous_items,
                        [site_name_arg, room_name_arg],
                    )
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
            "location_service",
            "location service client",
            "l",
            self.build_commands(),
            lambda s, _: [{"tower_location": "tl", "tray_location": "yl", "sensor": "sr"}.get(s, s[0])],
        )

    def list_sites(self):
        """Gets from the /sites endpoint a list of all sites.

        Returns:
            (list): A list of all sites.
        """
        return self.__service_client.get(["sites"]).json()

    def get_site(self, site_name):
        """Gets from the /sites/{site-name} endpoint a particular site.

        Args:
            site_name (str): The name of the site being requested.
        Returns:
            (dict): The site requested.
        """
        return self.__service_client.get(["sites", site_name]).json()

    def update_site(self, site_name, site=None, site_fname=None):
        """Puts to the /sites/{site-name} endpoint to create or update a site.

        Args:
            site_name (str): The name of the site being updated.
            site (str, optional): A formatted string with the site's
                information. Defaults to None. Either this or site_fname must be
                None.
            site_fname (str, optional): The filename of the file containing the
                site's information. Defaults to None. Either this or site must
                be None.
        Return:
            (None): None.
        """
        site = validate_update_content(site, site_fname)
        return self.__service_client.put(["sites", site_name], req_json=site)

    def list_rooms(self, site_name, omit_items):
        """Gets from the /sites/{site-name}/rooms endpoint a list of all rooms
        in a specified site.

        Args:
            site_name (str): The name of the site whose rooms are being
            requested.
            omit_items (bool): Whether or not to omit the rooms' items.
        Returns:
            (list): A list of all rooms.
        """
        if not omit_items:
            omit_items = None
        params = {"omitItems": omit_items}
        return self.__service_client.get(["sites", site_name, "rooms"], query_args=params).json()

    def get_room(self, site_name, room_name):
        """Gets from the /sites/{site-name}/rooms/{room-name} endpoint a
        particular room in the specified site.

        Args:
            site_name (str): The name of the site whose rooms are being
            requested.
            room_name (str): The name of the room being requested.
        Returns:
            (dict): The room requested.
        """
        return self.__service_client.get(["sites", site_name, "rooms", room_name]).json()

    def update_room(self, site_name, room_name, room=None, room_fname=None):
        """Puts to the /sites/{site-name}/rooms/{room-name} endpoint to create
        or update a room in the specified site.

        Args:
            site_name (str): The name of the site in which the room being
            updated is located.
            room_name (str): The name of the room being updated.
            room (str, optional): A formatted string with the room's
                information. Defaults to None. Either this or room_fname must be
                None.
            room_fname (str, optional): The filename of the file containing the
                room's information. Defaults to None. Either this or room must
                be None.
        Return:
            (None): None.
        """
        room = validate_update_content(room, room_fname)
        return self.__service_client.put(["sites", site_name, "rooms", room_name], req_json=room)

    def update_items(self, site_name, room_name, items=None, items_fname=None):
        """Puts to the /sites/{site-name}/rooms/{room-name}/items endpoint to
        create or update particular items in the specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.
            items (str, optional): A formatted string listing the items'
                information. Defaults to None. Either this or items_fname must
                be None.
            items_fname (str, optional): The filename of the file containing the
                items' information. Defaults to None. Either this or items must
                be None.
        Return:
            (None): None.
        """
        items = validate_update_content(items, items_fname)
        return self.__service_client.put(["sites", site_name, "rooms", room_name, "items"], req_json=items)

    def delete_items(self, site_name, room_name, items=None, items_fname=None):
        """Deletes from the /sites/{site-name}/rooms/{room-name}/items endpoint
        to delete particular items in the specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.
            items (str, optional): A formatted string listing the items'
                information. Defaults to None. Either this or items_fname must
                be None.
            items_fname (str, optional): The filename of the file containing the
                items' information. Defaults to None. Either this or items must
                be None.
        Return:
            (None): None.
        """
        items = validate_update_content(items, items_fname)
        return self.__service_client.delete(["sites", site_name, "rooms", room_name, "items"], req_json=items)

    def list_dashboard_metrics(self, site_name, room_name):
        """Lists from the /sites/{site-name}/rooms/{room-name}/dashboard-metrics
        endpoint the environment dashboard metrics for the specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.
        Return:
            (list): A list of the environment dashboard metrics for the
            specified room.
        """
        return self.__service_client.get(["sites", site_name, "rooms", room_name, "dashboard-metrics"]).json()

    def update_dashboard_metrics(self, site_name, room_name, dashboard_metrics, dashboard_metrics_fname=None):
        """Puts to the /sites/{site-name}/rooms/{room-name}/dashboard-metrics
        endpoint to create or update particular environment dashboard metrics
        for a specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.
            dashboard_metrics (list): List of the dashboard metrics to create
            or update.
            dashboard_metrics_fname (str, optional): The filename of the file
            containing the dashboard metrics' information. Defaults to None.
            Either this or dashboard_metrics must be None.
        Returns:
            (None): None.
        """

        dashboard_metrics = validate_update_content(dashboard_metrics, dashboard_metrics_fname)
        return self.__service_client.put(
            ["sites", site_name, "rooms", room_name, "dashboard-metrics"],
            req_json=dashboard_metrics,
        )

    def delete_dashboard_metrics(self, site_name, room_name, dashboard_metrics, dashboard_metrics_fname=None):
        """Deletes from the /sites/{site-name}/rooms/{room-name}/dashboard-metrics
        endpoint particular dashboard metrics for a specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.
            dashboard_metrics (list): List of the dashboard metrics to delete.
            dashboard_metrics_fname (str, optional): The filename of the file
            containing the dashboard metrics' information. Defaults to None.
            Either this or dashboard_metrics must be None.
        Returns:
            (None): None.
        """

        dashboard_metrics = validate_update_content(dashboard_metrics, dashboard_metrics_fname)
        return self.__service_client.delete(
            ["sites", site_name, "rooms", room_name, "dashboard-metrics"],
            req_json=dashboard_metrics,
        )

    def update_controls(self, site_name, room_name, controls, controls_fname=None):
        """Puts to the /sites/{site-name}/rooms/{room-name}/controls endpoint
        to create or update particular controls for a specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.
            controls (str, optional): A formatted string listing the controls'
                information. Defaults to None. Either this or controls_fname
                must be None.
            controls_fname (str): The filename of the file containing the
                listing of the controls' information. Defaults to None. Either
                this or controls must be None.
        Returns:
            (None): None.
        """

        controls = validate_update_content(controls, controls_fname)
        return self.__service_client.put(["sites", site_name, "rooms", room_name, "controls"], req_json=controls)

    def delete_controls(self, site_name, room_name, control_names, control_names_fname=None):
        """Deletes from the /sites/{site-name}/rooms/{room-name}/controls
        endpoint particular controls for a specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.
            control_names (list): List of names of the controls to delete.
            control_names_fname (str): The filename of the file containing the
                controls' names. Defaults to None. Either this or controls must
                be None.
        Returns:
            (None): None.
        """
        control_names = validate_update_content(control_names, control_names_fname)
        return self.__service_client.delete(
            ["sites", site_name, "rooms", room_name, "controls"], req_json=control_names
        )

    def list_sensors(self, site_name, room_name):
        """Gets from the /sites/{site-name}/rooms/{room-name}/sensors endpoint
        a list of all sensors in the specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.

        Returns:
            (list): A list of all sensors in the specified room.
        """
        return self.__service_client.get(["sites", site_name, "rooms", room_name, "sensors"]).json()

    def list_tower_locations(self, site_name, room_name):
        """Gets from the /sites/{site-name}/rooms/{room-name}/tower-locations
        endpoint a list of all tower locations in the specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.

        Returns:
            (list): A list of all tower locations in the specified room.
        """
        return self.__service_client.get(["sites", site_name, "rooms", room_name, "tower-locations"]).json()

    def list_tray_locations(self, site_name, room_name):
        """Gets from the /sites/{site-name}/rooms/{room-name}/tray-locations
        endpoint a list of all tray-locations in the specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.

        Returns:
            (list): A list of all tray-locations in the specified room.
        """
        return self.__service_client.get(["sites", site_name, "rooms", room_name, "tray-locations"]).json()

    def list_miscellaneous_items(self, site_name, room_name):
        """Gets from the /sites/{site-name}/rooms/{room-name}/miscellaneous-items
        endpoint a list of all miscellaneous items in the specified room.

        Args:
            site_name (str): The name of the site.
            room_name (str): The name of the room.

        Returns:
            (list): A list of all miscellaneous items in the specified room.
        """
        return self.__service_client.get(["sites", site_name, "rooms", room_name, "miscellaneous-items"]).json()
