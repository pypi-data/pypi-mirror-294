import asyncio
import logging
from .api import AccessTokenAuthImpl as AccessTokenAuthImpl, DEVICE_AUTH_CREDS as DEVICE_AUTH_CREDS, DeviceFlow as DeviceFlow, GoogleHybridAuth as GoogleHybridAuth, InvalidCredential as InvalidCredential, OAuthError as OAuthError, async_create_device_flow as async_create_device_flow, get_feature_access as get_feature_access
from .const import CONF_CALENDAR_ACCESS as CONF_CALENDAR_ACCESS, CONF_CREDENTIAL_TYPE as CONF_CREDENTIAL_TYPE, CredentialType as CredentialType, DEFAULT_FEATURE_ACCESS as DEFAULT_FEATURE_ACCESS, DOMAIN as DOMAIN, FeatureAccess as FeatureAccess
from _typeshed import Incomplete
from collections.abc import Mapping
from homeassistant.config_entries import ConfigEntry as ConfigEntry, ConfigFlowResult as ConfigFlowResult, OptionsFlow as OptionsFlow
from homeassistant.core import callback as callback
from homeassistant.helpers import config_entry_oauth2_flow as config_entry_oauth2_flow
from homeassistant.helpers.aiohttp_client import async_get_clientsession as async_get_clientsession
from typing import Any

_LOGGER: Incomplete

class OAuth2FlowHandler(config_entry_oauth2_flow.AbstractOAuth2FlowHandler, domain=DOMAIN):
    DOMAIN = DOMAIN
    _exchange_finished_task: asyncio.Task[bool] | None
    _reauth_config_entry: Incomplete
    _device_flow: Incomplete
    _web_auth: bool
    def __init__(self) -> None: ...
    @property
    def logger(self) -> logging.Logger: ...
    @property
    def extra_authorize_data(self) -> dict[str, Any]: ...
    external_data: Incomplete
    async def async_step_auth(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_step_creation(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    async def async_oauth_create_entry(self, data: dict) -> ConfigFlowResult: ...
    async def async_step_reauth(self, entry_data: Mapping[str, Any]) -> ConfigFlowResult: ...
    async def async_step_reauth_confirm(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
    @staticmethod
    def async_get_options_flow(config_entry: ConfigEntry) -> OptionsFlow: ...

class OptionsFlowHandler(OptionsFlow):
    config_entry: Incomplete
    def __init__(self, config_entry: ConfigEntry) -> None: ...
    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult: ...
