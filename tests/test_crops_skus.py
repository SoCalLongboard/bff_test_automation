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
    post,
    put,
)
from lib.crops_skus import (
    clean_up_test_crop,
    clean_up_test_sku,
    fds_create_crop,
    fds_create_sku,
    generate_crop_dict,
    generate_gtin_id,
    generate_sku_dict,
)

pytestmark = [pytest.mark.farm_def_service]

FARM_DEF_SKU_QUERY_LIMIT = 100


# ----- CROPs -----
# Endpoint: /api/crops-skus/crop [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__crops_skus__crop__options():
    verbs = options("/api/crops-skus/crop", "OPTIONS, POST")

    print(f"verbs supported for '/api/crops-skus/crop' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.post()
def test__crops_skus__crop__post(cleanup):
    crop_dict = generate_crop_dict()

    print("Generated crop dictionary:")
    pprint(crop_dict)
    print()

    crop_name = crop_dict["name"]

    bff_crop = post("/api/crops-skus/crop", crop_dict)
    cleanup(lambda: clean_up_test_crop(crop_name))

    print("BFF-generated crop:")
    pprint(bff_crop)
    print()

    fds_crop = farm_def_service_client().get_crop_by_name(crop_name)

    print("FDS-retrieved crop:")
    pprint(fds_crop)
    print()

    # full object comparison
    assert bff_crop == fds_crop
    print(f"Confirmed: {(bff_crop == fds_crop) = }")

    for key in crop_dict.keys():
        assert bff_crop[key] == crop_dict[key]
        print(f"Confirmed: {(bff_crop[key] == crop_dict[key]) = }  [{key}]")
    print()


# Endpoint: /api/crops-skus/crop/<crop-name> [OPTIONS, PUT]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__crops_skus__crop__crop_name__options(cleanup):
    crop_dict = generate_crop_dict()

    print("Generated crop dictionary:")
    pprint(crop_dict)
    print()

    fds_crop = fds_create_crop(crop_dict)
    crop_name = fds_crop["name"]
    cleanup(lambda: clean_up_test_crop(crop_name))

    print("FDS-generated crop:")
    pprint(fds_crop)
    print()

    verbs = options(f"/api/crops-skus/crop/{crop_name}", "OPTIONS, PUT")

    print(f"verbs supported for '/api/crops-skus/crop/[crop-name]' : {verbs}")
    print()


# @pytest.mark.isolate()
@pytest.mark.put()
def test__crops_skus__crop__crop_name__put(cleanup):
    crop_dict = generate_crop_dict()

    print("Generated crop dictionary:")
    pprint(crop_dict)
    print()

    # generate the initial crop
    fds_crop = fds_create_crop(crop_dict)
    crop_name = fds_crop["name"]
    cleanup(lambda: clean_up_test_crop(crop_name))

    # get initial value for switch/comparison
    is_seedable = fds_crop.get("isSeedable")

    print("FDS-generated crop:")
    pprint(fds_crop)
    print()

    # force difference/change for update
    crop_dict["isSeedable"] = not is_seedable

    print("Modified crop dictionary:")
    pprint(crop_dict)
    print()

    # modify the crop with a PUT
    bff_crop = put(f"/api/crops-skus/crop/{crop_name}", payload=crop_dict)

    print("BFF-modified crop:")
    pprint(bff_crop)
    print()

    # retrieve the same crop post-modification
    fds_crop = farm_def_service_client().get_crop_by_name(crop_name)

    print("FDS-retrieved crop:")
    pprint(fds_crop)
    print()

    assert fds_crop["isSeedable"] == bff_crop["isSeedable"]
    print(f"Confirmed: {(fds_crop['isSeedable'] == bff_crop['isSeedable']) = }")
    print()


# Endpoint: /api/crops-skus/crops [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__crops_skus__crops__options():
    verbs = options("/api/crops-skus/crops", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/crops-skus/crops' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__crops_skus__crops__head():
    response = head("/api/crops-skus/crops")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__crops_skus__crops__get(cleanup):
    crop_dict = generate_crop_dict()

    print("Generated crop dictionary:")
    pprint(crop_dict)
    print()

    # generate an initial crop (to ensure at least one returned)
    fds_crop = fds_create_crop(crop_dict)
    crop_name = fds_crop["name"]
    cleanup(lambda: clean_up_test_crop(crop_name))

    print("FDS-generated crop:")
    pprint(fds_crop)
    print()

    # get ALL currently-available crops
    bff_crops = get_json("/api/crops-skus/crops")

    print(f"Number of crops returned from BFF request: {len(bff_crops)}")
    print()

    bff_crop_names = [crop["name"] for crop in bff_crops]

    bff_crop = None
    for crop in bff_crops:
        if crop["name"] == crop_name:
            bff_crop = crop
            break

    assert bff_crop is not None
    print(f"Confirmed: crop {crop_name} is found among BFF-retrieved crops")
    print()

    print("BFF-retrieved crop:")
    pprint(bff_crop)
    print()

    assert crop_name in bff_crop_names
    print(f"Confirmed: {(crop_name in bff_crop_names) = }")

    assert len(bff_crops) > 0
    print(f"Confirmed: {(len(bff_crops) > 0) = }")
    print()


# ----- SKUs -----
# Endpoint: /api/crops-skus/sku [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__crops_skus__sku__options():
    verbs = options("/api/crops-skus/sku", "OPTIONS, POST")

    print(f"verbs supported for '/api/crops-skus/sku' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.post()
def test__crops_skus__sku__post(cleanup):
    # first, create a crop via FDS
    crop_dict = generate_crop_dict()

    print("Generated crop dictionary:")
    pprint(crop_dict)
    print()

    fds_crop = fds_create_crop(crop_dict)
    print("FDS-generated crop:")
    pprint(fds_crop)
    print()

    crop_name = fds_crop.get("name")
    cleanup(lambda: clean_up_test_crop(crop_name))

    # then create a sku via BFF
    sku_dict = generate_sku_dict(crop_name=crop_name)
    print("Generated sku dictionary:")
    pprint(sku_dict)
    print()

    bff_sku = post("/api/crops-skus/sku", sku_dict)
    cleanup(lambda: clean_up_test_sku(bff_sku["name"]))
    print("BFF-generated sku:")
    pprint(bff_sku)
    print()

    # verify contents
    for key in sku_dict.keys():
        assert bff_sku[key] == sku_dict[key]
        print(f"Confirmed: {(bff_sku[key] == sku_dict[key]) = }  [{key}]")
    print()


# Endpoint: /api/crops-skus/sku/<sku-name> [OPTIONS, PUT]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__crops_skus__sku__sku_name__options(cleanup):
    # first, create a crop via FDS
    crop_dict = generate_crop_dict()

    print("Generated crop dictionary:")
    pprint(crop_dict)
    print()

    fds_crop = fds_create_crop(crop_dict)
    print("FDS-generated crop:")
    pprint(fds_crop)
    print()

    crop_name = fds_crop["name"]
    cleanup(lambda: clean_up_test_crop(crop_name))

    # then create a sku via FDS
    sku_dict = generate_sku_dict(crop_name=crop_name)
    print("Generated sku dictionary:")
    pprint(sku_dict)
    print()

    fds_sku = fds_create_sku(sku_dict)
    cleanup(lambda: clean_up_test_sku(fds_sku["name"]))
    print("FDS-generated sku:")
    pprint(fds_sku)
    print()

    fds_sku_name = fds_sku["name"]
    verbs = options(f"/api/crops-skus/sku/{fds_sku_name}", "OPTIONS, PUT")

    print(f"verbs supported for '/api/crops-skus/sku/[sku-name]' : {verbs}")
    print()


# @pytest.mark.isolate()
@pytest.mark.put()
def test__crops_skus__sku__sku_name__put(cleanup):
    # first, create a crop via FDS
    crop_dict = generate_crop_dict()

    print("Generated crop dictionary:")
    pprint(crop_dict)
    print()

    fds_crop = fds_create_crop(crop_dict)
    print("FDS-generated crop:")
    pprint(fds_crop)
    print()

    crop_name = fds_crop["name"]
    cleanup(lambda: clean_up_test_crop(crop_name))

    # then create a sku via BFF
    sku_dict = generate_sku_dict(crop_name=crop_name)
    print("Generated sku dictionary:")
    pprint(sku_dict)
    print()

    fds_sku = fds_create_sku(sku_dict)
    cleanup(lambda: clean_up_test_sku(fds_sku["name"]))
    print("FDS-generated sku:")
    pprint(fds_sku)
    print()

    fds_sku_name = fds_sku.get("name")

    # tweak the dictionary for provide a change for the PUT
    sku_dict["gtin"] = generate_gtin_id()

    print("Modified sku dictionary:")
    pprint(sku_dict)
    print()

    # use BFF to modify the sku with a PUT
    bff_sku = put(f"/api/crops-skus/sku/{fds_sku_name}", sku_dict)
    print("BFF-modified sku:")
    pprint(bff_sku)
    print()

    # verify change
    assert bff_sku["gtin"] == sku_dict["gtin"]
    print(f"Confirmed: {(bff_sku['gtin'] == sku_dict['gtin']) = }")
    print()


# Endpoint: /api/crops-skus/skus [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__crops_skus__skus__options():
    verbs = options("/api/crops-skus/skus", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/crops-skus/skus' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__crops_skus__skus__head():
    response = head("/api/crops-skus/skus")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__crops_skus__skus__get(cleanup):
    # first, create a crop via FDS
    crop_dict = generate_crop_dict()

    print("Generated crop dictionary:")
    pprint(crop_dict)
    print()

    fds_crop = fds_create_crop(crop_dict)
    print("FDS-generated crop:")
    pprint(fds_crop)
    print()

    crop_name = fds_crop["name"]
    cleanup(lambda: clean_up_test_crop(crop_name))

    # then create a sku via FDS
    sku_dict = generate_sku_dict(crop_name=crop_name)
    print("Generated sku dictionary:")
    pprint(sku_dict)
    print()

    fds_sku = fds_create_sku(sku_dict)
    cleanup(lambda: clean_up_test_sku(fds_sku["name"]))
    print("FDS-generated sku:")
    pprint(fds_sku)
    print()

    # get all available skus via BFF
    bff_skus = get_json("/api/crops-skus/skus")
    bff_skus_record_count = len(bff_skus)

    assert bff_skus_record_count > 0
    print("Confirmed: BFF GET request returned a positive number of records.")

    print(f"Number of BFF SKUs returned: {bff_skus_record_count}")
    print()

    if bff_skus_record_count < FARM_DEF_SKU_QUERY_LIMIT:
        # isolate the target sku
        bff_sku = None
        for sku in bff_skus:
            if sku.get("defaultCropName") == crop_name:
                bff_sku = sku
                break

        print("BFF-retrieved sku:")
        pprint(bff_sku)
        print()

        assert fds_sku["internalExpirationDays"] == bff_sku["internalExpirationDays"]
        print(f"Confirmed: (fds_sku['internalExpirationDays'] == bff_sku['internalExpirationDays'])")

        assert fds_sku["externalExpirationDays"] == bff_sku["externalExpirationDays"]
        print(f"Confirmed: (fds_sku['externalExpirationDays'] == bff_sku['externalExpirationDays'])")
        print()
