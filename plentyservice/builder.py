"""Shortcuts to building service clients."""
import os

from . import common
from .clients import *
from .common import Cfg
from .constants import PROD


class ServiceClientBuilder:
    """Builder that short-cuts the construction of service clients."""

    def __init__(self, api_key, api_secret, environment_context, in_kubernetes, timeout):
        """Create a new builder around provided credentials.

        Args:
            api_key (str): The API key with which requests should be made.
            api_secret (str): The API secret with which requests should be made.
        """
        self.__api_key = api_key
        self.__api_secret = api_secret
        self.__environment_context = environment_context
        self.__in_kubernetes = in_kubernetes
        self.__timeout = timeout

    def __build_client(self, client_class, url, jwt_auth=False):
        """
        Helper function for repetitive logic in building default clients
        Args:
            client_class: The client to build
            url: An override url to use if desired
            jwt_auth: Enable use of jwt auth if service supports

        Returns:
            An instance of the desired client
        """
        service_url = url or common.get_service_url(
            client_class.service_name(),
            self.__environment_context,
            self.__in_kubernetes,
        )
        return client_class(self.__build_authenticated_inner_client(jwt_auth), service_url)

    def __build_authenticated_inner_client(self, use_jwt=False):
        """Build a new authenticated inner client.

        Returns:
            common.AuthenticatedClient: Newly created authenticated client.
        """
        return common.AuthenticatedClient(self.__api_key, self.__api_secret, self.__timeout, use_jwt)

    def build_alert_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the alert service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (alert_service.client.AlertServiceClient): The newly created
                client.
        """
        return self.__build_client(AlertServiceClient, url, jwt_auth)

    def build_device_management_client(self, url=None, jwt_auth=False):
        """Build a new client for the device management service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (device_management.client.DeviceManagementServiceClient): The
                newly created client.
        """
        return self.__build_client(DeviceManagementServiceClient, url, jwt_auth)

    def build_environment_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the environment service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (environment_service.client.EnvironmentServiceClient): The newly
                created client.
        """
        return self.__build_client(EnvironmentServiceClient, url, jwt_auth)

    def build_executive_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the executive service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (executive_service.client.ExecutiveServiceClient): The newly
                created client.
        """
        return self.__build_client(ExecutiveServiceClient, url, jwt_auth)

    def build_farm_def_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the farm def service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (farm_def_service.client.FarmDefServiceClient): The newly
                created client.
        """
        return self.__build_client(FarmDefServiceClient, url, jwt_auth)

    def build_farm_state_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the farm state service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (farm_state_service.client.FarmStateServiceClient): The newly
                created client.
        """
        return self.__build_client(FarmStateServiceClient, url, jwt_auth)

    def build_lab_testing_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the lab testing service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (lab_testing_service.client.LabTestingServiceClient):
                The newly created client.lab_testing_service.get_lab_test_type("water").
        """
        return self.__build_client(LabTestingServiceClient, url, jwt_auth)

    def build_location_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the location service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (location_service.client.LocationServiceClient): The newly
                created client.
        """
        return self.__build_client(LocationServiceClient, url, jwt_auth)

    def build_perception_object_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the perception object service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (perception_object_service.client.PerceptionObjectServiceClient):
                The newly created client.
        """
        return self.__build_client(PerceptionObjectServiceClient, url, jwt_auth)

    def build_product_quality_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the product quality service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (product_quality_service.client.ProductQualityServiceClient):
                The newly created client.
        """
        return self.__build_client(ProductQualityServiceClient, url, jwt_auth)

    def build_traceability_client(self, url=None, jwt_auth=False):
        """Build a new client for the traceability_store store.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (traceability_service.client.TraceabilityClient: The newly
                created client.
        """
        return self.__build_client(TraceabilityClient, url, jwt_auth)

    def build_traceability3_client(self, url=None, jwt_auth=False) -> TraceabilityService3Client:
        """Build a new client for the traceability_store store.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (traceability_service.client.TraceabilityService3Client: The newly
                created client.
        """
        return self.__build_client(TraceabilityService3Client, url, jwt_auth)

    def build_user_store_client(self, url=None, jwt_auth=False):
        """Build a new client for the user store.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (user_store.client.UserStoreClient): The newly created client.
        """
        return self.__build_client(UserStoreClient, url, jwt_auth)

    def build_varietal_information_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the varietal information service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (varietal_information_service.client.VarietalInformationServiceClient):
                The newly created client.
        """
        return self.__build_client(VarietalInformationServiceClient, url, jwt_auth)

    def build_workbin_service_client(self, url=None, jwt_auth=False):
        """Build a new client for the workbin service.

        Args:
            url (str): An override url.
            jwt_auth (boolean): True if to use jwt authentication

        Returns:
            (workbin_service.client.WorkbinServiceClient): The newly created
                client.
        """
        return self.__build_client(WorkbinServiceClient, url, jwt_auth)


def client_builder(
    api_key=None, api_secret=None, is_external=False, in_kubernetes=None, environment_context=None, timeout=None
):
    """Create a service client builder with API keys / secret from env vars.

    Returns:
        (ServiceClientBuilder): Builder using credentials from env vars.
    """
    # if is_external:
    #     return ExternalServiceClientBuilder
    if api_key is None:
        api_key = Cfg.get_plenty_api_key()
    if api_secret is None:
        api_secret = Cfg.get_plenty_api_secret()

    if in_kubernetes is None:
        in_kubernetes = Cfg.is_in_kubernetes()
    if environment_context is None:
        environment_context = Cfg.get_environment_context()

    return ServiceClientBuilder(
        api_key=api_key,
        api_secret=api_secret,
        in_kubernetes=in_kubernetes,
        environment_context=environment_context,
        timeout=timeout,
    )


def get_client_application_versions():
    """Gets all of the application names and their associated client versions.

    Returns:
        ({str: str}): All of the application names and their associated client
            versions.
    """
    return {client.application_name(): client.api_version() for client in CLIENTS}
