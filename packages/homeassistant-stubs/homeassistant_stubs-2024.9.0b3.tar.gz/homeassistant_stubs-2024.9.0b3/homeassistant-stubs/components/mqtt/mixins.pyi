import abc
import voluptuous as vol
from . import debug_info as debug_info, subscription as subscription
from .client import async_publish as async_publish
from .const import ATTR_DISCOVERY_HASH as ATTR_DISCOVERY_HASH, ATTR_DISCOVERY_PAYLOAD as ATTR_DISCOVERY_PAYLOAD, ATTR_DISCOVERY_TOPIC as ATTR_DISCOVERY_TOPIC, AVAILABILITY_ALL as AVAILABILITY_ALL, AVAILABILITY_ANY as AVAILABILITY_ANY, CONF_AVAILABILITY as CONF_AVAILABILITY, CONF_AVAILABILITY_MODE as CONF_AVAILABILITY_MODE, CONF_AVAILABILITY_TEMPLATE as CONF_AVAILABILITY_TEMPLATE, CONF_AVAILABILITY_TOPIC as CONF_AVAILABILITY_TOPIC, CONF_CONFIGURATION_URL as CONF_CONFIGURATION_URL, CONF_CONNECTIONS as CONF_CONNECTIONS, CONF_ENABLED_BY_DEFAULT as CONF_ENABLED_BY_DEFAULT, CONF_ENCODING as CONF_ENCODING, CONF_HW_VERSION as CONF_HW_VERSION, CONF_IDENTIFIERS as CONF_IDENTIFIERS, CONF_JSON_ATTRS_TEMPLATE as CONF_JSON_ATTRS_TEMPLATE, CONF_JSON_ATTRS_TOPIC as CONF_JSON_ATTRS_TOPIC, CONF_MANUFACTURER as CONF_MANUFACTURER, CONF_OBJECT_ID as CONF_OBJECT_ID, CONF_PAYLOAD_AVAILABLE as CONF_PAYLOAD_AVAILABLE, CONF_PAYLOAD_NOT_AVAILABLE as CONF_PAYLOAD_NOT_AVAILABLE, CONF_QOS as CONF_QOS, CONF_RETAIN as CONF_RETAIN, CONF_SCHEMA as CONF_SCHEMA, CONF_SERIAL_NUMBER as CONF_SERIAL_NUMBER, CONF_SUGGESTED_AREA as CONF_SUGGESTED_AREA, CONF_SW_VERSION as CONF_SW_VERSION, CONF_TOPIC as CONF_TOPIC, CONF_VIA_DEVICE as CONF_VIA_DEVICE, DEFAULT_ENCODING as DEFAULT_ENCODING, DOMAIN as DOMAIN, MQTT_CONNECTION_STATE as MQTT_CONNECTION_STATE
from .debug_info import log_message as log_message
from .discovery import MQTTDiscoveryPayload as MQTTDiscoveryPayload, MQTT_DISCOVERY_DONE as MQTT_DISCOVERY_DONE, MQTT_DISCOVERY_NEW as MQTT_DISCOVERY_NEW, MQTT_DISCOVERY_UPDATED as MQTT_DISCOVERY_UPDATED, clear_discovery_hash as clear_discovery_hash, set_discovery_hash as set_discovery_hash
from .models import DATA_MQTT as DATA_MQTT, MessageCallbackType as MessageCallbackType, MqttValueTemplate as MqttValueTemplate, MqttValueTemplateException as MqttValueTemplateException, PublishPayloadType as PublishPayloadType, ReceiveMessage as ReceiveMessage
from .subscription import EntitySubscription as EntitySubscription, async_prepare_subscribe_topics as async_prepare_subscribe_topics, async_subscribe_topics_internal as async_subscribe_topics_internal, async_unsubscribe_topics as async_unsubscribe_topics
from .util import mqtt_config_entry_enabled as mqtt_config_entry_enabled
from _typeshed import Incomplete
from abc import ABC, abstractmethod
from collections.abc import Callable as Callable, Coroutine
from homeassistant.config_entries import ConfigEntry as ConfigEntry
from homeassistant.const import ATTR_CONFIGURATION_URL as ATTR_CONFIGURATION_URL, ATTR_HW_VERSION as ATTR_HW_VERSION, ATTR_MANUFACTURER as ATTR_MANUFACTURER, ATTR_MODEL as ATTR_MODEL, ATTR_MODEL_ID as ATTR_MODEL_ID, ATTR_NAME as ATTR_NAME, ATTR_SERIAL_NUMBER as ATTR_SERIAL_NUMBER, ATTR_SUGGESTED_AREA as ATTR_SUGGESTED_AREA, ATTR_SW_VERSION as ATTR_SW_VERSION, ATTR_VIA_DEVICE as ATTR_VIA_DEVICE, CONF_DEVICE as CONF_DEVICE, CONF_ENTITY_CATEGORY as CONF_ENTITY_CATEGORY, CONF_ICON as CONF_ICON, CONF_MODEL as CONF_MODEL, CONF_MODEL_ID as CONF_MODEL_ID, CONF_NAME as CONF_NAME, CONF_UNIQUE_ID as CONF_UNIQUE_ID, CONF_VALUE_TEMPLATE as CONF_VALUE_TEMPLATE
from homeassistant.core import Event as Event, HassJobType as HassJobType, HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers.device_registry import DeviceEntry as DeviceEntry, DeviceInfo as DeviceInfo, EventDeviceRegistryUpdatedData as EventDeviceRegistryUpdatedData
from homeassistant.helpers.dispatcher import async_dispatcher_connect as async_dispatcher_connect, async_dispatcher_send as async_dispatcher_send
from homeassistant.helpers.entity import Entity as Entity, async_generate_entity_id as async_generate_entity_id
from homeassistant.helpers.entity_platform import AddEntitiesCallback as AddEntitiesCallback
from homeassistant.helpers.event import async_track_device_registry_updated_event as async_track_device_registry_updated_event, async_track_entity_registry_updated_event as async_track_entity_registry_updated_event
from homeassistant.helpers.issue_registry import IssueSeverity as IssueSeverity, async_create_issue as async_create_issue
from homeassistant.helpers.service_info.mqtt import ReceivePayloadType as ReceivePayloadType
from homeassistant.helpers.typing import ConfigType as ConfigType, DiscoveryInfoType as DiscoveryInfoType, UNDEFINED as UNDEFINED, UndefinedType as UndefinedType, VolSchemaType as VolSchemaType
from homeassistant.util.json import json_loads as json_loads
from typing import Any, Protocol

