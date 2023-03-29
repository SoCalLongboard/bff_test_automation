"""This module implements methods which interact the web API for the Plenty
alert service."""

from typing import Any, Optional, Dict
from ..models import CliCommand, CliSubCommand
from ..alert_service.models import (
    Alert,
    Alerts,
    Subscription,
    Subscriptions,
    SubscriptionsMap,
    AlertSerials,
)

from ..base_client import BaseClient
from ..common import (
    validate_update_content,
    AuthenticatedServiceClient,
    AuthenticatedClient,
    format_url_with_version,
)


class AlertServiceClient(BaseClient):
    """Client communicating with the Plenty alert service via REST."""

    _application_name = "Alert Service"
    _service_name = "alertservice"
    _api_version = "v1"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return AlertServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return AlertServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return AlertServiceClient._api_version

    def __init__(self, authenticated_client: AuthenticatedClient, url: str):
        """Create a new alert service client.

        Args:
            authenticated_client (common.AuthenticatedClient): Plenty service
                client that has credentials.
            url (str): The url  to use for the client.
        """

        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version()), True
        )

    def build_commands(self) -> CliCommand:
        """Builds the commands for this client.

        Returns:
            ({str: (str,{str: str})}): The commands for the client.
        """
        serial_arg = ["serial"], {"help": "the serial number of the alert"}
        site_maybe_arg = ["-s"], {"dest": "site", "help": "the site of the alert"}
        room_maybe_arg = ["-r"], {"dest": "room", "help": "the room of the alert"}
        input_type_maybe_arg = (
            ["-i"],
            {
                "dest": "input_type",
                "help": "the input type of the alert",
            },
        )
        field_maybe_arg = ["-f"], {"dest": "field", "help": "the field of the alert"}
        active_only_maybe_arg = (
            ["-ao"],
            {
                "dest": "active_only",
                "help": "whether to filter for active alert rules",
            },
        )
        alert_type_maybe_arg = (
            ["-a"],
            {
                "dest": "alert_type",
                "help": "the type of the alert",
            },
        )
        alert_arg = (
            ["alert_fname"],
            {"help": "the path of the file specifying the alert in JSON format"},
        )
        subscription_arg = (
            ["subscription_fname"],
            {"help": "the path of the file specifying the subscription in JSON format"},
        )
        username_arg = ["username"], {"help": "the username of the user"}

        return {
            "alert_rule": (
                "Manage alert rules.",
                {
                    "query": (
                        "Query all of the alerts.",
                        self.query_alert_rules,
                        [
                            site_maybe_arg,
                            room_maybe_arg,
                            input_type_maybe_arg,
                            alert_type_maybe_arg,
                            field_maybe_arg,
                            active_only_maybe_arg,
                        ],
                    ),
                    "create": (
                        "Create a new alert.",
                        self.create_alert_rule,
                        [alert_arg],
                    ),
                    "get": (
                        "Get info about an alert.",
                        self.get_alert_rule,
                        [serial_arg],
                    ),
                    "delete": (
                        "Delete an alert.",
                        self.delete_alert_rule,
                        [serial_arg],
                    ),
                    "update": (
                        "Update an alert.",
                        self.update_alert_rule,
                        [serial_arg, alert_arg],
                    ),
                    "event": (
                        "Handle and event for an alert rule.",
                        self.handle_alert_rule_event,
                        [serial_arg, alert_arg],
                    ),
                },
            ),
            "subscription": (
                "Manage subscriptions.",
                {
                    "list": (
                        "List the subscriptions for an alert rule.",
                        self.list_subscriptions_to_alert_rule,
                        [serial_arg],
                    ),
                    "create": (
                        "Create a new subscription.",
                        self.create_subscription,
                        [subscription_arg],
                    ),
                    "delete": (
                        "Delete a user's subscriptions to an alert rule.",
                        self.delete_subscription,
                        [serial_arg, username_arg],
                    ),
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
            "alert_service",
            "alert service client",
            "a",
            self.build_commands(),
            lambda s, _: [s[0]],
        )

    def query_alert_rules(
        self,
        site: Optional[str] = None,
        room: Optional[str] = None,
        input_type: Optional[str] = None,
        alert_type: Optional[str] = None,
        field: Optional[str] = None,
        active_only: Optional[str] = None,
    ) -> Alert:
        """Gets from the /alert_rules/query endpoint all alert rules matching
        some specifications.

        Args:
            site (str): The site of the alert rule. Defaults to None to not
                query on this property.
            room (str): The room of the alert rule. Defaults to None to not
                query on this property.
            input_type (str): The input type of the alert rule. Defaults to
                None to not query on this property.
            alert_type (str): The type of the alert rule. Defaults to None to not
                query on this property.
            field (str): The field of the alert rule. Defaults to None to not
                query on this property.
            active_only (str): Whether to only include alert rules that are
                currently active. Defaults to None to not filter for active
                alerts
        Returns:
            (dict): The alert rules.
        """
        query_args = {
            "site": site,
            "room": room,
            "inputType": input_type,
            "alert_type": alert_type,
            "field": field,
            "activeOnly": active_only,
        }
        return self.__service_client.get(
            ["alert_rules", "query"],
            query_args={k: v for k, v in query_args.items() if v is not None},
        ).json()

    def create_alert_rule(self, alert: Optional[Dict] = None, alert_fname: Optional[str] = None) -> Dict:
        """Posts to the /alert_rules/create endpoint a new alert rule to create.

        Args:
            alert (dict, optional): A dict with the alert rule's
                information. Defaults to None. Either this or alert_fname must
                be None.
            alert_fname (str, optional): The filename of the file contatining
                the alert's information. Defaults to None. Either this or
                alert must be None.
        Returns:
            (dict): The newly created alert.
        """
        alert = validate_update_content(alert, alert_fname)
        return self.__service_client.post(["alert_rules", "create"], req_json=alert).json()

    def get_alert_rule(self, serial: str) -> Dict:
        """Gets from the /alert_rule/{serial} endpoint a particular alert rule.

        Args:
            serial (str): The serial number of the alert rule being requested.
        Returns:
            (dict): The alert rule requested.
        """
        return self.__service_client.get(["alert_rule", serial]).json()

    def update_alert_rule(
        self,
        serial: str,
        alert: Optional[Dict] = None,
        alert_fname: Optional[str] = None,
    ) -> Dict:
        """Puts to the /alert_rule/{serial} endpoint to update a particular
        alert rule.

        Args:
            serial (str): The serial number of the alert rule being requested.
            alert (dict, optional): A dict with the alert rule's
                information. Defaults to None. Either this or alert_fname must
                be None.
            alert_fname (str, optional): The filename of the file contatining
                the alert's information. Defaults to None. Either this or
                alert must be None.
        Returns:
            (dict): The alert rule requested.
        """
        alert = validate_update_content(alert, alert_fname)
        return self.__service_client.put(["alert_rule", serial], req_json=alert).json()

    def delete_alert_rule(self, serial: str):
        """Deletes an alertrule  with the DELETE /alert_rule/{serial} endpoint.

        Args:
            serial (str): The serial number of the alert rule being deleted.
        Returns:
            (None): None.
        """
        self.__service_client.delete(["alert_rule", serial])

    def handle_alert_rule_event(
        self,
        serial: str,
        event: Optional[str] = None,
        event_fname: Optional[str] = None,
    ) -> Dict:
        """Posts to the /subscriptions/create endpoint a new device to create.

        Args:
            serial (str): The serial number of the alert rule.
            event (str, optional): A formatted string with the event's
                information. Defaults to None. Either this or event_fname must
                be None.
            event_fname (str, optional): The filename of the file
                contatining the evcent's information. Defaults to None. Either
                this or event must be None.
        Returns:
            (dict): The newly created subscription.
        """
        event = validate_update_content(event, event_fname)

        return self.__service_client.post(["alert_rule", serial, "handle_event"], req_json=event).json()

    def list_subscriptions_to_alert_rule(self, serial: str) -> Dict:
        """Gets all of the subscriptions for a given alert rule from the
        /alert_rule/{serial}/subscriptions endpoint.

        Args:
            serial (str): The serial number of the alert rule.
        Returns:
            (dict): The subscriptions.
        """
        return self.__service_client.get(["alert_rule", serial, "subscriptions"]).json()

    def batch_get_subscriptions(self, serials: AlertSerials) -> SubscriptionsMap:
        """Posts to the /subscriptions/batch_get endpoint to get subscriptions for given alert serials

        Args:
            serials (List[str]): The list of alert rule serial numbers.
        Returns:
            Dict[str, List]: The map of subscriptions for each alert rule serial
        """
        return self.__service_client.post(["subscriptions", "batch_get"], req_json=serials).json()

    def create_subscription(
        self,
        subscription: Optional[Dict] = None,
        subscription_fname: Optional[str] = None,
    ) -> Dict:
        """Posts to the /subscriptions/create endpoint a new device to create.

        Args:
            subscription (dict, optional): A formatted string with the
                subscription's information. Defaults to None. Either this or
                subscription_fname must be None.
            subscription_fname (str, optional): The filename of the file
                contatining the subscription's information. Defaults to None.
                Either this or subscription must be None.

        Returns:
            (dict): The newly created subscription.
        """
        subscription = validate_update_content(subscription, subscription_fname)

        return self.__service_client.post(["subscriptions", "create"], req_json=subscription).json()

    def delete_subscription(
        self,
        serial: str,
        username: str,
        contact_method: Optional[str] = None,
        update_user: Optional[str] = None,
    ):
        """Deletes to the /alert_rule/{serial}/subscriptions/{username}
        endpoint to delete all of a user's subscriptions to an alert.

        If contact_method is given, delets to the /alert_rule/{serial}/subscriptions/{username}/contact_method/{contact_method} endpoint to delete a user's subscriptions to an alert for given contact method.

        Args:
            serial (str): The serial number of the alert rule.
            username (str): The username of the user.
        """
        params = ["alert_rule", serial, "subscriptions", username]
        if contact_method:
            params += ["contact_method", contact_method]
        query_args = {"updateUser", update_user} if update_user else None
        self.__service_client.delete(params, query_args=query_args)

    def delete_subscription_by_match(
        self,
        serial: str,
        username: Optional[str] = None,
        contact_method: Optional[str] = None,
        contact_value: Optional[str] = None,
        update_user: Optional[str] = None,
    ) -> None:
        """Deletes to the /alert_rule/{serial}/subscriptions?username=[username]&contactMethod=[contactMethod]&contactValue=[contactValue] endpoint to delete all subscriptions to an alert that match the search criteria"""
        params = ["alert_rule", serial, "subscriptions"]

        query_args = {}
        if username:
            query_args["username"] = username
        if contact_method:
            query_args["contactMethod"] = contact_method
        if contact_value:
            query_args["contactValue"] = contact_value

        if update_user:
            query_args["updateUser"] = update_user

        self.__service_client.delete(params, query_args=query_args)
