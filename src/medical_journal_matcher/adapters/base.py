from __future__ import annotations

from collections.abc import Mapping, Sequence
from typing import Any, Protocol


class ArticleSearchAdapter(Protocol):
    """Search using only a pre-approved structured outbound query."""

    source_name: str

    async def search(self, query: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]: ...


class JournalFactAdapter(Protocol):
    """Return sourced journal facts without deciding gates or scores."""

    source_name: str

    async def fetch(self, journal_identity: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]: ...


class JcrAdapter(Protocol):
    """Read licensed or authorized user JCR facts through a replaceable boundary."""

    mode: str

    def lookup(self, journal_identity: Mapping[str, Any]) -> Sequence[Mapping[str, Any]]: ...
