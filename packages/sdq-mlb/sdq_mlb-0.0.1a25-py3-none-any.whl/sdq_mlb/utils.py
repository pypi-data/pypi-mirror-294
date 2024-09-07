import functools
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
import polars as pl


def get_mlb_full_df() -> pl.DataFrame:
    return _DataFramesGetter().get_mlb_dataframes().players


@dataclass
class _DataFramesGetter:

    @dataclass
    class _MLBDataFrames:
        players: pl.DataFrame = field(default_factory=pl.DataFrame)
        hitting: pl.DataFrame = field(default_factory=pl.DataFrame)
        pitching: pl.DataFrame = field(default_factory=pl.DataFrame)

    db_path: Path = Path("mymlb.db")

    def get_mlb_dataframes(self) -> _MLBDataFrames:
        self._get_player_stats()
        return self.dataframes

    @property
    def _connection(self) -> sqlite3.Connection:
        return sqlite3.connect(self.db_path)

    @functools.cached_property
    def dataframes(self) -> _MLBDataFrames:
        return self._MLBDataFrames(
            players=pl.read_database("SELECT * FROM player", self._connection),
            hitting=pl.read_database("SELECT * FROM hitting", self._connection),
            pitching=pl.read_database("SELECT * FROM pitching", self._connection),
        )

    def _get_player_stats(self) -> None:
        self._merge_hitting()
        self._merge_pitching()

    def _merge_hitting(self) -> None:
        self.dataframes.hitting = self.dataframes.hitting.rename(
            {col: col.lower() for col in self.dataframes.hitting.columns}
        )
        self.dataframes.players = self.dataframes.players.join(
            self.dataframes.hitting,
            how="left",
            left_on="id",
            right_on="player",
            suffix="_h",
        )

    def _merge_pitching(self) -> None:
        self.dataframes.pitching = self.dataframes.pitching.rename(
            {col: col.lower() for col in self.dataframes.pitching.columns}
        )
        self.dataframes.players = self.dataframes.players.join(
            self.dataframes.pitching,
            how="left",
            left_on=["id", "season"],
            right_on=["player", "season"],
            suffix="_p",
        )
