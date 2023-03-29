"""A list of all of the clients."""

from .alert_service.client import AlertServiceClient
from .device_management_service.client import DeviceManagementServiceClient
from .environment_service.client import EnvironmentServiceClient
from .executive_service.client import ExecutiveServiceClient
from .farm_def_service.client import FarmDefServiceClient
from .farm_state_service.client import FarmStateServiceClient
from .lab_testing_service.client import LabTestingServiceClient
from .location_service.client import LocationServiceClient
from .perception_object_service.client import PerceptionObjectServiceClient
from .product_quality_service.client import ProductQualityServiceClient
from .traceability_service.client import TraceabilityService3Client
from .traceability_store.client import TraceabilityClient
from .user_store.client import UserStoreClient
from .varietal_information_service.client import VarietalInformationServiceClient
from .workbin_service.client import WorkbinServiceClient

CLIENTS = [
    AlertServiceClient,
    DeviceManagementServiceClient,
    EnvironmentServiceClient,
    ExecutiveServiceClient,
    FarmDefServiceClient,
    FarmStateServiceClient,
    LabTestingServiceClient,
    LocationServiceClient,
    PerceptionObjectServiceClient,
    ProductQualityServiceClient,
    TraceabilityClient,
    TraceabilityService3Client,
    UserStoreClient,
    VarietalInformationServiceClient,
    WorkbinServiceClient,
]

# EXTERNAL_CLIENTS = [AWSClient, GoogleSheetClient, RedisClient]
