# Standard library imports
from pprint import pprint

# 3rd party library imports
import pytest

# Project library imports
from lib.clients import (
    executive_service_client,
    farm_def_service_client,
    get_json,
    head,
    options,
    post,
)
from lib.production_workcenters import get_task_record


# Endpoint: /api/production/workcenters [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.options()
def test__production__workcenters__options():
    verbs = options("/api/production/workcenters", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/production/workcenters' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.head()
def test__production__workcenters__head():
    response = head("/api/production/workcenters")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.get()
def test__production__workcenters__get():
    # get ALL workcenters via BFF
    bff_workcenters = get_json("/api/production/workcenters")

    print("BFF workcenters:")
    pprint(bff_workcenters)
    print()

    bff_current_user_farm_def_path = get_json("/api/core/current-user")["currentFarmDefPath"]
    bff_current_site = bff_current_user_farm_def_path.split("/")[1]
    bff_current_farm = bff_current_user_farm_def_path.split("/")[3]

    print(f"BFF user -- current farm-def path: {bff_current_user_farm_def_path}")
    print()

    # get the full site tree for the same site/farm
    fds_site_tree = farm_def_service_client().get_object_by_path_v2(bff_current_user_farm_def_path)

    print("FDS site tree (same farm-def path):")
    pprint(fds_site_tree)
    print()

    assert fds_site_tree["name"] == bff_current_farm
    print(f"Confirmed: {(fds_site_tree['name'] == bff_current_farm) = }")

    assert fds_site_tree["path"] == bff_current_user_farm_def_path
    print(f"Confirmed: {(fds_site_tree['path'] == bff_current_user_farm_def_path) = }")

    bff_parent_path = f"sites/{bff_current_site}"
    assert fds_site_tree["parentPath"] == bff_parent_path
    print(f"Confirmed: {(fds_site_tree['parentPath'] == bff_parent_path) = }")
    print()

    # compare BFF and FDS workcenter expressions
    for bff_workcenter in bff_workcenters:
        workcenter = bff_workcenter["name"]
        workcenter_display_name = bff_workcenter["displayName"]

        assert fds_site_tree["workCenters"][workcenter]["name"] == workcenter
        print(f"Confirmed: {(fds_site_tree['workCenters'][workcenter]['name'] == workcenter) = }")

        assert fds_site_tree["workCenters"][workcenter]["displayName"] == workcenter_display_name
        print(f"Confirmed: {(fds_site_tree['workCenters'][workcenter]['displayName'] == workcenter_display_name) = }")

        assert fds_site_tree["workCenters"][workcenter]["parentPath"] == bff_current_user_farm_def_path
        print(
            f"Confirmed: {(fds_site_tree['workCenters'][workcenter]['parentPath'] == bff_current_user_farm_def_path) = }"
        )

        bff_workcenter_path = f"{bff_current_user_farm_def_path}/workCenters/{workcenter}"
        assert fds_site_tree["workCenters"][workcenter]["path"] == bff_workcenter_path
        print(f"Confirmed: {(fds_site_tree['workCenters'][workcenter]['path'] == bff_workcenter_path) = }")


# Endpoint: /api/production/workcenters/<workcenter_name> [OPTIONS, HEAD, GET]
WORKCENTER_NAME = "Transplant"


# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.options()
def test__production__workcenters__get_workcenter_by_name__options():
    verbs = options(f"/api/production/workcenters/{WORKCENTER_NAME}", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/production/workcenters/[workcenter-name]' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.head()
def test__production__workcenters__get_workcenter_by_name__head():
    response = head(f"/api/production/workcenters/{WORKCENTER_NAME}")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.get()
def test__production__workcenters__get_workcenter_by_name__get():
    # get a SPECIFIC workcenter via BFF
    bff_workcenter = get_json(f"/api/production/workcenters/{WORKCENTER_NAME}")

    print(f"BFF workcenter [{WORKCENTER_NAME}]:")
    pprint(bff_workcenter)
    print()

    bff_current_user_farm_def_path = get_json("/api/core/current-user")["currentFarmDefPath"]
    bff_current_site = bff_current_user_farm_def_path.split("/")[1]
    bff_current_farm = bff_current_user_farm_def_path.split("/")[3]

    print(f"BFF user -- current farm-def path: {bff_current_user_farm_def_path}")
    print()

    # get the full site tree for the same site/farm
    fds_site_tree = farm_def_service_client().get_object_by_path_v2(bff_current_user_farm_def_path)

    assert fds_site_tree["name"] == bff_current_farm
    print(f"Confirmed: {(fds_site_tree['name'] == bff_current_farm) = }")

    assert fds_site_tree["path"] == bff_current_user_farm_def_path
    print(f"Confirmed: {(fds_site_tree['path'] == bff_current_user_farm_def_path) = }")

    bff_parent_path = f"sites/{bff_current_site}"
    assert fds_site_tree["parentPath"] == bff_parent_path
    print(f"Confirmed: {(fds_site_tree['parentPath'] == bff_parent_path) = }")
    print()

    # isolate the same workcenter from the FDS-derived site tree
    fds_workcenter = fds_site_tree["workCenters"][WORKCENTER_NAME]

    print(f"FDS workcenter [{WORKCENTER_NAME}]:")
    pprint(fds_workcenter)
    print()

    # compare BFF and FDS workcenter expressions
    assert fds_workcenter["name"] == fds_workcenter["name"]
    print(f"Confirmed: {(fds_workcenter['name'] == fds_workcenter['name']) = }")

    assert fds_workcenter["displayName"] == fds_workcenter["displayName"]
    print(f"Confirmed: {(fds_workcenter['displayName'] == fds_workcenter['displayName']) = }")

    assert fds_workcenter["kind"] == "workCenter"
    print(f"Confirmed: {(fds_workcenter['kind'] == 'workCenter') = }")

    assert fds_workcenter["path"] == fds_workcenter["path"]
    print(f"Confirmed: {(fds_workcenter['path'] == fds_workcenter['path']) = }")


# Endpoint: /api/production/workcenters/create-task [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.executive_service()
@pytest.mark.options()
def test__production__workcenters__create_task__options():
    verbs = options("/api/production/workcenters/create-task", "OPTIONS, POST")

    print(f"verbs supported for '/api/production/workcenters/create-task' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.executive_service()
@pytest.mark.post()
def test__production__workcenters__create_task__post():
    task_record = get_task_record()

    print("Task record:")
    pprint(task_record)
    print()

    bff_task = post("/api/production/workcenters/create-task", task_record)

    print("BFF task:")
    pprint(bff_task)
    print()

    # Get the workcenter plan for the same workcenter/date
    planned_date = task_record["plannedDate"]
    workcenter = task_record["workcenter"]

    es_plan = executive_service_client().get_workcenter_plan(planned_date=planned_date, workcenter=workcenter)

    print("ES plan:")
    pprint(es_plan)
    print()

    assert bff_task["executionDetails"] == es_plan["detailsOfTasksFromPlan"][0]["executionDetails"]
    assert bff_task["taskDetails"] == es_plan["detailsOfTasksFromPlan"][0]["taskDetails"]
