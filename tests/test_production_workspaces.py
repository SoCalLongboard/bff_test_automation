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
    post,
    put,
    workbin_service_client,
)
from lib.production_workspaces import (
    get_new_workbin_instance_payload,
    get_new_workbin_task_definition,
    get_site_farm_from_farm_def_path,
)


# Endpoint: /api/production/workspaces [OPTIONS, HEAD, GET]
# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.options()
def test__production__workspaces__options():
    verbs = options("/api/production/workspaces", "OPTIONS, HEAD, GET")

    print(f"verbs supported for '/api/production/workspaces' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.head()
def test__production__workspaces__head():
    response = head("/api/production/workspaces")

    pprint(response)


# @pytest.mark.isolate()
@pytest.mark.farm_def_service()
@pytest.mark.get()
def test__production__workspaces__get():
    # get ALL workspaces via BFF
    bff_workspaces = get_json("/api/production/workspaces")

    print("BFF workspaces:")
    pprint(bff_workspaces)
    print()

    bff_current_user_farm_def_path = get_json("/api/core/current-user")["currentFarmDefPath"]

    bff_current_site, bff_current_farm = get_site_farm_from_farm_def_path(bff_current_user_farm_def_path)

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

    # compare BFF and FDS workspace expressions
    for bff_workspace in bff_workspaces:
        role = bff_workspace["role"]
        role_display_name = bff_workspace["roleDisplayName"]

        assert fds_site_tree["roles"][role]["name"] == role
        print(f"Confirmed: {(fds_site_tree['roles'][role]['name'] == role) = }")

        assert fds_site_tree["roles"][role]["displayName"] == role_display_name
        print(f"Confirmed: {(fds_site_tree['roles'][role]['displayName'] == role_display_name) = }")

        assert fds_site_tree["roles"][role]["kind"] == "role"
        print(f"Confirmed: {(fds_site_tree['roles'][role]['kind'] == 'role') = }")

        assert fds_site_tree["roles"][role]["parentPath"] == bff_current_user_farm_def_path
        print(f"Confirmed: {(fds_site_tree['roles'][role]['parentPath'] == bff_current_user_farm_def_path) = }")

        bff_role = f"{bff_current_user_farm_def_path}/roles/{role}"
        assert fds_site_tree["roles"][role]["path"] == bff_role
        print(f"Confirmed: {(fds_site_tree['roles'][role]['path'] == bff_role) = }")


# Endpoint: /api/production/workspaces/create-workbin-instance [OPTIONS, POST]
# @pytest.mark.isolate()
@pytest.mark.executive_service()
@pytest.mark.options()
def test__production__workspaces__create_workbin_instance__options():
    verbs = options("/api/production/workspaces/create-workbin-instance", "OPTIONS, POST")

    print(f"verbs supported for '/api/production/workspaces/create-workbin-instance' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.executive_service()
@pytest.mark.post()
def test__production__workspaces__create_workbin_instance__post():
    task_definition = get_new_workbin_task_definition()

    print("New workbin task definition:")
    pprint(task_definition)
    print()

    bff_workbin_task_definition = post(
        "/api/plentyservice/workbin-service/upsert-workbin-task-definition",
        task_definition,
    )

    print("BFF Workbin Task Definition:")
    pprint(bff_workbin_task_definition)
    print()

    workbin_task_definition_id = bff_workbin_task_definition["id"]
    print(f"{workbin_task_definition_id = }")
    print()

    # validate workbin_task_definition via workbin_service
    wbs_workbin_task_definition = workbin_service_client().get_workbin_task_definition_by_id(workbin_task_definition_id)

    print("WBS Workbin Task Definition:")
    pprint(wbs_workbin_task_definition)
    print()

    # perform object-to-object comparison of workbin task definitions
    assert bff_workbin_task_definition == wbs_workbin_task_definition
    print(f"Confirmed: bff_workbin_task_definition == wbs_workbin_task_definition")
    print()

    bff_workbin_instance_payload = get_new_workbin_instance_payload(bff_workbin_task_definition)

    print("New workbin instance payload:")
    pprint(bff_workbin_instance_payload)
    print()

    bff_workbin_instance = post("/api/production/workspaces/create-workbin-instance", bff_workbin_instance_payload)

    print("BFF Workbin Instance:")
    pprint(bff_workbin_instance)
    print()

    workbin_instance_id = bff_workbin_instance["id"]
    print(f"{workbin_instance_id = }")
    print()

    wbs_workbin_instance_response = workbin_service_client().get_workbin_task_instance_by_id(workbin_instance_id)
    wbs_workbin_instance = wbs_workbin_instance_response["workbinTaskInstance"]

    print("WBS Workbin Instance:")
    pprint(wbs_workbin_instance)
    print()

    validation_fields = [
        "completer",
        "id",
        "resultForPassFailCheck",
        "status",
        "values",
        "workbin",
        "workbinTaskDefinitionId",
    ]

    # perform field-based comparison of workbin instances
    for field in validation_fields:
        assert bff_workbin_instance[field] == wbs_workbin_instance[field]
        print(f"Confirmed: bff_workbin_instance[{field}] == wbs_workbin_instance[{field}]")


# Endpoint: /api/production/workspaces/update-workbin-instance [OPTIONS, PUT]
# @pytest.mark.isolate()
@pytest.mark.executive_service()
@pytest.mark.options()
def test__production__workspaces__update_workbin_instance__options():
    verbs = options("/api/production/workspaces/update-workbin-instance", "OPTIONS, PUT")

    print(f"verbs supported for '/api/production/workspaces/update-workbin-instance' : {verbs}")


# @pytest.mark.isolate()
@pytest.mark.executive_service()
@pytest.mark.put()
def test__production__workspaces__update_workbin_instance__put():
    # First, create a new workbin instance
    task_definition = get_new_workbin_task_definition()

    print("New workbin task definition:")
    pprint(task_definition)
    print()

    bff_workbin_task_definition = post(
        "/api/plentyservice/workbin-service/upsert-workbin-task-definition",
        task_definition,
    )

    print("BFF Workbin Task Definition:")
    pprint(bff_workbin_task_definition)
    print()

    workbin_task_definition_id = bff_workbin_task_definition["id"]
    print(f"{workbin_task_definition_id = }")
    print()

    bff_workbin_instance_payload = get_new_workbin_instance_payload(bff_workbin_task_definition)

    print("Original workbin instance payload:")
    pprint(bff_workbin_instance_payload)
    print()

    bff_workbin_instance = post("/api/production/workspaces/create-workbin-instance", bff_workbin_instance_payload)

    print("Original BFF Workbin Instance:")
    pprint(bff_workbin_instance)
    print()

    workbin_instance_id = bff_workbin_instance["id"]
    print(f"{workbin_instance_id = }")
    print()

    # Next PUT a change to the existing workbin instance
    new_workbin_instance_payload = get_new_workbin_instance_payload(bff_workbin_task_definition)

    print("Update workbin instance payload:")
    new_workbin_instance_payload["workbinTaskInstanceId"] = workbin_instance_id
    new_workbin_instance_payload["status"] = "SKIPPED"
    new_workbin_instance_payload["comment"] = "added description..."
    pprint(new_workbin_instance_payload)
    print()

    bff_workbin_instance = put("/api/production/workspaces/update-workbin-instance", new_workbin_instance_payload)

    print("Updated BFF Workbin Instance:")
    pprint(bff_workbin_instance)
    print()

    # Finally, confirm the change made by the PUT operation
    workbin_instance_id = bff_workbin_instance["id"]
    print(f"{workbin_instance_id = }")
    print()

    wbs_workbin_instance_response = workbin_service_client().get_workbin_task_instance_by_id(workbin_instance_id)
    wbs_workbin_instance = wbs_workbin_instance_response["workbinTaskInstance"]

    print("WBS Workbin Instance:")
    pprint(wbs_workbin_instance)
    print()

    validation_fields = [
        "completer",
        "id",
        "resultForPassFailCheck",
        "status",
        "values",
        "workbin",
        "workbinTaskDefinitionId",
    ]

    # perform field-based comparison of workbin instances
    for field in validation_fields:
        assert bff_workbin_instance[field] == wbs_workbin_instance[field]
        print(f"Confirmed: bff_workbin_instance[{field}] == wbs_workbin_instance[{field}]")
