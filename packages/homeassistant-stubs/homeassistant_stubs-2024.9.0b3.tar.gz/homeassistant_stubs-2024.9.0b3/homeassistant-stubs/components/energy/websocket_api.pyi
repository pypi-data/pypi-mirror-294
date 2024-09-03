from .const import DOMAIN as DOMAIN
from .data import DEVICE_CONSUMPTION_SCHEMA as DEVICE_CONSUMPTION_SCHEMA, ENERGY_SOURCE_SCHEMA as ENERGY_SOURCE_SCHEMA, EnergyManager as EnergyManager, EnergyPreferencesUpdate as EnergyPreferencesUpdate, async_get_manager as async_get_manager
from .types import EnergyPlatform as EnergyPlatform, GetSolarForecastType as GetSolarForecastType, SolarForecastType as SolarForecastType
from .validate import async_validate as async_validate
from collections.abc import Callable, Coroutine
from homeassistant.components import recorder as recorder, websocket_api as websocket_api
from homeassistant.components.recorder.statistics import StatisticsRow as StatisticsRow
from homeassistant.const import UnitOfEnergy as UnitOfEnergy
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.integration_platform import async_process_integration_platforms as async_process_integration_platforms
from homeassistant.helpers.singleton import singleton as singleton
from typing import Any

EnergyWebSocketCommandHandler = Callable[[HomeAssistant, websocket_api.ActiveConnection, dict[str, Any], EnergyManager], None]
AsyncEnergyWebSocketCommandHandler = Callable[[HomeAssistant, websocket_api.ActiveConnection, dict[str, Any], EnergyManager], Coroutine[Any, Any, None]]

def async_setup(hass: HomeAssistant) -> None: ...
async def async_get_energy_platforms(hass: HomeAssistant) -> dict[str, GetSolarForecastType]: ...
def _ws_with_manager(func: AsyncEnergyWebSocketCommandHandler | EnergyWebSocketCommandHandler) -> websocket_api.AsyncWebSocketCommandHandler: ...
def ws_get_prefs(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any], manager: EnergyManager) -> None: ...
async def ws_save_prefs(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any], manager: EnergyManager) -> None: ...
async def ws_info(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def ws_validate(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def ws_solar_forecast(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any], manager: EnergyManager) -> None: ...
async def ws_get_fossil_energy_consumption(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
