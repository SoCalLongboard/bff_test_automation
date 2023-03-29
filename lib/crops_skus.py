# Standard library imports
from random import choice
import string

# Project library imports
from lib.clients import farm_def_service_client
from lib.colors import get_random_color_pair
from lib.utils import (
    rand_alpha_str,
    rand_char_str,
    rand_boolean,
    rand_num_str,
    get_sample_range,
)
import plentyservice


def _crop_name_available(crop_name):
    # I don't LOVE this, but...
    # the farm-def check for a crop's prior existence either returns the crop or fails,
    # hence, a failure is GOOD here as there is no name conflict.
    try:
        farm_def_service_client().get_crop_by_name(crop_name)
    except plentyservice.request_error.RequestError:
        return True

    print(f"Crop name availability check: {crop_name} already exists...")
    return False


def _generate_crop_name():
    # Examples: "X11", "X1X", "XX1", "XXX"

    while True:
        crop_name = f"{rand_alpha_str(1)}{rand_char_str(2)}"

        if _crop_name_available(crop_name):
            break

    return crop_name


def _generate_netsuite_id():
    # Example: "5-005-0002-09"
    return f"{rand_num_str(1)}-{rand_num_str(3)}-{rand_num_str(4)}-{rand_num_str(2)}"


def generate_gtin_id():
    # Example: "10810567030698"
    return f"{rand_num_str(14)}"


def _get_random_crop_type_name():
    # derive valid crop_type_name values from a farm-def endpoint
    crop_types = farm_def_service_client().search_crop_types()
    valid_crop_type_names = [crop_type["name"] for crop_type in crop_types]

    return choice(valid_crop_type_names)


def generate_crop_dict(name=None, type_name=None):
    # for PUTs, reuse values
    # otherwise generate new original values
    crop_name = name if name else _generate_crop_name()
    crop_type_name = type_name if type_name else _get_random_crop_type_name()

    crop_dict = {
        "childCrops": [],
        "commonName": f"{crop_name} BFFTEST Common Name",
        "cropTypeName": crop_type_name,
        "cultivar": f"{crop_name} Cultivar",
        "description": f"{crop_name} Description",
        "displayAbbreviation": f"{crop_name}",
        "group": f"{crop_name} Group",
        "isSeedable": rand_boolean(),
        "media": f"{crop_name} Media",
        "name": crop_name,
        "properties": {},
        "seedPartNumbers": [],
    }

    return crop_dict


def fds_create_crop(crop_dict):
    new_crop = farm_def_service_client().create_crop(crop_dict)

    return new_crop


def clean_up_test_crop(crop_name):
    print(f"Deleting test crop: {crop_name}")
    farm_def_service_client().delete_crop(crop_name)
    print()


# ----- SKUs -----
def _get_random_sku_type():
    # derive valid sku_type_name values from a farm-def endpoint
    valid_sku_types = farm_def_service_client().search_sku_types()
    # TODO support cases in the future
    valid_sku_type_names = [sku_type["name"] for sku_type in valid_sku_types if "Case" not in sku_type["name"]]

    return choice(valid_sku_type_names)


def _generate_expiration_interval():
    expiration_map = {}

    # Internal: 0 < X < 6
    internal_range = get_sample_range(1, 5)
    internal = choice(internal_range)
    expiration_map["internal"] = internal

    # External: internal < X < 16
    external_range = get_sample_range(internal + 1, 15)
    external = choice(external_range)
    expiration_map["external"] = external

    return expiration_map


def _get_product_weight(type_name):
    type_name = type_name.lower()

    # supporting cases now requires the addition of a childSkuName field to the dictionary
    # being built (for the clamshells contained) -- avoid testing cases until this is worked out
    # TODO add case/child sku support
    # if type_name.startswith("case"):
    #     # cases hold 6 clamshells (4.5 or 9 ounces each)
    #     if "4o5" in type_name:
    #         return 27.0
    #     else:
    #         return 54.0

    # strip alpha chars before 1st digit
    type_name = type_name.lstrip(string.ascii_lowercase)

    # return an appropriate float value given a matched initial digit
    # NOTE: weights for cases are individual clamshell weights, not a case aggregate
    weights = {
        "1": 16.0,  # bulk, 1lb in oz
        "3": 42.0,  # bulk, 3lb in oz
        "4": 4.0,  # clamshell, 4oz (for both the 4 and 4.5 oz values)
        "9": 4.0,  # clamshell, 9oz
    }

    return weights[type_name[0]]


def _get_brand_type_name(type_name):
    type_name = type_name.lower()

    if type_name.startswith("bulk"):
        return None

    return choice(["Plenty", "Marketside"])


def generate_sku_dict(crop_name, type_name=None):
    # handle re-use for PUTs
    sku_type_name = type_name if type_name else _get_random_sku_type()

    product_weight = _get_product_weight(sku_type_name)
    brand_type_name = _get_brand_type_name(sku_type_name)

    expiration_map = _generate_expiration_interval()
    color_pair = get_random_color_pair()

    sku_dict = {
        "allowedCropNames": [f"{crop_name}"],
        "brandTypeName": brand_type_name,
        "defaultCropName": crop_name,
        "description": f"{crop_name} {sku_type_name} Description",
        "externalExpirationDays": expiration_map["external"],
        "gtin": generate_gtin_id(),
        "internalExpirationDays": expiration_map["internal"],
        "labelPrimaryColor": color_pair["primary"],
        "labelSecondaryColor": color_pair["secondary"],
        "netsuiteItem": _generate_netsuite_id(),
        "packagingLotCropCode": f"{crop_name}",
        "productName": f"{crop_name} BFFTEST Test SKU",
        "productWeightOz": product_weight,
        "properties": {},
        "skuTypeName": sku_type_name,
    }

    return sku_dict


def fds_create_sku(sku_dict):
    new_sku = farm_def_service_client().create_sku(sku_dict)

    return new_sku


def clean_up_test_sku(sku_name):
    print(f"Deleting test sku: {sku_name}")
    farm_def_service_client().delete_sku(sku_name)
    print()