_LOGGER: Incomplete
MQTT_ATTRIBUTES_BLOCKED: Incomplete

class SetupEntity(Protocol):
    async def __call__(self, hass: HomeAssistant, async_add_entities: AddEntitiesCallback, config: ConfigType, config_entry: ConfigEntry, discovery_data: DiscoveryInfoType | None = None) -> None: ...

def async_handle_schema_error(discovery_payload: MQTTDiscoveryPayload, err: vol.Invalid) -> None: ...
def _handle_discovery_failure(hass: HomeAssistant, discovery_payload: MQTTDiscoveryPayload) -> None: ...
def _verify_mqtt_config_entry_enabled_for_discovery(hass: HomeAssistant, domain: str, discovery_payload: MQTTDiscoveryPayload) -> bool: ...

class _SetupNonEntityHelperCallbackProtocol(Protocol):
    async def __call__(self, config: ConfigType, discovery_data: DiscoveryInfoType) -> None: ...

def async_setup_non_entity_entry_helper(hass: HomeAssistant, domain: str, async_setup: _SetupNonEntityHelperCallbackProtocol, discovery_schema: vol.Schema) -> None: ...
def async_setup_entity_entry_helper(hass: HomeAssistant, entry: ConfigEntry, entity_class: type[MqttEntity] | None, domain: str, async_add_entities: AddEntitiesCallback, discovery_schema: VolSchemaType, platform_schema_modern: VolSchemaType, schema_class_mapping: dict[str, type[MqttEntity]] | None = None) -> None: ...
def init_entity_id_from_config(hass: HomeAssistant, entity: Entity, config: ConfigType, entity_id_format: str) -> None: ...

