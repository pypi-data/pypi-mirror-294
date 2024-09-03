from . import UnifiConfigEntry as UnifiConfigEntry
from .const import DEVICE_STATES as DEVICE_STATES
from .entity import HandlerT as HandlerT, UnifiEntity as UnifiEntity, UnifiEntityDescription as UnifiEntityDescription, async_client_device_info_fn as async_client_device_info_fn, async_device_available_fn as async_device_available_fn, async_device_device_info_fn as async_device_device_info_fn, async_wlan_available_fn as async_wlan_available_fn, async_wlan_device_info_fn as async_wlan_device_info_fn
from .hub import UnifiHub as UnifiHub
from _typeshed import Incomplete
from aiounifi.interfaces.api_handlers import ItemEvent as ItemEvent
from aiounifi.models.api import ApiItemT
from aiounifi.models.client import Client
from aiounifi.models.device import Device, TypedDeviceTemperature as TypedDeviceTemperature, TypedDeviceUptimeStatsWanMonitor as TypedDeviceUptimeStatsWanMonitor
from aiounifi.models.wlan import Wlan
from collections.abc import Callable as Callable
from dataclasses import dataclass
from datetime import date, datetime
from decimal import Decimal
from homeassistant.components.sensor import SensorDeviceClass as SensorDeviceClass, SensorEntity as SensorEntity, SensorEntityDescription as SensorEntityDescription, SensorStateClass as SensorStateClass, UnitOfTemperature as UnitOfTemperature
from homeassistant.const import EntityCategory as EntityCategory, PERCENTAGE as PERCENTAGE, UnitOfDataRate as UnitOfDataRate, UnitOfPower as UnitOfPower, UnitOfTime as UnitOfTime
from homeassistant.core import Event as core_Event, HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.typing import StateType as StateType
from homeassistant.util import slugify as slugify
from typing import Literal

def async_bandwidth_sensor_allowed_fn(hub: UnifiHub, obj_id: str) -> bool: ...
def async_uptime_sensor_allowed_fn(hub: UnifiHub, obj_id: str) -> bool: ...
def async_client_rx_value_fn(hub: UnifiHub, client: Client) -> float: ...
def async_client_tx_value_fn(hub: UnifiHub, client: Client) -> float: ...
def async_client_uptime_value_fn(hub: UnifiHub, client: Client) -> datetime: ...
def async_wlan_client_value_fn(hub: UnifiHub, wlan: Wlan) -> int: ...
def async_device_clients_value_fn(hub: UnifiHub, device: Device) -> int: ...
def async_device_uptime_value_fn(hub: UnifiHub, device: Device) -> datetime | None: ...
def async_uptime_value_changed_fn(old: StateType | date | datetime | Decimal, new: datetime | float | str | None) -> bool: ...
def async_device_outlet_power_supported_fn(hub: UnifiHub, obj_id: str) -> bool: ...
def async_device_outlet_supported_fn(hub: UnifiHub, obj_id: str) -> bool: ...
def async_device_uplink_mac_supported_fn(hub: UnifiHub, obj_id: str) -> bool: ...
def device_system_stats_supported_fn(stat_index: int, hub: UnifiHub, obj_id: str) -> bool: ...
def async_client_is_connected_fn(hub: UnifiHub, obj_id: str) -> bool: ...
def async_device_state_value_fn(hub: UnifiHub, device: Device) -> str: ...
def async_device_wan_latency_supported_fn(wan: Literal['WAN', 'WAN2'], monitor_target: str, hub: UnifiHub, obj_id: str) -> bool: ...
def async_device_wan_latency_value_fn(wan: Literal['WAN', 'WAN2'], monitor_target: str, hub: UnifiHub, device: Device) -> int | None: ...
def _device_wan_latency_monitor(wan: Literal['WAN', 'WAN2'], monitor_target: str, device: Device) -> TypedDeviceUptimeStatsWanMonitor | None: ...
def make_wan_latency_sensors() -> tuple[UnifiSensorEntityDescription, ...]: ...
def async_device_temperatures_value_fn(temperature_name: str, hub: UnifiHub, device: Device) -> float: ...
def async_device_temperatures_supported_fn(temperature_name: str, hub: UnifiHub, obj_id: str) -> bool: ...
def _device_temperature(temperature_name: str, temperatures: list[TypedDeviceTemperature]) -> float | None: ...
def make_device_temperatur_sensors() -> tuple[UnifiSensorEntityDescription, ...]: ...

@dataclass(frozen=True, kw_only=True)
class UnifiSensorEntityDescription(SensorEntityDescription, UnifiEntityDescription[HandlerT, ApiItemT]):
    value_fn: Callable[[UnifiHub, ApiItemT], datetime | float | str | None]
    is_connected_fn: Callable[[UnifiHub, str], bool] | None = ...
    value_changed_fn: Callable[[StateType | date | datetime | Decimal, datetime | float | str | None], bool] = ...
    def __init__(self, *, key, device_class=..., entity_category=..., entity_registry_enabled_default=..., entity_registry_visible_default=..., force_update=..., icon=..., has_entity_name=..., name=..., translation_key=..., translation_placeholders=..., unit_of_measurement=..., api_handler_fn, device_info_fn, object_fn, unique_id_fn, allowed_fn=..., available_fn=..., name_fn=..., supported_fn=..., event_is_on=..., event_to_subscribe=..., should_poll=..., last_reset=..., native_unit_of_measurement=..., options=..., state_class=..., suggested_display_precision=..., suggested_unit_of_measurement=..., value_fn, is_connected_fn=..., value_changed_fn=...) -> None: ...

ENTITY_DESCRIPTIONS: tuple[UnifiSensorEntityDescription, ...]

async def async_setup_entry(hass: HomeAssistant, config_entry: UnifiConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class UnifiSensorEntity(UnifiEntity[HandlerT, ApiItemT], SensorEntity):
    entity_description: UnifiSensorEntityDescription[HandlerT, ApiItemT]
    _attr_available: bool
    def _make_disconnected(self, *_: core_Event) -> None: ...
    _attr_native_value: Incomplete
    def async_update_state(self, event: ItemEvent, obj_id: str) -> None: ...
    async def async_added_to_hass(self) -> None: ...
    async def async_will_remove_from_hass(self) -> None: ...
