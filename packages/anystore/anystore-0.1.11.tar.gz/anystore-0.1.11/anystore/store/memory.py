"""
Simple memory dictionary store
"""

from datetime import datetime, timedelta
from typing import Any, Generator

from anystore.exceptions import DoesNotExist
from anystore.logging import get_logger
from anystore.store.base import BaseStore
from anystore.types import Value


log = get_logger(__name__)


class MemoryStore(BaseStore):
    def __init__(self, **data):
        super().__init__(**data)
        self._store: dict[str, Any] = {}
        self._ttl: dict[str, datetime] = {}

    def _write(self, key: str, value: Value, **kwargs) -> None:
        self._store[key] = value
        ttl = kwargs.get("ttl")
        if ttl:
            self._ttl[key] = datetime.now() + timedelta(seconds=ttl)

    def _read(self, key: str, raise_on_nonexist: bool | None = True, **kwargs) -> Any:
        self._check_ttl(key)
        # `None` could be stored as an actual value, to implement `raise_on_nonexist`
        # we need to check this first:
        if raise_on_nonexist and not self._exists(key):
            raise DoesNotExist
        res = self._store.get(key)
        # mimic fs read mode:
        if kwargs.get("mode") == "r" and isinstance(res, bytes):
            res = res.decode()
        return res

    def _exists(self, key: str) -> bool:
        self._check_ttl(key)
        return key in self._store

    def _delete(self, key: str) -> None:
        self._store.pop(key, None)

    def _get_key_prefix(self) -> str:
        return "anystore"

    def _iterate_keys(self, prefix: str | None = None) -> Generator[str, None, None]:
        prefix = self.get_key(prefix or "")
        key_prefix = self._get_key_prefix()
        for key in self._store:
            if key.startswith(prefix):
                yield key[len(key_prefix) + 1 :]

    def _check_ttl(self, key: str) -> None:
        ttl = self._ttl.get(key)
        if ttl and datetime.now() > ttl:
            self._delete(key)
