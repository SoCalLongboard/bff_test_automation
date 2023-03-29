# Standard library imports
from random import choice

# Project library imports
from lib.clients import farm_def_service_client
from lib.utils import rand_char_str

TEST_DEVICE_PREFIX = "BFFTEST"
TEST_DEVICE_SERIAL_LENGTH = 16


def _get_random_device_type_name():
    # derive valid device_type_name values from a farm-def endpoint
    valid_device_types = farm_def_service_client().search_device_types()

    return choice(valid_device_types)["name"]


# generate an alphanumeric device serial with common prefix
def _generate_device_serial():
    test_device_suffix = rand_char_str(TEST_DEVICE_SERIAL_LENGTH - len(TEST_DEVICE_PREFIX))

    return f"{TEST_DEVICE_PREFIX}{test_device_suffix}"


def get_device_dict():
    device_dict = {"serial": _generate_device_serial(), "typeName": _get_random_device_type_name()}

    return device_dict


def clean_up_test_device(device):
    print(f"Deleting test device: {device['serial']}")
    farm_def_service_client().delete_device(device["id"])
