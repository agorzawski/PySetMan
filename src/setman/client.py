from typing import Any
import requests
from models.data import Setting, ParametersResponse, Context, DriveResult, Realm, Device, Rule

APPLICATION_JSON = "application/json"


class SetManClient:
    """
    Simple SetMan client that covers basic operations to get/control the settings:

    - get: realms, contexts, parameters, devices, settings (from resident or any other context), rules
    - send trims (for resident or any other context)
    - drive all

    """
    EP_REALMS = "/realms"
    EP_PARAMETERS = "/parameters"
    EP_CONTEXTS = "/contexts"
    EP_DEVICES = "/devices"
    EP_RULES = "/rules"


    EP_SETTINGS = "/settings/context"
    EP_RESIDENT_SETTINGS = "/settings/resident"

    EP_TRIM = "/trims"
    EP_RESIDENT_TRIM = "/trims/resident"
    EP_DRIVE_ALL = "/devices/drive"

    def __init__(self, ip: str = '127.0.0.1', port: int = 8000, protocol: str = 'http'):
        self.url = f"{protocol}://{ip}:{port}{{}}"

    def drive_all(self, realm: Realm | None = None) -> DriveResult:
        """
        Drive all resident settings
        :param realm: for a given realm
        :return:
        """
        params = self._get_params_for_request(realm)
        response = self._post_request_and_handle_exception(self.url.format(self.EP_DRIVE_ALL), payload={},
                                                           params=params)
        return DriveResult.from_dict(response.json())

    def send_trim(self,
                  comment: str,
                  values: dict[str, float | int | str],
                  context: Context | None = None) -> ParametersResponse:
        """
        Sends a trim to the resident or any other context.

        :param comment: comment/descrtion to be saved along the succesfull trim
        :param values: dictionary of parameter -> value to be trimmed
        :param context: context to act on, defaults (if None) is the resident
        :return: json response from the server or raises exception if some issues were encountered.
        """
        payload = {
            "comment": comment,
            "values": values,
        }
        params = {}
        if context is not None:
            endpoint = self.url.format(self.EP_TRIM)
            params = {"context_name": context.name}
        else:
            endpoint = self.url.format(self.EP_RESIDENT_TRIM)
        response = self._post_request_and_handle_exception(endpoint, payload, params=params)
        return response.json()

    def get_realms(self) -> list[Realm]:
        response = self._get_request_and_handle_exception(self.url.format(self.EP_REALMS))
        return [Realm.from_dict(realm) for realm in response.json()["realms"]]

    def get_contexts(self, realm: Realm | None = None) -> list[Context]:
        params = self._get_params_for_request(realm)
        response = self._get_request_and_handle_exception(self.url.format(self.EP_CONTEXTS), params=params)
        return [Context.from_dict(context) for context in response.json()]

    def get_parameters(self, realm: Realm | None = None, trimmable: bool = True) -> ParametersResponse:
        params = {"trimmable": str(trimmable)}
        if realm is not None:
            params["realm"] = realm.abbreviation
        response = self._get_request_and_handle_exception(self.url.format(self.EP_PARAMETERS),
                                                          params=params)
        return ParametersResponse.from_dict(response.json())

    def get_resident_settings(self) -> list[Setting]:
        response = self._get_request_and_handle_exception(self.url.format(self.EP_RESIDENT_SETTINGS))
        return [Setting.from_dict(setting) for setting in response.json()["settings"]]

    def get_settings(self, context: str | Context) -> list[Setting]:
        params = {"context_name": context.name if isinstance(context, Context) else context}
        response = self._get_request_and_handle_exception(self.url.format(self.EP_SETTINGS), params=params)
        return [Setting.from_dict(setting) for setting in response.json()["settings"]]

    def get_devices(self, realm: Realm | None = None) -> list[Device]:
        params = self._get_params_for_request(realm)
        response = self._get_request_and_handle_exception(self.url.format(self.EP_DEVICES), params=params)
        return [Device.from_dict(device) for device in response.json()]

    def get_rules(self, realm: Realm | None = None) -> list[Rule]:
        params = self._get_params_for_request(realm)
        response = self._get_request_and_handle_exception(self.url.format(self.EP_RULES), params=params)
        return [Rule.from_dict(rule) for rule in response.json()["rules"]]

    @staticmethod
    def _get_params_for_request(realm: Realm | None = None) -> dict[Any, Any]:
        params = {}
        if realm is not None:
            params["realm"] = realm.abbreviation
        return params

    @staticmethod
    def _get_request_and_handle_exception(url: str, params=None):
        if params is None:
            params = {}
        response = requests.get(url, headers={"accept": APPLICATION_JSON},
                                params=params)
        if response.status_code != 200:
            raise ValueError(f"Request failed: HTTP {response.status_code} with response: {response.text}")
        return response

    @staticmethod
    def _post_request_and_handle_exception(url: str, payload: dict[str, Any], params=None):
        if params is None:
            params = {}
        response = requests.post(
            url,
            headers={
                "accept": APPLICATION_JSON,
                "Content-Type": APPLICATION_JSON,
            },
            params=params,
            json=payload,
        )
        if response.status_code != 200:
            raise ValueError(f"Request failed: HTTP {response.status_code} with response: {response.text}")
        return response
