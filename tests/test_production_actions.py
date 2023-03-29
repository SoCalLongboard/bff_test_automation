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
from lib.production_actions import get_all_actions_for_site

pytestmark = [pytest.mark.farm_def_service]


# Endpoint: /api/production/actions/<action_path> [OPTIONS, HEAD, GET]
ACTION_PATH = "sites/SSF2/interfaces/Traceability/methods/AddOrChangeCrop"


# @pytest.mark.isolate()
@pytest.mark.options()
def test__production__actions__action_path__options():
    verbs = options(f"/api/production/actions/{ACTION_PATH}", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/production/actions/[action-path]' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__production__actions__action_path__head():
    response = head(f"/api/production/actions/{ACTION_PATH}")

    pprint(response)
    print()


# @pytest.mark.isolate()
@pytest.mark.get()
def test_production__actions__action_path__get():
    # Get a SPECIFIC action via BFF
    bff_action = get_json(f"/api/production/actions/{ACTION_PATH}")

    print("BFF action:")
    pprint(bff_action)
    print()

    # Get the same action via FDS
    fds_action = farm_def_service_client().get_method_descriptor(ACTION_PATH)

    print("FDS action:")
    pprint(fds_action)
    print()

    # compare the action from both sources
    bff_action_name = "".join(bff_action["name"].split())  # remove spaces from BFF version

    assert bff_action_name == fds_action["name"]
    print(f"Confirmed: {(bff_action_name == fds_action['name']) = }")

    assert bff_action["description"] == fds_action["description"]
    print(f"Confirmed: {(bff_action['description'] == fds_action['description']) = }")

    assert bff_action["actionType"] == fds_action["type"]
    print(f"Confirmed: {(bff_action['actionType'] == fds_action['type']) = }")


# Endpoint: /api/production/actions/all/sites/<site>/farms/<farm> [OPTIONS, HEAD, GET]
# this request requires that the supported method types (tell, request)
# be passed as query string parameters in this fashion:
FARM = "Tigris"
METHOD_TYPES = ["request", "tell"]
QUERY_STRING = "?method-types[]=tell&method-types[]=request"
SITE = "SSF2"


# @pytest.mark.isolate()
@pytest.mark.options()
def test__production__actions__get_actions_for_site_farm__options():
    verbs = options(f"/api/production/actions/all/sites/{SITE}/farms/{FARM}{QUERY_STRING}", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/production/actions/all/sites/[SITE]/farms/[FARM]' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__production__actions__get_actions_for_site_farm__head():
    response = head(f"/api/production/actions/all/sites/{SITE}/farms/{FARM}{QUERY_STRING}")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__production__actions__get_actions_for_site_farm__get():
    # get all 'request' and 'tell' actions for a specific farm via BFF
    bff_actions = get_json(f"/api/production/actions/all/sites/{SITE}/farms/{FARM}{QUERY_STRING}")

    print("BFF actions:")
    pprint(bff_actions)
    print()

    fds_actions = get_all_actions_for_site(SITE, FARM)

    print("FDS actions:")
    pprint(fds_actions)
    print()

    assert len(bff_actions) == len(fds_actions)
    print(f"Confirmed: {(len(bff_actions) == len(fds_actions)) = }")
