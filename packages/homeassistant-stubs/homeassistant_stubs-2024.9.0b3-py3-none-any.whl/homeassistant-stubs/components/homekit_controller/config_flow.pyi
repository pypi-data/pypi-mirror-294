from .const import DOMAIN as DOMAIN, KNOWN_DEVICES as KNOWN_DEVICES
from .storage import async_get_entity_storage as async_get_entity_storage
from .utils import async_get_controller as async_get_controller
from _typeshed import Incomplete
from aiohomekit import Controller as Controller
from aiohomekit.controller.abstract import AbstractDiscovery as AbstractDiscovery, AbstractPairing as AbstractPairing, FinishPairing as FinishPairing
from aiohomekit.model.categories import Categories
from homeassistant.components import bluetooth as bluetooth, zeroconf as zeroconf
from homeassistant.config_entries import ConfigFlow as ConfigFlow, ConfigFlowResult as ConfigFlowResult
from homeassistant.core import callback as callback
from homeassistant.data_entry_flow import AbortFlow as AbortFlow
from homeassistant.helpers.typing import VolDictType as VolDictType
from typing import Any

HOMEKIT_DIR: str
HOMEKIT_BRIDGE_DOMAIN: str
HOMEKIT_IGNORE: Incomplete
PAIRING_FILE: str
PIN_FORMAT: Incomplete
_LOGGER: Incomplete
BLE_DEFAULT_NAME: str
INSECURE_CODES: Incomplete

def normalize_hkid(hkid: str) -> str: ...
def formatted_category(category: Categories) -> str: ...
def ensure_pin_format(pin: str, allow_insecure_setup_codes: Any = None) -> str: ...

class HomekitControllerFlowHandler(ConfigFlow, domain=DOMAIN):
    VERSION: int
    model: Incomplete
    hkid: Incomplete
    name: Incomplete
    category: Incomplete
    devices: Incomplete
    controller: Incomplete
    finish_pairing: Incomplete
    def __init__(self) -> None: ...
    async def _async_setup_controller(self) -> None: ...
    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_unignore(self, user_input: dict[str, Any]) -> ConfigFlowResult: ...
    def _hkid_is_homekit(self, hkid: str) -> bool: ...
    async def async_step_zeroconf(self, discovery_info: zeroconf.ZeroconfServiceInfo) -> ConfigFlowResult: ...
    async def async_step_bluetooth(self, discovery_info: bluetooth.BluetoothServiceInfoBleak) -> ConfigFlowResult: ...
    async def async_step_pair(self, pair_info: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_busy_error(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_max_tries_error(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_protocol_error(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    def _async_step_pair_show_form(self, errors: dict[str, str] | None = None, description_placeholders: dict[str, str] | None = None) -> ConfigFlowResult: ...
    async def _entry_from_accessory(self, pairing: AbstractPairing) -> ConfigFlowResult: ...

class InsecureSetupCode(Exception): ...
