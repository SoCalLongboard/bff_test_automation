# Standard library imports
from datetime import date, timedelta
from random import choice

# Project library imports
from lib.clients import product_quality_service_client, get_automation_username

from lib.utils import rand_num_str, rand_char_str


def get_postharvest_query_string_payload(site):
    # This function should return a dict with these fields:
    #       site        :   SSF2 or LAX1 (for now)
    #       startDate   :   YYYY-MM-DD (yesterday in ISO-8601 form)
    #       endDate     :   YYYY-MM-DD (tomorrow in ISO-8601 form)

    one_day = timedelta(days=1)

    today = date.today()
    yesterday = (today - one_day).isoformat()
    tomorrow = (today + one_day).isoformat()

    return {
        "site": site,
        "startDate": yesterday,
        "endDate": tomorrow,
    }


def _get_postharvest_cultivar():
    cultivars = [
        "BAC",
        "CRC",
        "WHC",
        "SP2",
        "PPS",
    ]

    return choice(cultivars)


def get_postharvest_notes():
    # prefix used to make BFFTEST records easier to identify
    return f"BFFTEST {rand_char_str(12)}"


def _get_postharvest_purpose():
    purposes = [
        "N/A",
        "Internal Use",
        "Shelf Life",
        "Ops Research",
    ]

    return choice(purposes)


def _get_postharvest_sample_number():
    # prefix used to make BFFTEST records easier to identify
    # Valid range: -2147483648 <= x <= 2147483647
    sample_number_prefix = "9090"
    sample_number_suffix = rand_num_str(4)

    return int(f"{sample_number_prefix}{sample_number_suffix}")


def _get_postharvest_type_of_cut():
    types_of_cut = [
        "Automated Harvester",
        "Manual",
    ]

    return choice(types_of_cut)


def _get_postharvest_units():
    units = [
        "grams",
        "ounces",
    ]

    return choice(units)


def generate_postharvest_dict(farm):

    return {
        "cultivar": _get_postharvest_cultivar(),
        "evaluationDate": date.today().isoformat(),
        "harvestDate": date.today().isoformat(),
        "harvestLocation": farm,
        "notes": get_postharvest_notes(),
        "purpose": _get_postharvest_purpose(),
        "sampleNumber": _get_postharvest_sample_number(),
        "typeOfCut": _get_postharvest_type_of_cut(),
        "units": _get_postharvest_units(),
    }


def get_bulk_deletion_payload(ids):
    """

    :param ids: id values for postharvest records to delete
    :type ids: list

    :return: a bulk deletion payload structure
    :rtype: dict
    """
    deletes = []
    for id_value in ids:
        deletes.append({"primaryValue": str(id_value)})

    return {
        "dataset": "qa",
        "deletes": deletes,
        "updates": [],
    }


# NOTE: this routine assumes that the record exists...
def cleanup_test_postharvest(postharvest_id):
    print(f"Deleting postharvest test record: {postharvest_id}")
    product_quality_service_client().delete_postharvest_qa(postharvest_id)


def generate_sensory_event_dict(site):
    return {
        "cultivar": _get_postharvest_cultivar(),
        "harvestDate": date.today().isoformat(),
        "testDate": date.today().isoformat(),
        "serial": get_postharvest_notes(),
        "site": site,
        "username": get_automation_username(),
    }


def create_sensory_event(sensory_event_dict):
    sensory_event = product_quality_service_client().create_sensory_event(sensory_event_dict)

    return sensory_event


def cleanup_test_sensory_event(sensory_event_id):
    print(f"Deleting postharvest test record: {sensory_event_id}")
    product_quality_service_client().delete_sensory_event(sensory_event_id)


def _get_flavor_presence():
    options = [
        "Present",
        "Absent",
    ]

    return choice(options)


def _get_flavor_keys_by_cultivar(cultivar):
    cultivars = {
        "SP2": [
            "flavor-SWEET-4-LOW",
            "flavor-FRESHCUTGRASS-6-MEDIUM",
            "flavor-BROCCOLI/SPICE-6-MEDIUM",
            "flavor-BITTER-4-LOW",
        ],
        "E31": [
            "flavor-SWEET-4-LOW",
            "flavor-FRESHCUTGRASS-6-MEDIUM",
            "flavor-BROCCOLI/SPICE-6-MEDIUM",
            "flavor-BITTER-4-LOW",
        ],
        "WHC": [
            "flavor-SWEET-4-LOW",
            "flavor-FRESHCUTGRASS-6-MEDIUM",
            "flavor-BROCCOLI/SPICE-6-MEDIUM",
            "flavor-BITTER-4-LOW",
        ],
        "CRC": [
            "flavor-SWEET-4-LOW",
            "flavor-FRESHCUTGRASS-4-LOW",
            "flavor-SPICE-10-HIGH",
            "flavor-BITTER-10-HIGH",
        ],
        "BAC": [
            "flavor-SWEET-4-LOW",
            "flavor-FRESHCUTGRASS-4-LOW",
            "flavor-SPICE-10-HIGH",
            "flavor-BITTER-10-HIGH",
        ],
        "PPS": [
            "flavor-SWEET-4-LOW",
            "flavor-SOUR-4-LOW",
            "flavor-DAMPCUTGRASS-6-MEDIUM",
            "flavor-EARTHY-6-MEDIUM",
            "flavor-UMAMI-4-LOW",
        ],
    }

    return cultivars[cultivar]


def generate_sensory_rating_dict(cultivar):
    sensory_rating_dict = {}
    for flavor_key in _get_flavor_keys_by_cultivar(cultivar):
        sensory_rating_dict[flavor_key] = _get_flavor_presence()

    return sensory_rating_dict


def cleanup_test_sensory_rating(sensory_rating_id):
    print(f"Deleting postharvest test record: {sensory_rating_id}")
    product_quality_service_client().delete_sensory_rating(sensory_rating_id)
