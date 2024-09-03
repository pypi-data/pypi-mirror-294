from _typeshed import Incomplete
from collections.abc import Callable as Callable, Coroutine
from dataclasses import dataclass
from enum import Enum
from homeassistant.helpers.entity import EntityDescription as EntityDescription
from typing import Any, Generic, TypeVar
from uiprotect.data import Event as Event, NVR, ProtectAdoptableDeviceModel, SmartDetectObjectType as SmartDetectObjectType

_LOGGER: Incomplete
T = TypeVar('T', bound=ProtectAdoptableDeviceModel | NVR)

class PermRequired(int, Enum):
    NO_WRITE = 1
    WRITE = 2
    DELETE = 3

@dataclass(frozen=True, kw_only=True)
class ProtectEntityDescription(EntityDescription, Generic[T]):
    ufp_required_field: str | None = ...
    ufp_value: str | None = ...
    ufp_value_fn: Callable[[T], Any] | None = ...
    ufp_enabled: str | None = ...
    ufp_perm: PermRequired | None = ...
    has_required: Callable[[T], bool] = ...
    get_ufp_enabled: Callable[[T], bool] | None = ...
    def get_ufp_value(self, obj: T) -> Any: ...
    def __post_init__(self) -> None: ...
    def __init__(self, *, key, device_class=..., entity_category=..., entity_registry_enabled_default=..., entity_registry_visible_default=..., force_update=..., icon=..., has_entity_name=..., name=..., translation_key=..., translation_placeholders=..., unit_of_measurement=..., ufp_required_field=..., ufp_value=..., ufp_value_fn=..., ufp_enabled=..., ufp_perm=..., has_required=..., get_ufp_enabled=...) -> None: ...

@dataclass(frozen=True, kw_only=True)
class ProtectEventMixin(ProtectEntityDescription[T]):
    ufp_event_obj: str | None = ...
    ufp_obj_type: SmartDetectObjectType | None = ...
    def get_event_obj(self, obj: T) -> Event | None: ...
    def has_matching_smart(self, event: Event) -> bool: ...
    def __post_init__(self) -> None: ...
    def __init__(self, *, key, device_class=..., entity_category=..., entity_registry_enabled_default=..., entity_registry_visible_default=..., force_update=..., icon=..., has_entity_name=..., name=..., translation_key=..., translation_placeholders=..., unit_of_measurement=..., ufp_required_field=..., ufp_value=..., ufp_value_fn=..., ufp_enabled=..., ufp_perm=..., has_required=..., get_ufp_enabled=..., ufp_event_obj=..., ufp_obj_type=...) -> None: ...

@dataclass(frozen=True, kw_only=True)
class ProtectSetableKeysMixin(ProtectEntityDescription[T]):
    ufp_set_method: str | None = ...
    ufp_set_method_fn: Callable[[T, Any], Coroutine[Any, Any, None]] | None = ...
    async def ufp_set(self, obj: T, value: Any) -> None: ...
    def __init__(self, *, key, device_class=..., entity_category=..., entity_registry_enabled_default=..., entity_registry_visible_default=..., force_update=..., icon=..., has_entity_name=..., name=..., translation_key=..., translation_placeholders=..., unit_of_measurement=..., ufp_required_field=..., ufp_value=..., ufp_value_fn=..., ufp_enabled=..., ufp_perm=..., has_required=..., get_ufp_enabled=..., ufp_set_method=..., ufp_set_method_fn=...) -> None: ...
