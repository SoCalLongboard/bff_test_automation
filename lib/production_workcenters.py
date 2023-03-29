# Standard library imports
from datetime import date
import json

GROW_LANE_VALUE = "sites/LAX1/areas/VerticalGrow/lines/GrowRoom1/machines/GrowLine1/containerLocations/A0"
GROW_LINE_OPERATION_MODE_VALUE = "ONE_IN_ONE_OUT"
TASK_PATH = "sites/LAX1/farms/LAX1/workCenters/Transplant/interfaces/Transplant/methods/LoadEmptiesToVerticalGrow"
WORKCENTER = "sites/LAX1/farms/LAX1/workCenters/Transplant"


def _get_planned_date():
    return date.today().isoformat()


def _get_task_parameter_json_payload():
    task = {
        "tower_count": 3,
        "grow_lane": {"value": GROW_LANE_VALUE},
        "grow_line_operation_mode": {"value": GROW_LINE_OPERATION_MODE_VALUE},
    }

    return json.dumps(task)


def get_task_record():
    return {
        "workcenter": WORKCENTER,
        "plannedDate": _get_planned_date(),
        "taskPath": TASK_PATH,
        "taskParametersJsonPayload": _get_task_parameter_json_payload(),
    }
