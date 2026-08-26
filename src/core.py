import requests
from data import Setting, ParametersResponse, Context

"""
Simple client ONLY to act on resident context
"""
class SetManClient:

    EP_PARAMETERS = "/parameters"
    EP_CONTEXTS = "/contexts"
    EP_RESIDENT_SETTINGS = "/settings/resident"
    EP_RESIDENT_TRIM = "/trims/resident"
    
    def __init__(self, ip:str='127.0.0.1', port:int=8000):
        self.url=f"http://{ip}:{port}{{}}"

    def send_trim(self, comment, values):
        payload = {"comment": comment, 
                   "values": values,}   
        response = self._post_request_and_handle_exception(self.url.format(self.EP_RESIDENT_TRIM), payload)
        return response.json()

    def get_contexts(self):
        response = self._get_request_and_handle_exception(self.url.format(self.EP_CONTEXTS))
        return [Context.from_dict(context) for context in response.json()]

    def get_parameters(self, trimmable=True) -> ParametersResponse:
       response = self._get_request_and_handle_exception(self.url.format(self.EP_PARAMETERS)+'?trimmable=true')
       return ParametersResponse(**response.json())

    def get_resident_settings(self) -> list[Setting]:
        response = self._get_request_and_handle_exception(self.url.format(self.EP_RESIDENT_SETTINGS))
        return [Setting.from_dict(setting) for setting in response.json()["settings"]]

    @staticmethod
    def _get_request_and_handle_exception(url):
        response = requests.get(url, headers={"accept": "application/json"},)
        if response.status_code != 200:            
            raise ValueError(f"Request failed: HTTP {response.status_code} with response: {response.text}")
        return response
       
    @staticmethod
    def _post_request_and_handle_exception(url, payload):
        response = requests.post(
            url,
            headers={
                "accept": "application/json",
                "Content-Type": "application/json",
            },
            json=payload,
        )   
        if response.status_code != 200:            
            raise ValueError(f"Request failed: HTTP {response.status_code} with response: {response.text}")            
        return response
        