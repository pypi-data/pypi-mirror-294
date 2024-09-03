import asyncio
import logging
import voluptuous as vol
from . import condition as condition, service as service, template as template
from .condition import ConditionCheckerType as ConditionCheckerType, trace_condition_function as trace_condition_function
from .dispatcher import async_dispatcher_connect as async_dispatcher_connect, async_dispatcher_send_internal as async_dispatcher_send_internal
from .event import async_call_later as async_call_later, async_track_template as async_track_template
from .script_variables import ScriptVariables as ScriptVariables
from .template import Template as Template
from .trace import TraceElement as TraceElement, async_trace_path as async_trace_path, script_execution_set as script_execution_set, trace_append_element as trace_append_element, trace_id_get as trace_id_get, trace_path as trace_path, trace_path_get as trace_path_get, trace_path_stack_cv as trace_path_stack_cv, trace_set_result as trace_set_result, trace_stack_cv as trace_stack_cv, trace_stack_pop as trace_stack_pop, trace_stack_push as trace_stack_push, trace_stack_top as trace_stack_top, trace_update_result as trace_update_result
from .trigger import async_initialize_triggers as async_initialize_triggers, async_validate_trigger_config as async_validate_trigger_config
from .typing import ConfigType as ConfigType, TemplateVarsType as TemplateVarsType, UNDEFINED as UNDEFINED, UndefinedType as UndefinedType
from _typeshed import Incomplete
from collections.abc import AsyncGenerator, Callable as Callable, Mapping, Sequence
from contextvars import ContextVar
from dataclasses import dataclass
from datetime import datetime, timedelta
from functools import cached_property as cached_property
from homeassistant import exceptions as exceptions
from homeassistant.components import scene as scene
from homeassistant.components.logger import LOGSEVERITY as LOGSEVERITY
from homeassistant.const import ATTR_AREA_ID as ATTR_AREA_ID, ATTR_DEVICE_ID as ATTR_DEVICE_ID, ATTR_ENTITY_ID as ATTR_ENTITY_ID, ATTR_FLOOR_ID as ATTR_FLOOR_ID, ATTR_LABEL_ID as ATTR_LABEL_ID, CONF_ALIAS as CONF_ALIAS, CONF_CHOOSE as CONF_CHOOSE, CONF_CONDITION as CONF_CONDITION, CONF_CONDITIONS as CONF_CONDITIONS, CONF_CONTINUE_ON_ERROR as CONF_CONTINUE_ON_ERROR, CONF_CONTINUE_ON_TIMEOUT as CONF_CONTINUE_ON_TIMEOUT, CONF_COUNT as CONF_COUNT, CONF_DEFAULT as CONF_DEFAULT, CONF_DELAY as CONF_DELAY, CONF_DEVICE_ID as CONF_DEVICE_ID, CONF_DOMAIN as CONF_DOMAIN, CONF_ELSE as CONF_ELSE, CONF_ENABLED as CONF_ENABLED, CONF_ERROR as CONF_ERROR, CONF_EVENT as CONF_EVENT, CONF_EVENT_DATA as CONF_EVENT_DATA, CONF_EVENT_DATA_TEMPLATE as CONF_EVENT_DATA_TEMPLATE, CONF_FOR_EACH as CONF_FOR_EACH, CONF_IF as CONF_IF, CONF_MODE as CONF_MODE, CONF_PARALLEL as CONF_PARALLEL, CONF_REPEAT as CONF_REPEAT, CONF_RESPONSE_VARIABLE as CONF_RESPONSE_VARIABLE, CONF_SCENE as CONF_SCENE, CONF_SEQUENCE as CONF_SEQUENCE, CONF_SERVICE as CONF_SERVICE, CONF_SERVICE_DATA as CONF_SERVICE_DATA, CONF_SERVICE_DATA_TEMPLATE as CONF_SERVICE_DATA_TEMPLATE, CONF_SET_CONVERSATION_RESPONSE as CONF_SET_CONVERSATION_RESPONSE, CONF_STOP as CONF_STOP, CONF_TARGET as CONF_TARGET, CONF_THEN as CONF_THEN, CONF_TIMEOUT as CONF_TIMEOUT, CONF_UNTIL as CONF_UNTIL, CONF_VARIABLES as CONF_VARIABLES, CONF_WAIT_FOR_TRIGGER as CONF_WAIT_FOR_TRIGGER, CONF_WAIT_TEMPLATE as CONF_WAIT_TEMPLATE, CONF_WHILE as CONF_WHILE, EVENT_HOMEASSISTANT_STOP as EVENT_HOMEASSISTANT_STOP, SERVICE_TURN_ON as SERVICE_TURN_ON
from homeassistant.core import Context as Context, Event as Event, HassJob as HassJob, HomeAssistant as HomeAssistant, ServiceResponse as ServiceResponse, State as State, SupportsResponse as SupportsResponse, callback as callback
from homeassistant.util import slugify as slugify
from homeassistant.util.async_ import create_eager_task as create_eager_task
from homeassistant.util.dt import utcnow as utcnow
from homeassistant.util.hass_dict import HassKey as HassKey
from homeassistant.util.signal_type import SignalType as SignalType, SignalTypeFormat as SignalTypeFormat
from types import MappingProxyType
from typing import Any, Literal, TypedDict, overload