class MqttAttributesMixin(Entity):
    _attributes_extra_blocked: frozenset[str]
    _attr_tpl: Callable[[ReceivePayloadType], ReceivePayloadType] | None
    _attributes_sub_state: Incomplete
    _attributes_config: Incomplete
    def __init__(self, config: ConfigType) -> None: ...
    async def async_added_to_hass(self) -> None: ...
    def attributes_prepare_discovery_update(self, config: DiscoveryInfoType) -> None: ...
    async def attributes_discovery_update(self, config: DiscoveryInfoType) -> None: ...
    def _attributes_prepare_subscribe_topics(self) -> None: ...
    def _attributes_subscribe_topics(self) -> None: ...
    async def async_will_remove_from_hass(self) -> None: ...
    _attr_extra_state_attributes: Incomplete
    def _attributes_message_received(self, msg: ReceiveMessage) -> None: ...

class MqttAvailabilityMixin(Entity):
    _availability_sub_state: Incomplete
    _available: Incomplete
    _available_latest: bool
    def __init__(self, config: ConfigType) -> None: ...
    async def async_added_to_hass(self) -> None: ...
    def availability_prepare_discovery_update(self, config: DiscoveryInfoType) -> None: ...
    async def availability_discovery_update(self, config: DiscoveryInfoType) -> None: ...
    _avail_topics: Incomplete
    _avail_config: Incomplete
    def _availability_setup_from_config(self, config: ConfigType) -> None: ...
    def _availability_prepare_subscribe_topics(self) -> None: ...
    def _availability_message_received(self, msg: ReceiveMessage) -> None: ...
    def _availability_subscribe_topics(self) -> None: ...
    def async_mqtt_connection_state_changed(self, state: bool) -> None: ...
    async def async_will_remove_from_hass(self) -> None: ...
    @property
    def available(self) -> bool: ...

async def cleanup_device_registry(hass: HomeAssistant, device_id: str | None, config_entry_id: str | None) -> None: ...
def get_discovery_hash(discovery_data: DiscoveryInfoType) -> tuple[str, str]: ...
def send_discovery_done(hass: HomeAssistant, discovery_data: DiscoveryInfoType) -> None: ...
def stop_discovery_updates(hass: HomeAssistant, discovery_data: DiscoveryInfoType, remove_discovery_updated: Callable[[], None] | None = None) -> None: ...
async def async_remove_discovery_payload(hass: HomeAssistant, discovery_data: DiscoveryInfoType) -> None: ...
async def async_clear_discovery_topic_if_entity_removed(hass: HomeAssistant, discovery_data: DiscoveryInfoType, event: Event[er.EventEntityRegistryUpdatedData]) -> None: ...

class MqttDiscoveryDeviceUpdateMixin(ABC, metaclass=abc.ABCMeta):
    hass: Incomplete
    log_name: Incomplete
    _discovery_data: Incomplete
    _device_id: Incomplete
    _config_entry: Incomplete
    _config_entry_id: Incomplete
    _skip_device_removal: bool
    _remove_discovery_updated: Incomplete
    _remove_device_updated: Incomplete
    def __init__(self, hass: HomeAssistant, discovery_data: DiscoveryInfoType, device_id: str | None, config_entry: ConfigEntry, log_name: str) -> None: ...
    def _entry_unload(self, *_: Any) -> None: ...
    async def async_discovery_update(self, discovery_payload: MQTTDiscoveryPayload) -> None: ...
    async def _async_device_removed(self, event: Event[EventDeviceRegistryUpdatedData]) -> None: ...
    async def _async_tear_down(self) -> None: ...
    @abstractmethod
    async def async_update(self, discovery_data: MQTTDiscoveryPayload) -> None: ...
    @abstractmethod
    async def async_tear_down(self) -> None: ...

