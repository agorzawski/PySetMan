
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class Setting:
    parameter_name: str
    value: float
    last_updated: datetime

    @classmethod
    def from_dict(cls, data):
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
