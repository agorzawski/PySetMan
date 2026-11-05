from unittest.mock import Mock, patch
import pytest
from setman.client import SetManClient, SetManServerException
from models.data import Context, Setting
from setman.endpoints import EP_RESIDENT_SETTINGS, EP_CONTEXTS, EP_PARAMETERS

DEFAULT_HEADERS = {"accept": "application/json"}
DEFAULT_NO_PARAMS = {}
DEFAULT_PROTOCOL_ADDRESS = "http://127.0.0.1:8000{}"
JSON_RESPONSE_ONE_SETTING = {
    "settings": [
        {
            "parameter_name": "TEST_PARAMETER_BLAH_1",
            "value": 0.0025,
            "last_updated": "2026-08-26T15:25:51.515201Z"
        },
    ]
}
JSON_RESPONSE_TWO_PARAMETERS = {
    "parameters": [
        {
            "name": "PARAMETER_BLAH_1",
            "parameter_type": "P_TYPE_1",
            "engineering_unit": "P_EGU_1",
            "skills": ["trimmable"],
        },
        {
            "name": "PARAMETER_BLAH_2",
            "parameter_type": "P_TYPE_2",
            "engineering_unit": "P_EGU_2",
            "skills": ["trimmable"],
        },
    ],
    "total": 2,
    "page": None,
    "size": None,
}
JSON_RESPONSE_ONE_CONTEXT = [
    {
        "id": "4248d809-fb82-4d79-9e00-803ef197cf97",
        "name": "BLAH CONTEXT",
        "realm": "ACC",
        "resident": True,
    },
]


class TestSetManClient:

    @pytest.fixture
    def client(self):
        return SetManClient()

    @staticmethod
    def mock_response(status_code=200, json_data=None, text="",):
        response = Mock()
        response.status_code = status_code
        response.text = text
        response.json.return_value = json_data
        return response

    @patch("requests.get")
    def test_get_contexts(self, mock_get, client):
        mock_get.return_value = self.mock_response(json_data=JSON_RESPONSE_ONE_CONTEXT)
        result = client.get_contexts()
        assert len(result) == 1
        assert isinstance(result[0], Context)
        assert result[0].name == "BLAH CONTEXT"
        assert result[0].resident is True
        mock_get.assert_called_once_with(DEFAULT_PROTOCOL_ADDRESS.format(EP_CONTEXTS),
                                         headers=DEFAULT_HEADERS,
                                         params=DEFAULT_NO_PARAMS,)


    @patch("requests.get")
    def test_get_parameters(self, mock_get, client):
        mock_get.return_value = self.mock_response(json_data=JSON_RESPONSE_TWO_PARAMETERS)
        result = client.get_parameters()
        assert result.total == 2
        assert len(result.parameters) == 2
        assert result.parameters[0].name == "PARAMETER_BLAH_1"
        mock_get.assert_called_once_with(DEFAULT_PROTOCOL_ADDRESS.format(EP_PARAMETERS),
                                         headers=DEFAULT_HEADERS,
                                         params={"trimmable": "True"},)

    @patch("requests.get")
    def test_get_resident_settings(self, mock_get, client):
        mock_get.return_value = self.mock_response(json_data=JSON_RESPONSE_ONE_SETTING)
        result = client.get_resident_settings()
        assert len(result) == 1
        assert isinstance(result[0], Setting)

        mock_get.assert_called_once_with(DEFAULT_PROTOCOL_ADDRESS.format(EP_RESIDENT_SETTINGS),
                                         headers=DEFAULT_HEADERS,
                                         params=DEFAULT_NO_PARAMS,)

    @patch("requests.get")
    def test_get_http_error(self, mock_get, client):
        mock_get.return_value = self.mock_response(status_code=500, text="Internal server error",)
        with pytest.raises(SetManServerException, match="Request failed: HTTP 500",):
            client.get_contexts()

    @patch("requests.post")
    def test_post_http_error(self, mock_post, client):
        mock_post.return_value = self.mock_response(status_code=400, text="Invalid trim",)
        with pytest.raises(SetManServerException,match="Request failed: HTTP 400"):
            client.send_trim(comment="Test", values={"PARAM": 1.5},)