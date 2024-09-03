from .const import DOMAIN as DOMAIN
from .device_info import NestDeviceInfo as NestDeviceInfo, async_nest_devices_by_device_id as async_nest_devices_by_device_id
from .events import EVENT_NAME_MAP as EVENT_NAME_MAP, MEDIA_SOURCE_EVENT_TITLE_MAP as MEDIA_SOURCE_EVENT_TITLE_MAP
from _typeshed import Incomplete
from collections.abc import Mapping
from dataclasses import dataclass
from google_nest_sdm.device import Device as Device
from google_nest_sdm.event import ImageEventBase as ImageEventBase
from google_nest_sdm.event_media import ClipPreviewSession as ClipPreviewSession, EventMediaStore, ImageSession as ImageSession
from google_nest_sdm.google_nest_subscriber import GoogleNestSubscriber as GoogleNestSubscriber
from google_nest_sdm.transcoder import Transcoder
from homeassistant.components.ffmpeg import get_ffmpeg_manager as get_ffmpeg_manager
from homeassistant.components.media_player import BrowseError as BrowseError, MediaClass as MediaClass, MediaType as MediaType
from homeassistant.components.media_source.error import Unresolvable as Unresolvable
from homeassistant.components.media_source.models import BrowseMediaSource as BrowseMediaSource, MediaSource as MediaSource, MediaSourceItem as MediaSourceItem, PlayMedia as PlayMedia
from homeassistant.core import HomeAssistant as HomeAssistant, callback as callback
from homeassistant.helpers.storage import Store as Store
from homeassistant.helpers.template import DATE_STR_FORMAT as DATE_STR_FORMAT
from typing import Any

_LOGGER: Incomplete
MEDIA_SOURCE_TITLE: str
DEVICE_TITLE_FORMAT: str
CLIP_TITLE_FORMAT: str
EVENT_MEDIA_API_URL_FORMAT: str
EVENT_THUMBNAIL_URL_FORMAT: str
STORAGE_KEY: str
STORAGE_VERSION: int
STORAGE_SAVE_DELAY_SECONDS: int
MEDIA_PATH: Incomplete
DISK_READ_LRU_MAX_SIZE: int

async def async_get_media_event_store(hass: HomeAssistant, subscriber: GoogleNestSubscriber) -> EventMediaStore: ...
async def async_get_transcoder(hass: HomeAssistant) -> Transcoder: ...

class NestEventMediaStore(EventMediaStore):
    _hass: Incomplete
    _subscriber: Incomplete
    _store: Incomplete
    _media_path: Incomplete
    _data: Incomplete
    _devices: Incomplete
    def __init__(self, hass: HomeAssistant, subscriber: GoogleNestSubscriber, store: Store[dict[str, Any]], media_path: str) -> None: ...
    async def async_load(self) -> dict | None: ...
    async def async_save(self, data: dict) -> None: ...
    def get_media_key(self, device_id: str, event: ImageEventBase) -> str: ...
    def _map_device_id(self, device_id: str) -> str: ...
    def get_image_media_key(self, device_id: str, event: ImageEventBase) -> str: ...
    def get_clip_preview_media_key(self, device_id: str, event: ImageEventBase) -> str: ...
    def get_clip_preview_thumbnail_media_key(self, device_id: str, event: ImageEventBase) -> str: ...
    def get_media_filename(self, media_key: str) -> str: ...
    async def async_load_media(self, media_key: str) -> bytes | None: ...
    async def async_save_media(self, media_key: str, content: bytes) -> None: ...
    async def async_remove_media(self, media_key: str) -> None: ...
    async def _get_devices(self) -> Mapping[str, str]: ...

async def async_get_media_source(hass: HomeAssistant) -> MediaSource: ...
def async_get_media_source_devices(hass: HomeAssistant) -> Mapping[str, Device]: ...

@dataclass
class MediaId:
    device_id: str
    event_token: str | None = ...
    @property
    def identifier(self) -> str: ...
    def __init__(self, device_id, event_token=...) -> None: ...

def parse_media_id(identifier: str | None = None) -> MediaId | None: ...

class NestMediaSource(MediaSource):
    name: str
    hass: Incomplete
    def __init__(self, hass: HomeAssistant) -> None: ...
    async def async_resolve_media(self, item: MediaSourceItem) -> PlayMedia: ...
    async def async_browse_media(self, item: MediaSourceItem) -> BrowseMediaSource: ...

async def _async_get_clip_preview_sessions(device: Device) -> dict[str, ClipPreviewSession]: ...
async def _async_get_image_sessions(device: Device) -> dict[str, ImageSession]: ...
def _browse_root() -> BrowseMediaSource: ...
async def _async_get_recent_event_id(device_id: MediaId, device: Device) -> MediaId | None: ...
def _browse_device(device_id: MediaId, device: Device) -> BrowseMediaSource: ...
def _browse_clip_preview(event_id: MediaId, device: Device, event: ClipPreviewSession) -> BrowseMediaSource: ...
def _browse_image_event(event_id: MediaId, device: Device, event: ImageSession) -> BrowseMediaSource: ...
