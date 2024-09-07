from __future__ import annotations
import os
from dataclasses import dataclass
from typing import TYPE_CHECKING, ClassVar, Literal, Mapping, overload
import bs4
import httpx
from .types import HittingStats, StacastRanking, PitchingStats

if TYPE_CHECKING:
    from .. import Player


@dataclass
class Client:
    player: Player
    _content: bytes = b""

    TIMEOUT: ClassVar[str | None] = os.getenv("HTTPX_TIMEOUT")
    _SOUP_STRAINER: ClassVar[bs4.SoupStrainer] = bs4.SoupStrainer(
        id=["hittingStandard", "pitchingStandard", "statcast-rankings"]
    )

    @property
    def soup(self) -> bs4.BeautifulSoup:
        return bs4.BeautifulSoup(self._content, "lxml", parse_only=self._SOUP_STRAINER)

    def get_pitching(self) -> dict[str, PitchingStats]:
        stats: dict[str, PitchingStats] = {}
        statcast: bs4.Tag | None = self.soup.select_one("div#pitchingStandard table")
        if statcast:
            stats = self._get_statcast_values(statcast, type="pitching")
        return stats

    def get_ranking(self) -> dict[str, StacastRanking]:
        stats: dict[str, StacastRanking] = {}
        statcast: bs4.Tag | None = self.soup.select_one(
            "section#statcast-rankings table"
        )
        if statcast:
            stats = self._get_statcast_values(statcast, type="ranking")
        return stats

    def get_hitting(self) -> dict[str, HittingStats]:
        stats: dict[str, HittingStats] = {}
        statcast: bs4.Tag | None = self.soup.select_one("div#hittingStandard table")
        if statcast:
            stats = self._get_statcast_values(statcast, type="hitting")
        return stats

    def _get_statcast_header(self, statcast: bs4.Tag) -> list[str]:
        return [cell.text.strip() for cell in statcast.select("thead tr th")]

    @overload
    def _get_statcast_values(
        self, statcast: bs4.Tag, type: Literal["ranking"]
    ) -> dict[str, StacastRanking]: ...

    @overload
    def _get_statcast_values(
        self, statcast: bs4.Tag, type: Literal["pitching"]
    ) -> dict[str, PitchingStats]: ...

    @overload
    def _get_statcast_values(
        self, statcast: bs4.Tag, type: Literal["hitting"]
    ) -> dict[str, HittingStats]: ...

    def _get_statcast_values(
        self,
        statcast: bs4.Tag,
        type: Literal["hitting"] | Literal["pitching"] | Literal["ranking"],
    ) -> Mapping[str, StacastRanking | PitchingStats | HittingStats]:
        stats: dict[str, StacastRanking | PitchingStats | HittingStats] = {}

        for line in statcast.select("tbody tr"):
            year_stats: dict[str, str] = {
                self._get_statcast_header(statcast)[cell_id]: cell.text.strip()
                for cell_id, cell in enumerate(line.select("td"))
            }
            year: str = year_stats.get("Season", "").lower()
            if year == "player" or "season" in year:
                year = year_stats["Season"] = "all"
            stats[year] = self._convert_year_stats(year_stats)

        return stats

    @staticmethod
    def _convert_year_stats(
        year_stats: dict[str, str]
    ) -> StacastRanking | PitchingStats:
        converted: StacastRanking | PitchingStats = {}
        known_keys: list[str] = list(
            (HittingStats.__annotations__ | PitchingStats.__annotations__).keys()
        )
        for key, val in year_stats.items():
            if key not in known_keys:
                continue
            if not val:
                converted[key] = 0
            elif val.isdigit():
                converted[key] = int(val)
            else:
                try:
                    converted[key] = float(val)
                except ValueError:
                    converted[key] = str(val)
        return converted

    async def get_stats(self, session: httpx.AsyncClient) -> Player:
        async with self.player.semaphore:
            resp: httpx.Response = await session.get(
                self.player.url,
                timeout=float(self.TIMEOUT) if self.TIMEOUT else None,
                follow_redirects=True,
            )
            resp.raise_for_status()
            self._content = resp.content
            return self.player

    def get_stats_sync(self) -> Player:
        resp: httpx.Response = httpx.get(
            self.player.url,
            timeout=float(self.TIMEOUT) if self.TIMEOUT else None,
            follow_redirects=True,
        )
        resp.raise_for_status()
        self._content = resp.content
        self.get_hitting()
        self.get_pitching()
        self.get_ranking()
        return self.player
