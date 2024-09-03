import voluptuous as vol
from .const import CONF_IGNORE_STRING as CONF_IGNORE_STRING, CONF_RESTORE_LIGHT_STATE as CONF_RESTORE_LIGHT_STATE, CONF_SENSOR_STRING as CONF_SENSOR_STRING, CONF_TLS_VER as CONF_TLS_VER, CONF_VAR_SENSOR_STRING as CONF_VAR_SENSOR_STRING, DEFAULT_IGNORE_STRING as DEFAULT_IGNORE_STRING, DEFAULT_RESTORE_LIGHT_STATE as DEFAULT_RESTORE_LIGHT_STATE, DEFAULT_SENSOR_STRING as DEFAULT_SENSOR_STRING, DEFAULT_TLS_VERSION as DEFAULT_TLS_VERSION, DEFAULT_VAR_SENSOR_STRING as DEFAULT_VAR_SENSOR_STRING, DOMAIN as DOMAIN, HTTPS_PORT as HTTPS_PORT, HTTP_PORT as HTTP_PORT, ISY_CONF_NAME as ISY_CONF_NAME, ISY_CONF_UUID as ISY_CONF_UUID, ISY_URL_POSTFIX as ISY_URL_POSTFIX, SCHEME_HTTP as SCHEME_HTTP, SCHEME_HTTPS as SCHEME_HTTPS, UDN_UUID_PREFIX as UDN_UUID_PREFIX
from _typeshed import Incomplete
from collections.abc import Mapping
from homeassistant.components import dhcp as dhcp, ssdp as ssdp
from homeassistant.config_entries import ConfigEntry as ConfigEntry, ConfigFlow as ConfigFlow, ConfigFlowResult as ConfigFlowResult, OptionsFlow as OptionsFlow, SOURCE_IGNORE as SOURCE_IGNORE
from homeassistant.const import CONF_HOST as CONF_HOST, CONF_NAME as CONF_NAME, CONF_PASSWORD as CONF_PASSWORD, CONF_USERNAME as CONF_USERNAME
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.data_entry_flow import AbortFlow as AbortFlow
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers import aiohttp_client as aiohttp_client
from typing import Any

_LOGGER: Incomplete

def _data_schema(schema_input: dict[str, str]) -> vol.Schema: ...
async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, str]: ...

class Isy994ConfigFlow(ConfigFlow, domain=DOMAIN):
    VERSION: int
    discovered_conf: Incomplete
    _existing_entry: Incomplete
    def __init__(self) -> None: ...
    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def _async_set_unique_id_or_update(self, isy_mac: str, ip_address: str, port: int | None) -> None: ...
    async def async_step_dhcp(self, discovery_info: dhcp.DhcpServiceInfo) -> ConfigFlowResult: ...
    async def async_step_ssdp(self, discovery_info: ssdp.SsdpServiceInfo) -> ConfigFlowResult: ...
    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> ConfigFlowResult: ...
    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...

class OptionsFlowHandler(OptionsFlow):
    config_entry: Incomplete
    def __init__(self, config_entry: ConfigEntry) -> None: ...
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...

class InvalidHost(HomeAssistantError): ...
class CannotConnect(HomeAssistantError): ...
class InvalidAuth(HomeAssistantError): ...
