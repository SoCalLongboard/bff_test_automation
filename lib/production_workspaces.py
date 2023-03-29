# Standard library imports
from random import choice, sample

# Project library imports
from lib.clients import get_json, get_automation_username
from lib.utils import rand_char_str, get_sample_range

DEFAULT_FARM = "sites/LAX1/farms/LAX1"
DEFAULT_PRIORITY = "REGULAR"
DEFAULT_STATUS = "COMPLETED"

SAMPLE_FLOOR = 2
SAMPLE_CEILING = 6


def _get_workspace_roles():
    workspace_role_list = get_json("/api/production/workspaces")

    workspace_role_names = [record["role"] for record in workspace_role_list]

    return workspace_role_names


def _get_workplace_roles_sample(floor, ceiling):
    # pick a random integer (sample size) within a specified range
    span = get_sample_range(floor, ceiling)
    sample_size = choice(span)

    workplace_roles_sample = sample(_get_workspace_roles(), sample_size)

    return workplace_roles_sample


def get_new_workbin_task_definition():
    title_identifier = rand_char_str(8)

    return {
        "farm": DEFAULT_FARM,
        "priority": DEFAULT_PRIORITY,
        "shortTitle": f"Short WBT def {title_identifier}",
        "title": f"Full WBT def {title_identifier}",
        "workbins": _get_workplace_roles_sample(SAMPLE_FLOOR, SAMPLE_CEILING),
    }


def get_new_workbin_instance_payload(workbin_task_definition):
    username = get_automation_username()

    return {
        "completer": username,
        "resultForPassFailCheck": False,
        "status": DEFAULT_STATUS,
        "workbin": choice(workbin_task_definition["workbins"]),
        "workbinTaskDefinitionId": workbin_task_definition["id"],
    }


def get_site_farm_from_farm_def_path(path):
    split_path = path.split("/")

    return split_path[1], split_path[3]  # site, farm, respectively
