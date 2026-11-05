from typing import Any
import requests
from models.data import Setting, ParametersResponse, Context, DriveResult, Realm, Device, Rule
from models.trim_history import TrimRecord
from uuid import UUID
from setman.endpoints import *
from setman.response_codes import HTTP_RESPONSE_OK

APPLICATION_JSON = "application/json"


class SetManClient:
    """
    Simple SetMan client that covers basic operations to get/control the settings:

    - get: realms, contexts, parameters, devices, settings (from resident or any other context), rules
    - send trims (for resident or any other context)
    - drive all

    """
    def __init__(self, ip: str = '127.0.0.1', port: int = 8000, protocol: str = 'http'):
        self.url = f"{protocol}://{ip}:{port}{{}}"

    def drive_all(self, realm: Realm | None = None) -> DriveResult:
        """
        Drive all resident settings
        :param realm: for a given realm
        :return:
        """
        _params = self._get_params_for_request(realm)
        _response = self._post_request_and_handle_exception(self.url.format(EP_DRIVE_ALL), payload={},
                                                           params=_params)
        return DriveResult.from_dict(_response.json())

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
            endpoint = self.url.format(EP_TRIM)
            params = {"context_name": context.name}
        else:
            endpoint = self.url.format(EP_RESIDENT_TRIM)
        _response = self._post_request_and_handle_exception(endpoint, payload, params=params)
        return _response.json()

    def get_realms(self) -> list[Realm]:
        _response = self._get_request_and_handle_exception(self.url.format(EP_REALMS))
        return [Realm.from_dict(realm) for realm in _response.json()["realms"]]

    def get_contexts(self, realm: Realm | None = None) -> list[Context]:
        _params = self._get_params_for_request(realm)
        _response = self._get_request_and_handle_exception(self.url.format(EP_CONTEXTS), params=_params)
        return [Context.from_dict(context)
                for context in _response.json()] # FIXME change in server to unify the response json

    def get_parameters(self, realm: Realm | None = None, trimmable: bool = True) -> ParametersResponse:
        _params = {"trimmable": str(trimmable)}
        if realm is not None:
            _params["realm"] = realm.abbreviation
        _response = self._get_request_and_handle_exception(self.url.format(EP_PARAMETERS),
                                                          params=_params)
        return ParametersResponse.from_dict(_response.json())

    def get_resident_settings(self, realm: Realm | None = None) -> list[Setting]:
        _params = self._get_params_for_request(realm)
        _response = self._get_request_and_handle_exception(self.url.format(EP_RESIDENT_SETTINGS), params=_params)
        return [Setting.from_dict(setting)
                for setting in _response.json()["settings"]]

    def get_settings(self, context: str | Context) -> list[Setting]:
        _params = {"context_name": context.name if isinstance(context, Context) else context}
        _response = self._get_request_and_handle_exception(self.url.format(EP_SETTINGS), params=_params)
        return [Setting.from_dict(setting)
                for setting in _response.json()["settings"]]

    def get_devices(self, realm: Realm | None = None) -> list[Device]:
        _params = self._get_params_for_request(realm)
        _response = self._get_request_and_handle_exception(self.url.format(EP_DEVICES), params=_params)
        return [Device.from_dict(device)
                for device in _response.json()] # FIXME change in server to unify the response json

    def get_rules(self, realm: Realm | None = None) -> list[Rule]:
        _params = self._get_params_for_request(realm)
        _response = self._get_request_and_handle_exception(self.url.format(EP_RULES), params=_params)
        return [Rule.from_dict(rule)
                for rule in _response.json()["rules"]]

    def get_trim_record(self, record_id: str | UUID) -> TrimRecord:
        _response = self._get_request_and_handle_exception(self.url.format(EP_TRIM_HISTORY_ONE.format(record_id)))
        return TrimRecord.from_dict(_response.json()) # FIXME change in server to unify the response json

    def get_trim_records(self, context: str | Context | None = None, parameter_names: list[str] | None = None) -> list[TrimRecord]:
        _response = None
        _params = {"context": context.name if isinstance(context, Context) else context}
        if parameter_names is None:
            _response = self._get_request_and_handle_exception(self.url.format(EP_TRIM_HISTORY),
                                                               params=_params)
        else:
            _params["parameter_names"] = parameter_names
            print(_params)
            _response = self._post_request_and_handle_exception(self.url.format(EP_TRIM_HISTORY),
                                                                payload=_params,)

        return [TrimRecord.from_dict(trim_history)
                for trim_history in _response.json()["history"]]


    def set_residency(self, context: str | Context | None, resident:bool) -> None:
        _params = {"name": context.name if isinstance(context, Context) else context,
                   "resident": resident}
        print(_params)
        self._put_request_and_handle_exception(self.url.format(EP_RESIDENCY), payload=_params)

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
        _response = requests.get(url, headers={"accept": APPLICATION_JSON},
                                params=params)
        if _response.status_code != HTTP_RESPONSE_OK:
            raise SetManServerException(f"Request failed: HTTP {_response.status_code} with response: {_response.text}")
        return _response

    @staticmethod
    def _post_request_and_handle_exception(url: str, payload: dict[str, Any], params=None):
        if params is None:
            params = {}
        _response = requests.post(
            url,
            headers={
                "accept": "*/*",
                "Content-Type": APPLICATION_JSON,
            },
            params=params,
            json=payload,
        )
        if _response.status_code != HTTP_RESPONSE_OK:
            raise SetManServerException(f"Request failed: HTTP {_response.status_code} with response: {_response.text}")
        return _response

    @staticmethod
    def _put_request_and_handle_exception(url: str, payload: dict[str, Any]):
        _response = requests.put(
            url,
            headers={
                "accept": "*/*",
                "Content-Type": APPLICATION_JSON,
            },
            json = payload
        )
        if _response.status_code != HTTP_RESPONSE_OK:
            raise SetManServerException(f"Request failed: HTTP {_response.status_code} with response: {_response.text}")
        return _response


class SetManServerException(Exception):
    """marker for server error"""