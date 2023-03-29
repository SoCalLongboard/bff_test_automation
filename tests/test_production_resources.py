# Standard library imports
from os import environ
from pprint import pprint

# 3rd party library imports
import pytest

# Project library imports
from lib.clients import (
    get_json,
    head,
    options,
    post,
    traceability_service_client,
)


pytestmark = [pytest.mark.traceability_service]


# Endpoint: /api/production/resources/get-operation-history [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__production__resources__get_operation_history__options():
    verbs = options("/api/production/resources/get-operation-history", "OPTIONS, POST")

    print(f"verbs supported for '/api/production/resources/get-operation-history' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.post()
def test__production__resources__get_operation_history__post():
    environment = environ["ENVIRONMENT_CONTEXT"]
    container_map = {
        "dev": "P900-0008480B:4OYW-X8C0-47",
        "staging": "P900-0008480B:Q7LZ-LWL5-N8",
    }

    # TODO: resolve BFF authentication issue
    bff_operation_history = post(
        "/api/production/resources/get-operation-history", payload={"containerId": container_map[environment]}
    )

    print("BFF operation history:")
    pprint(bff_operation_history)


# Endpoint: /api/production/resources/labels [OPTIONS, HEAD, GET]
QUERY_STRING = "?containerType=TOWER"


# @pytest.mark.isolate()
@pytest.mark.options()
def test__production__resources__labels__options():
    verbs = options(f"/api/production/resources/labels{QUERY_STRING}", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/production/resources/labels' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__production__resources__labels__head():
    response = head(f"/api/production/resources/labels{QUERY_STRING}")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__production__resources__labels__get():
    bff_labels = get_json(f"/api/production/resources/labels{QUERY_STRING}")

    print(f"Number of labels returned from BFF request : {len(bff_labels)}")
    print()

    # isolate a single label from the returned list
    bff_label = bff_labels[0]

    print("BFF label:")
    pprint(bff_label)
    print()

    # get the id of the label to search the traceability service
    bff_label_id = bff_label["id"]
    print(f"{bff_label_id = }")
    print()

    # search by criteria but isolate the sole member returned for comparison
    t3_label = traceability_service_client().filter_labels({"id": bff_label_id})[0]

    print("T3 label:")
    pprint(t3_label)
    print()

    assert bff_label == t3_label
    print("Confirmed: artifacts are congruent")
