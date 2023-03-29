"""This module implements methods which interact the web API for the Plenty
farm state service."""

import json

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, format_url_with_version


class FarmStateServiceClient(BaseClient):
    """Client communicating with the Plenty farm state service via REST."""

    _application_name = "Farm State Service"
    _service_name = "farm-state-service"
    _api_version = "v0"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return FarmStateServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return FarmStateServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return FarmStateServiceClient._api_version

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

    def build_commands(self):
        """Builds the commands for this client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        site_arg = ["site"], {"help": "A string of the site"}
        seeding_arg = (
            ["seeding_model"],
            {"help": "the JSON of the seeding model corresponding to the seeding event"},
        )
        planting_arg = (
            ["planting_model"],
            {"help": "the JSON of the planting model corresponding to the planting event"},
        )
        harvesting_arg = (
            ["harvesting_model"],
            {"help": "the JSON of the harvesting model corresponding to the event"},
        )
        device_location_arg = (
            ["device_location_model"],
            {"help": "the json of the new device location for move inventory"},
        )
        serial_arg = ["serial"], {"help": "the serial of the inventory to be moved"}
        filter_arg = (
            ["query_filter"],
            {"help": "JSON containing the query filter as described in FSS README"},
        )
        start_datetime_arg = ["start_datetime"], {"help": "A string of the start date"}
        end_datetime_arg_opt = (
            ["end_datetime"],
            {
                "nargs": "?",
                "help": "end datetime in ISO8601; defaults to now",
            },
        )

        return {
            "update": (
                "Update the state of the farm with an event",
                {
                    "seeding": (
                        "Update the state of the farm with a seeding event.",
                        self.put_seeding,
                        [seeding_arg],
                    ),
                    "planting": (
                        "Update the state of the farm with a planting event.",
                        self.put_planting,
                        [planting_arg],
                    ),
                    "harvesting": (
                        "Update the state of the farm with a harvesting event.",
                        self.put_harvesting,
                        [harvesting_arg],
                    ),
                    "move_inventory": (
                        "Update the state of the farm with an inventory location move.",
                        self.put_move_inventory,
                        [serial_arg, device_location_arg],
                    ),
                },
            ),
            "state": (
                "Get the current/past state of the farm.",
                {
                    "current": (
                        "Get the current state of the farm filtered by a query filter JSON.",
                        self.get_current,
                        [site_arg, filter_arg],
                    ),
                    "records": (
                        "Get all records of farm state changes in a date range (start and end datetimes specified) filtered by a query filter JSON.",
                        self.get_records,
                        [
                            site_arg,
                            filter_arg,
                            start_datetime_arg,
                            end_datetime_arg_opt,
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
            "farm_state",
            "farm state service client",
            "f",
            self.build_commands(),
            lambda s, _: [s[0]],
        )

    def put_seeding(self, seeding_model):
        """Updates the farm state service with a seeding event by putting to
        /event/seeding endpoint.

        Args:
            seeding_model (str): The seeding model.
        Returns:
            (list): A list farm state models that got created/modified as a
                result of this update.
        """
        return self.__service_client.put(["event", "seeding"], req_json=json.loads(seeding_model)).json()

    def delete_seeding(self, seeding_model):
        """Updates the farm state service with a seeding event deletion.

        Args:
            seeding_model (str): The seeding model.
        Returns:
            (list): A list farm state models that got created/modified as a
                result of this update.
        """
        return self.__service_client.delete(["event", "seeding"], req_json=json.loads(seeding_model)).json()

    def put_planting(self, planting_model):
        """Updates the farm state service with a planting event by putting to
        /event/planting endpoint.

        Args:
            planting_model (str): The planting model.
        Returns:
            (list): A list farm state models that got created/modified as a
                result of this update.
        """
        return self.__service_client.put(["event", "planting"], req_json=json.loads(planting_model)).json()

    def delete_planting(self, planting_model):
        """Updates the farm state service with a planting event deletion.

        Args:
            planting_model (str): The planting model.
        Returns:
            (list): A list farm state models that got created/modified as a
                result of this update.
        """
        return self.__service_client.delete(["event", "planting"], req_json=json.loads(planting_model)).json()

    def put_harvesting(self, harvesting_model):
        """Updates the farm state service with a harvesting event by putting to
            /event/harvesting endpoint.

        Args:
            harvesting_model (str): The harvesting model.
        Returns:
            (list): A list farm state models that got created/modified as a
                result of this update.
        """
        return self.__service_client.put(["event", "harvesting"], req_json=json.loads(harvesting_model)).json()

    def delete_harvesting(self, harvesting_model):
        """Updates the farm state service with a harvesting event deletion.

        Args:
            harvesting_model (str): The harvesting model.
        Returns:
            (list): A list farm state models that got created/modified as a
                result of this update.
        """
        return self.__service_client.delete(["event", "harvesting"], req_json=json.loads(harvesting_model)).json()

    def put_move_inventory(self, serial, device_location_model):
        """Updates the farm state service with a move inventory event by
        putting to /inventory/move/{serial} endpoint.

        Args:
            serial (str): The serial of the device.
            device_location_model (str): The device's new location model.
        Returns:
            (list): A list farm state models that got created/modified as a
                result of this update.
        """
        return self.__service_client.put(
            ["inventory", "move", serial], req_json=json.loads(device_location_model)
        ).json()

    def get_current(self, site, query_filter):
        """Gets from the /farm/current endpoint a list of all farm state models
        representing the current state of the farm.

        Args:
            site (str): The site in question.
            query_filter (str): The query filter to apply.
        Returns:
            (list): A list of farm state models representing the current state
                of the farm. Filtered by the filter passed in.
        """
        return self.__service_client.post(["farm", "current", site], req_json=json.loads(query_filter)).json()

    def get_records(self, site, query_filter, start_datetime, end_datetime=None):
        """Gets from the /farm/records endpoint a list of all farm state models
        representing the previous state of the farm.

        Args:
            site (str): The site in question.
            query_filter (str): The query filter to apply.
            start_datetime (str): The start datetime in ISO8601 format.
            end_datetime (str): The end datetime in ISO8601 format; defaults to
                now.
        Returns:
            (list): A list of farm state models representing all records of farm
                state changes.
        """
        if end_datetime:
            params = {"startDate": start_datetime, "endDate": end_datetime}
        else:
            params = {"startDate": start_datetime}
        return self.__service_client.post(
            ["farm", "records", site],
            query_args=params,
            req_json=json.loads(query_filter),
        ).json()
