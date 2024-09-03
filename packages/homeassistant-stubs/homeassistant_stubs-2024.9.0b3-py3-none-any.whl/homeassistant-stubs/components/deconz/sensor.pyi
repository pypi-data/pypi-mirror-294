from .const import ATTR_DARK as ATTR_DARK, ATTR_ON as ATTR_ON
from .deconz_device import DeconzDevice as DeconzDevice
from .hub import DeconzHub as DeconzHub
from _typeshed import Incomplete
from collections.abc import Callable as Callable
from dataclasses import dataclass
from datetime import datetime
from homeassistant.components.sensor import DOMAIN as DOMAIN, SensorDeviceClass as SensorDeviceClass, SensorEntity as SensorEntity, SensorEntityDescription as SensorEntityDescription, SensorStateClass as SensorStateClass
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE as ATTR_TEMPERATURE, ATTR_VOLTAGE as ATTR_VOLTAGE, CONCENTRATION_MICROGRAMS_PER_CUBIC_METER as CONCENTRATION_MICROGRAMS_PER_CUBIC_METER, CONCENTRATION_PARTS_PER_BILLION as CONCENTRATION_PARTS_PER_BILLION, CONCENTRATION_PARTS_PER_MILLION as CONCENTRATION_PARTS_PER_MILLION, EntityCategory as EntityCategory, LIGHT_LUX as LIGHT_LUX, PERCENTAGE as PERCENTAGE, UnitOfEnergy as UnitOfEnergy, UnitOfPower as UnitOfPower, UnitOfPressure as UnitOfPressure, UnitOfTemperature as UnitOfTemperature
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.typing import StateType as StateType
from pydeconz.interfaces.sensors import SensorResources
from pydeconz.models.event import EventType as EventType
from pydeconz.models.sensor import SensorBase as PydeconzSensorBase
from pydeconz.models.sensor.air_quality import AirQuality
from pydeconz.models.sensor.carbon_dioxide import CarbonDioxide
from pydeconz.models.sensor.consumption import Consumption
from pydeconz.models.sensor.daylight import Daylight
from pydeconz.models.sensor.formaldehyde import Formaldehyde
from pydeconz.models.sensor.generic_status import GenericStatus
from pydeconz.models.sensor.humidity import Humidity
from pydeconz.models.sensor.light_level import LightLevel
from pydeconz.models.sensor.moisture import Moisture
from pydeconz.models.sensor.particulate_matter import ParticulateMatter
from pydeconz.models.sensor.power import Power
from pydeconz.models.sensor.pressure import Pressure
from pydeconz.models.sensor.temperature import Temperature
from pydeconz.models.sensor.time import Time
from typing import Generic, TypeVar

PROVIDES_EXTRA_ATTRIBUTES: Incomplete
ATTR_CURRENT: str
ATTR_POWER: str
ATTR_DAYLIGHT: str
ATTR_EVENT_ID: str
T = TypeVar('T', AirQuality, CarbonDioxide, Consumption, Daylight, Formaldehyde, GenericStatus, Humidity, LightLevel, Moisture, ParticulateMatter, Power, Pressure, Temperature, Time, PydeconzSensorBase)

@dataclass(frozen=True, kw_only=True)
class DeconzSensorDescription(SensorEntityDescription, Generic[T]):
    instance_check: type[T] | None = ...
    name_suffix: str = ...
    old_unique_id_suffix: str = ...
    supported_fn: Callable[[T], bool]
    update_key: str
    value_fn: Callable[[T], datetime | StateType]
    def __init__(self, *, key, device_class=..., entity_category=..., entity_registry_enabled_default=..., entity_registry_visible_default=..., force_update=..., icon=..., has_entity_name=..., name=..., translation_key=..., translation_placeholders=..., unit_of_measurement=..., last_reset=..., native_unit_of_measurement=..., options=..., state_class=..., suggested_display_precision=..., suggested_unit_of_measurement=..., instance_check=..., name_suffix=..., old_unique_id_suffix=..., supported_fn, update_key, value_fn) -> None: ...

ENTITY_DESCRIPTIONS: tuple[DeconzSensorDescription, ...]

async def async_setup_entry(hass: HomeAssistant, config_entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None: ...

class DeconzSensor(DeconzDevice[SensorResources], SensorEntity):
    TYPE = DOMAIN
    entity_description: DeconzSensorDescription
    unique_id_suffix: Incomplete
    _update_key: Incomplete
    _name_suffix: Incomplete
    def __init__(self, device: SensorResources, hub: DeconzHub, description: DeconzSensorDescription) -> None: ...
    @property
    def native_value(self) -> StateType | datetime: ...
    @property
    def extra_state_attributes(self) -> dict[str, bool | float | int | str | None]: ...

class DeconzBatteryTracker:
    sensor: Incomplete
    hub: Incomplete
    description: Incomplete
    async_add_entities: Incomplete
    unsubscribe: Incomplete
    def __init__(self, sensor_id: str, hub: DeconzHub, description: DeconzSensorDescription, async_add_entities: AddEntitiesCallback) -> None: ...
    def async_update_callback(self) -> None: ...