SCRIPT_MODE_PARALLEL: str
SCRIPT_MODE_QUEUED: str
SCRIPT_MODE_RESTART: str
SCRIPT_MODE_SINGLE: str
SCRIPT_MODE_CHOICES: Incomplete
DEFAULT_SCRIPT_MODE = SCRIPT_MODE_SINGLE
CONF_MAX: str
DEFAULT_MAX: int
CONF_MAX_EXCEEDED: str
_MAX_EXCEEDED_CHOICES: Incomplete
DEFAULT_MAX_EXCEEDED: str
ATTR_CUR: str
ATTR_MAX: str
DATA_SCRIPTS: HassKey[list[ScriptData]]
DATA_SCRIPT_BREAKPOINTS: HassKey[dict[str, dict[str, set[str]]]]
DATA_NEW_SCRIPT_RUNS_NOT_ALLOWED: HassKey[None]
RUN_ID_ANY: str
NODE_ANY: str
_LOGGER: Incomplete
_LOG_EXCEPTION: Incomplete
_TIMEOUT_MSG: str
_SHUTDOWN_MAX_WAIT: int
ACTION_TRACE_NODE_MAX_LEN: int
SCRIPT_BREAKPOINT_HIT: Incomplete
SCRIPT_DEBUG_CONTINUE_STOP: SignalTypeFormat[Literal['continue', 'stop']]
SCRIPT_DEBUG_CONTINUE_ALL: str
script_stack_cv: ContextVar[list[str] | None]

class ScriptData(TypedDict):
    instance: Script
    started_before_shutdown: bool

class ScriptStoppedError(Exception): ...

def _set_result_unless_done(future: asyncio.Future[None]) -> None: ...
def action_trace_append(variables: dict[str, Any], path: str) -> TraceElement: ...
async def trace_action(hass: HomeAssistant, script_run: _ScriptRun, stop: asyncio.Future[None], variables: dict[str, Any]) -> AsyncGenerator[TraceElement]: ...
def make_script_schema(schema: Mapping[Any, Any], default_script_mode: str, extra: int = ...) -> vol.Schema: ...

STATIC_VALIDATION_ACTION_TYPES: Incomplete
REPEAT_WARN_ITERATIONS: int
REPEAT_TERMINATE_ITERATIONS: int

async def async_validate_actions_config(hass: HomeAssistant, actions: list[ConfigType]) -> list[ConfigType]: ...
async def async_validate_action_config(hass: HomeAssistant, config: ConfigType) -> ConfigType: ...

class _HaltScript(Exception): ...
class _AbortScript(_HaltScript): ...
class _ConditionFail(_HaltScript): ...

class _StopScript(_HaltScript):
    response: Incomplete
    def __init__(self, message: str, response: Any) -> None: ...

