from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class SettingChange:
    parameter: str
    old_value: float
    new_value: float

    @classmethod
    def from_dict(cls, json: dict) -> "SettingChange":
        return cls(json["parameter"], json["old_value"], json["new_value"])


@dataclass
class TrimRecord:
    id: UUID
    context_name: str
    comment: str
    timestamp: datetime
    triggers: list[SettingChange]
    results: list[SettingChange]

    @classmethod
    def from_dict(cls, json: dict) -> "TrimRecord":
        return cls(
            id=json["id"],
            context_name=json["context_name"],
            comment=json["comment"],
            timestamp=datetime.fromisoformat(json["timestamp"].replace("Z", "+00:00")),
            triggers=[SettingChange.from_dict(trigger) for trigger in json["triggers"]],
            results=[SettingChange.from_dict(result) for result in json["results"]],
        )