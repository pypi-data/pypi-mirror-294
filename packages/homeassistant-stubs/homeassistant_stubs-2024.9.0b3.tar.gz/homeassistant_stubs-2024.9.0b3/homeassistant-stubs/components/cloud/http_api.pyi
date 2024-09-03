from .assist_pipeline import async_create_cloud_pipeline as async_create_cloud_pipeline
from .client import CloudClient as CloudClient
from .const import DATA_CLOUD as DATA_CLOUD, PREF_ALEXA_REPORT_STATE as PREF_ALEXA_REPORT_STATE, PREF_DISABLE_2FA as PREF_DISABLE_2FA, PREF_ENABLE_ALEXA as PREF_ENABLE_ALEXA, PREF_ENABLE_GOOGLE as PREF_ENABLE_GOOGLE, PREF_GOOGLE_REPORT_STATE as PREF_GOOGLE_REPORT_STATE, PREF_GOOGLE_SECURE_DEVICES_PIN as PREF_GOOGLE_SECURE_DEVICES_PIN, PREF_REMOTE_ALLOW_REMOTE_ENABLE as PREF_REMOTE_ALLOW_REMOTE_ENABLE, PREF_TTS_DEFAULT_VOICE as PREF_TTS_DEFAULT_VOICE, REQUEST_TIMEOUT as REQUEST_TIMEOUT
from .google_config import CLOUD_GOOGLE as CLOUD_GOOGLE
from .repairs import async_manage_legacy_subscription_issue as async_manage_legacy_subscription_issue
from .subscription import async_subscription_info as async_subscription_info
from _typeshed import Incomplete
from aiohttp import web as web
from collections.abc import Awaitable as Awaitable, Callable as Callable, Coroutine
from hass_nabucasa import Cloud as Cloud
from homeassistant.components import websocket_api as websocket_api
from homeassistant.components.homeassistant import exposed_entities as exposed_entities
from homeassistant.components.http import HomeAssistantView as HomeAssistantView, KEY_HASS as KEY_HASS, require_admin as require_admin
from homeassistant.components.http.data_validator import RequestDataValidator as RequestDataValidator
from homeassistant.const import CLOUD_NEVER_EXPOSED_ENTITIES as CLOUD_NEVER_EXPOSED_ENTITIES
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.exceptions import HomeAssistantError as HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from homeassistant.util.location import async_detect_location_info as async_detect_location_info
from http import HTTPStatus
from typing import Any, Concatenate

_LOGGER: Incomplete
_CLOUD_ERRORS: dict[type[Exception], tuple[HTTPStatus, str]]

def async_setup(hass: HomeAssistant) -> None: ...
def _handle_cloud_errors(handler: Callable[Concatenate[_HassViewT, web.Request, _P], Awaitable[web.Response]]) -> Callable[Concatenate[_HassViewT, web.Request, _P], Coroutine[Any, Any, web.Response]]: ...
def _ws_handle_cloud_errors(handler: Callable[[HomeAssistant, websocket_api.ActiveConnection, dict[str, Any]], Coroutine[None, None, None]]) -> Callable[[HomeAssistant, websocket_api.ActiveConnection, dict[str, Any]], Coroutine[None, None, None]]: ...
def _process_cloud_exception(exc: Exception, where: str) -> tuple[HTTPStatus, str]: ...

class GoogleActionsSyncView(HomeAssistantView):
    url: str
    name: str
    async def post(self, request: web.Request) -> web.Response: ...

class CloudLoginView(HomeAssistantView):
    url: str
    name: str
    async def post(self, request: web.Request, data: dict[str, Any]) -> web.Response: ...

class CloudLogoutView(HomeAssistantView):
    url: str
    name: str
    async def post(self, request: web.Request) -> web.Response: ...

class CloudRegisterView(HomeAssistantView):
    url: str
    name: str
    async def post(self, request: web.Request, data: dict[str, Any]) -> web.Response: ...

class CloudResendConfirmView(HomeAssistantView):
    url: str
    name: str
    async def post(self, request: web.Request, data: dict[str, Any]) -> web.Response: ...

class CloudForgotPasswordView(HomeAssistantView):
    url: str
    name: str
    async def post(self, request: web.Request, data: dict[str, Any]) -> web.Response: ...

async def websocket_cloud_remove_data(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def websocket_cloud_status(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
def _require_cloud_login(handler: Callable[[HomeAssistant, websocket_api.ActiveConnection, dict[str, Any]], None]) -> Callable[[HomeAssistant, websocket_api.ActiveConnection, dict[str, Any]], None]: ...
async def websocket_subscription(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
def validate_language_voice(value: tuple[str, str]) -> tuple[str, str]: ...
async def websocket_update_prefs(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def websocket_hook_create(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def websocket_hook_delete(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def _account_data(hass: HomeAssistant, cloud: Cloud[CloudClient]) -> dict[str, Any]: ...
async def websocket_remote_connect(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def websocket_remote_disconnect(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def google_assistant_get(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def google_assistant_list(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def google_assistant_update(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def alexa_get(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def alexa_list(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def alexa_sync(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
async def thingtalk_convert(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
def tts_info(hass: HomeAssistant, connection: websocket_api.ActiveConnection, msg: dict[str, Any]) -> None: ...
