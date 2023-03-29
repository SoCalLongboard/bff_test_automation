"""This module implements methods which interact the web API for the Plenty traceability store."""

from typing import Dict, List, Optional

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, format_url_with_version


class TraceabilityClient(BaseClient):
    """Client communicating with the Plenty traceability store via REST."""

    _application_name = "Traceability Store"
    _service_name = "traceability-store"
    _api_version = "v0"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return TraceabilityClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return TraceabilityClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return TraceabilityClient._api_version

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
        """Build the commands for this client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        site_arg = ["site"], {"help": "the site"}
        start_datetime_arg = (
            ["start_datetime"],
            {"help": "the start datetime of the range"},
        )
        end_datetime_arg = ["end_datetime"], {"help": "the end datetime of the range"}
        packaging_lot_arg = ["packaging_lot"], {"help": "the packaging lot to get"}
        pti_arg = ["case_id"], {"help": "the PTI record to get"}
        start_date_maybe_arg = (
            ["--start-date"],
            {"dest": "start_date", "help": "the start date of the range"},
        )
        end_date_maybe_arg = (
            ["--end-date"],
            {"dest": "end_date", "help": "the end date of the range"},
        )

        return {
            "planting": (
                "Planting records.",
                {
                    "list": (
                        "List a range of planting records.",
                        self.list_plantings,
                        [site_arg, start_datetime_arg, end_datetime_arg],
                    )
                },
            ),
            "packaging": (
                "Packaging record.",
                {
                    "get": (
                        "Get a specific packaging lot record.",
                        self.get_packaging_lot,
                        [packaging_lot_arg],
                    )
                },
            ),
            "pti": (
                "PTI record.",
                {
                    "get": (
                        "Get a specific PTI record.",
                        self.get_pti_record,
                        [pti_arg],
                    ),
                    "list": (
                        "List PTI records for a given site.",
                        self.get_pti_records,
                        [site_arg, start_date_maybe_arg, end_date_maybe_arg],
                    ),
                },
            ),
            "action": (
                "Action record.",
                {
                    "netsuite": (
                        "Release the packaging lots in NetSuite.",
                        self.release_packaging_lots_in_netsuite,
                        [site_arg, start_date_maybe_arg, end_date_maybe_arg],
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
            "traceability",
            "traceability store client",
            "t",
            self.build_commands(),
            lambda s, _: [{"planting": "pl", "packaging": "pa"}.get(s, s[0])],
        )

    def list_plantings(self, site: str, start_datetime: str, end_datetime: str) -> list:
        """Get from the /planting_records endpoint a list of all planting records found for a site for a given start and end date range.

        Args:
            site (str): The site of interest.
            start_datetime (str): The start datetime for the beginning of date
                range.
            end_datetime (str): The end datetime for the end of the date range.
        Returns:
            (list): A list of planting models.
        """
        params = {"site": site, "startDate": start_datetime, "endDate": end_datetime}
        return self.__service_client.get(["planting_records"], query_args=params).json()

    def list_harvestings(self, site: str, start_datetime: str, end_datetime: str) -> List:
        """Get from the /harvesting_records endpoint a list of all harvesting records found for a site for a given start and end date range.

        Args:
            site (str): The site of interest.
            start_datetime (str): The start datetime for the beginning of date
                range.
            end_datetime (str): The end datetime for the end of the date range.
        Returns:
            (list): A list of harvesting models.
        """
        params = {"site": site, "startDate": start_datetime, "endDate": end_datetime}
        return self.__service_client.get(["harvesting_records"], query_args=params).json()

    def list_postharvestings(self, site: str, start_datetime: str, end_datetime: str) -> List:
        """Get from the /postharvest_records endpoint a list of all post harvest records found for a site for a given start and end date range.

        Args:
            site (str): The site of interest.
            start_datetime (str): The start datetime for the beginning of date
                range.
            end_datetime (str): The end datetime for the end of the date range.
        Returns:
            (list): A list of postharvest models.
        """
        params = {"site": site, "startDate": start_datetime, "endDate": end_datetime}
        return self.__service_client.get(["postharvest_records"], query_args=params).json()

    def get_packaging_lots(self, site: str, start_datetime: str, end_datetime: str) -> List:
        """Get from the /packaging_lots endpoint a list of all packaging lots found for a site for a given start and end date range.

        Args:
            site (str): The site of interest.
            start_datetime (str): The start datetime for the beginning of date
                range.
            end_datetime (str): The end datetime for the end of the date range.
        Returns:
            (list): A list of packaging lots models.
        """
        params = {"site": site, "startDate": start_datetime, "endDate": end_datetime}
        return self.__service_client.get("packaging_lots", query_args=params).json()

    def get_packaging_lot(self, packaging_lot: str) -> Dict:
        """Get from the /packaging_lot endpoint the specifics of a given packaging lot.

        Args:
            packaging_lot (str): The packaging lot id.
        Returns:
            (dict): The specific packaging lot.
        """
        return self.__service_client.get("packaging_lot", query_args={"packagingLot": packaging_lot}).json()

    def release_packaging_lots_in_netsuite(self, site: str, start_date: str, end_date: str) -> Dict:
        """Release the packaging lots in NetSuite for the given site and date range.

        Args:
            packaging_lot_ids (list): A list of packaging lot IDs.
            site (str): The site the packaging lots are related to.
            start_date (str): The start date in ISO8601 format.
            end_date (str): The end date in ISO8601 format.

        Returns:
            (dict): The success response object.
        """
        data = {"site": site, "startDate": start_date, "endDate": end_date}
        return self.__service_client.post(["packaging-lots/release-in-netsuite"], req_json=data).json()

    def create_pti_record(
        self,
        site: str,
        product: str,
        unit_type: str,
        gtin: str,
        lot: str,
        netsuite_item: str,
        package_date: str,
        internal_expiration_date: str,
    ) -> Dict:
        """Create a PTI label record.

        Args:
            site (str): The site a PTI record is creating for.
            product (str): The product (cultivar).
            unit_type (str): The unit type.
            gtin (str): The GTIN.
            lot (str): The packaging lot.
            netsuite_item (str): The Netsuite item.
            package_date (str): The packaging date in ISO8601 format.
            internal_expiration_date (str): The internal expiration date string in ISO8601 format.
        Returns:
            (dict): The created PTI label record.
        """
        return self.create_pti_records(
            site,
            product,
            unit_type,
            gtin,
            lot,
            netsuite_item,
            package_date,
            internal_expiration_date,
            total_count=1,
        )[0]

    def create_pti_records(
        self,
        site: str,
        product: str,
        unit_type: str,
        gtin: str,
        lot: str,
        netsuite_item: str,
        package_date: str,
        internal_expiration_date: str,
        total_count: int = 1,
    ) -> Dict:
        """Create the PTI label records.

        Args:
            site (str): The site a PTI record is creating for.
            product (str): The product (cultivar).
            unit_type (str): The unit type.
            gtin (str): The GTIN.
            lot (str): The packaging lot.
            netsuite_item (str): The Netsuite item.
            package_date (str): The packaging date in ISO8601 format.
            internal_expiration_date (str): The internal expiration date string in ISO8601 format.
            total_count (int): The total count of records to create.
        Returns:
            (dict): The created PTI labels records.
        """
        pti_label = {
            "site": site,
            "product": product,
            "unitType": unit_type,
            "gtin": gtin,
            "lot": lot,
            "netsuiteItem": netsuite_item,
            "packageDate": package_date,
            "internalExpirationDate": internal_expiration_date,
        }
        return self.__service_client.post(["bulk", "pti", str(total_count)], req_json=pti_label).json()

    def create_deferred_pti_record(self, internal_qr_code_content: object) -> Dict:
        """Create a PTI label record by its internal QR code content.

        Args:
            internal_qr_code_content (object): The internal QR code content of PTI label.
        Returns:
            (dict): The created PTI label record.
        """
        return self.__service_client.post(["deferred-pti"], req_json=internal_qr_code_content).json()

    def get_pti_record(self, case_id: str) -> Dict:
        """Get a PTI record by its case ID.

        Args:
            case_id (str): The case ID of the PTI record.
        Returns:
            (dict): The specific PTI record.
        """
        return self.__service_client.get(["pti", case_id]).json()

    def get_pti_records(
        self,
        site: str,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ) -> List:
        """Get a list of PTI records.

        Args:
            site (str): The site of the PTI records.
            start_date (str): The start datetime for the beginning of a date range.
            end_date (str): The end datetime for the end of a date range.
        Returns:
            (list): A list of PTI record models.
        """
        return self.__service_client.get(
            ["pti"],
            query_args={"site": site, "startDate": start_date, "endDate": end_date},
        ).json()

    def remove_pti_record(self, case_id: str) -> Dict:
        """Remove a PTI record by its case ID.

        Args:
            case_id (str): The case ID of the PTI record.
        Returns:
            (dict): The specific PTI record.
        """
        return self.__service_client.delete(["pti", case_id]).json()

    def finalize_pti_labels_by_case_ids(self, case_ids: list) -> Dict:
        """Finalize PtiLabels identified by a list of case IDs.

        Args:
            case_ids (list): A list of case IDs.
        Returns:
            (dict): The success response object.
        """
        return self.__service_client.post(["actions/finalize-by-case-ids"], req_json=case_ids).json()

    def finalize_pti_labels(self, internal_qr_code_content_list: list) -> Dict:
        """Finalize PtiLabels identified by a list of internal QR code content entities.

        Args:
            internal_qr_code_content_list (list): A list of internal QR code content entities.
        Returns:
            (dict): The success response object.
        """
        return self.__service_client.post(["actions/finalize"], req_json=internal_qr_code_content_list).json()

    def persist_pti_labels_to_netsuite(self, case_ids: list) -> Dict:
        """Persist PtiLabels identified by a list of case IDs to NetSuite.

        Args:
            case_ids (list): A list of case IDs.
        Returns:
            (dict): The success response object.
        """
        return self.__service_client.post(["actions/persist-pti-labels-to-netsuite"], req_json=case_ids).json()

    def get_pti_records_by_pallet_serial_id(self, pallet_serial_id: str) -> List:
        """Get all PTI label records related to the pallet serial ID.

        Args:
            pallet_serial_id (str): The pallet serial ID the PTI label records are related to.
        Returns:
            (dict): The PTI labels records.
        """
        params = {"palletSerialId": pallet_serial_id}
        return self.__service_client.get(["pti"], query_args=params).json()

    def get_pti_records_by_sscc(self, sscc: str) -> List:
        """Get all PTI label records related to the SSCC.

        Args:
            sscc (str): The SSCC the PTI label records are related to.
        Returns:
            (dict): The PTI labels records.
        """
        params = {"sscc": sscc}
        return self.__service_client.get(["pti"], query_args=params).json()

    def create_pallet(self) -> Dict:
        """Create a pallet with the auto-generated pallet serial ID and SSCC.

        Returns:
            (dict): The created pallet object.
        """
        return self.__service_client.post(["pallets"]).json()

    def get_pallet(self, pallet_serial_id: str) -> Dict:
        """Get a pallet by the pallet serial ID.

        Args:
            pallet_serial_id (str): The pallet serial ID.
        Returns:
            (dict): The pallet object.
        """
        return self.__service_client.get(["pallets", pallet_serial_id]).json()

    def add_cases_to_pallet(self, pallet_serial_id: str, case_ids: list) -> Dict:
        """Add (assign) the cases to the given pallet.

        Args:
            pallet_serial_id (str): The pallet serial ID.
            case_ids (list): A list of case IDs.
        Returns:
            (dict): The success response object.
        """
        return self.__service_client.post(["pallets", pallet_serial_id, "cases"], req_json=case_ids).json()

    def remove_cases_from_pallet(self, pallet_serial_id: str, case_ids: list) -> Dict:
        """Remove (un-assign) the cases from the given pallet.

        Args:
            pallet_serial_id (str): The pallet serial ID.
            case_ids (list): A list of case IDs.
        Returns:
            (dict): The success response object.
        """
        return self.__service_client.delete(["pallets", pallet_serial_id, "cases"], req_json=case_ids).json()
