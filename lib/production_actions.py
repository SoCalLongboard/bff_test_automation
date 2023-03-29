# Standard library imports
from typing import Dict, List

# 3rd party library imports
from inflection import titleize

# Project library imports
from lib.clients import farm_def_service_client

METHOD_TYPES = ["request", "tell"]

"""
NOTE: This code is a nearly verbatim copy of the production actions handling under:

https://github.com/PlentyAg/Sprout/tree/master/server/sprout/api/production/actions

Tweaks are largely limited to skipping Flask-based jsonification. 
"""


def get_all_actions_for_site(site, farm):
    """
    Returns all tells/requests that are associated with given site and farm.

    returns array containing each tell/request "name", "description", FD "path" and type: tell/request.

    query args:
    tells: get all tells
    requests: get all requests
    ex: ?method-types[]=tell&method-types[]=requests --> gets both tells and requests.

    :return: json array of
    {
     "name": string
     "description": string
     "path": string
     "type": string - 'tell' or 'request'
    }
    """
    return _get_actions_for_site_and_farm(site, farm)


def _get_actions_in_farm_def_obj(farm_def_obj: Dict):
    """
    For given farm def object, see if it has "interfaces" field. if it does then
    pull out matching method types (ex: tell or request).
    """
    actions = []

    # ToDo: need to determine if ok to filter these
    if farm_def_obj.get("kind") == "deviceLocation":
        return actions

    for interface in farm_def_obj.get("interfaces", {}).values():
        for method in interface.get("methods", {}).values():
            if method.get("type") in METHOD_TYPES:
                actions.append(
                    {
                        "name": titleize(method.get("name")),
                        "description": method.get("description"),
                        "path": method.get("path"),
                        "type": method.get("type"),
                    }
                )
    return actions


def _get_all_actions_under_farm_def_obj(farm_def_obj: Dict):
    """
    Recursively digs through given farm_def_obj looking for actions with matching method_types.
    """
    if not isinstance(farm_def_obj, dict):
        return []

    actions = _get_actions_in_farm_def_obj(farm_def_obj)

    for key, value in farm_def_obj.items():
        if isinstance(value, dict) and not key == "interfaces":
            actions += _get_all_actions_under_farm_def_obj(value)

    return actions


def _get_actions_for_site_and_farm(site: str, farm: str):
    """
    Returns all actions (w/ given method_types: tell or request) that are associated with given site and farm.

    site: farm def site name
    farm: farm def farm name
    method_types: array of method types should be searched for (ex: [ 'tell', 'request' ])

    :return: json array of
    {
     "name": string
     "description": string
     "path": string
     "type": string - 'tell' or 'request'
    }
    """
    site_obj = farm_def_service_client().get_object_by_path_v2(f"sites/{site}")

    farm_obj = site_obj.get("farms", {}).get(farm, {})
    # the mappings object indicates which "areas" are used by this farm.
    mappings = farm_obj.get("mappings", [])
    objs_ids_in_farm_mapping = [mapping.get("to", "") for mapping in mappings]

    # get the actions in the root of the site.
    actions = _get_actions_in_farm_def_obj(site_obj)

    # get actions in each "area" associated with the given farm.
    all_areas = site_obj.get("areas", {})
    for area_obj in all_areas.values():
        if area_obj.get("id") in objs_ids_in_farm_mapping:
            actions += _get_all_actions_under_farm_def_obj(area_obj)

    return actions
