from typing import Any
import requests
from data import Setting, ParametersResponse, Context

APPLICATION_JSON = "application/json"

"""
Simple client that covers:
- get contexts
- get parameters
- get settings (from resident or any other context)
- send trims (for resident or any other context)

"""
class SetManClient:

    EP_PARAMETERS = "/parameters"
    EP_CONTEXTS = "/contexts"

    EP_SETTINGS = "/settings/context"
    EP_RESIDENT_SETTINGS = "/settings/resident"

    EP_TRIM = "/trims"
    EP_RESIDENT_TRIM = "/trims/resident"

    def __init__(self, ip:str='127.0.0.1', port:int=8000, protocol:str='http'):
        self.url=f"{protocol}://{ip}:{port}{{}}"

    def send_trim(self, comment: str, values: dict[str, float | int | str], context: Context = None,):
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

    def get_contexts(self):
        response = self._get_request_and_handle_exception(self.url.format(self.EP_CONTEXTS))
        return [Context.from_dict(context) for context in response.json()]

    def get_parameters(self, trimmable:bool=True) -> ParametersResponse:
       params = {"trimmable":str(trimmable)}
       response = self._get_request_and_handle_exception(self.url.format(self.EP_PARAMETERS),
                                                         params=params)
       return ParametersResponse.from_dict(response.json())

    def get_resident_settings(self) -> list[Setting]:
        response = self._get_request_and_handle_exception(self.url.format(self.EP_RESIDENT_SETTINGS))
        return [Setting.from_dict(setting) for setting in response.json()["settings"]]

    def get_settings(self, context: str| Context):
        params = {"context_name": context.name if isinstance(context, Context) else context}
        response = self._get_request_and_handle_exception(self.url.format(self.EP_SETTINGS), params=params)
        return [Setting.from_dict(setting) for setting in response.json()["settings"]]

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
    def _post_request_and_handle_exception(url:str, payload: dict[str, Any], params=None):
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
        