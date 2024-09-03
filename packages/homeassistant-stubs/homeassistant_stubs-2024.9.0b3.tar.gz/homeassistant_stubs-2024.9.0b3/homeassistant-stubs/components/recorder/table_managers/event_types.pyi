from . import BaseLRUTableManager as BaseLRUTableManager
from ..core import Recorder as Recorder
from ..db_schema import EventTypes as EventTypes
from ..queries import find_event_type_ids as find_event_type_ids
from ..tasks import RefreshEventTypesTask as RefreshEventTypesTask
from ..util import execute_stmt_lambda_element as execute_stmt_lambda_element
from _typeshed import Incomplete
from collections.abc import Iterable
from homeassistant.core import Event as Event
from homeassistant.util.collection import chunked_or_all as chunked_or_all
from homeassistant.util.event_type import EventType as EventType
from sqlalchemy.orm.session import Session as Session
from typing import Any

CACHE_SIZE: int

class EventTypeManager(BaseLRUTableManager[EventTypes]):
    active: bool
    _non_existent_event_types: Incomplete
    def __init__(self, recorder: Recorder) -> None: ...
    def load(self, events: list[Event], session: Session) -> None: ...
    def get(self, event_type: EventType[Any] | str, session: Session, from_recorder: bool = False) -> int | None: ...
    def get_many(self, event_types: Iterable[EventType[Any] | str], session: Session, from_recorder: bool = False) -> dict[EventType[Any] | str, int | None]: ...
    def add_pending(self, db_event_type: EventTypes) -> None: ...
    def post_commit_pending(self) -> None: ...
    def clear_non_existent(self, event_type: EventType[Any] | str) -> None: ...
    def evict_purged(self, event_types: Iterable[str]) -> None: ...
