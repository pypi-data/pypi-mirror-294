from __future__ import annotations
import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, ClassVar
from ..player import PlayerDict
from ..baseball_savant import types
from .player import Player as DBPlayer

if TYPE_CHECKING:
    from .. import Player


__all__: list[str] = ["Client"]


@dataclass
class Client:
    db_path: Path = Path("mymlb.db")

    _connection: sqlite3.Connection | None = None

    TABLES: ClassVar[dict[str, type]] = {
        "hitting": types.HittingStats,
        "pitching": types.PitchingStats,
        # "ranking": types.StacastRanking,
    }

    @property
    def connection(self) -> sqlite3.Connection:
        if not self._connection:
            self._connection = sqlite3.connect(self.db_path, isolation_level=None)
            self._connection.row_factory = sqlite3.Row
        return self._connection

    @property
    def cursor(self) -> sqlite3.Cursor:
        return self.connection.cursor()

    def create_tables(self) -> None:
        self._create_player_table()
        for name, type in self.TABLES.items():
            self.cursor.execute(self._write_sql_create(name, type))

    def _create_player_table(self) -> None:
        columns: list[str] = [
            column
            for column in self._get_columns(PlayerDict)
            if "statcast" not in column
        ]
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS player
            ({', '.join(columns)}, PRIMARY KEY (id))
            """
        )

    def _write_sql_create(self, name: str, type: type) -> str:
        columns: str = ", ".join(
            [
                *self._escape_strings(self._get_columns(type)),
                "`player`",
                "PRIMARY KEY (`player`, `Season`)",
                "FOREIGN KEY(`player`) REFERENCES `player`(`id`)",
            ]
        )
        return f"CREATE TABLE IF NOT EXISTS {name} ({columns})"

    def _get_columns(self, type: type) -> list[str]:
        return list(type.__annotations__.keys())

    def _escape_strings(self, strings: list[str]) -> list[str]:
        return [f"`{string}`" for string in strings]

    def insert_player(
        self, player: Player, *, fail_safe: bool = False
    ) -> sqlite3.Row | None:
        if fail_safe:
            try:
                self._insert_player(player)
            except sqlite3.IntegrityError:
                pass
        else:
            self._insert_player(player)
        return self.cursor.execute(
            "SELECT *FROM player WHERE id = ?", (player.id,)
        ).fetchone()

    def _insert_player(self, player: Player) -> None:
        self._insert_player_meta(player)
        for table, type in self.TABLES.items():
            self._insert_player_stats(player, table, type)

    def _insert_player_meta(self, player: Player) -> ...:
        keys: list[str] = list(set(self._get_columns(PlayerDict)) ^ {"statcast"})
        columns: list[str] = self._escape_strings(keys)
        values: list[str] = [f":{column}" for column in keys]
        sql: str = (
            f"INSERT INTO player({', '.join(columns)}) VALUES ({', '.join(values)})"
        )
        data: PlayerDict = player.to_dict()
        del data["statcast"]  # type: ignore
        self.cursor.execute(sql, data)

    def _insert_player_stats(self, player: Player, table: str, type: type) -> ...:
        columns: list[str] = self._get_columns(type)
        sql: str = f"""
            INSERT INTO {table} (
            {', '.join(self._escape_strings(columns))}, `player`
            )
            VALUES ({', '.join([f':{column}' for column in columns])}, :player_id)
        """
        for year_data in getattr(player, table, {}).values():
            year_data["player_id"] = player.id
        self.cursor.executemany(sql, getattr(player, table, {}).values())

    def get_player(self, player: Player) -> DBPlayer | None:
        return DBPlayer.search(self, player)

    def get_players(self) -> dict[str, DBPlayer]:
        results: dict[str, DBPlayer] = {}
        player_ids: list[int] = [
            row["id"] for row in self.cursor.execute("SELECT id FROM player").fetchall()
        ]
        for player_id in player_ids:
            if player := DBPlayer.search(self, player_id):
                results[str(player_id)] = player
        return results
