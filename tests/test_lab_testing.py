# Standard library imports
from pprint import pprint

# 3rd party library imports
import pytest

# Project library imports
from lib.clients import (
    head,
    options,
)

pytestmark = [pytest.mark.farm_def_service]


# Endpoint: /api/lab-testing/products/<farm-def path> [OPTIONS, HEAD, GET]
PATH = "sites/SSF2/areas/PrimaryPostHarvest"


# @pytest.mark.isolate()
@pytest.mark.options()
def test__lab_testing__products__farm_def_path__options():
    verbs = options(f"/api/lab-testing/products/{PATH}", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/lab-testing/products/[path]' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__lab_testing__products__farm_def_path__head():
    response = head(f"/api/lab-testing/products/{PATH}")

    pprint(response)

    # @pytest.mark.skip("waiting for addition of lab-testing API")
    # # @pytest.mark.isolate()
    # def test_xxx_lab_testing__products__farm_def_path__get():
    #     bff_products = get_json(f"/api/lab-testing/products/{PATH}")
    #
    #     print("BFF lab-testing products")
    #     pprint(bff_products)
    #     print()
    #
    #     with open("bff_lab_testing_products.json", "w") as write_file:
    #         json.dump(write_file, bff_products, indent=4)

    # TODO add BFF and service validation

    """
    farm-def-service validations:

    # area_object = get_farm_def_service_client().get_object_by_path(area_path, 0)
    # crop = get_farm_def_service_client().search_crops_by_farm_path(farm_def_obj.get("path")) # see 'helper'
    """
