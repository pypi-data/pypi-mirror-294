from .const import CurrentTemperatureSelector as CurrentTemperatureSelector, DEFAULT_CURRENT_TEMP_SELECTOR as DEFAULT_CURRENT_TEMP_SELECTOR, DEFAULT_SCAN_INTERVAL as DEFAULT_SCAN_INTERVAL, DEFAULT_TARGET_TEMP_SELECTOR as DEFAULT_TARGET_TEMP_SELECTOR, TargetTemperatureSelector as TargetTemperatureSelector
from dataclasses import dataclass
from eq3btsmart.thermostat import Thermostat as Thermostat

@dataclass(slots=True)
class Eq3Config:
    mac_address: str
    current_temp_selector: CurrentTemperatureSelector = ...
    target_temp_selector: TargetTemperatureSelector = ...
    external_temp_sensor: str = ...
    scan_interval: int = ...
    default_away_hours: float = ...
    default_away_temperature: float = ...
    def __init__(self, mac_address, current_temp_selector=..., target_temp_selector=..., external_temp_sensor=..., scan_interval=..., default_away_hours=..., default_away_temperature=...) -> None: ...

@dataclass(slots=True)
class Eq3ConfigEntryData:
    eq3_config: Eq3Config
    thermostat: Thermostat
    def __init__(self, eq3_config, thermostat) -> None: ...
