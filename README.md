# PySetMan

Simple python client to interact with the `SetMan Service` `0.16.0`

## Client

```python
class SetManClient:
    def __init__(self, ip: str = '127.0.0.1', port: int = 8000, protocol: str = 'http')
```

### Public methods

```python
def drive_all(self, realm: Realm | None = None) -> DriveResult
def send_trim(self, comment: str, values: dict[str, float | int | str], context: Context | None = None) -> ParametersResponse
def get_realms(self) -> list[Realm]
def get_contexts(self, realm: Realm | None = None) -> list[Context]
def get_context_residency_history(self, realm: Realm | None = None, context: Context | None = None) -> list[ContextResidency]
def get_parameters(self, realm: Realm | None = None, trimmable: bool = True) -> ParametersResponse
def get_resident_settings(self, realm: Realm | None = None) -> list[Setting]
def get_settings(self, context: str | Context) -> list[Setting]
def get_devices(self, realm: Realm | None = None) -> list[Device]
def get_rules(self, realm: Realm | None = None) -> list[Rule]
def get_trim_record(self, record_id: str | UUID) -> TrimRecord
def get_trim_records(self, context: str | Context | None = None, parameter_names: list[str] | None = None) -> list[TrimRecord]
def set_residency(self, context: str | Context | None, resident: bool) -> None
```

### Errors

```python
class SetManServerException(Exception)
```


## Example usage

> Example below assumes setman-service running locally, see [https://bitbucket.org/myrrha/mcs-setman-srv/src/main/](https://bitbucket.org/myrrha/mcs-setman-srv/src/main/)

```python
client = SetManClient()

# list available Contexts/Realms/ Settings

c = client.get_contexts()
print(c)

r = client.get_realms()
print(r)

s = client.get_resident_settings()
print(s) 
```

Send new values:

```python
client.send_trim("Arbitrary trim", {"PARAMETER_1": 1.2, "PARAMETER_2": 3.4})
```

