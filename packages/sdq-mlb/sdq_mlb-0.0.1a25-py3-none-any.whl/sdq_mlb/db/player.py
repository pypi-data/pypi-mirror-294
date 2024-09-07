from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from functools import cached_property
from typing import TYPE_CHECKING, Any, Literal, Mapping, overload
from ..baseball_savant.types import HittingStats, PitchingStats

if TYPE_CHECKING:
    from . import Client
    from .. import Player as Source


@dataclass
class Player:
    id: int
    firstname: str
    lastname: str
    slug: str
    url: str

    db: Client

    @overload
    @classmethod
    def search(cls, db: Client, player: int) -> Player | None: ...

    @overload
    @classmethod
    def search(cls, db: Client, player: Source) -> Player | None: ...

    @classmethod
    def search(cls, db: Client, player: Source | int) -> Player | None:
        if not isinstance(player, int):
            player = player.id
        row: sqlite3.Row | None = db.cursor.execute(
            "SELECT * FROM player WHERE id = ?", (player,)
        ).fetchone()
        if row:
            data = dict(row)
            data.pop("statcast", "")
            return cls(**data, db=db)
        return None

    @cached_property
    def hitting(self) -> dict[str, HittingStats]:
        return self._get_stats(src="hitting")

    @cached_property
    def pitching(self) -> dict[str, PitchingStats]:
        return self._get_stats(src="pitching")

    @overload
    def _get_stats(self, src: Literal["hitting"]) -> dict[str, HittingStats]: ...

    @overload
    def _get_stats(self, src: Literal["pitching"]) -> dict[str, PitchingStats]: ...

    def _get_stats(
        self, src: Literal["hitting"] | Literal["pitching"]
    ) -> Mapping[str, Mapping[str, Any]]:
        rows: list[sqlite3.Row] = self.db.cursor.execute(
            f"""
            SELECT {src}.* FROM {src}
            JOIN player ON {src}.player = player.id
            WHERE player.id = ?
            """,
            (self.id,),
        ).fetchall()
        results: dict[str, dict[str, Any]] = {}
        for year in rows:
            data: dict[str, Any] = dict(year)
            data.pop("player", "")
            results[year["Season"]] = data
        return results
