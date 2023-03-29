# Standard library imports
from datetime import (
    datetime,
    timedelta,
    timezone,
)
from pprint import pprint
from random import choice

# Project library imports
from lib.clients import (
    device_management_service_client,
    perception_object_service_client,
)
from lib.utils import rand_char_str


def _get_random_content_type():
    content_types = [
        "gif",
        "jpg",
        "png",
    ]

    return choice(content_types)


def _get_random_site():
    sites = [
        "LAR1",
        "SSF2",
    ]

    return choice(sites)


def _get_random_area():
    areas = [
        "Propagation",
        "VerticalGrow",
    ]

    return choice(areas)


def _generate_minimal_perception_object_payload(device_serial):
    return {
        "contentType": _get_random_content_type(),
        "site": _get_random_site(),
        "area": _get_random_area(),
        "devices": [{"deviceSerial": device_serial}],
    }


def _get_randomly_chosen_device():
    site = _get_random_site()
    devices = device_management_service_client().query_by_loc(site)["devices"]

    return choice(devices)


def generate_perception_object():
    device = _get_randomly_chosen_device()

    print("Test device:")
    pprint(device)
    print()

    return perception_object_service_client().ingest_object(
        _generate_minimal_perception_object_payload(device["serial"])
    )


def get_search_date_interval_payload(uuid):
    """
    Return the query string keys and timestamps in ISO 8601 format
    for isolating a 48-hour search window.

    Also include the passed UUID in the dict.
    """
    one_day = timedelta(days=1)
    now = datetime.now(timezone.utc)

    now_minus_24h = now - one_day
    now_plus_24h = now + one_day

    return {
        "uuid": uuid,
        "dt_utc__gte": now_minus_24h.isoformat(),
        "dt_utc__lte": now_plus_24h.isoformat(),
    }


# tag generation
def _get_random_tag():
    return f"BFFTEST tag {rand_char_str(10)}"


def get_add_tag_payload(uuid):

    return {
        "uuid": uuid,
        "tag": _get_random_tag(),
    }


# label generation
def _get_label_set_name():
    return f"BFFTEST Label Set {rand_char_str(10)}"


def _get_is_ground_truth():
    return choice([True, False])


def _get_labeler_type():
    return "+ labeler type +"


def _get_labeler_id():
    return "+ labeler id +"


def _generate_label(index):
    return {
        "label": f"BFFTEST Label {index}",
        "probabilityScore": "",
        "scope": "+ scope +",
        "geometryPoints": [[], [], []],
        "metadata": {},
    }


def _generate_label_list(label_count):
    labels = []

    for i in range(label_count):
        labels.append(_generate_label(i))

    return labels


def get_add_label_set_payload(label_count=3):
    return {
        "name": _get_label_set_name(),
        "isGroundTruth": _get_is_ground_truth(),
        "labelerType": _get_labeler_type(),
        "labelerId": _get_labeler_id(),
        "labels": _generate_label_list(label_count),
    }