class _ScriptRun:
    _action: dict[str, Any]
    _hass: Incomplete
    _script: Incomplete
    _variables: Incomplete
    _context: Incomplete
    _log_exceptions: Incomplete
    _step: int
    _started: bool
    _stop: Incomplete
    _stopped: Incomplete
    _conversation_response: Incomplete
    def __init__(self, hass: HomeAssistant, script: Script, variables: dict[str, Any], context: Context | None, log_exceptions: bool) -> None: ...
    def _changed(self) -> None: ...
    async def _async_get_condition(self, config: ConfigType) -> ConditionCheckerType: ...
    def _log(self, msg: str, *args: Any, level: int = ..., **kwargs: Any) -> None: ...
    def _step_log(self, default_message: str, timeout: float | None = None) -> None: ...
    async def async_run(self) -> ScriptRunResult | None: ...
    async def _async_step(self, log_exceptions: bool) -> None: ...
    def _finish(self) -> None: ...
    async def async_stop(self) -> None: ...
    def _handle_exception(self, exception: Exception, continue_on_error: bool, log_exceptions: bool) -> None: ...
    def _log_exception(self, exception: Exception) -> None: ...
    def _get_pos_time_period_template(self, key: str) -> timedelta: ...
    async def _async_delay_step(self) -> None: ...
    def _get_timeout_seconds_from_action(self) -> float | None: ...
    async def _async_wait_template_step(self) -> None: ...
    def _async_set_remaining_time_var(self, timeout_handle: asyncio.TimerHandle | None) -> None: ...
    async def _async_run_long_action(self, long_task: asyncio.Task[_T]) -> _T | None: ...
    async def _async_call_service_step(self) -> None: ...
    async def _async_device_step(self) -> None: ...
    async def _async_scene_step(self) -> None: ...
    async def _async_event_step(self) -> None: ...
    async def _async_condition_step(self) -> None: ...
    def _test_conditions(self, conditions: list[ConditionCheckerType], name: str, condition_path: str | None = None) -> bool | None: ...
    async def _async_repeat_step(self) -> None: ...
    async def _async_choose_step(self) -> None: ...
    async def _async_if_step(self) -> None: ...
    @overload
    def _async_futures_with_timeout(self, timeout: float) -> tuple[list[asyncio.Future[None]], asyncio.TimerHandle, asyncio.Future[None]]: ...
    @overload
    def _async_futures_with_timeout(self, timeout: None) -> tuple[list[asyncio.Future[None]], None, None]: ...
    async def _async_wait_for_trigger_step(self) -> None: ...
    def _async_handle_timeout(self) -> None: ...
    async def _async_wait_with_optional_timeout(self, futures: list[asyncio.Future[None]], timeout_handle: asyncio.TimerHandle | None, timeout_future: asyncio.Future[None] | None, unsub: Callable[[], None]) -> None: ...
    async def _async_variables_step(self) -> None: ...
    async def _async_set_conversation_response_step(self) -> None: ...
    async def _async_stop_step(self) -> None: ...
    async def _async_sequence_step(self) -> None: ...
    async def _async_parallel_step(self) -> None: ...
    async def _async_run_script(self, script: Script) -> None: ...

class _QueuedScriptRun(_ScriptRun):
    lock_acquired: bool
    async def async_run(self) -> None: ...
    def _finish(self) -> None: ...

def _schedule_stop_scripts_after_shutdown(hass: HomeAssistant) -> None: ...
async def _async_stop_scripts_after_shutdown(hass: HomeAssistant, point_in_time: datetime) -> None: ...
async def _async_stop_scripts_at_shutdown(hass: HomeAssistant, event: Event) -> None: ...
_VarsType = dict[str, Any] | MappingProxyType[str, Any]

def _referenced_extract_ids(data: Any, key: str, found: set[str]) -> None: ...

class _ChooseData(TypedDict):
    choices: list[tuple[list[ConditionCheckerType], Script]]
    default: Script | None

class _IfData(TypedDict):
    if_conditions: list[ConditionCheckerType]
    if_then: Script
    if_else: Script | None

@dataclass
class ScriptRunResult:
    conversation_response: str | None | UndefinedType
    service_response: ServiceResponse
    variables: dict[str, Any]
    def __init__(self, conversation_response, service_response, variables) -> None: ...

