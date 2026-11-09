import logging
from uuid import UUID

from models.data import Setting, ParametersResponse, Context, DriveResult, Realm, Device, Rule, ContextResidency
from models.trim_history import TrimRecord

from setman.cilent_default import AbstractSetManClient, RestSetManClient


class SetManClient:
    """
    Simple SetMan client that covers basic operations to get/control the settings:

    - get: realms, contexts, parameters, devices, settings (from resident or any other context), rules
    - send trims (for resident or any other context)
    - drive all

    """
    logger = logging.getLogger(__name__)

    def __init__(self, ip: str = '127.0.0.1', port: int = 8000, protocol: str = 'http'):
        self._client: AbstractSetManClient  = RestSetManClient(ip, port, protocol)

    def drive_all(self, realm: Realm | None = None) -> DriveResult:
        """
        Drive all resident settings
        :param realm: for a given realm (if None == ACC realm is treated)
        :return: DriveResult with details of the action
        """
        return self._client.drive_all(realm)

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
        return self._client.send_trim(comment, values, context)

    def get_realms(self) -> list[Realm]:
        """
        Returns a list of all realms defined on the server
        :return: Realms list
        """
        return self._client.get_realms()

    def get_contexts(self, realm: Realm | None = None) -> list[Context]:
        """
        Returns a list of all contexts available on the server
        :param realm: optional realm to get contexts for (if None == ACC realm is selected)
        :return: List of Contexts
        """
        return self._client.get_contexts(realm)

    def get_context_residency_history(self, realm: Realm | None = None, context: Context | None = None) -> list[ContextResidency]:
        """
        Returns a list of residency history on the server.
        :param realm: optional realm to get contexts for (if None == ACC realm is selected)
        :param context: optional context to act on, defaults (if None == all contexts)
        :return: List of ContextResidency
        """
        return self._client.get_context_residency_history(realm, context)

    def get_parameters(self, realm: Realm | None = None, trimmable: bool = True) -> ParametersResponse:
        """
        Returns a list of parameters available on the server

        :param realm: optional realm to get parameters for, defaults (if None == ACC realm is selected)
        :param trimmable: optional (defaults to True) to get those trimmable or not.
        :return: List of Parameter
        """
        return self._client.get_parameters(realm, trimmable)

    def get_resident_settings(self, realm: Realm | None = None) -> list[Setting]:
        """
        Returns a list of resident settings available for the given realm
        :param realm:
        :return:
        """
        return self._client.get_resident_settings(realm)

    def get_settings(self, context: str | Context) -> list[Setting]:
        """
        Returns a list of settings available for the given context
        :param context: Context to get settings for
        :return: List of Setting
        """
        return self._client.get_settings(context)

    def get_devices(self, realm: Realm | None = None) -> list[Device]:
        """
        Returns a list of devices available for the given realm
        :param realm: optional realm to get devices for (if None == ACC realm is selected)
        :return:
        """
        return self._client.get_devices(realm)

    def get_rules(self, realm: Realm | None = None) -> list[Rule]:
        """
        Returns a list of rules available for the given realm
        :param realm: optional realm to get rules for (if None == ACC realm is selected)
        :return:
        """
        return self._client.get_rules(realm)

    def get_trim_record(self, record_id: str | UUID) -> TrimRecord:
        """
        Returns a details for the given trim record id
        :param record_id: unique trim record id
        :return:
        """
        return self._client.get_trim_record(record_id)

    def get_trim_records(self, context: str | Context | None = None, parameter_names: list[str] | None = None) -> list[TrimRecord]:
        """
        Returns a list of trim records available for the given context
        :param context: optional, defaults to None==All contexts
        :param parameter_names: additional filter based on particular parameter names.
                                Defaults to None == all available parameter names.
        :return:
        """
        return self._client.get_trim_records(context, parameter_names)

    def set_residency(self, context: str | Context | None, resident:bool) -> None:
        """
        Sets a residency for the given context
        :param context: Context to set residency for
        :param resident: True or False to set residency or unset residency
        :return:
        """
        self._client.set_residency(context, resident)
        return None
