"""This module implements methods that interact with the API for the Plenty
lab testing service."""

import base64
from typing import Optional, Dict, List
from ..models import CliCommand, CliSubCommand

from ..base_client import BaseClient
from ..common import (
    AuthenticatedServiceClient,
    AuthenticatedClient,
    Cfg,
    format_url_with_version,
)


class LabTestingServiceClient(BaseClient):
    """Client communicating with the Plenty lab testing service via REST."""

    _application_name = "LabTestingService"
    _service_name = "lab-testing-service"
    _api_version = "v0"

    @staticmethod
    def application_name() -> str:
        """Get the application name of the service.
        Returns:
            (str): The application name of the service.
        """
        return LabTestingServiceClient._application_name

    @staticmethod
    def service_name() -> str:
        """Get the subdomain of the service.
        Returns:
            (str): The subdomain of the service.
        """
        return LabTestingServiceClient._service_name

    @staticmethod
    def api_version() -> str:
        """Get the api version of this client to the service.
        Returns:
            (str): The api version of this client.
        """
        return LabTestingServiceClient._api_version

    def __init__(self, authenticated_client: AuthenticatedClient, url: str) -> None:
        """Create a new alert service client.

        Args:
            authenticated_client (common.AuthenticatedClient): Plenty service
                client that has credentials.
            url (str): The url to use for the client.
            subdomain (str): An override subdomain.
        """
        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version())
        )

    def build_commands(self) -> CliCommand:
        """Builds the commands for this client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        provider_arg = ["name"], {"help": "the provider of a lab test"}
        kind_arg = ["name"], {"help": "the kind of lab test"}
        uuid_arg = ["uuid"], {"help": "the uuid of lab test type"}
        id_arg = ["id"], {"help": "the id of lab test sample"}
        event_kind_arg = ["event_kind"], {"help": "an event kind (e.g. blob, manual)"}
        event_data_arg = (
            ["event_data"],
            {"help": "a structure containing a lab event metadata"},
        )
        test_type_arg = (
            ["test_type"],
            {"help": "a structure containing a lab test type definition"},
        )
        sample_arg = (
            ["sample"],
            {
                "help": "a lab test sample definition "
                + " (e.g. plenty_username, lab_test_kind, lab_test_provider,"
                + " farm_def_id, farm_def_path, sample_type"
            },
        )
        samples_arg = (
            ["samples"],
            {
                "help": "a list of lab test sample definitions "
                + " (e.g. plenty_username, lab_test_kind, lab_test_provider,"
                + " farm_def_id, farm_def_path, sample_type"
            },
        )
        sample_ids_arg = ["samples"], {"help": "a list of lab test sample ids"}
        days_without_results = (
            ["days_without_results"],
            {"help": "days without lab results after sample was created"},
        )
        alert_when_days_without_results = (
            ["trigger_alert"],
            {
                "help": "Trigger a Plenty alert service message to LAB-TESTING-<lab_test_name> "
                + 'for "prod" k8s env if a lab result is not found after x days'
            },
        )
        lab_tests_per_page_maybe_arg = (
            ["-resultsperpage"],
            {
                "dest": "lab_tests_per_page",
                "help": "the lab_tests_per_page for the query",
            },
        )
        page_maybe_arg = (
            ["-page"],
            {
                "dest": "page",
                "help": "the page to load for the query",
            },
        )
        lab_test_provider_maybe_arg = (
            ["-o"],
            {
                "dest": "lab_test_provider",
                "help": "the lab_test_provider of the lab sample",
            },
        )
        lab_test_kind_maybe_arg = (
            ["-k"],
            {
                "dest": "lab_test_kind",
                "help": "the lab_test_kind of the lab sample",
            },
        )
        lab_test_passed_maybe_arg = (
            ["-t"],
            {
                "dest": "lab_test_passed",
                "help": "the lab_test_passed status of the lab sample",
            },
        )
        lab_test_sample_id_maybe_arg = (
            ["-sid"],
            {
                "dest": "lab_test_sample_id",
                "help": "the lab_test_sample_id of the lab sample",
            },
        )
        created_by_username_maybe_arg = (
            ["-usr"],
            {
                "dest": "created_by_username",
                "help": "the created_by_username of the lab sample",
            },
        )
        farm_def_id_maybe_arg = (
            ["-id"],
            {
                "dest": "farm_def_id",
                "help": "the farm_def_id of the lab sample",
            },
        )
        farm_def_path_maybe_arg = (
            ["-fp"],
            {
                "dest": "farm_def_path",
                "help": "the farm_def_path of the lab sample",
            },
        )
        sample_type_maybe_arg = (
            ["-s"],
            {
                "dest": "sample_type",
                "help": "the sample type of the lab sample",
            },
        )
        notes_maybe_arg = (
            ["-n"],
            {
                "dest": "notes",
                "help": "the notes of the lab sample",
            },
        )
        sub_location_maybe_arg = (
            ["-sl"],
            {
                "dest": "sub_location",
                "help": "the sub location of the lab sample",
            },
        )
        label_details_maybe_arg = (
            ["-sticker"],
            {
                "dest": "label_details",
                "help": "the label details of the lab sample",
            },
        )
        sample_date_start_maybe_arg = (
            ["-sds"],
            {
                "dest": "sample_date_start",
                "help": "the sample start date of the lab sample",
            },
        )
        sample_date_end_maybe_arg = (
            ["-sde"],
            {
                "dest": "sample_date_end",
                "help": "the sample end date of the lab sample",
            },
        )
        lot_code_maybe_arg = (
            ["-x"],
            {
                "dest": "lot_code",
                "help": "the lot code of the lab sample",
            },
        )
        product_code_maybe_arg = (
            ["-y"],
            {
                "dest": "product_code",
                "help": "the product code of the lab sample",
            },
        )
        predicted_harvest_date_maybe_arg = (
            ["-z"],
            {
                "dest": "product_code",
                "help": "the predicted harvest date of the lab sample",
            },
        )
        trial_id_maybe_arg = (
            ["-trial"],
            {
                "dest": "trial_id",
                "help": "the trial_id of the lab sample",
            },
        )
        treatment_id_maybe_arg = (
            ["-treatment"],
            {
                "dest": "treatment_id",
                "help": "the treatment_id of the lab sample",
            },
        )
        harvest_cycle_maybe_arg = (
            ["-harvestcycle"],
            {
                "dest": "harvest_cycle",
                "help": "the harvest_cycle of the lab sample",
            },
        )
        health_status_maybe_arg = (
            ["-healthstatus"],
            {
                "dest": "health_status",
                "help": "the health_status of the lab sample",
            },
        )
        container_id_maybe_arg = (
            ["-containerid"],
            {
                "dest": "container_id",
                "help": "the container id of the lab sample",
            },
        )
        material_lot_maybe_arg = (
            ["-materiallot"],
            {
                "dest": "material_lot",
                "help": "the material lot of the lab sample",
            },
        )
        start_time_maybe_arg = (
            ["-stime"],
            {
                "dest": "start_time",
                "help": "the start time of the lab test",
            },
        )
        end_time_maybe_arg = (
            ["-ftime"],
            {
                "dest": "end_time",
                "help": "the end time of the lab test",
            },
        )
        nutrient_stage_maybe_arg = (
            ["-nutrientstage"],
            {
                "dest": "nutrient_stage",
                "help": "the nutrient stage of the lab sample",
            },
        )
        dump_refill_status_maybe_arg = (
            ["-dumprefillstatus"],
            {
                "dest": "dump_refill_status",
                "help": "the dump refill status of the lab sample",
            },
        )
        order_by_maybe_arg = (
            ["-orderby"],
            {
                "dest": "order_by",
                "help": "the order by field sequence of lab tests",
            },
        )
        farm_def_path_arg = (
            ["-fpsl"],
            {
                "dest": "farm_def_path",
                "help": "the farm_def_path of to get sub locations from",
            },
        )
        return {
            "types": (
                "Manage lab test types.",
                {
                    "get": (
                        "Get info about a lab test type.",
                        self.get_lab_test_type_by_uuid,
                        [uuid_arg],
                    ),
                    "list": ("List all lab test types.", self.list_lab_test_types, []),
                    "create": (
                        "Create lab test type.",
                        self.create_lab_test_type,
                        [test_type_arg],
                    ),
                },
            ),
            "samples": (
                "Manage lab test samples.",
                {
                    "get": (
                        "Get info about a lab test sample by id.",
                        self.get_lab_test_sample_by_id,
                        [id_arg],
                    ),
                    "list": (
                        "List all lab test samples.",
                        self.list_lab_test_samples,
                        [
                            lab_tests_per_page_maybe_arg,
                            page_maybe_arg,
                            lab_test_provider_maybe_arg,
                            lab_test_kind_maybe_arg,
                            lab_test_passed_maybe_arg,
                            lab_test_sample_id_maybe_arg,
                            created_by_username_maybe_arg,
                            farm_def_id_maybe_arg,
                            farm_def_path_maybe_arg,
                            sample_type_maybe_arg,
                            notes_maybe_arg,
                            sub_location_maybe_arg,
                            label_details_maybe_arg,
                            sample_date_start_maybe_arg,
                            sample_date_end_maybe_arg,
                            lot_code_maybe_arg,
                            product_code_maybe_arg,
                            predicted_harvest_date_maybe_arg,
                            trial_id_maybe_arg,
                            treatment_id_maybe_arg,
                            harvest_cycle_maybe_arg,
                            health_status_maybe_arg,
                            start_time_maybe_arg,
                            container_id_maybe_arg,
                            material_lot_maybe_arg,
                            end_time_maybe_arg,
                            nutrient_stage_maybe_arg,
                            dump_refill_status_maybe_arg,
                            order_by_maybe_arg,
                        ],
                    ),
                    "create": (
                        "Create lab test samples",
                        self.create_lab_test_samples,
                        [samples_arg],
                    ),
                    "delete": (
                        "Delete lab test samples",
                        self.delete_lab_test_samples,
                        [sample_ids_arg],
                    ),
                    "no_results": (
                        "Get lab test samples without results after X days",
                        self.get_lab_samples_without_results_after_x_days,
                        [
                            provider_arg,
                            kind_arg,
                            days_without_results,
                            alert_when_days_without_results,
                        ],
                    ),
                    "url_for_s3": (
                        "Get S3 link for file linked to lab test",
                        self.get_url_for_s3_file_uuid,
                        [uuid_arg],
                    ),
                    "sub_locations": (
                        "Get lab test sub location for farm_def path",
                        self.get_sub_locations_from_farm_def_path,
                        [farm_def_path_arg],
                    ),
                },
            ),
            "events": (
                "Manage lab test events.",
                {
                    "create": (
                        "Create lab event",
                        self.create_lab_test_event,
                        [event_kind_arg, event_data_arg],
                    )
                },
            ),
        }

    def build_cli_subcommand(self) -> CliSubCommand:
        """Bulid the CLI subcommand for this client.

        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return (
            "lab_testing_service",
            "lab testing service client",
            "lt",
            self.build_commands(),
            lambda s, _: [s[0]],
        )

    def get_lab_test_type_by_uuid(self, uuid: str) -> Dict:
        """Gets a lab test type by UUID from /lab-test-type/{id} endpoint

        Args:
            type (str): The UUID of a lab test type
        Returns:
            (dict): The requested lab test type.
        """
        return self.__service_client.get(["lab-test-type", uuid]).json()

    def list_lab_test_types(self) -> Dict:
        """Gets lab tests types from /lab-test-type endpoint.

        Returns:
            (list): A list of lab test types.
        """
        return self.__service_client.get(["lab-test-type"]).json()

    def create_lab_test_type(self, test_type: dict) -> Dict:
        """Create a lab test type from /lab-test-type/ endpoint

        Args:
            test_type (dict): The test_type data structure for a lab test type
        Returns:
            (dict): The created lab type result.
        """
        return self.__service_client.post(["lab-test-type"], req_json=test_type).json()

    def get_lab_test_sample_by_id(self, id: str) -> Dict:
        """Gets a lab test sample by id from /lab-test-sample/{id} endpoint

        Args:
            id (str): The ID of the lab test sample
        Returns:
            (dict): The requested lab test sample.
        """
        return self.__service_client.get(["lab-test-sample", id]).json()

    def list_lab_test_samples(
        self,
        lab_tests_per_page: Optional[str] = None,
        page: Optional[str] = None,
        lab_test_provider: Optional[str] = None,
        lab_test_kind: Optional[str] = None,
        lab_test_passed: Optional[str] = None,
        lab_test_sample_id: Optional[str] = None,
        created_by_username: Optional[str] = None,
        farm_def_id: Optional[str] = None,
        farm_def_path: Optional[str] = None,
        sample_type: Optional[str] = None,
        notes: Optional[str] = None,
        sub_location: Optional[str] = None,
        label_details: Optional[str] = None,
        sample_date_start: Optional[str] = None,
        sample_date_end: Optional[str] = None,
        lot_code: Optional[str] = None,
        product_code: Optional[str] = None,
        predicted_harvest_date: Optional[str] = None,
        trial_id: Optional[str] = None,
        treatment_id: Optional[str] = None,
        harvest_cycle: Optional[str] = None,
        health_status: Optional[str] = None,
        container_id: Optional[str] = None,
        material_lot: Optional[str] = None,
        start_time: Optional[str] = None,
        end_time: Optional[str] = None,
        nutrient_stage: Optional[str] = None,
        dump_refill_status: Optional[str] = None,
        order_by: Optional[str] = None,
    ) -> Dict:
        """Gets lab tests by name from /lab-test-sample endpoint.
        Args:
            lab_tests_per_page: The test samples per page. Defaults to 500
            page: The results page to load for a given query. Defaults to 1
            lab_test_provider: The provider of the lab test. Defaults to None to not
                query on this property.
            lab_test_kind: The kind of the lab test. Defaults to None to not
                query on this property.
            lab_test_passed: The passed status of the lab test. Defaults to None to not
                query on this property.
            lab_test_sample_id: The sample id of the lab test. Defaults to None to not
                query on this property.
            created_by_username: The username that created the lab test. Defaults to None to not
                query on this property.
            farm_def_id: The farm def id of the lab test. Defaults to None to not
                query on this property.
            farm_def_path: The farm def path of the lab test. Defaults to None to not
                query on this property.
            sample_type (str): The sample type of the lab test. Defaults to None to not
                query on this property.
            notes (str): The notes of the lab test. Defaults to None to not
                query on this property.
            sub_location (str): The sub location of the lab test. Defaults to None to not
                query on this property.
            label_details (str): The label details of the lab test. Defaults to None to not
                query on this property.
            sample_date_start (str): The sample start date of the lab test. Defaults to None to not
                query on this property.
            sample_date_end (str): The sample end date of the lab test. Defaults to None to not
                query on this property.
            lot_code (str): The lot code of the lab test. Defaults to None to not
                query on this property.
            product_code (str): The product code of the lab test. Defaults to None to not
                query on this property.
            predicted_harvest_date (str): The predicted harvest date of the lab test.
                Defaults to None to not query on this property.
            trial_id (str): The trial id of the lab test.
                Defaults to None to not query on this property.
            treatment_id (str): The treatment id of the lab test.
                Defaults to None to not query on this property.
            harvest_cycle (str): The harvest cycle of the lab test.
                Defaults to None to not query on this property.
            health_status (str): The health status of the lab test.
                Defaults to None to not query on this property.
            container_id (str): The container id for the lab test.
                Defaults to None to not query on this property.
            material_lot (str): The material lot for the lab test.
                Defaults to None to not query on this property.
            start_time (str): The start_time of the lab test. Defaults to None to not
                query on this property.
            end_time (str): The end_time of the lab test. Defaults to None to not
                query on this property.
            nutrient_stage (str): The nutrient stage of the lab test.
                Defaults to None to not query on this property.
            dump_refill_status (str): The dump refill status of the lab test.
                Defaults to None to not query on this property.
            order_by (str): The order by field sequence of lab tests. Defaults to None to not
                query on this property.
        Returns:
            (list): A list of lab samples with the provided filters
        """
        query_args = {
            "lab_tests_per_page": lab_tests_per_page,
            "page": page,
            "lab_test_provider": lab_test_provider,
            "lab_test_kind": lab_test_kind,
            "lab_test_passed": lab_test_passed,
            "lab_test_sample_id": lab_test_sample_id,
            "created_by_username": created_by_username,
            "farm_def_id": farm_def_id,
            "farm_def_path": farm_def_path,
            "sample_type": sample_type,
            "notes": notes,
            "sub_location": sub_location,
            "label_details": label_details,
            "sample_date_start": sample_date_start,
            "sample_date_end": sample_date_end,
            "lot_code": lot_code,
            "product_code": product_code,
            "predicted_harvest_date": predicted_harvest_date,
            "trial_id": trial_id,
            "treatment_id": treatment_id,
            "harvest_cycle": harvest_cycle,
            "health_status": health_status,
            "container_id": container_id,
            "material_lot": material_lot,
            "start_time": start_time,
            "end_time": end_time,
            "nutrient_stage": nutrient_stage,
            "dump_refill_status": dump_refill_status,
            "order_by": order_by,
        }
        return self.__service_client.get(
            ["lab-test-sample"],
            query_args={k: v for k, v in query_args.items() if v is not None},
        ).json()

    def create_lab_test_samples(self, samples: list) -> List:
        """Create lab test samples in bulk from /lab-test-samples endpoint

        Args:
            samples (list): The list of data structure with sample values
        Returns:
            (dict): The created lab samples result.
        """
        return self.__service_client.post(["lab-test-samples"], req_json=samples).json()

    def update_lab_test_samples(self, samples: list) -> List:
        """Update lab test samples in bulk from /lab-test-samples endpoint.

        Args:
            samples (list): The list of data structure with sample values
        Returns:
            (dict): The updated lab samples result.
        """
        return self.__service_client.put(["lab-test-samples"], req_json=samples).json()

    def get_lab_samples_without_results_after_x_days(
        self,
        lab_test_provider: str,
        lab_test_kind: str,
        sample_type: str,
        days_without_results: int,
        alert: Optional[bool] = False,
    ) -> Dict:
        """Gets lab tests by name from /lab-test-sample/<lab_test_provider>/<lab_test_kind>/
                                                <sample_type>/no-results-after-x-days/<days>
          end point, that haven't been received after X <days> after sample was taken

        Args:
            lab_test_provider (str): The lab test provider
            lab_test_kind (str): The lab test kind
            sample_type (str): The lab test sample type
            days_without_results (int): The amount of days without results after sample was taken
            alert (bool): Trigger plenty alert service in k8s "prod" env if a lab result not found
        Returns:
            (list): A list of lab test samples.
        """
        return self.__service_client.get(
            [
                "lab-test-sample",
                lab_test_provider,
                lab_test_kind,
                sample_type,
                "no-results-after-x-days",
                days_without_results,
            ],
            query_args={"alert": str(alert).lower()},
        ).json()

    def get_url_for_s3_file_uuid(self, uuid: str) -> Dict:
        """Gets url for S3 file associated with lab test

        Args:
            uuid (str): The UUID of the lab test file id
        Returns:
            (dict): The S3 url to access a lab test file.
        """
        return self.__service_client.get(["lab-test-file-url", uuid]).json()

    def get_sub_locations_from_farm_def_path(self, farm_def_path: str) -> Dict:
        """Gets lab test S3 link for results in PDF/Excel

        Args:
            farm_def_path (str): The farm def path on which to get sub locations
        Returns:
            (dict): The sub locations for the farm def path
        """
        return self.__service_client.get(
            ["lab-test-sample/sub-location"],
            query_args={"farm_def_path": farm_def_path},
        ).json()

    def create_lab_test_event(self, event_kind: str, event_data: dict) -> Dict:
        """Creates a lab event.

        Args:
            event_kind   (str): The kind of event
            event (dict): A structure containing a lab event metadata
        Returns:
            (dict): The results of creating lab event
        """
        return self.__service_client.post(["lab-test-event", event_kind], req_json=event_data).json()

    def delete_lab_test_samples(self, samples: list) -> List:
        """Delete lab test sample in bulk from /lab-test-samples endpoint

        Args:
            samples (list): The list of lab test sample ids to delete
        Returns:
            (dict): The results of deleting the lab test samples.
        """
        return self.__service_client.delete(["lab-test-samples"], req_json=samples).json()

    def external_submit_test_results(self, test_results: dict) -> Dict:
        """Submit lab test results for samples

        Args:
            test_results (dict): Test results for samples
        Returns:
            (dict): Status of test results processing.
        """
        auth = f"{Cfg.get_plenty_api_key()}:{Cfg.get_plenty_api_secret()}"
        additional_headers = {"Authorization": "Basic ".encode("utf-8") + base64.b64encode(auth.encode("utf-8"))}
        return self.__service_client.post(
            ["external", "submit-test-results"], additional_headers=additional_headers, req_json=test_results
        ).json()

    def lab_tests_by_lot_code(self, site: str, sample_date_start: str, sample_date_end: str) -> Dict:
        """Get lab testing results for lot codes.

        Args:
            site (str): Site
            sample_date_start (str): start date to filter samples, YYYY-MM-DD
            sample_date_start (str): end date to filter samples, YYYY-MM-DD
        Returns:
            (dict): keys are lot names with possible values true|false represents tests are passed or not
        """
        return self.__service_client.get(
            ["lab-tests-by-lot-code"],
            query_args={"site": site, "sample_date_start": sample_date_start, "sample_date_end": sample_date_end},
        ).json()

    def ingest_in_house_google_sheet_test_results(self):
        """Call the In-House Google Sheet Ingest process.

        Returns:
            (dict): Message with the processed results.
        """
        return self.__service_client.post(["ingest-in-house-google-sheet"]).json()
