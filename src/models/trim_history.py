from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class SettingChange:
    parameter: str
    old_value: float
    new_value: float


@dataclass
class TrimRecord:
    id: UUID
    context_name: str
    comment: str
    timestamp: datetime
    triggers: list[SettingChange]
    results: list[SettingChange]
