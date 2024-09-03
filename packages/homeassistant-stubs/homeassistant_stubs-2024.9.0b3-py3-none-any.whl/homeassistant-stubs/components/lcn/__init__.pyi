import pypck
from .const import ADD_ENTITIES_CALLBACKS as ADD_ENTITIES_CALLBACKS, CONF_DIM_MODE as CONF_DIM_MODE, CONF_DOMAIN_DATA as CONF_DOMAIN_DATA, CONF_SK_NUM_TRIES as CONF_SK_NUM_TRIES, CONNECTION as CONNECTION, DOMAIN as DOMAIN, PLATFORMS as PLATFORMS
from .helpers import AddressType as AddressType, DeviceConnectionType as DeviceConnectionType, InputType as InputType, async_update_config_entry as async_update_config_entry, generate_unique_id as generate_unique_id, get_device_model as get_device_model, import_lcn_config as import_lcn_config, register_lcn_address_devices as register_lcn_address_devices, register_lcn_host_device as register_lcn_host_device
from .schemas import CONFIG_SCHEMA as CONFIG_SCHEMA
from .services import SERVICES as SERVICES
from .websocket import register_panel_and_ws_api as register_panel_and_ws_api
from _typeshed import Incomplete
from collections.abc import Callable as Callable
from homeassistant import config_entries as config_entries
from homeassistant.const import CONF_ADDRESS as CONF_ADDRESS, CONF_DEVICE_ID as CONF_DEVICE_ID, CONF_DOMAIN as CONF_DOMAIN, CONF_IP_ADDRESS as CONF_IP_ADDRESS, CONF_NAME as CONF_NAME, CONF_PASSWORD as CONF_PASSWORD, CONF_PORT as CONF_PORT, CONF_RESOURCE as CONF_RESOURCE, CONF_USERNAME as CONF_USERNAME
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.device_registry import DeviceInfo as DeviceInfo
from homeassistant.helpers.entity import Entity as Entity
from homeassistant.helpers.typing import ConfigType as ConfigType

_LOGGER: Incomplete

async def async_setup(hass: HomeAssistant, config: ConfigType) -> bool: ...
async def async_setup_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> bool: ...
async def async_unload_entry(hass: HomeAssistant, config_entry: config_entries.ConfigEntry) -> bool: ...
def async_host_input_received(hass: HomeAssistant, config_entry: config_entries.ConfigEntry, device_registry: dr.DeviceRegistry, inp: pypck.inputs.Input) -> None: ...
def _async_fire_access_control_event(hass: HomeAssistant, device: dr.DeviceEntry, address: AddressType, inp: InputType) -> None: ...
def _async_fire_send_keys_event(hass: HomeAssistant, device: dr.DeviceEntry, address: AddressType, inp: InputType) -> None: ...

class LcnEntity(Entity):
    _attr_should_poll: bool
    config: Incomplete
    entry_id: Incomplete
    device_connection: Incomplete
    _unregister_for_inputs: Incomplete
    _name: Incomplete
    def __init__(self, config: ConfigType, entry_id: str, device_connection: DeviceConnectionType) -> None: ...
    @property
    def address(self) -> AddressType: ...
    @property
    def unique_id(self) -> str: ...
    @property
    def device_info(self) -> DeviceInfo | None: ...
    async def async_added_to_hass(self) -> None: ...
    async def async_will_remove_from_hass(self) -> None: ...
    @property
    def name(self) -> str: ...
    def input_received(self, input_obj: InputType) -> None: ...
