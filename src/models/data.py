from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Setting:
    parameter_name: str
    value: float
    last_updated: datetime

    @classmethod
    def from_dict(cls, data) -> "Setting":
        return cls(
            parameter_name=data["parameter_name"],
            value=data["value"],
            last_updated=datetime.fromisoformat(
                data["last_updated"].replace("Z", "+00:00")
            ),
        )


@dataclass
class Parameter:
    name: str
    parameter_type: str
    engineering_unit: str
    skills: list[str]


@dataclass
class ParametersResponse:
    parameters: list[Parameter]
    total: int
    page: Optional[int] = None
    size: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ParametersResponse":
        return cls(
            parameters=[
                Parameter(**parameter)
                for parameter in data["parameters"]
            ],
            total=data["total"],
            page=data.get("page"),
            size=data.get("size"),
        )


@dataclass
class Context:
    name: str
    resident: bool
    resident_since: datetime | None = None
    resident_until: datetime | None = None

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data["name"],
            resident=bool(data["resident"]),
            resident_since=(
                datetime.fromisoformat(data["resident_since"].replace("Z", "+00:00"))
                if data["resident_since"]
                else None
            ),
            resident_until=(
                datetime.fromisoformat(data["resident_until"].replace("Z", "+00:00"))
                if data["resident_until"]
                else None
            ),
        )


@dataclass
class DriveResult:
    success: bool
    succeeded_parameters: dict[str, float]
    failed_parameters: dict[str, float]

    @classmethod
    def from_dict(cls, data: dict) -> "DriveResult":
        return cls(
            success=data["success"],
            succeeded_parameters=data["succeeded_parameters"],
            failed_parameters=data["failed_parameters"],
        )
