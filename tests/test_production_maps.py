# Standard library imports
from pprint import pprint

# 3rd party library imports
import pytest

# Project library imports
from lib.clients import (
    get_json,
    head,
    options,
    traceability_service_client,
)


pytestmark = [pytest.mark.traceability_service]


# Endpoint: /api/production/maps/state [OPTIONS, HEAD, GET]
QUERY_STRING = "?site=SSF2&area=VerticalGrow&line=GrowRoom"


# @pytest.mark.isolate()
@pytest.mark.options()
def test__production__maps__state__options():
    verbs = options(f"/api/production/maps/state{QUERY_STRING}", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/production/maps/state' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__production__maps__state__head():
    response = head(f"/api/production/maps/state{QUERY_STRING}")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__production__maps__state__get():
    bff_response = get_json(f"/api/production/maps/state{QUERY_STRING}")

    # isolate the first member as a sample
    bff_first_member_key = list(bff_response.keys())[0]  # Python 3.10 convention...
    bff_first_member = bff_response[bff_first_member_key]
    bff_resource_state = bff_first_member["resourceState"]
    container_id = bff_resource_state["containerId"]

    print("BFF-retrieved response (first/sample member):")
    pprint(bff_first_member)
    print()

    # retrieve the corresponding member by container ID via traceability
    t3_maps_container_state = traceability_service_client().get_state_by_id(container_id, id_type="CONTAINER_ID")

    print("T3-retrieved member:")
    pprint(t3_maps_container_state)
    print()

    assert bff_resource_state == t3_maps_container_state
    print("Confirmed: state objects are congruent")
