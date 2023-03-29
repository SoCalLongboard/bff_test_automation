# Standard library imports
from pprint import pprint

# 3rd party library imports
import pytest

# Project library imports
from lib.clients import (
    farm_def_service_client,
    get_json,
    head,
    options,
)
from lib.devices import (
    get_device_dict,
    clean_up_test_device,
)

pytestmark = [pytest.mark.farm_def_service]


# Endpoint: /api/devices [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__devices__options():
    verbs = options("/api/devices", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/devices' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__devices__head():
    response = head("/api/devices")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test_devices__get():
    device_dict = get_device_dict()

    print("Generated device dictionary (used in requests):")
    pprint(device_dict)
    print()

    fds_device = farm_def_service_client().create_device(device_dict)

    print("FDS-generated device:")
    pprint(fds_device)
    print()

    device_serial = fds_device["serial"]
    device_type_name = fds_device["deviceTypeName"]

    bff_devices = get_json("/api/devices")

    # isolate the specific device
    bff_device = None
    for device in bff_devices:
        if device["serial"] == device_serial:
            bff_device = device
            break

    print("BFF-retrieved device:")
    pprint(bff_device)
    print()

    assert bff_device["deviceTypeName"] == device_type_name
    print(f"Confirmed: {(bff_device['deviceTypeName'] == device_type_name) = }")
    print()

    clean_up_test_device(fds_device)
