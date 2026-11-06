from datetime import datetime
from uuid import UUID

from models.data import Realm, Setting, Context, ParametersResponse, Parameter, ContextResidency, DriveResult, Rule, \
    Device
from models.trim_history import SettingChange, TrimRecord


def realm_from_dict(data: dict) -> Realm:
        return Realm(
            name=data["name"],
            abbreviation=data["abbreviation"],
            description=data["description"],
        )

def rule_from_dict(data: dict) -> Rule:
    return Rule(
            type=data["type"],
            input_parameters=data["input_parameters"],
            output_parameters=data["output_parameters"],
            )

def context_from_dict(data: dict) -> Context:
    return Context(
        id=UUID(data["id"]),
        name=data["name"],
        realm=data["realm"],
        resident=bool(data["resident"]),
    )

def context_residency_from_dict(data: dict) -> ContextResidency:
    return ContextResidency(
        id=UUID(data["id"]),
        context_name=data["context_name"],
        context_id=UUID(data["context_id"]),
        realm=data["realm"],
        timestamp=datetime.fromisoformat(
            data["timestamp"].replace("Z", "+00:00")
        ),
        event=data["event"],
    )


def setting_from_dict(data: dict) -> Setting:
    return Setting(
        parameter_name=data["parameter_name"],
        value=data["value"],
        last_updated=datetime.fromisoformat(
            data["last_updated"].replace("Z", "+00:00")
        )
    )

def parameter_response_from_dict(data: dict) -> ParametersResponse:
    return ParametersResponse(
        parameters=[
            Parameter(**parameter)
            for parameter in data["parameters"]
        ],
        total=data["total"],
        page=data.get("page"),
        size=data.get("size"),
    )

def drive_result_from_dict(data: dict) -> DriveResult:
    return DriveResult(
            success=data["success"],
            succeeded_parameters=data["succeeded_parameters"],
            failed_parameters=data["failed_parameters"],
        )

def device_from_dict(data: dict) -> Device:
    return Device(
            adapter_type=data["adapter_type"],
            input_parameter_name=data["input_parameter_name"],
            device_setpoint_name=data["device_setpoint_name"],
            device_readback_name=data["device_readback_name"],
            device_acquired_name=data["device_acquired_name"],
        )

def setting_change_from_dict(data: dict) -> SettingChange:
    return SettingChange(data["parameter"], data["old_value"], data["new_value"])

def trim_record_from_dict(data: dict) -> TrimRecord:
    return TrimRecord(
            id=data["id"],
            context_name=data["context_name"],
            comment=data["comment"],
            timestamp=datetime.fromisoformat(data["timestamp"].replace("Z", "+00:00")),
            triggers=[setting_change_from_dict(trigger) for trigger in data["triggers"]],
            results=[setting_change_from_dict(result) for result in data["results"]],
        )