class MqttDiscoveryUpdateMixin(Entity):
    _discovery_data: Incomplete
    _discovery_update: Incomplete
    _remove_discovery_updated: Incomplete
    _removed_from_hass: bool
    _registry_hooks: Incomplete
    def __init__(self, hass: HomeAssistant, discovery_data: DiscoveryInfoType | None, discovery_update: Callable[[MQTTDiscoveryPayload], Coroutine[Any, Any, None]] | None = None) -> None: ...
    async def async_added_to_hass(self) -> None: ...
    async def _async_remove_state_and_registry_entry(self) -> None: ...
    async def _async_process_discovery_update(self, payload: MQTTDiscoveryPayload, discovery_update: Callable[[MQTTDiscoveryPayload], Coroutine[Any, Any, None]], discovery_data: DiscoveryInfoType) -> None: ...
    async def _async_process_discovery_update_and_remove(self) -> None: ...
    def _async_discovery_callback(self, payload: MQTTDiscoveryPayload) -> None: ...
    async def async_removed_from_registry(self) -> None: ...
    async def add_to_platform_finish(self) -> None: ...
    def add_to_platform_abort(self) -> None: ...
    async def async_will_remove_from_hass(self) -> None: ...
    def _cleanup_discovery_on_remove(self) -> None: ...

def device_info_from_specifications(specifications: dict[str, Any] | None) -> DeviceInfo | None: ...

class MqttEntityDeviceInfo(Entity):
    _device_specifications: Incomplete
    _config_entry: Incomplete
    def __init__(self, specifications: dict[str, Any] | None, config_entry: ConfigEntry) -> None: ...
    def device_info_discovery_update(self, config: DiscoveryInfoType) -> None: ...
    @property
    def device_info(self) -> DeviceInfo | None: ...

class MqttEntity(MqttAttributesMixin, MqttAvailabilityMixin, MqttDiscoveryUpdateMixin, MqttEntityDeviceInfo, metaclass=abc.ABCMeta):
    _attr_force_update: bool
    _attr_has_entity_name: bool
    _attr_should_poll: bool
    _default_name: str | None
    _entity_id_format: str
    hass: Incomplete
    _config: Incomplete
    _attr_unique_id: Incomplete
    _sub_state: Incomplete
    _discovery: Incomplete
    _subscriptions: Incomplete
    def __init__(self, hass: HomeAssistant, config: ConfigType, config_entry: ConfigEntry, discovery_data: DiscoveryInfoType | None) -> None: ...
    def _init_entity_id(self) -> None: ...
    async def async_added_to_hass(self) -> None: ...
    async def mqtt_async_added_to_hass(self) -> None: ...
    async def discovery_update(self, discovery_payload: MQTTDiscoveryPayload) -> None: ...
    async def async_will_remove_from_hass(self) -> None: ...
    async def async_publish(self, topic: str, payload: PublishPayloadType, qos: int = 0, retain: bool = False, encoding: str | None = ...) -> None: ...
    async def async_publish_with_config(self, topic: str, payload: PublishPayloadType) -> None: ...
    @staticmethod
    @abstractmethod
    def config_schema() -> VolSchemaType: ...
    _attr_name: Incomplete
    def _set_entity_name(self, config: ConfigType) -> None: ...
    _attr_entity_category: Incomplete
    _attr_entity_registry_enabled_default: Incomplete
    _attr_icon: Incomplete
    def _setup_common_attributes_from_config(self, config: ConfigType) -> None: ...
    def _setup_from_config(self, config: ConfigType) -> None: ...
    @abstractmethod
    def _prepare_subscribe_topics(self) -> None: ...
    @abstractmethod
    async def _subscribe_topics(self) -> None: ...
    def _attrs_have_changed(self, attrs_snapshot: tuple[tuple[str, Any | UndefinedType], ...]) -> bool: ...
    def _message_callback(self, msg_callback: MessageCallbackType, attributes: set[str] | None, msg: ReceiveMessage) -> None: ...
    def add_subscription(self, state_topic_config_key: str, msg_callback: Callable[[ReceiveMessage], None], tracked_attributes: set[str] | None, disable_encoding: bool = False) -> bool: ...

def update_device(hass: HomeAssistant, config_entry: ConfigEntry, config: ConfigType) -> str | None: ...
def async_removed_from_device(hass: HomeAssistant, event: Event[EventDeviceRegistryUpdatedData], mqtt_device_id: str, config_entry_id: str) -> bool: ...
