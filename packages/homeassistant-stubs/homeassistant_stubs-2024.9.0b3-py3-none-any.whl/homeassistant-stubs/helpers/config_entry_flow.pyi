from .service_info.mqtt import MqttServiceInfo as MqttServiceInfo
from .typing import DiscoveryInfoType as DiscoveryInfoType
from _typeshed import Incomplete
from collections.abc import Awaitable, Callable
from homeassistant import config_entries as config_entries
from homeassistant.components import onboarding as onboarding
from homeassistant.components.bluetooth import BluetoothServiceInfoBleak as BluetoothServiceInfoBleak
from homeassistant.components.dhcp import DhcpServiceInfo as DhcpServiceInfo
from homeassistant.components.ssdp import SsdpServiceInfo as SsdpServiceInfo
from homeassistant.components.zeroconf import ZeroconfServiceInfo as ZeroconfServiceInfo
from homeassistant.core import HomeAssistant as HomeAssistant
from typing import Any

DiscoveryFunctionType = Callable[[HomeAssistant], _R]
_LOGGER: Incomplete

class DiscoveryFlowHandler(config_entries.ConfigFlow):
    VERSION: int
    _domain: Incomplete
    _title: Incomplete
    _discovery_function: Incomplete
    def __init__(self, domain: str, title: str, discovery_function: DiscoveryFunctionType[_R]) -> None: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult: ...
    async def async_step_confirm(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult: ...
    async def async_step_discovery(self, discovery_info: DiscoveryInfoType) -> config_entries.ConfigFlowResult: ...
    async def async_step_bluetooth(self, discovery_info: BluetoothServiceInfoBleak) -> config_entries.ConfigFlowResult: ...
    async def async_step_dhcp(self, discovery_info: DhcpServiceInfo) -> config_entries.ConfigFlowResult: ...
    async def async_step_homekit(self, discovery_info: ZeroconfServiceInfo) -> config_entries.ConfigFlowResult: ...
    async def async_step_mqtt(self, discovery_info: MqttServiceInfo) -> config_entries.ConfigFlowResult: ...
    async def async_step_zeroconf(self, discovery_info: ZeroconfServiceInfo) -> config_entries.ConfigFlowResult: ...
    async def async_step_ssdp(self, discovery_info: SsdpServiceInfo) -> config_entries.ConfigFlowResult: ...
    async def async_step_import(self, _: dict[str, Any] | None) -> config_entries.ConfigFlowResult: ...

def register_discovery_flow(domain: str, title: str, discovery_function: DiscoveryFunctionType[Awaitable[bool] | bool]) -> None: ...

class WebhookFlowHandler(config_entries.ConfigFlow):
    VERSION: int
    _domain: Incomplete
    _title: Incomplete
    _description_placeholder: Incomplete
    _allow_multiple: Incomplete
    def __init__(self, domain: str, title: str, description_placeholder: dict, allow_multiple: bool) -> None: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.ConfigFlowResult: ...

def register_webhook_flow(domain: str, title: str, description_placeholder: dict, allow_multiple: bool = False) -> None: ...
async def webhook_async_remove_entry(hass: HomeAssistant, entry: config_entries.ConfigEntry) -> None: ...
