from .const import CONF_ALLOW_EA as CONF_ALLOW_EA
from .data import UFPConfigEntry as UFPConfigEntry, async_get_data_for_entry_id as async_get_data_for_entry_id
from .utils import async_create_api_client as async_create_api_client
from homeassistant import data_entry_flow as data_entry_flow
from homeassistant.components.repairs import ConfirmRepairFlow as ConfirmRepairFlow, RepairsFlow as RepairsFlow
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from uiprotect import ProtectApiClient as ProtectApiClient
from uiprotect.data import Bootstrap as Bootstrap, Camera as Camera

class ProtectRepair(RepairsFlow):
    _api: ProtectApiClient
    _entry: UFPConfigEntry
    def __init__(self, *, api: ProtectApiClient, entry: UFPConfigEntry) -> None: ...
    def _async_get_placeholders(self) -> dict[str, str]: ...

class EAConfirmRepair(ProtectRepair):
    async def async_step_init(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult: ...
    async def async_step_start(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult: ...
    async def async_step_confirm(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult: ...

class CloudAccountRepair(ProtectRepair):
    async def async_step_init(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult: ...
    async def async_step_confirm(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult: ...

class RTSPRepair(ProtectRepair):
    _camera_id: str
    _camera: Camera | None
    _bootstrap: Bootstrap | None
    def __init__(self, *, api: ProtectApiClient, entry: UFPConfigEntry, camera_id: str) -> None: ...
    def _async_get_placeholders(self) -> dict[str, str]: ...
    async def _get_boostrap(self) -> Bootstrap: ...
    async def _get_camera(self) -> Camera: ...
    async def _enable_rtsp(self) -> None: ...
    async def async_step_init(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult: ...
    async def async_step_start(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult: ...
    async def async_step_confirm(self, user_input: dict[str, str] | None = None) -> data_entry_flow.FlowResult: ...

def _async_get_or_create_api_client(hass: HomeAssistant, entry: ConfigEntry) -> ProtectApiClient: ...
async def async_create_fix_flow(hass: HomeAssistant, issue_id: str, data: dict[str, str | int | float | None] | None) -> RepairsFlow: ...
