# Standard library imports
from pprint import pprint

# 3rd party library imports
import pytest

# Project library imports
from lib.clients import (
    get_json,
    head,
    options,
    post,
    product_quality_service_client,
    put,
)
from lib.product_quality import (
    cleanup_test_postharvest,
    cleanup_test_sensory_event,
    cleanup_test_sensory_rating,
    create_sensory_event,
    generate_postharvest_dict,
    generate_sensory_event_dict,
    generate_sensory_rating_dict,
    get_bulk_deletion_payload,
    get_postharvest_notes,
    get_postharvest_query_string_payload,
)

pytestmark = [pytest.mark.product_quality_service]

TEST_FARM = "TIGRIS"
TEST_SITE = "SSF2"


# Endpoint: /api/quality/bulk/postharvest [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__product_quality__bulk__postharvest__options():
    verbs = options("/api/quality/bulk/postharvest", "OPTIONS, POST")

    print(f"verbs supported for '/api/quality/bulk/postharvest' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.post()
def test__product_quality__bulk__postharvest__post():
    # create the initial record
    postharvest_dict = generate_postharvest_dict(TEST_FARM)

    print("Postharvest dict:")
    pprint(postharvest_dict)
    print()

    bff_postharvest_record = post("/api/quality/postharvest", payload=postharvest_dict)

    print("BFF Postharvest record:")
    pprint(bff_postharvest_record)
    print()

    bff_postharvest_id = bff_postharvest_record["id"]

    # build the payload with a list of record id values
    bulk_deletion_payload = get_bulk_deletion_payload([bff_postharvest_id])

    print("Bulk deletion payload:")
    pprint(bulk_deletion_payload)
    print()

    # use bulk deletion to remove the record
    response = post("/api/quality/bulk/postharvest", payload=bulk_deletion_payload)

    print("Bulk delete response:")
    pprint(response)
    print()

    assert not response
    print(f"Confirmed record {bff_postharvest_id} removed by bulk deletion")


# Endpoint: /api/quality/postharvest [OPTIONS, HEAD, GET, POST]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__product_quality__postharvest__options():
    verbs = options("/api/quality/postharvest", "OPTIONS, POST")

    print(f"verbs supported for '/api/quality/postharvest' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__product_quality__postharvest__head():
    pqs_payload = get_postharvest_query_string_payload(TEST_SITE)

    response = head("/api/quality/postharvest", params=pqs_payload)

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__product_quality__postharvest__get(cleanup):
    # create the initial record
    postharvest_dict = generate_postharvest_dict(TEST_FARM)

    print("Postharvest dict:")
    pprint(postharvest_dict)
    print()

    bff_postharvest_record = post("/api/quality/postharvest", postharvest_dict)

    print("BFF Postharvest record:")
    pprint(bff_postharvest_record)
    print()

    bff_postharvest_id = bff_postharvest_record["id"]
    cleanup(lambda: cleanup_test_postharvest(bff_postharvest_id))

    # confirm the record is retrievable via the BFF endpoint
    pqs_payload = get_postharvest_query_string_payload(TEST_FARM)
    bff_postharvest_records = get_json("/api/quality/postharvest", params=pqs_payload)

    # search for the specific record
    found_postharvest_record = None
    for record in bff_postharvest_records["report"]:
        if record["id"] == bff_postharvest_id:
            found_postharvest_record = record
            break

    assert found_postharvest_record is not None
    print(f"Confirmed: postharvest record {bff_postharvest_id} found among all records")
    print()

    print("Found BFF Postharvest record:")
    pprint(found_postharvest_record)
    print()

    # find the common fields among both record representations
    intersection = list(filter(lambda x: x in bff_postharvest_record.keys(), found_postharvest_record.keys()))
    for key in intersection:
        assert found_postharvest_record[key] == bff_postharvest_record[key]
        print(f"Confirmed: {(found_postharvest_record[key] == bff_postharvest_record[key]) = }  [{key}]")
    print()


# @pytest.mark.isolate()
@pytest.mark.post()
def test__product_quality__postharvest__post(cleanup):
    # create the record via the BFF endpoint
    postharvest_dict = generate_postharvest_dict(TEST_FARM)

    print("Postharvest dict:")
    pprint(postharvest_dict)
    print()

    bff_postharvest_record = post("/api/quality/postharvest", postharvest_dict)

    print("BFF Postharvest record:")
    pprint(bff_postharvest_record)
    print()

    bff_postharvest_id = bff_postharvest_record["id"]
    cleanup(lambda: cleanup_test_postharvest(bff_postharvest_id))

    # confirm the record is retrievable via FQS
    pqs_postharvest_record = product_quality_service_client().get_postharvest_qa_by_id(bff_postharvest_id)

    print("FQS Postharvest record:")
    pprint(pqs_postharvest_record)
    print()

    # full object comparison
    assert bff_postharvest_record == pqs_postharvest_record
    print("Confirmed: BFF postharvest record == PQS postharvest record")
    print()


# Endpoint: /api/quality/postharvest/<postharvest_qa_id> [OPTIONS, HEAD, GET, PUT]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__product_quality__postharvest__postharvest_qa_id__options():
    # the OPTIONS check doesn't care about the ID value
    postharvest_qa_id = "FOO"
    verbs = options(f"/api/quality/postharvest/{postharvest_qa_id}", "OPTIONS, PUT")

    print(f"verbs supported for '/api/quality/postharvest/[postharvest_qa_id]' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__product_quality__postharvest__postharvest_qa_id__head(cleanup):
    postharvest_dict = generate_postharvest_dict(TEST_FARM)

    print("Postharvest dict:")
    pprint(postharvest_dict)
    print()

    bff_postharvest_record = post("/api/quality/postharvest", postharvest_dict)

    print("BFF Postharvest record:")
    pprint(bff_postharvest_record)
    print()

    bff_postharvest_id = bff_postharvest_record["id"]
    cleanup(lambda: cleanup_test_postharvest(bff_postharvest_id))

    response = head(f"/api/quality/postharvest/{bff_postharvest_id}")

    pprint(response)
    print()


# @pytest.mark.isolate()
@pytest.mark.get()
def test__product_quality__postharvest__postharvest_qa_id__get(cleanup):
    # create the initial record
    postharvest_dict = generate_postharvest_dict(TEST_FARM)

    print("Postharvest dict:")
    pprint(postharvest_dict)
    print()

    bff_postharvest_record = post("/api/quality/postharvest", postharvest_dict)

    print("BFF Postharvest record:")
    pprint(bff_postharvest_record)
    print()

    bff_postharvest_id = bff_postharvest_record["id"]
    cleanup(lambda: cleanup_test_postharvest(bff_postharvest_id))

    # confirm the record is retrievable by id via the BFF endpoint
    retrieved_postharvest_record = get_json(f"/api/quality/postharvest/{bff_postharvest_id}")

    print("Retrieved Postharvest record:")
    pprint(retrieved_postharvest_record)
    print()

    # find the common fields among both record representations
    intersection = list(filter(lambda x: x in bff_postharvest_record.keys(), retrieved_postharvest_record.keys()))
    for key in intersection:
        assert retrieved_postharvest_record[key] == bff_postharvest_record[key]
        print(f"Confirmed: {(retrieved_postharvest_record[key] == bff_postharvest_record[key]) = }  [{key}]")
    print()


# @pytest.mark.isolate()
@pytest.mark.put()
def test__product_quality__postharvest__postharvest_qa_id__put(cleanup):
    # create the initial record
    # NOTE: the query string says "site" but this requires a *FARM* value!
    postharvest_dict = generate_postharvest_dict(TEST_FARM)

    print("Postharvest dict:")
    pprint(postharvest_dict)
    print()

    bff_postharvest_record = post("/api/quality/postharvest", postharvest_dict)

    print("BFF Postharvest record:")
    pprint(bff_postharvest_record)
    print()

    bff_postharvest_id = bff_postharvest_record["id"]
    cleanup(lambda: cleanup_test_postharvest(bff_postharvest_id))

    # generate a new note to render record change visible
    new_note = get_postharvest_notes()

    # alter the record prior to PUT-ting back into the service
    bff_postharvest_record["notes"] = new_note

    # modify the record via the BFF endpoint
    revised_postharvest_record = put(f"/api/quality/postharvest/{bff_postharvest_id}", bff_postharvest_record)

    print("Revised Postharvest record:")
    pprint(revised_postharvest_record)
    print()

    # confirm the alteration
    assert revised_postharvest_record["notes"] == new_note
    print("Confirmed 'notes' field changed")

    assert revised_postharvest_record["id"] == bff_postharvest_record["id"]
    print("Confirmed that this is a single, changed record")
    print()


# Endpoint: /api/quality/sensory/events [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__product_quality__sensory__events__options():
    verbs = options("/api/quality/sensory/events", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/quality/sensory/events' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__product_quality__sensory__events__head():
    # This endpoint requires a querystring in the form:
    #     ?site=SSF1&startDate=2022-09-19&endDate=2022-09-19
    # This test also requires existing data for a target site
    # within the target interval.

    qs_payload = get_postharvest_query_string_payload(TEST_SITE)

    response = head("/api/quality/sensory/events", params=qs_payload)

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__product_quality__sensory__events__get(cleanup):
    # create a sensory event via PQS
    sensory_event_dict = generate_sensory_event_dict(TEST_FARM)

    print("Sensory Event dictionary:")
    pprint(sensory_event_dict)
    print()

    pqs_sensory_event = create_sensory_event(sensory_event_dict)

    print("PQS Sensory Event:")
    pprint(pqs_sensory_event)
    print()

    pqs_sensory_event_id = pqs_sensory_event["id"]
    cleanup(lambda: cleanup_test_sensory_event(pqs_sensory_event_id))

    # get sensory events for the farm & time interval intersection
    pqs_payload = get_postharvest_query_string_payload(TEST_FARM)
    bff_sensory_event_records = get_json("/api/quality/sensory/events", params=pqs_payload)

    # isolate the specific event by id
    bff_sensory_event = None

    for record in bff_sensory_event_records["report"]:
        if record["id"] == pqs_sensory_event_id:
            bff_sensory_event = record
            break

    assert bff_sensory_event is not None
    print("Confirmed target event among retrieved events")
    print()

    print("BFF Sensory Event:")
    pprint(bff_sensory_event)
    print()

    # find the common fields among both record representations
    intersection = list(filter(lambda x: x in bff_sensory_event.keys(), pqs_sensory_event.keys()))
    for key in intersection:
        assert pqs_sensory_event[key] == bff_sensory_event[key]
        print(f"Confirmed: {(pqs_sensory_event[key] == bff_sensory_event[key]) = }  [{key}]")
    print()


# Endpoint: /api/quality/sensory/events/<event_id>/ratings [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__product_quality__sensory__events__event_id__ratings__options():
    # TODO create a record; get and pass ID value
    event_id = "FOO"
    verbs = options(f"/api/quality/sensory/events/{event_id}/ratings", "OPTIONS, POST")

    print(f"verbs supported for '/api/quality/sensory/events/[event_id]/ratings' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.post()
def test__product_quality__sensory__events__event_id__ratings__post(cleanup):
    # create a sensory event via PQS
    sensory_event_dict = generate_sensory_event_dict(TEST_FARM)

    print("Sensory Event dictionary:")
    pprint(sensory_event_dict)
    print()

    pqs_sensory_event = create_sensory_event(sensory_event_dict)

    print("PQS Sensory Event:")
    pprint(pqs_sensory_event)
    print()

    sensory_event_id = pqs_sensory_event["id"]
    cleanup(lambda: cleanup_test_sensory_event(sensory_event_id))

    sensory_event_cultivar = pqs_sensory_event["cultivar"]

    sensory_rating_dict = generate_sensory_rating_dict(cultivar=sensory_event_cultivar)

    print("Sensory Rating dictionary:")
    pprint(sensory_rating_dict)
    print()

    # post the payload to get the sensory rating
    bff_sensory_rating = post(f"/api/quality/sensory/events/{sensory_event_id}/ratings", payload=sensory_rating_dict)

    print("BFF Sensory Rating:")
    pprint(bff_sensory_rating)
    print()

    sensory_rating_id = bff_sensory_rating["id"]
    cleanup(lambda: cleanup_test_sensory_rating(sensory_rating_id))

    bff_flavor_notes = bff_sensory_rating["dodFlavorNotes"]

    for flavor, rating in sensory_rating_dict.items():
        # the flavor key above is in the form: "flavor-FRESHCUTGRASS-4-LOW"
        flavor_key = flavor.split("-")[1]
        assert bff_flavor_notes[flavor_key]["userSelection"] == rating
        print(f"Confirmed rating match for {flavor}")
    print()


# Endpoint: /api/quality/sensory/ratings [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.options()
def test__product_quality__sensory__ratings__options():
    verbs = options("/api/quality/sensory/ratings", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/quality/sensory/ratings' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.head()
def test__product_quality__sensory__ratings__head():
    # NOTE: This endpoint requires a querystring in the form:
    #     ?site=SSF1&startDate=2022-09-19&endDate=2022-09-19

    qs_payload = get_postharvest_query_string_payload(TEST_SITE)

    response = head("/api/quality/sensory/ratings", params=qs_payload)

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.get()
def test__product_quality__sensory__ratings__get(cleanup):
    # create a sensory event via PQS
    sensory_event_dict = generate_sensory_event_dict(TEST_FARM)

    print("Sensory Event dictionary:")
    pprint(sensory_event_dict)
    print()

    pqs_sensory_event = create_sensory_event(sensory_event_dict)

    print("PQS Sensory Event:")
    pprint(pqs_sensory_event)
    print()

    sensory_event_id = pqs_sensory_event["id"]
    cleanup(lambda: cleanup_test_sensory_event(sensory_event_id))

    sensory_event_cultivar = pqs_sensory_event["cultivar"]

    sensory_rating_dict = generate_sensory_rating_dict(cultivar=sensory_event_cultivar)

    print("Sensory Rating dictionary:")
    pprint(sensory_rating_dict)
    print()

    # post the payload to get the sensory rating
    bff_sensory_rating = post(f"/api/quality/sensory/events/{sensory_event_id}/ratings", payload=sensory_rating_dict)

    print("BFF Sensory Rating:")
    pprint(bff_sensory_rating)
    print()

    sensory_rating_id = bff_sensory_rating["id"]
    cleanup(lambda: cleanup_test_sensory_rating(sensory_rating_id))

    # retrieve the sensory rating via BFF
    pqs_payload = get_postharvest_query_string_payload(TEST_FARM)
    bff_sensory_event_records = get_json("/api/quality/sensory/ratings", params=pqs_payload)

    # find the target rating among the returned report
    found_sensory_rating = None
    for record in bff_sensory_event_records["report"]:
        if record["id"] == sensory_rating_id:
            found_sensory_rating = record

    assert found_sensory_rating is not None
    print("Confirmed: target rating found in retrieved ratings")
    print()

    print("Found Sensory Rating:")
    pprint(found_sensory_rating)
    print()

    # find the common fields among both record representations
    intersection = list(filter(lambda x: x in bff_sensory_rating.keys(), found_sensory_rating.keys()))
    for key in intersection:
        assert found_sensory_rating[key] == bff_sensory_rating[key]
        print(f"Confirmed: {(found_sensory_rating[key] == bff_sensory_rating[key]) = }  [{key}]")
    print()
