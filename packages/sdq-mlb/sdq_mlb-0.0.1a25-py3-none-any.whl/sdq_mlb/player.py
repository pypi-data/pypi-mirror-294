from __future__ import annotations
import asyncio
from functools import cached_property
import json
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, ClassVar, Coroutine, TypedDict, overload
import httpx
from .baseball_savant import (
    Client,
    HittingStats,
    PitchingStats,
    StacastRanking,
    StatCast,
)
from .types import PlayerDict
from .db import Client as DBClient

if TYPE_CHECKING:
    from .db import Player as DBPlayer


__all__: list[str] = ["Player", "PlayerDict"]


@dataclass
class Player:

    SEP: ClassVar[str] = ", "
    BASE_URL: ClassVar[str] = "https://baseballsavant.mlb.com/savant-player/"

    def __init__(
        self,
        id: str,
        fullname: str,
        semaphore: asyncio.Semaphore = asyncio.Semaphore(100),
    ) -> None:
        if self.SEP not in fullname:
            raise ValueError("Not a player")
        self.id: int = int(id)
        self.fullname: str = fullname
        self.semaphore: asyncio.Semaphore = semaphore
        self.client: Client = Client(self)
        self._hitting: dict[str, HittingStats] = {}
        self._pitching: dict[str, PitchingStats] = {}
        self._ranking: dict[str, StacastRanking] = {}

    @property
    def firstname(self) -> str:
        return self.fullname.split(self.SEP)[-1]

    @property
    def lastname(self) -> str:
        return self.fullname.split(self.SEP)[0]

    @property
    def slug(self) -> str:
        return "-".join([self.firstname, self.lastname, str(self.id)]).lower()

    @property
    def url(self) -> str:
        return f"{self.BASE_URL}{self.slug}"

    def get_statcast(self) -> StatCast:
        return self.statcast

    @property
    def statcast(self) -> StatCast:
        return {
            "hitting": self.hitting,
            "pitching": self.pitching,
            "ranking": self.ranking,
        }

    @property
    def pitching(self) -> dict[str, PitchingStats]:
        if not self._pitching:
            self._pitching = self.client.get_pitching()
        return self._pitching

    @property
    def hitting(self) -> dict[str, HittingStats]:
        if not self._hitting:
            self._hitting = self.client.get_hitting()
        return self._hitting

    @property
    def ranking(self) -> dict[str, StacastRanking]:
        if not self._ranking:
            self._ranking = self.client.get_ranking()
        return self._ranking

    def __repr__(self) -> str:
        return (
            f'<Player(id={self.id}, lastname="{self.lastname}", '
            f'firstname="{self.firstname}")>'
        )

    def to_dict(self) -> PlayerDict:
        return {
            "id": self.id,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "slug": self.slug,
            "url": self.url,
            "statcast": self.statcast,
        }

    def to_json(self, file: Path | None = None) -> bytes:
        data: bytes = json.dumps(self.to_dict()).encode("utf-8")
        if file:
            file.write_bytes(data)
        return data

    @overload
    def get_stats(self) -> Player: ...

    @overload
    async def get_stats(self, session: httpx.AsyncClient) -> Player: ...

    def get_stats(
        self, session: httpx.AsyncClient | None = None
    ) -> Player | Coroutine[Any, Any, Player]:
        if session is not None:
            return self.client.get_stats(session)
        else:
            return self.client.get_stats_sync()

    @cached_property
    def stored(self) -> DBPlayer | None:
        return DBClient().get_player(self)
