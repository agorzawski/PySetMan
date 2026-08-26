import requests
from dataclasses import dataclass
from datetime import datetime


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


"""
Simple client ONLY to act on resident context
"""
class SetManClient:

    EP_RESIDENT_SETTINGS = "/settings/resident"
    EP_RESIDENT_TRIM = "/trims/resident"
    
    def __init__(self, ip, port=8000):
        self.url=f"http://{ip}:{port}{{}}"

    def send_trim(self, comment, values):
        payload = {"comment": comment, 
                   "values": values,}   
        response = self._post_request_and_handle_exception(self.url.format(self.EP_RESIDENT_TRIM), payload)
        return response.json()
   
    def get_resident_settings(self) -> list[Setting]:
        response = self._get_request_and_handle_exception(self.url.format(self.EP_RESIDENT_SETTINGS))
        return [Setting.from_dict(setting) for setting in response.json()["settings"]]

    def _get_request_and_handle_exception(self, url):
        response = requests.get(url, headers={"accept": "application/json"},)
        if response.status_code != 200:            
            raise ValueError(f"Request failed: HTTP {response.status_code} with response: {response.text}")
        return response
       
    def _post_request_and_handle_exception(self, url, payload):
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
        