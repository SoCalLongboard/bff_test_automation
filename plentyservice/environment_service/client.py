"""This module implements methods which interact the web API for the Plenty environment service."""
from typing import Dict, List, Optional

from ..base_client import BaseClient
from ..common import AuthenticatedServiceClient, filter_query_args, format_url_with_version, str_to_json


class EnvironmentServiceClient(BaseClient):
    """Client communicating with the Plenty environment service via REST."""

    _application_name = "Environment Service"
    _service_name = "environment-service"
    _api_version = "v1"

    @staticmethod
    def application_name():
        """Get the application name of the service.

        Returns:
            (str): The application name of the service.
        """
        return EnvironmentServiceClient._application_name

    @staticmethod
    def service_name():
        """Get the name of the service.

        Returns:
            (str): The name of the service.
        """
        return EnvironmentServiceClient._service_name

    @staticmethod
    def api_version():
        """Get the api version of this client to the service.

        Returns:
            (str): The api version of this client.
        """
        return EnvironmentServiceClient._api_version

    def __init__(self, authenticated_client, url):
        """Create a new environment client.

        Args:
            authenticated_client (common.AuthenticatedClient): Plenty service client that has
                credentials.
            url (str): The url to use for the client.
        """

        self.__service_client = AuthenticatedServiceClient(
            authenticated_client, format_url_with_version(url, self.api_version())
        )

    def build_commands(self):
        """Stub for building the commands for this client."""

        return {
            "alert_rules": (
                "AlertRules commands",
                {
                    "create": (
                        "Create an AlertRule",
                        self.create_alert_rule,
                        [(["alert_rule"], {"help": "attributes of the AlertRule as JSON string"})],
                    ),
                    "get": (
                        "Get an AlertRule by ID",
                        self.get_alert_rule_by_id,
                        [(["alert_rule_id"], {"help": "id of the AlertRule"})],
                    ),
                    "search": (
                        "Search AlertRules",
                        self.search_alert_rules,
                        [(["search_criteria"], {"help": "criteria of the search"})],
                    ),
                    "update": (
                        "Update an AlertRule",
                        self.update_alert_rule,
                        [
                            (["alert_rule_id"], {"help": "id of the AlertRule"}),
                            (["alert_rule"], {"help": "attributes of the AlertRule as JSON string"}),
                        ],
                    ),
                    "delete": (
                        "Delete an AlertRule",
                        self.delete_alert_rule,
                        [(["alert_rule_id"], {"help": "id of the AlertRule"})],
                    ),
                },
            ),
            "metrics": (
                "Metrics commands",
                {
                    "create": (
                        "Create a Metric",
                        self.create_metric,
                        [(["metric"], {"help": "attributes of the Metric as JSON string"})],
                    ),
                    "get": (
                        "Get a Metric by ID",
                        self.get_metric_by_id,
                        [(["metric_id"], {"help": "id of the Metric"})],
                    ),
                    "search": (
                        "Search Metrics",
                        self.search_metrics,
                        [(["search_criteria"], {"help": "criteria of the search"})],
                    ),
                    "update": (
                        "Update a Metric",
                        self.update_metric,
                        [
                            (["metric_id"], {"help": "id of the Metric"}),
                            (["metric"], {"help": "attributes of the Metric as JSON string"}),
                        ],
                    ),
                    "delete": ("Delete a Metric", self.delete_metric, [(["metric_id"], {"help": "id of the Metric"})]),
                },
            ),
            "users_metrics": (
                "Users Metrics commands",
                {
                    "search": (
                        "Search Users Metrics",
                        self.search_users_metrics,
                        [(["search_criteria"], {"help": "criteria of the search"})],
                    ),
                    "create": (
                        "Mark a Metric as Favorite",
                        self.create_users_metric,
                        [(["metric"], {"help": "attributes of the Metric as JSON string"})],
                    ),
                    "delete": (
                        "Delete Metric from Favorite",
                        self.delete_users_metric,
                        [(["metric_id"], {"help": "id of the Metric"})],
                    ),
                },
            ),
            "subscriptions": (
                "Subscriptions commands",
                {
                    "create": (
                        "Create a Subscription",
                        self.create_subscription,
                        [(["subscription"], {"help": "attributes of the Subscription as JSON string"})],
                    ),
                    "get": (
                        "Get a Subscription by ID",
                        self.get_subscription_by_id,
                        [(["subscription_id"], {"help": "id of the Subscription"})],
                    ),
                    "search": (
                        "Search Subscriptions",
                        self.search_subscriptions,
                        [(["search_criteria"], {"help": "criteria of the search"})],
                    ),
                    "update": (
                        "Update a Subscription",
                        self.update_subscription,
                        [
                            (["subscription_id"], {"help": "id of the Subscription"}),
                            (["subscription"], {"help": "attributes of the Subscription as JSON string"}),
                        ],
                    ),
                    "delete": (
                        "Delete an Subscription",
                        self.delete_subscription,
                        [(["subscription_id"], {"help": "id of the Subscription"})],
                    ),
                },
            ),
            "dashboards": (
                "Dashboards commands",
                {
                    "create": (
                        "Create a Dashboard",
                        self.create_dashboard,
                        [(["dashboard"], {"help": "attributes of the Dashboard as JSON string"})],
                    ),
                    "get": (
                        "Get a Dashboard by ID",
                        self.get_dashboard_by_id,
                        [(["dashboard_id"], {"help": "id of the Dashboard"})],
                    ),
                    "search": (
                        "Search Dashboards",
                        self.search_dashboards,
                        [(["search_criteria"], {"help": "criteria of the search"})],
                    ),
                    "update": (
                        "Update a Dashboard",
                        self.update_dashboard,
                        [
                            (["dashboard_id"], {"help": "id of the Dashboard"}),
                            (["dashboard"], {"help": "attributes of the Dashboard as JSON string"}),
                        ],
                    ),
                    "delete": (
                        "Delete a Dashboard",
                        self.delete_dashboard,
                        [(["dashboard_id"], {"help": "id of the Dashboard"})],
                    ),
                },
            ),
            "users_dashboards": (
                "Users Dashboards commands",
                {
                    "search": (
                        "Search Users Dashboards",
                        self.search_users_dashboards,
                        [(["search_criteria"], {"help": "criteria of the search"})],
                    ),
                    "create": (
                        "Mark a Dashboard as Favorite",
                        self.create_users_dashboard,
                        [(["users_dashboard"], {"help": "attributes of the Users Dashboard as JSON string"})],
                    ),
                    "delete": (
                        "Delete Dashboard from Favorite",
                        self.delete_users_dashboard,
                        [(["dashboard_id"], {"help": "id of the Dashboard"})],
                    ),
                },
            ),
        }

    def build_cli_subcommand(self):
        """Bulid the CLI subcommand for this client.

        Returns:
            ((str, str, str, ({str: (str, {str: str})}), func)): Everything
                needed for a CLI subcommand.
        """
        return (
            "environment",
            "environment service client",
            "e",
            self.build_commands(),
            lambda s, _: [{"users_dashboards": "ud", "users_metrics": "um"}.get(s, s[0])],
        )

    #
    # AlertRules
    #
    def create_alert_rule(self, request: Dict) -> Dict:
        return self.__service_client.post(["alert-rules"], req_json=str_to_json(request)).json()

    def get_alert_rule_by_id(self, alert_rule_id: str) -> Dict:
        return self.__service_client.get(["alert-rules", alert_rule_id]).json()

    def search_alert_rules(self, request: Dict) -> Dict:
        return self.__service_client.post(["alert-rules", "search"], req_json=str_to_json(request)).json()

    def list_alert_rules(
        self,
        metric_id: Optional[str] = None,
        stars_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        alert_rule_types: Optional[List[str]] = None,
        is_enabled: Optional[bool] = None,
        is_snoozed: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict:
        query_args = filter_query_args(
            {
                "metricId": metric_id,
                "startsAt": stars_at,
                "endsAt": ends_at,
                "alertRuleTypes[]": alert_rule_types,
                "isEnabled": is_enabled,
                "isSnoozed": is_snoozed,
                "limit": limit,
                "offset": offset,
                "sortBy": sort_by,
                "order": order,
            }
        )

        return self.__service_client.get(["alert-rules"], quert_args=query_args).json()

    def update_alert_rule(self, alert_rule_id: str, request: Dict) -> Dict:
        return self.__service_client.put(["alert-rules", alert_rule_id], req_json=str_to_json(request)).json()

    def delete_alert_rule(self, alert_rule_id: str) -> Dict:
        return self.__service_client.delete(["alert-rules", alert_rule_id]).json()

    #
    # AlertRuleTypes
    #
    def list_alert_rule_types(self) -> List:
        query_args = filter_query_args({})
        return self.__service_client.get(["alert-rules"], quert_args=query_args).json()

    #
    # Metrics
    #
    def create_metric(self, request: Dict) -> Dict:
        return self.__service_client.post(["metrics"], req_json=str_to_json(request)).json()

    def get_metric_by_id(self, metric_id: str) -> Dict:
        return self.__service_client.get(["metrics", metric_id]).json()

    def search_metrics(self, request: Dict) -> Dict:
        return self.__service_client.post(["metrics", "search"], req_json=str_to_json(request)).json()

    def list_metrics(
        self,
        path: Optional[str] = None,
        measurement_type: Optional[str] = None,
        observation_name: Optional[str] = None,
        include_alerts: Optional[str] = None,
        starts_at: Optional[str] = None,
        ends_at: Optional[str] = None,
        alert_rule_types: Optional[List[str]] = None,
        is_enabled: Optional[bool] = None,
        is_snoozed: Optional[bool] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict:
        query_args = filter_query_args(
            {
                "path": path,
                "measurementType": measurement_type,
                "observationName": observation_name,
                "includeAlerts": include_alerts,
                "startsAt": starts_at,
                "endsAt": ends_at,
                "alertRuleTypes[]": alert_rule_types,
                "isEnabled": is_enabled,
                "isSnoozed": is_snoozed,
                "limit": limit,
                "offset": offset,
                "sortBy": sort_by,
                "order": order,
            }
        )

        return self.__service_client.get(["metrics"], quert_args=query_args).json()

    def update_metric(self, metric_id: str, request: Dict) -> Dict:
        return self.__service_client.put(["metrics", metric_id], req_json=str_to_json(request)).json()

    def delete_metric(self, metric_id: str) -> Dict:
        return self.__service_client.delete(["metrics", metric_id]).json()

    #
    # Users Metrics
    #
    def search_users_metrics(self, request: Dict) -> Dict:
        return self.__service_client.post(["users-metrics", "search"], req_json=str_to_json(request)).json()

    def list_users_metrics(
        self,
        metric_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict:
        query_args = filter_query_args(
            {"metricId": metric_id, "limit": limit, "offset": offset, "sortBy": sort_by, "order": order}
        )

        return self.__service_client.get(["users-metrics"], quert_args=query_args).json()

    def create_users_metric(self, request: Dict) -> Dict:
        return self.__service_client.post(["users-metrics"], req_json=str_to_json(request)).json()

    def delete_users_metric(self, metric_id: str) -> Dict:
        return self.__service_client.delete(["users-metrics", metric_id]).json()

    #
    # Subscriptions
    #
    def create_subscription(self, request: Dict) -> Dict:
        return self.__service_client.post(["subscriptions"], req_json=str_to_json(request)).json()

    def get_subscription_by_id(self, subscription_id: str) -> Dict:
        return self.__service_client.get(["subscriptions", subscription_id]).json()

    def search_subscriptions(self, request: Dict) -> Dict:
        return self.__service_client.post(["subscriptions", "search"], req_json=str_to_json(request)).json()

    def list_subscriptions(
        self,
        alert_rule_id: Optional[str] = None,
        method: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict:
        query_args = filter_query_args(
            {
                "alertRuleId": alert_rule_id,
                "method": method,
                "limit": limit,
                "offset": offset,
                "sortBy": sort_by,
                "order": order,
            }
        )

        return self.__service_client.get(["subscriptions"], quert_args=query_args).json()

    def update_subscription(self, subscription_id: str, request: Dict) -> Dict:
        return self.__service_client.put(["subscriptions", subscription_id], req_json=str_to_json(request)).json()

    def delete_subscription(self, subscription_id: str) -> Dict:
        return self.__service_client.delete(["subscriptions", subscription_id]).json()

    #
    # Dashboards
    #
    def create_dashboard(self, request: Dict) -> Dict:
        return self.__service_client.post(["dashboards"], req_json=str_to_json(request)).json()

    def get_dashboard_by_id(self, metric_id: str) -> Dict:
        return self.__service_client.get(["dashboards", metric_id]).json()

    def search_dashboards(self, request: Dict) -> Dict:
        return self.__service_client.post(["dashboards", "search"], req_json=str_to_json(request)).json()

    def list_dashboards(
        self,
        name: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict:
        query_args = filter_query_args(
            {"name": name, "limit": limit, "offset": offset, "sortBy": sort_by, "order": order}
        )

        return self.__service_client.get(["dashboards"], quert_args=query_args).json()

    def update_dashboard(self, dashboard_id: str, request: Dict) -> Dict:
        return self.__service_client.put(["dashboards", dashboard_id], req_json=str_to_json(request)).json()

    def delete_dashboard(self, dashboard_id: str) -> Dict:
        return self.__service_client.delete(["dashboards", dashboard_id]).json()

    #
    # Users Dashboards
    #
    def search_users_dashboards(self, request: Dict) -> Dict:
        return self.__service_client.post(["users-dashboards", "search"], req_json=str_to_json(request)).json()

    def list_users_dashboards(
        self,
        dashboard_id: Optional[str] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
        sort_by: Optional[str] = None,
        order: Optional[str] = None,
    ) -> Dict:
        query_args = filter_query_args(
            {"dashboardId": dashboard_id, "limit": limit, "offset": offset, "sortBy": sort_by, "order": order}
        )

        return self.__service_client.get(["users-dashboards"], quert_args=query_args).json()

    def create_users_dashboard(self, request: Dict) -> Dict:
        return self.__service_client.post(["users-dashboards"], req_json=str_to_json(request)).json()

    def delete_users_dashboard(self, dashboard_id: str) -> Dict:
        return self.__service_client.delete(["users-dashboards", dashboard_id]).json()
