"""This module implements methods which interact the web API for
the Plenty product quality service"""

import json
from typing import Optional

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, filter_query_args, format_url_with_version, str_to_json


class ProductQualityServiceClient(BaseClient):
    """Client communicating with the Plenty product quality service via REST"""

    _service_name = "productqualityservice"
    _api_version = "v0"

    @staticmethod
    def service_name():
        """Get the name of the service.
        Returns:
            (str): The name of the service.
        """
        return ProductQualityServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.
        Returns:
            (str): The api version of this client.
        """
        return ProductQualityServiceClient._api_version

    def __init__(self, authenticated_client, url):
        """Create a new product quality service client.
                Args:
                    authenticated_client (common.AuthenticatedClient): Plenty service
                        client that has credentials.
                    url (str): The url to use for the client.
        format_url_with_version
        """

        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version())
        )
        self.__service_client_v1 = AuthenticatedServiceClient(authenticated_client, format_url_with_version(url, "v1"))

    def build_commands(self):
        """Builds the commands for this client.
        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        site_arg = ["site"], {"help": "A string of the site"}
        date_arg = ["date"], {"help": "The date as a string"}
        start_arg = ["start_date"], {"help": "The start date as a string"}
        end_arg = ["end_date"], {"help": "The end date as a string"}
        event_arg = ["event_model"], {"help": "The event model JSON as a string"}
        ratings_arg = ["ratings_model"], {"help": "The ratings model JSON as a string"}
        qa_arg = ["qa_model"], {"help": "The QA post harvest model JSON as a string"}
        event_id_arg = ["event_id"], {"help": "The ID of the event as a string"}
        username_arg = ["username"], {"help": "The username as a string"}
        fgqa_find_by_args = [
            (
                ["--crop"],
                {"help": "filter by crop"},
            ),
            (
                ["--case_type"],
                {"help": "filter by case_type"},
            ),
            (
                ["--username"],
                {"help": "filter by username"},
            ),
            (
                ["--started_at"],
                {"help": "filter resources where createdAt is after --started_at"},
            ),
            (
                ["--ended_at"],
                {"help": "filter resources where createdAt is before --ended_at"},
            ),
        ]

        return {
            "update": (
                "Update the state of PQS",
                {
                    "events": ("Post to events endpoint", self.post_events, [event_arg]),
                    "ratings": ("Post to ratings endpoint", self.post_ratings, [ratings_arg]),
                    "qa": ("Post to QA endpoint", self.post_qa_update, [qa_arg]),
                },
            ),
            "state": (
                "Get the current or past state of PQS",
                {
                    "events": ("Get to events endpoint", self.get_events, [date_arg, site_arg]),
                    "ratings": ("Get to ratings endpoint", self.get_ratings, [date_arg, site_arg]),
                    "qa": ("Get to QA endpoint", self.get_qa, [date_arg, site_arg]),
                },
            ),
            "postharvest-qa": (
                "PostharvesdtQa commands",
                {
                    "create": (
                        "Create a PostharvestQa entry",
                        self.create_postharvest_qa,
                        [(["postharvest_qa"], {"help": "attributes of the PostharvestQa as a JSON string"})],
                    ),
                    "get": (
                        "Fetch a PostharvestQa entry by its ID",
                        self.get_postharvest_qa_by_id,
                        [(["postharvest_qa_id"], {"help": "the id of the PostharvestQa entry to fetch"})],
                    ),
                    "find_all_by": (
                        "Fetch a list of PostharvestQa entries",
                        self.find_all_postharvest_qa_by,
                        [
                            (["--site"], {"help": "filter entries matching the given site"}),
                            (["--date"], {"help": "filter entries where harvestDate is equal to the given date"}),
                            (
                                ["--start_date"],
                                {
                                    "help": "filter entries where the harvestDate is greater or equal than the given start_date"
                                },
                            ),
                            (
                                ["--end_date"],
                                {
                                    "help": "filter entries where the harvestDate is less or equal than the given start_date"
                                },
                            ),
                        ],
                    ),
                    "update": (
                        "Update a PostharvestQa entry",
                        self.update_postharvest_qa,
                        [
                            (["postharvest_qa_id"], {"help": "the id of the PostharvestQa entry to update"}),
                            (["postharvest_qa"], {"help": "attributes of the PostharvestQa as a JSON string"}),
                        ],
                    ),
                    "delete": (
                        "Delete a PostharvestQa entry matching the given ID",
                        self.delete_postharvest_qa,
                        [(["postharvest_qa_id"], {"help": "the id of the PostharvestQa entry to delete"})],
                    ),
                },
            ),
            "sensory-event": (
                "Sensory Events commands",
                {
                    "create": (
                        "Create a Sensory Event entry",
                        self.create_sensory_event,
                        [(["sensory_event"], {"help": "attributes of the Sensory Event as a JSON string"})],
                    ),
                    "get": (
                        "Fetch a Sensory Event entry by its ID",
                        self.get_sensory_event_by_id,
                        [(["sensory_event_id"], {"help": "the id of the Sensory Event entry to fetch"})],
                    ),
                    "find_all_by": (
                        "Fetch a list of Sensory Event entries",
                        self.find_all_sensory_event_by,
                        [
                            (["--site"], {"help": "filter entries matching the given site"}),
                            (["--cultivar"], {"help": "ilter entries matching the given cultivar"}),
                            (
                                ["--harvest_date"],
                                {"help": "filter entries where harvestDate is equal to the given date"},
                            ),
                            (["--test_date"], {"help": "filter entries where testDate is equal to the given date"}),
                            (
                                ["--start_date"],
                                {
                                    "help": "filter entries where the testDate is greater or equal than the given start_date"
                                },
                            ),
                            (
                                ["--end_date"],
                                {
                                    "help": "filter entries where the testDate is less or equal than the given start_date"
                                },
                            ),
                        ],
                    ),
                    "update": (
                        "Update a Sensory Event entry",
                        self.update_sensory_event,
                        [
                            (["sensory_event_id"], {"help": "the id of the Sensory Event entry to update"}),
                            (["sensory_event"], {"help": "attributes of the Sensory Event as a JSON string"}),
                        ],
                    ),
                    "delete": (
                        "Delete a Sensory Event entry matching the given ID",
                        self.delete_sensory_event,
                        [(["sensory_event_id"], {"help": "the id of the Sensory Event entry to delete"})],
                    ),
                },
            ),
            "sensory-rating": (
                "Sensory Ratings commands",
                {
                    "create": (
                        "Create a Sensory Rating entry",
                        self.create_sensory_rating,
                        [(["sensory_rating"], {"help": "attributes of the Sensory Rating model as a JSON string"})],
                    ),
                    "get": (
                        "Fetch a Sensory Rating entry by its ID",
                        self.get_sensory_rating_by_id,
                        [(["sensory_rating_id"], {"help": "the id of the Sensory Rating entry to fetch"})],
                    ),
                    "find_all_by": (
                        "Fetch a list of Sensory Rating entries",
                        self.find_all_sensory_rating_by,
                        [
                            (["--site"], {"help": "filter entries matching the given site"}),
                            (["--username"], {"help": "filter entries matching the given username"}),
                            (["--event_id"], {"help": "filter entries belonging to a specific event"}),
                            (["--test_date"], {"help": "filter entries where testDate is equal to the given date"}),
                            (
                                ["--start_date"],
                                {
                                    "help": "filter entries where the testDate is greater or equal than the given start_date"
                                },
                            ),
                            (
                                ["--end_date"],
                                {
                                    "help": "filter entries where the testDate is less or equal than the given start_date"
                                },
                            ),
                        ],
                    ),
                    "delete": (
                        "Delete a Sensory Rating entry matching the given ID",
                        self.delete_sensory_rating,
                        [(["sensory_rating_id"], {"help": "the id of the Sensory Rating entry to delete"})],
                    ),
                },
            ),
            "fgqa-case-content-qa": (
                "Finished Goods QA CaseContentQa commands",
                {
                    "find": (
                        "List CaseContentQa resources",
                        self.find_case_content_qa_by,
                        fgqa_find_by_args,
                    ),
                    "get": (
                        "Find a CaseContentQa resource for a given id",
                        self.get_case_content_qa_by_id,
                        [
                            (
                                ["case_content_qa_id"],
                                {"help": "The id of the CaseContentQa"},
                            )
                        ],
                    ),
                    "delete": (
                        "Delete a CaseContentQa resource for a given id",
                        self.delete_case_content_qa,
                        [
                            (
                                ["case_content_qa_id"],
                                {"help": "The id of the CaseContentQa to delete"},
                            )
                        ],
                    ),
                },
            ),
            "fgqa-case-qa": (
                "Finished Goods QA CaseQa commands",
                {
                    "find": (
                        "List CaseQa resources",
                        self.find_case_qa_by,
                        fgqa_find_by_args,
                    ),
                    "get": (
                        "Find CaseQa resource for a given id",
                        self.get_case_qa_by_id,
                        [
                            (
                                ["case_qa_id"],
                                {"help": "The id of the CaseQa"},
                            )
                        ],
                    ),
                    "delete": (
                        "Delete CaseQa resource for a given id",
                        self.delete_case_qa,
                        [(["case_qa_id"], {"help": "The id of the CaseQa to delete"})],
                    ),
                },
            ),
        }

    def build_cli_subcommand(self):
        """Build the CLI subcommand for this client.
        Returns:
            ((str, str, str, ({str: (str,{str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return (
            "product_quality",
            "product quality service client",
            "pqs",
            self.build_commands(),
            lambda s, _: [
                {
                    "fgqa-case-content-qa": "fccq",
                    "fgqa-case-qa": "fcq",
                    "state": "s",
                    "sensory-event": "se",
                    "sensory-rating": "sr",
                }.get(s, s[0])
            ],
        )

    def create_postharvest_qa(self, postharvest_qa):
        """Create a PostharvestQa entry.

        Args:
            postharvest_qa (str|dict): attributes of a PostharvestQa
        Returns:
            The PostharvestQa created as JSON
        """
        return self.__service_client_v1.post(["postharvest"], req_json=str_to_json(postharvest_qa)).json()

    def get_postharvest_qa_by_id(self, postharvest_qa_id):
        """Fetch a PostharvestQa by its ID.

        Args:
            postharvest_qa_id (str): the id of the PostharvestQa to fetch
        Returns:
            The PostharvestQa matching the given id
        """
        return self.__service_client_v1.get(["postharvest", postharvest_qa_id]).json()

    def find_all_postharvest_qa_by(
        self,
        site: Optional[str] = None,
        date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        """Fetch a list of PostharvestQa entries with optional filters.

        Args:
            site: (str) filter entries matching the given site
            date: (str) [format: YYYY-MM-DD] filter entries where harvestDate is equal to the given date
            start_date: (str) [format: YYYY-MM-DD] filter entries where the harvestDate is greater or equal than the given start_date
            end_date: (str) [format: YYYY-MM-DD] filter entries where the harvestDate is less or equal than the given start_date
        Returns:
            A list of PostharvestQa entries matching the filters
        """
        query_args = filter_query_args(
            {
                "site": site,
                "date": date,
                "startDate": start_date,
                "endDate": end_date,
            }
        )
        return self.__service_client_v1.get(["postharvest"], query_args=query_args).json()

    def update_postharvest_qa(self, postharvest_qa_id, postharvest_qa):
        """Update a PostharvestQa entry.

        Args:
            postharvest_qa_id (str): the id of the PostharvestQa entry to update
            postharvest_qa (str|dict): attributes of a PostharvestQa
        Returns:
            The updated PostharvestQa as JSON
        """
        return self.__service_client_v1.put(
            ["postharvest", postharvest_qa_id], req_json=str_to_json(postharvest_qa)
        ).json()

    def delete_postharvest_qa(self, postharvest_qa_id):
        """Delete a PostharvestQa entry (soft-delete).

        Args:
            postharvest_qa_id (str): the id of the PostharvestQa entry to delete
        Returns:
            The deleted PostharvestQa as JSON
        """
        return self.__service_client_v1.delete(["postharvest", postharvest_qa_id]).json()

    def find_all_qa_results_by(
        self,
        site: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        purpose: Optional[str] = None,
    ):
        """Get pass/fail QA result for PostHarvestQA entities.

        @param site: (str) the site of the data
        @param start_date: (str) the earliest harvest date of PostHarvestQA to return
        @param end_date: (str) the latest harvest date of PostHarvestQA to return
        @param purpose: (strt) filter PostharvestQA entries for the given purpose
        @return: List, of QaResult entities, which represent detailed QA info for every PackagingLot.
        """
        query_args = filter_query_args({"site": site, "startDate": start_date, "endDate": end_date, "purpose": purpose})
        return self.__service_client_v1.get(["postharvest", "qa-results"], query_args=query_args).json()

    def create_sensory_event(self, sensory_event):
        """Create a Sensory Event entry.

        Args:
            sensory_event (str|dict): attributes of a Sensory Event
        Returns:
            The Sensory Event created as JSON
        """
        return self.__service_client_v1.post(["sensory", "events"], req_json=str_to_json(sensory_event)).json()

    def get_sensory_event_by_id(self, sensory_event_id):
        """Fetch a Sensory Event entry by its ID.

        Args:
            sensory_event_id (str): The id of the Sensory Event id to fetch
        Returns:
            The Sensory Event matching the given id
        """
        return self.__service_client_v1.get(["sensory", "events", sensory_event_id]).json()

    def find_all_sensory_event_by(
        self,
        site: Optional[str] = None,
        cultivar: Optional[str] = None,
        harvest_date: Optional[str] = None,
        test_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        """Fetch a list of Sensory Event entries with optional filters.

        Args:
            site: (str) filter entries matching the given site
            cultivar: (str) filter entries matching the given cultivar
            harvest_date: (str) [format: YYYY-MM-DD] filter entries where harvestDate is equal to the given date
            test_date: (str) [format: YYYY-MM-DD] filter entries where testDate is equal to the given date
            start_date: (str) [format: YYYY-MM-DD] filter entries where the testDate is greater or equal than the given start_date
            end_date: (str) [format: YYYY-MM-DD] filter entries where the testDate is less or equal than the given start_date
        Returns:
            list(JSON) list of Sensory Event entries corresponding to the filter parameters
        """
        query_args = filter_query_args(
            {
                "site": site,
                "cultivar": cultivar,
                "harvestDate": harvest_date,
                "testDate": test_date,
                "startDate": start_date,
                "endDate": end_date,
            }
        )
        return self.__service_client_v1.get(["sensory", "events"], query_args=query_args).json()

    def update_sensory_event(self, sensory_event_id, sensory_event):
        """Update a Sensory Event entry.

        Args:
            sensory_event_id (str): The id of the Sensory Event id to update
            sensory_event (str|dict): attributes of a Sensory Event
        Returns:
            The updated Sensory Event as JSON
        """

        return self.__service_client_v1.put(
            ["sensory", "events", sensory_event_id], req_json=str_to_json(sensory_event)
        ).json()

    def delete_sensory_event(self, sensory_event_id):
        """Delete a Sensory Event entry.

        Args:
            sensory_event_id (str): The id of the Sensory Event to delete
        Returns:
            The deletd Sensory Event as JSON
        """
        return self.__service_client_v1.delete(["sensory", "events", sensory_event_id]).json()

    def create_sensory_rating(self, sensory_rating):
        """Create a Sensory Rating entry.

        Args:
            sensory_rating (str|dict): attributes of a Sensory Rating
        Returns:
            The Sensory Rating created as JSON
        """
        return self.__service_client_v1.post(["sensory", "ratings"], req_json=str_to_json(sensory_rating)).json()

    def get_sensory_rating_by_id(self, sensory_rating_id):
        """Fetch a Sensory Rating entry by its ID.

        Args:
            sensory_rating_id (str): the id of the Sensory Rating to fetch
        Returns:
            The Sensory Rating matching the given id
        """
        return self.__service_client_v1.get(["sensory", "ratings", sensory_rating_id]).json()

    def find_all_sensory_rating_by(
        self,
        site: Optional[str] = None,
        username: Optional[str] = None,
        event_id: Optional[str] = None,
        test_date: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
    ):
        """Fetch a list of Sensory Rating entries with optional filters.

        Args:
            site: (str) filter entries matching the given site
            username: (str) filter entries matching the given username
            event_id: (str) filter entries belonging to a specific event
            test_date: (str) [format: YYYY-MM-DD] filter entries where testDate is equal to the given date
            start_date: (str) [format: YYYY-MM-DD] filter entries where the testDate is greater or equal than the given start_date
            end_date: (str) [format: YYYY-MM-DD] filter entries where the testDate is less or equal than the given start_date
        Returns:
            list(JSON) list of Sensory Rating entries corresponding to the filter parameters
        """
        query_args = filter_query_args(
            {
                "site": site,
                "username": username,
                "eventId": event_id,
                "testDate": test_date,
                "startDate": start_date,
                "endDate": end_date,
            }
        )
        return self.__service_client_v1.get(["sensory", "ratings"], query_args=query_args).json()

    def delete_sensory_rating(self, sensory_rating_id):
        """Delete Sensory Rating entry.

        Args:
            sensory_rating_id (str): the id of the Sensory Rating to delete
        Returns:
            The deleted Sensory Rating as JSON
        """
        return self.__service_client_v1.delete(["sensory", "ratings", sensory_rating_id]).json()

    # deprecated
    def post_events(self, event_model):
        """Creates new sensory event entries in the Postgres database by posting to
        /sensory/events endpoint.

        Args:
            event_model (str): The event model.
        Returns:
            (list): A list of event models that got created/modified.
        """
        return self.__service_client.post(["sensory", "events"], req_json=json.loads(event_model)).json()

    # deprecated
    def get_events(self, date, site):
        """Gets event data by getting to
        /sensory/events endpoint.

        Args:
            date (str): the date of the test
            site (str): the site of the test
        Returns:
            (list): A list of event models.
        """
        params = {"testDate": date, "site": site}
        return self.__service_client.get(["sensory", "events"], query_args=params).json()

    # deprecated
    def get_events_range(self, site, start_date, end_date):
        """Gets event data by getting to
        /sensory/events/range endpoint.

        Args:
            start_date (str): the earliest date of tests to return
            end_date (str): the latest date of tests to return
            site (str): the site of the test
        Returns:
            (list): A list of event models.
        """
        params = {"site": site, "startDate": start_date, "endDate": end_date}
        return self.__service_client.get(["sensory", "events", "range"], query_args=params).json()

    # deprecated
    def get_events_id(self, event_id):
        """Gets event data by getting to
        /sensory/events/{id} endpoint.

        Args:
            event_id (str): the ID
        Returns:
            (list): A list of event models.
        """
        return self.__service_client.get(["sensory", "events", event_id], query_args={"id": event_id}).json()

    # deprecated
    def delete_events(self, event_id):
        """Deletes event data by deleting to
        /sensory/events endpoint.

        Args:
            event_id (str): the ID
        """
        return self.__service_client.delete(["sensory", "events"], query_args={"id": event_id})

    # deprecated
    def post_ratings(self, ratings_model):
        """Creates rating data by posting to
        /sensory/ratings endpoint.

        Args:
            ratings_model (str): The ratings model
        Returns:
            (list): A list of ratings that were created/modified.
        """
        if isinstance(ratings_model, str):
            ratings_model = json.loads(ratings_model)
        return self.__service_client.post(["sensory", "ratings"], req_json=ratings_model).json()

    # deprecated
    def get_ratings_all(self):
        """Gets all rating data by getting to
        /sensory/ratings/all endpoint.

        Returns:
            (list): A list of ratings models.
        """
        return self.__service_client.get(["sensory", "ratings", "all"]).json()

    # deprecated
    def get_ratings(self, date, site):
        """Gets rating data by getting to
        /sensory/ratings endpoint.

        Args:
            date (str): the date of the ratings
            site (str): the site of the test
        Returns:
            (list): A list of ratings models.
        """
        params = {"testDate": date, "site": site}
        return self.__service_client.get(["sensory", "ratings"], query_args=params).json()

    # deprecated
    def get_ratings_for_event(self, event_id):
        """Gets ratings data by event ID by getting to
        /sensory/ratings/forEvent endpoint.

        Args:
            event_id (str): the event ID
        Returns:
            (list): A list of ratings models.
        """
        params = {"eventId": event_id}
        return self.__service_client.get(["sensory", "ratings", "forEvent"], query_args=params).json()

    # deprecated
    def get_ratings_range(self, site, start_date, end_date):
        """Gets ratings data in a range by getting to
        /sensory/ratings/range endpoint.

        Args:
            start_date (str): the earliest date of tests to return
            end_date (str): the latest date of tests to return
            site (str): the site of the test
        Returns:
            (list): A list of ratings models.
        """
        params = {"site": site, "startDate": start_date, "endDate": end_date}
        return self.__service_client.get(["sensory", "ratings", "range"], query_args=params).json()

    # deprecated
    def get_events_user(self, username, event_id):
        """Gets event data by username by getting to
        /sensory/events/user endpoint.

        Args:
            username (str): the username
            event_id (str): the event ID
        Returns:
            (list): A list of event models.
        """
        params = {"username": username, "eventId": event_id}
        return self.__service_client.get(["sensory", "events", "user"], query_args=params).json()

    # deprecated
    def delete_ratings(self, rating_id, username):
        """Deletes ratings data by deleting to
        /sensory/ratings endpoint.

        Args:
            rating_id (str): the ratings model ID
            username (str): the username
        """
        params = {"id": rating_id, "username": username}
        return self.__service_client.delete(["sensory", "ratings"], query_args=params)

    # deprecated
    def post_qa_submit(self, qa_model):
        """Creates QA data by posting to
        /sensory/qa/submit endpoint.

        Args:
            qa_model (str): the QA model to post
        Returns:
            (list): A list of qa models that were created/updated.
        """
        return self.__service_client.post(["sensory", "qa", "submit"], req_json=json.loads(qa_model)).json()

    # deprecated
    def get_postharvest_qa_by_id_v0(self, postharvest_qa_id):
        """Gets a PostharvestQa model by its ID.
        Args:
            postharvest_qa_id (str): the ID
        Returns:
            (str): Requested PostharvestQa model or error.
        """
        return self.__service_client.get(["sensory", "qa", postharvest_qa_id]).json()

    # deprecated
    def get_qa(self, date, site):
        """Gets QA data by getting to
        /sensory/qa endpoint.

        Args:
            date (str): the date of the data
            site (str): the site with the data
        Returns:
            (list): A list of qa models.
        """
        params = {"site": site, "date": date}
        return self.__service_client.get(["sensory", "qa"], query_args=params).json()

    # deprecated
    def delete_qa_delete(self, qa_id):
        """Deletes QA data by deleting to
        /sensory/qa/delete endpoint.

        Args:
            qa_id (str): the ID
        """
        params = {"id": qa_id}
        return self.__service_client.delete(["sensory", "qa", "delete"], query_args=params)

    # deprecated
    def post_qa_update(self, qa_model):
        """Updates QA data by posting to
        /sensory/qa/update endpoint.

        Args:
            qa_model (str): the model to update
        Returns:
            (list): A list of qa models updated.
        """
        return self.__service_client.post(["sensory", "qa", "update"], req_json=json.loads(qa_model)).json()

    # deprecated
    def get_qa_range(self, site, start_date, end_date):
        """Gets QA data by getting to
        /sensory/qa/range endpoint.

        Args:
            start_date (str): the earliest date of data to return
            end_date (str): the latest date of data to return
            site (str): the site of the data
        Returns:
            (list): A list of QA models.
        """
        params = {"site": site, "startDate": start_date, "endDate": end_date}
        return self.__service_client.get(["sensory", "qa", "range"], query_args=params).json()

    # deprecated
    def get_qa_result_by_lot_number(self, site, start_date, end_date):
        """Get pass/fail QA result for PostHarvestQA entities.

        @param site: (str) the site of the data
        @param start_date: (str) the earliest harvest date of PostHarvestQA to return
        @param end_date: (str)the latest harvest date of PostHarvestQA to return
        @return: List, of PostHarvestQAResult entities, which represent detailed QA info
                for every PackagingLot.
        """
        params = {"site": site, "startDate": start_date, "endDate": end_date}
        return self.__service_client.get(["sensory", "qa", "lot_results"], query_args=params).json()

    def post_seedling_qa(self, seedling_qa):
        """Creates new SeedlingQA entry in the Postgres database by posting to
        /seedling_qa endpoint.

        Args:
            seedling_qa (str): SeedlingQA JSON model or error.
        Returns:
            (str): Created SeedlingQA item.
        """
        if isinstance(seedling_qa, str):
            seedling_qa = json.loads(seedling_qa)
        return self.__service_client.post(["sensory", "seedling_qa"], req_json=seedling_qa).json()

    def put_seedling_qa(self, seedling_qa):
        """Updates SeedlingQA entries in the Postgres database by posting to
        /seedling_qa endpoint.

        Args:
            seedling_qa (str): SeedlingQA JSON model.
        Returns:
            (str): Updated SeedlingQA item or error.
        """
        if isinstance(seedling_qa, str):
            seedling_qa = json.loads(seedling_qa)
        return self.__service_client.put(["sensory", "seedling_qa"], req_json=seedling_qa).json()

    def get_seedling_qa_by_site_and_date_range(self, site, start_date, end_date):
        """Gets SeedlingQA data by requesting
        /seedling_qa endpoint.

        Args:
            start_date (str): the earliest date of item to return
            end_date (str): the latest date of item to return
            site (str): the site of the test
        Returns:
            (list): A list of event models.
        """
        params = {"site": site, "startDate": start_date, "endDate": end_date}
        return self.__service_client.get(["sensory", "seedling_qa"], query_args=params).json()

    def get_seedling_qa_by_id(self, seedling_qa_id):
        """Gets event data by getting to
        /seedling_qa/{id} endpoint.

        Args:
            seedling_qa_id (str): the ID
        Returns:
            (str): Requested SeedlingQA item or error.
        """
        return self.__service_client.get(["sensory", "seedling_qa", seedling_qa_id]).json()

    def delete_seedling_qa(self, seedling_qa_id):
        """Deletes event data by deleting to
        /seedling_qa endpoint.

        Args:
            seedling_qa_id (str): the ID
        """
        return self.__service_client.delete(["sensory", "seedling_qa", seedling_qa_id]).json()

    def create_case_qa(self, case_qa):
        """Creates CaseQa result from case evaluation.

        @param case_qa: CaseQa instance
        @return created CaseQa instance
        """
        if isinstance(case_qa, str):
            case_qa = json.loads(case_qa)
        return self.__service_client.post(["finished-good", "case-evaluations"], req_json=case_qa).json()

    def update_case_qa(self, case_qa_id, case_qa):
        """Updates CaseQa result.

        @param case_qa_id: ID of CaseQa to update
        @param case_qa: CaseQa instance with updated values
        @return updated CaseQa instance
        """
        if isinstance(case_qa, str):
            case_qa = json.loads(case_qa)
        return self.__service_client.put(["finished-good", "case-evaluations", case_qa_id], req_json=case_qa).json()

    def get_case_qa_by_id(self, case_qa_id):
        """Returns CaseQa result from case evaluation by id.

        @param case_qa_id: ID of CaseQa to return
        @return updated CaseQa instance
        """
        return self.__service_client.get(["finished-good", "case-evaluations", case_qa_id]).json()

    def find_case_qa_by(
        self,
        crop=None,
        case_type=None,
        username=None,
        started_at=None,
        ended_at=None,
        sort=None,
        limit=None,
        offset=None,
    ):
        """Returns CaseQa result from case evaluation by id.

        @param crop: filter by crop if not None
        @param case_type: filter by case_type if not None
        @param username: username to filter by
        @param started_at: ISO8601 formatted date,
            filters all records where created_at >= started_at date
        @param ended_at: ISO8601 formatted date,
            filters all records where created_at <= ended_at date
        @param sort: field plus order (`<field>:asc`, `<field>:desc`).
            If field passed without order, desc is used by default
        @param limit: limit number of returned records, integer, default to 20
        @param offset: offset to use for paging
        @return list of filtered CaseQa instances
        """
        query_args = {
            "crop": crop,
            "caseType": case_type,
            "username": username,
            "startedAt": started_at,
            "endedAt": ended_at,
            "sort": sort,
            "limit": limit,
            "offset": offset,
        }
        query_args = {k: v for k, v in query_args.items() if v is not None}
        return self.__service_client.get(["finished-good", "case-evaluations"], query_args=query_args).json()

    def delete_case_qa(self, case_qa_id):
        """Soft delete CaseQa entity.

        @param case_qa_id: id of entity to delete
        @return deleted CaseQa instances
        """
        return self.__service_client.delete(["finished-good", "case-evaluations", case_qa_id]).json()

    def create_case_content_qa(self, case_content_qa):
        """Creates CaseContentQa result from case evaluation.

        @param case_content_qa: CaseContentQa instance
        @return created CaseContentQa instance
        """
        if isinstance(case_content_qa, str):
            case_content_qa = json.loads(case_content_qa)
        return self.__service_client.post(
            ["finished-good", "case-content-evaluations"], req_json=case_content_qa
        ).json()

    def update_case_content_qa(self, case_content_qa_id, case_content_qa):
        """Updates CaseContentQa result.

        @param case_content_qa_id: ID of CaseContentQa to update
        @param case_content_qa: CaseContentQa instance with updated values
        @return updated CaseContentQa instance
        """
        if isinstance(case_content_qa, str):
            case_content_qa = json.loads(case_content_qa)
        return self.__service_client.put(
            ["finished-good", "case-content-evaluations", case_content_qa_id],
            req_json=case_content_qa,
        ).json()

    def get_case_content_qa_by_id(self, case_content_qa_id):
        """Returns CaseContentQa result from case evaluation by id.

        @param case_content_qa_id: ID of CaseContentQa to return
        @return updated CaseContentQa instance
        """
        return self.__service_client.get(["finished-good", "case-content-evaluations", case_content_qa_id]).json()

    def find_case_content_qa_by(
        self,
        crop=None,
        sku=None,
        case_type=None,
        username=None,
        started_at=None,
        ended_at=None,
        sort=None,
        limit=None,
        offset=None,
    ):
        """Returns CaseContentQa result from case evaluation by id.

        @param crop: filter by crop if not None
        @param sku: filter by sku if not None
        @param case_type: filter by case_type if not None
        @param username: username to filter by
        @param started_at: ISO8601 formatted date,
            filters all records where created_at >= started_at date
        @param ended_at: ISO8601 formatted date,
            filters all records where created_at <= ended_at date
        @param sort: field plus order (`<field>:asc`, `<field>:desc`).
            If field passed without order, desc is used by default
        @param limit: limit number of returned records, integer, default to 20
        @param offset: offset to use for paging
        @return list of filtered CaseContentQa instances
        """
        query_args = {
            "crop": crop,
            "sku": sku,
            "caseType": case_type,
            "username": username,
            "startedAt": started_at,
            "endedAt": ended_at,
            "sort": sort,
            "limit": limit,
            "offset": offset,
        }
        query_args = {k: v for k, v in query_args.items() if v is not None}
        return self.__service_client.get(["finished-good", "case-content-evaluations"], query_args=query_args).json()

    def delete_case_content_qa(self, case_content_qa_id):
        """Soft delete CaseContentQa entity.

        @param case_content_qa_id: id of entity to delete
        @return deleted CaseContentQa instances
        """
        return self.__service_client.delete(["finished-good", "case-content-evaluations", case_content_qa_id]).json()

    def get_finished_good_measurement_types(self):
        """Returns list of available measurement types -
            the list of properties for CaseQa.CaseChecks and CaseContentQa.ClamshellChecks.

        @return: List of MeasurementType
        """
        return self.__service_client.get(["finished-good", "measurement-types"]).json()
