"""This module implements methods which interact the web API for the Plenty
varietal information store."""

from ..base_client import BaseClient
from ..common import (
    validate_update_content,
    AuthenticatedServiceClient,
    format_url_with_version,
)


class VarietalInformationServiceClient(BaseClient):
    """Client communicating with the Plenty varietal information service via
    REST."""

    _application_name = "Varietal Information Service"
    _service_name = "varietal-information-service"
    _api_version = "v0"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return VarietalInformationServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return VarietalInformationServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return VarietalInformationServiceClient._api_version

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
        site_arg = ["site"], {"help": "the site to get the record versions for"}
        datetime_arg = ["datetime"], {"help": "a datetime in ISO8601 format"}
        record_fname_arg = (
            ["record_fname"],
            {"help": "a file containing the varietal record in JSON format"},
        )
        attribute_arg = (
            ["attribute"],
            {"help": "an attribute to filter the record with"},
        )
        crop_arg = (
            ["crop"],
            {"help": "a crop_id (such as A10) to filter the record with"},
        )

        return {
            "records": (
                "Manage records.",
                {
                    "versions": (
                        "List all record versions for a site.",
                        self.get_versions,
                        [site_arg],
                    ),
                    "latest": (
                        "Get most recent record for a site.",
                        self.get_latest_record,
                        [site_arg],
                    ),
                    "get": (
                        "Get most recent record for a site at or before a given datetime,",
                        self.get_record,
                        [site_arg, datetime_arg],
                    ),
                    "upload": (
                        "Create a record for a site.",
                        self.put_record,
                        [site_arg, record_fname_arg],
                    ),
                    "attribute": (
                        "Get most recent record for a site at or before a given datetime and filter for one attribute.",
                        self.get_record_and_summarize,
                        [site_arg, datetime_arg, attribute_arg],
                    ),
                    "crop": (
                        "Get most recent record for a site at or before a given datetime and filter for one crop.",
                        self.get_record_crop,
                        [site_arg, datetime_arg, crop_arg],
                    ),
                },
            )
        }

    def build_cli_subcommand(self):
        """Bulid the CLI subcommand for this client.

        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return (
            "varietal_information",
            "varietal information service client",
            "v",
            self.build_commands(),
            lambda s, _: [s[0]],
        )

    def get_versions(self, site):
        """Gets from the /versions/{site} endpoint a list of all versions
        (records) for a given site.

        Args:
            site (str): The site to list all records from.
        Returns:
            (list): A list of all versions.
        """
        return self.__service_client.get(["versions", site]).json()

    def get_latest_record(self, site):
        """Gets from the /records/{site} endpoint the most recent record for a
        particular site.

        Args:
            site (str): The site to get the record from.
        Returns:
            (dict): The most recent varietal info record available for a site.
        """
        return self.__service_client.get(["records", site]).json()

    def get_record(self, site, datetime):
        """Gets from the /records/{site}/{datetime} endpoint the most recent
        record available for a given site that occurred at or before the given
        datetime.

        Args:
            site (str): The site to get the record from.
            datetime (str): The datetime in ISO8601 format.
        Returns:
            (dict): The most recent varietal info record available for a site
                at or before the given datetime.
        """
        return self.__service_client.get(["records", site, datetime]).json()

    def put_record(self, site, record=None, record_fname=None):
        """Puts a given record to the /records/{site} endpoint to be stored.

        Args:
            site (str): The site to upload the record to.
            record (str, optional): A formatted string with the varietal record
                information. Defaults to None. Either this or record_fname must
                be None.
            record_fname (str, optional): The filename of the file containing
                the varietal record information. Defaults to None. Either this
                or user must be None.
        Returns:
            (str): Success if the record is validated successfully and
                persisited.
        """
        record = validate_update_content(record, record_fname)
        self.__service_client.put(["records", site], req_json=record)

    def get_record_and_summarize(self, site, datetime, attribute):
        """Gets from the /records/{site}/{datetime} endpoint the most recent
        record available for a given site that occurred at or before the given
        datetime. Then returns a summary of just one attribute across all crops.

        Args:
            site (str): The site to get the record from.
            datetime (str): The datetime in ISO8601 format.
            attribute (str): The attribute to summarize on.
        Returns:
            (dict): The most recent varietal info record available for a site
                at or before the given datetime as a summary.
        """
        varietal_dict = self.__service_client.get(["records", site, datetime]).json()
        summary_dict = {}
        for crop_id, crop_info in varietal_dict["varietals"].items():
            summary_dict[crop_id] = crop_info[attribute]
        return summary_dict

    def get_record_crop(self, site, datetime, crop):
        """Gets from the /records/{site}/{datetime} endpoint the most recent
        record available for a given site that occurred at or before the given
        datetime. Then returns a only the info for a specific crop.

        Args:
            site (str): The site to get the record from.
            datetime (str): The datetime in ISO8601 format.
            crop (str): The crop to summarize on.
        Returns:
            (dict): The most recent varietal info record available for a site
                at or before the given datetime as a summary.
        """
        return self.__service_client.get(["records", site, datetime]).json()["varietals"][crop]