class Script:
    top_level: Incomplete
    _hass: Incomplete
    sequence: Incomplete
    name: Incomplete
    unique_id: Incomplete
    domain: Incomplete
    running_description: Incomplete
    _change_listener: Incomplete
    _change_listener_job: Incomplete
    script_mode: Incomplete
    _log_exceptions: Incomplete
    last_action: Incomplete
    last_triggered: Incomplete
    _runs: Incomplete
    max_runs: Incomplete
    _max_exceeded: Incomplete
    _queue_lck: Incomplete
    _config_cache: Incomplete
    _repeat_script: Incomplete
    _choose_data: Incomplete
    _if_data: Incomplete
    _parallel_scripts: Incomplete
    _sequence_scripts: Incomplete
    variables: Incomplete
    _variables_dynamic: Incomplete
    _copy_variables_on_run: Incomplete
    def __init__(self, hass: HomeAssistant, sequence: Sequence[dict[str, Any]], name: str, domain: str, *, change_listener: Callable[[], Any] | None = None, copy_variables: bool = False, log_exceptions: bool = True, logger: logging.Logger | None = None, max_exceeded: str = ..., max_runs: int = ..., running_description: str | None = None, script_mode: str = ..., top_level: bool = True, variables: ScriptVariables | None = None) -> None: ...
    @property
    def change_listener(self) -> Callable[..., Any] | None: ...
    @change_listener.setter
    def change_listener(self, change_listener: Callable[[], Any]) -> None: ...
    _logger: Incomplete
    def _set_logger(self, logger: logging.Logger | None = None) -> None: ...
    def update_logger(self, logger: logging.Logger | None = None) -> None: ...
    def _changed(self) -> None: ...
    def _chain_change_listener(self, sub_script: Script) -> None: ...
    @property
    def is_running(self) -> bool: ...
    @property
    def runs(self) -> int: ...
    @property
    def supports_max(self) -> bool: ...
    @cached_property
    def referenced_labels(self) -> set[str]: ...
    @cached_property
    def referenced_floors(self) -> set[str]: ...
    @cached_property
    def referenced_areas(self) -> set[str]: ...
    @staticmethod
    def _find_referenced_target(target: Literal['area_id', 'floor_id', 'label_id'], referenced: set[str], sequence: Sequence[dict[str, Any]]) -> None: ...
    @cached_property
    def referenced_devices(self) -> set[str]: ...
    @staticmethod
    def _find_referenced_devices(referenced: set[str], sequence: Sequence[dict[str, Any]]) -> None: ...
    @cached_property
    def referenced_entities(self) -> set[str]: ...
    @staticmethod
    def _find_referenced_entities(referenced: set[str], sequence: Sequence[dict[str, Any]]) -> None: ...
    def run(self, variables: _VarsType | None = None, context: Context | None = None) -> None: ...
    async def async_run(self, run_variables: _VarsType | None = None, context: Context | None = None, started_action: Callable[..., Any] | None = None) -> ScriptRunResult | None: ...
    async def _async_stop(self, aws: list[asyncio.Task[None]], update_state: bool) -> None: ...
    async def async_stop(self, update_state: bool = True, spare: _ScriptRun | None = None) -> None: ...
    async def _async_get_condition(self, config: ConfigType) -> ConditionCheckerType: ...
    def _prep_repeat_script(self, step: int) -> Script: ...
    def _get_repeat_script(self, step: int) -> Script: ...
    async def _async_prep_choose_data(self, step: int) -> _ChooseData: ...
    async def _async_get_choose_data(self, step: int) -> _ChooseData: ...
    async def _async_prep_if_data(self, step: int) -> _IfData: ...
    async def _async_get_if_data(self, step: int) -> _IfData: ...
    async def _async_prep_parallel_scripts(self, step: int) -> list[Script]: ...
    async def _async_get_parallel_scripts(self, step: int) -> list[Script]: ...
    async def _async_prep_sequence_script(self, step: int) -> Script: ...
    async def _async_get_sequence_script(self, step: int) -> Script: ...
    def _log(self, msg: str, *args: Any, level: int = ..., **kwargs: Any) -> None: ...

def breakpoint_clear(hass: HomeAssistant, key: str, run_id: str | None, node: str) -> None: ...
def breakpoint_clear_all(hass: HomeAssistant) -> None: ...
def breakpoint_set(hass: HomeAssistant, key: str, run_id: str | None, node: str) -> None: ...
def breakpoint_list(hass: HomeAssistant) -> list[dict[str, Any]]: ...
def debug_continue(hass: HomeAssistant, key: str, run_id: str) -> None: ...
def debug_step(hass: HomeAssistant, key: str, run_id: str) -> None: ...
def debug_stop(hass: HomeAssistant, key: str, run_id: str) -> None: ...
