from . import BondConfigEntry as BondConfigEntry
from .const import SERVICE_SET_FAN_SPEED_TRACKED_STATE as SERVICE_SET_FAN_SPEED_TRACKED_STATE
from .entity import BondEntity as BondEntity
from .models import BondData as BondData
from .utils import BondDevice as BondDevice
from _typeshed import Incomplete
from homeassistant.components.fan import DIRECTION_FORWARD as DIRECTION_FORWARD, DIRECTION_REVERSE as DIRECTION_REVERSE, FanEntity as FanEntity, FanEntityFeature as FanEntityFeature
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers import entity_platform as entity_platform
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.util.percentage import percentage_to_ranged_value as percentage_to_ranged_value, ranged_value_to_percentage as ranged_value_to_percentage
from homeassistant.util.scaling import int_states_in_range as int_states_in_range
from typing import Any

_LOGGER: Incomplete
PRESET_MODE_BREEZE: str

async def async_setup_entry(hass: HomeAssistant, entry: BondConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class BondFan(BondEntity, FanEntity):
    _power: Incomplete
    _speed: Incomplete
    _direction: Incomplete
    _attr_preset_modes: Incomplete
    _attr_supported_features: Incomplete
    def __init__(self, data: BondData, device: BondDevice) -> None: ...
    _attr_preset_mode: Incomplete
    def _apply_state(self) -> None: ...
    @property
    def _speed_range(self) -> tuple[int, int]: ...
    @property
    def percentage(self) -> int: ...
    @property
    def speed_count(self) -> int: ...
    @property
    def current_direction(self) -> str | None: ...
    async def async_set_percentage(self, percentage: int) -> None: ...
    async def async_set_power_belief(self, power_state: bool) -> None: ...
    async def async_set_speed_belief(self, speed: int) -> None: ...
    async def async_turn_on(self, percentage: int | None = None, preset_mode: str | None = None, **kwargs: Any) -> None: ...
    async def async_set_preset_mode(self, preset_mode: str) -> None: ...
    async def async_turn_off(self, **kwargs: Any) -> None: ...
    async def async_set_direction(self, direction: str) -> None: ...
