from collections.abc import Callable as Callable
from homeassistant.components import http as http
from homeassistant.core import HomeAssistant as HomeAssistant
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.loader import bind_hass as bind_hass
from homeassistant.util.network import is_ip_address as is_ip_address, is_loopback as is_loopback, normalize_url as normalize_url

TYPE_URL_INTERNAL: str
TYPE_URL_EXTERNAL: str
SUPERVISOR_NETWORK_HOST: str

class NoURLAvailableError(HomeAssistantError): ...

def is_internal_request(hass: HomeAssistant) -> bool: ...
def get_supervisor_network_url(hass: HomeAssistant, *, allow_ssl: bool = False) -> str | None: ...
def is_hass_url(hass: HomeAssistant, url: str) -> bool: ...
def get_url(hass: HomeAssistant, *, require_current_request: bool = False, require_ssl: bool = False, require_standard_port: bool = False, require_cloud: bool = False, allow_internal: bool = True, allow_external: bool = True, allow_cloud: bool = True, allow_ip: bool | None = None, prefer_external: bool | None = None, prefer_cloud: bool = False) -> str: ...
def _get_request_host() -> str | None: ...
def _get_internal_url(hass: HomeAssistant, *, allow_ip: bool = True, require_current_request: bool = False, require_ssl: bool = False, require_standard_port: bool = False) -> str: ...
def _get_external_url(hass: HomeAssistant, *, allow_cloud: bool = True, allow_ip: bool = True, prefer_cloud: bool = False, require_current_request: bool = False, require_ssl: bool = False, require_standard_port: bool = False, require_cloud: bool = False) -> str: ...
def _get_cloud_url(hass: HomeAssistant, require_current_request: bool = False) -> str: ...
def is_cloud_connection(hass: HomeAssistant) -> bool: ...
