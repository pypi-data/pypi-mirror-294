from .coordinator import BTHomePassiveBluetoothProcessorCoordinator as BTHomePassiveBluetoothProcessorCoordinator
from homeassistant.config_entries import ConfigEntry as ConfigEntry

BTHomeConfigEntry = ConfigEntry[BTHomePassiveBluetoothProcessorCoordinator]
