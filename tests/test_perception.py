# Standard library imports
from pprint import pprint

# 3rd party library imports
import pytest

# Project library imports
from lib.clients import (
    get_json,
    head,
    options,
    # perception_object_service_client,
    post,
)
from lib.perception import (
    generate_perception_object,
    get_add_label_set_payload,
    get_add_tag_payload,
    get_search_date_interval_payload,
)

pytestmark = [
    pytest.mark.perception_object_service,
    pytest.mark.skip("Pending proper test environment support"),
]


# Endpoint: /api/perception/add-label-set [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__perception__add_label_set__options():
    verbs = options("/api/perception/add-label-set", "OPTIONS, POST")

    print(f"verbs supported for '/api/perception/add-label-set' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.post()
#
# NOTE: Per Pradeep, the create/update label set bits are being reworked in the near future.
#       We agreed to defer these tests for now as the POS and BFF routines have gone unchanged
#       for nearly two years at this point so there are no likely change-based disruptions to observe.
#
def test__perception__add_label_set__post():
    pos_perception_object = generate_perception_object()

    print("POS Perception Object:")
    pprint(pos_perception_object)
    print()

    uuid = pos_perception_object["uuid"]

    add_label_set_payload = get_add_label_set_payload()

    print("Label set:")
    pprint(add_label_set_payload)
    print()

    label_set_name = add_label_set_payload["name"]

    label_set_addition_response = post(f"/api/perception/add-label-set?uuid={uuid}", payload=add_label_set_payload)

    print("BFF Label Set addition response")
    pprint(label_set_addition_response)
    print()


# Endpoint: /api/perception/add-tag [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__perception__add_tag__options():
    verbs = options("/api/perception/add-tag", "OPTIONS, POST")

    print(f"verbs supported for '/api/perception/add-tag' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.post()
def test__perception__add_tag__post():
    pos_perception_object = generate_perception_object()

    print("POS Perception Object:")
    pprint(pos_perception_object)
    print()

    pos_perception_object_uuid = pos_perception_object["uuid"]

    add_tag_payload = get_add_tag_payload(pos_perception_object_uuid)

    # the same key/value pairs are passed in both the query string AND the passed JSON for this request
    tag = add_tag_payload["tag"]
    uuid = add_tag_payload["uuid"]

    bff_perception_tagging_response = post(f"/api/perception/add-tag?uuid={uuid}&tag={tag}", payload=add_tag_payload)

    print("BFF Perception Object tagging response:")
    pprint(bff_perception_tagging_response)
    print()

    assert bff_perception_tagging_response["data"][0]["tagId"]["name"] == add_tag_payload["tag"]
    print(f"Confirmed: tag name {add_tag_payload['tag']} found in returned response")
    print()

    # get a dict of query string parameters for a 48-hour search window (pass the UUID to include it as well)
    qs_params = get_search_date_interval_payload(pos_perception_object_uuid)

    print("Query string parameters -- date interval:")
    pprint(qs_params)
    print()

    # a single item list should have been returned but take the "first" record anyway
    bff_perception_object = get_json("/api/perception/search", params=qs_params)["data"]["results"][0]

    print("BFF Perception Object")
    pprint(bff_perception_object)
    print()

    assert bff_perception_object["objectTags"][0]["tagId"]["name"] == add_tag_payload["tag"]
    print(f"Confirmed: tag name {add_tag_payload['tag']} found in perception object")
    print()


# Endpoint: /api/perception/search [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__perception__search__options():
    verbs = options("/api/perception/search", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/perception/search' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__perception__search__head():
    response = head("/api/perception/search")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__perception__search__get():
    pos_perception_object = generate_perception_object()

    print("POS Perception Object:")
    pprint(pos_perception_object)
    print()

    pos_perception_object_uuid = pos_perception_object["uuid"]

    # get a dict of query string parameters for a 48-hour search window (pass the UUID to include it as well)
    qs_params = get_search_date_interval_payload(pos_perception_object_uuid)

    print("Query string parameters -- date interval")
    pprint(qs_params)
    print()

    # a single item list should have been returned but take the "first" record anyway
    bff_perception_object = get_json("/api/perception/search", params=qs_params)["data"]["results"][0]

    print("BFF Perception Object")
    pprint(bff_perception_object)
    print()

    # find the common fields among both record representations
    intersection = list(filter(lambda x: x in bff_perception_object.keys(), pos_perception_object.keys()))
    for key in intersection:
        assert pos_perception_object[key] == bff_perception_object[key]
        print(f"Confirmed: {(pos_perception_object[key] == bff_perception_object[key]) = }  [{key}]")
    print()


# Endpoint: /api/perception/update-label-set [OPTIONS, PUT]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__perception__update_label_set__options():
    verbs = options("/api/perception/update-label-set", "OPTIONS, PUT")

    print(f"verbs supported for '/api/perception/update-label-set' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.put()
#
# NOTE: Per Pradeep, the create/update label set bits are being reworked in the near future.
#       We agreed to defer these tests for now as the POS and BFF routines have gone unchanged
#       for nearly two years at this point so there are no likely change-based disruptions to observe.
#
def test__perception__update_label_set__put():
    pos_perception_object = generate_perception_object()

    print("POS Perception Object:")
    pprint(pos_perception_object)
    print()

    pos_perception_object_uuid = pos_perception_object["uuid"]
