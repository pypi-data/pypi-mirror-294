import asyncio
import json
import sys
from collections import UserDict
from concurrent.futures import ThreadPoolExecutor
from functools import cached_property
from pathlib import Path
from typing import Any, ClassVar, Coroutine, Literal, overload
import httpx
import polars as pl
from bs4 import BeautifulSoup
from . import Player, PlayerDict
from .baseball_savant import StatCast
from .db import Client as DBClient
from .df import PlayerDataFrame


__all__: list[str] = ["Players"]


if sys.version_info >= (3, 12):
    from typing import Self
else:
    from typing_extensions import Self


class Players(UserDict):

    BASE_URL: ClassVar[str] = "http://baseballsavant.mlb.com/"
    MLB_SEARCH: ClassVar[str] = BASE_URL + "statcast_search"
    MAX_SIMULTANOUS_HTTP_CALLS: ClassVar[int] = 10

    def __init__(
        self, dbfile: Path | None = None, stdout: bool = True, *args: Any, **kwargs: Any
    ) -> None:
        self.data: dict[int, Player]
        self._by_slug: dict[str, Player] = {}
        self.semaphore: asyncio.Semaphore = asyncio.Semaphore(
            self.MAX_SIMULTANOUS_HTTP_CALLS
        )
        self.db_path: Path | None = dbfile
        self.stdout: bool = stdout
        super().__init__(self, *args, **kwargs)

    @overload
    def fetch(self, stats: Literal[False] = False, from_db: bool = False) -> Self: ...

    @overload
    async def fetch(
        self, stats: Literal[True] = True, from_db: bool = False
    ) -> Self: ...

    @overload
    async def fetch(
        self, stats: bool = True, from_db: Literal[True] = True
    ) -> Self: ...

    def fetch(
        self, stats: bool = False, from_db: bool = True
    ) -> Self | Coroutine[Any, Any, Self]:
        if from_db:
            return self._read_db()
        if self.db_path:
            DBClient(self.db_path).create_tables()
        if stats:
            return self._async_fetch()
        else:
            return self._fetch()
        return self

    async def _async_fetch(self) -> Self:
        tasks: list[Coroutine] = []

        async def get_stats(player: Player, session: httpx.AsyncClient) -> Player:
            if self.stdout:
                print(f"{player.slug:>35s}: downloading data")
            player.semaphore = self.semaphore
            return await player.get_stats(session)

        self._fetch()

        async with httpx.AsyncClient() as session:
            for player in self.data.values():
                tasks.append(get_stats(player, session))
            await asyncio.gather(*tasks)

        def parse_html(player: Player) -> StatCast:
            if self.stdout:
                print(f"{player.slug:>35s}: computing stats")
            player.get_statcast()
            insert_into_db(player)
            return player.statcast

        def insert_into_db(player: Player) -> None:
            if self.db_path:
                if self.stdout:
                    print(f"{player.slug:>35s}: inserting in db")
                DBClient(self.db_path).insert_player(player, fail_safe=True)

        with ThreadPoolExecutor() as executor:
            loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
            soup_tasks = [
                loop.run_in_executor(executor, parse_html, player)
                for player in self.data.values()
            ]
            await asyncio.gather(*soup_tasks)

        return self

    def _fetch(self) -> Self:
        home: httpx.Response = httpx.get(self.MLB_SEARCH, follow_redirects=True)
        home.raise_for_status()
        return self._parse_bs4(BeautifulSoup(home.content, "html.parser"))

    def _parse_bs4(self, soup: BeautifulSoup) -> Self:
        for player in soup.find_all("option"):
            try:
                self.add(
                    Player(
                        id=player.attrs["value"],
                        fullname=player.text.strip().split("\n")[-1].strip(),
                    )
                )
            except (KeyError, ValueError):
                continue
        return self

    def add(self, player: Player) -> Self:
        self.data[player.id] = player
        self._by_slug[player.slug] = player
        return self

    def get_one(
        self,
        *,
        firstname: str = "",
        lastname: str = "",
        id: int = 0,
        strict: bool = False,
    ) -> Player | None:
        if id:
            return super().get(id)
        if firstname or lastname:
            results: list[Player] = []
            for player in self[lastname]:
                if strict and self._search_by(player, firstname, strict=True):
                    results.append(player)
                else:
                    if self._search_by(player, firstname):
                        results.append(player)
            if len(results) > 1:
                raise ValueError(f"Multiple players for the search: {len(results)}")
            elif len(results) == 1:
                return results[0]
            else:
                return None

    def get_all(
        self,
        *,
        firstname: str = "",
        lastname: str = "",
        id: int = 0,
        strict: bool = False,
    ) -> list[Player]:
        if id:
            if player := self.get_one(id=id):
                return [player]
        if firstname or lastname:
            players: list[Player] = self[lastname]
            if strict:
                return [
                    player
                    for player in players
                    if self._search_by(player, firstname, strict=True)
                ]
            return [player for player in players if self._search_by(player, firstname)]
        return []

    @staticmethod
    def _search_by(
        player: Player, value: str, *, by: str = "firstname", strict: bool = False
    ) -> bool:
        value = str(value).lower()
        player_value: str = str(getattr(player, by, "")).lower()
        if strict:
            return player_value == value
        return value in player_value or player_value in value

    @overload
    def __getitem__(self, key: int) -> Player: ...

    @overload
    def __getitem__(self, key: str) -> list[Player]: ...

    def __getitem__(self, key: int | str) -> Player | list[Player]:
        if isinstance(key, int):
            return super().__getitem__(key)
        return [player for slug, player in self._by_slug.items() if key.lower() in slug]

    @overload  # type: ignore
    def get(self, key: int) -> Player: ...

    @overload
    def get(self, key: str) -> list[Player]: ...

    def get(self, key: int | str) -> Player | list[Player]:
        return self[key]

    def __getattr__(self, key: str) -> list[Player]:
        if val := self.__getitem__(key):
            return val
        else:
            return getattr(self.df, key)()

    def to_dict(
        self, by: Literal["id"] | Literal["slug"] = "id"
    ) -> dict[str | int, PlayerDict]:
        return {
            id: player.to_dict()
            for id, player in (self.data if by == "id" else self._by_slug).items()
        }

    def to_json(
        self, by: Literal["id"] | Literal["slug"] = "id", file: Path | None = None
    ) -> bytes:
        data: bytes = json.dumps(self.to_dict(by=by)).encode("utf-8")
        if file:
            file.write_bytes(data)
        return data

    def _read_db(self) -> Self:
        if self.db_path:
            for id, raw in DBClient(self.db_path).get_players().items():
                player: Player = Player(id, f"{raw.lastname}, {raw.firstname}")
                if player.stored:
                    player._hitting = player.stored.hitting
                    player._pitching = player.stored.pitching
                self.add(player)
        return self

    @cached_property
    def df(self) -> PlayerDataFrame:
        if self.db_path:
            return PlayerDataFrame(DBClient(self.db_path))
        return PlayerDataFrame()

    def as_polars(self) -> pl.DataFrame:
        return self.df.df

    abhr: pl.DataFrame
