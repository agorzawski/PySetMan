from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass(frozen=True, eq=True)
class Setting:
    parameter_name: str
    value: float
    last_updated: datetime


@dataclass(frozen=True, eq=True)
class Realm:
    name: str
    abbreviation: str
    description: str


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


@dataclass(frozen=True, eq=True)
class Context:
    id: UUID
    name: str
    realm: str
    resident: bool


@dataclass(frozen=True)
class ContextResidency:
    id: UUID
    context_id: UUID
    context_name: str
    realm: str
    timestamp: datetime
    event: str


@dataclass
class DriveResult:
    success: bool
    succeeded_parameters: dict[str, float]
    failed_parameters: dict[str, float]


@dataclass(frozen=True, eq=True)
class Rule:
    type: str
    input_parameters: list[str]
    output_parameters: list[str]


@dataclass(frozen=True, eq=True)
class Device:
    adapter_type: str
    input_parameter_name: str
    device_setpoint_name: str
    device_readback_name: str
    device_acquired_name: str

