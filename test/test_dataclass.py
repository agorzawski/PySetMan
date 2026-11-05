from datetime import datetime, timezone
from models.data import Setting, Parameter, ParametersResponse, Context

PARAMETER_2_DICT_JSON = {
    "name": "PARAMETER_2",
    "parameter_type": "TAPE_2",
    "engineering_unit": "Tm",
    "skills": ["trimmable"],
}
PARAMETER_1_DICT_JSON = {
    "name": "PARAMETER_1",
    "parameter_type": "TYPE_1",
    "engineering_unit": "rad",
    "skills": ["trimmable"],
}
SOME_DATE_DATETIME = datetime(2026, 8, 26, 11, 24, 30, 20181, tzinfo=timezone.utc, )
SOME_DATE_STRING = "2026-08-26T11:24:30.020181Z"
JSON_DICT_SETTING = {
    "parameter_name": "PARAMETER_1",
    "value": 1.234,
    "last_updated": SOME_DATE_STRING,
}
RANDOM_ID_1 = "7202082a-38f5-424e-9416-3af62758dd34"
RANDOM_ID_2 = "87e21853-2b65-4e51-93c7-7f2a4156b26e"
RANDOM_ID_3 = "4248d809-fb82-4d79-9e00-803ef197cf97"

class TestSetting:

    def test_from_dict(self):
        result = Setting.from_dict(JSON_DICT_SETTING)
        assert result.parameter_name == "PARAMETER_1"
        assert result.value == 1.234
        assert result.last_updated == SOME_DATE_DATETIME

    def test_from_dict_converts_z_to_utc(self):
        result = Setting.from_dict(JSON_DICT_SETTING)
        assert result.last_updated.tzinfo == timezone.utc


class TestParameter:

    def test_construction(self):
        parameter = Parameter(
            name="PARAMETER_1",
            parameter_type="KL",
            engineering_unit="rad",
            skills=["trimmable"],
        )
        assert parameter.name == "PARAMETER_1"
        assert parameter.skills == ["trimmable"]


class TestParametersResponse:

    def test_from_dict(self):
        data = {
            "parameters": [PARAMETER_1_DICT_JSON, PARAMETER_2_DICT_JSON,],
            "total": 2,
            "page": None,
            "size": None,
        }

        result = ParametersResponse.from_dict(data)

        assert result.total == 2
        assert result.page is None
        assert result.size is None

        assert len(result.parameters) == 2

        assert isinstance(result.parameters[0], Parameter)
        assert result.parameters[0].name == "PARAMETER_1"
        assert result.parameters[0].engineering_unit == "rad"

        assert isinstance(result.parameters[1], Parameter)
        assert result.parameters[1].name == "PARAMETER_2"
        assert result.parameters[1].engineering_unit == "Tm"


class TestContext:

    def test_from_dict_resident(self):
        data = {
            "id": RANDOM_ID_1,
            "name": "CONTEXT_1",
            "realm": "ACC",
            "resident": True,
        }

        result = Context.from_dict(data)
        assert result.name == "CONTEXT_1"
        assert result.resident is True

    def test_from_dict_non_resident(self):
        data = {
            "id": RANDOM_ID_2,
            "name": "CONTEXT_2",
            "realm": "ACC",
            "resident": False,
        }

        result = Context.from_dict(data)
        assert result.name == "CONTEXT_2"
        assert result.resident is False

