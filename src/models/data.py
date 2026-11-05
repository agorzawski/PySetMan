from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True, eq=True)
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


@dataclass(frozen=True, eq=True)
class Realm:
    name: str
    abbreviation: str
    description: str

    @classmethod
    def from_dict(cls, data) -> "Realm":
        return cls(
            name=data["name"],
            abbreviation=data["abbreviation"],
            description=data["description"],
        )


@dataclass(frozen=True, eq=True)
class Parameter:
    name: str
    parameter_type: str
    engineering_unit: str
    skills: list[str]


@dataclass(frozen=True, eq=True)
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


@dataclass(frozen=True, eq=True)
class Context:
    id: UUID
    name: str
    realm: str
    resident: bool

    @classmethod
    def from_dict(cls, data):
        return cls(
            id=UUID(data["id"]),
            name=data["name"],
            realm=data["realm"],
            resident=bool(data["resident"]),
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
