import asyncio
from typing import Union
from urllib.parse import quote

from .dataclass import DDPlayer, Master, Query, DMap, DDStatsSql, DDStatus
from .deflt import API

__all__ = (
    "DDnetApi",
    "DDstats",
    "DDStatsDB"
)


class DDStatsDB(API):
    def __init__(self):
        super().__init__()

    @staticmethod
    def powered() -> str:
        return 'ddstats.org'

    async def _rt(self, url: str):
        return await self._generate(url, DDStatsSql)

    async def next(self, dd: DDStatsSql):
        return await self._rt(dd.next_url)

    async def sql(self, sql: str):
        return await self._rt(f"https://db.ddstats.org/ddnet-7b306cf?sql={quote(sql)}")

    async def mapinfo(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/mapinfo.json")

    async def teamrace(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/teamrace.json")

    async def race(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/race.json")

    async def maps(self):
        return await self._rt("https://db.ddstats.org/ddnet-7b306cf/maps.json")


class DDnetApi(API):
    def __init__(self):
        super().__init__()
        self.url = "https://ddnet.org/"

    @staticmethod
    def powered() -> str:
        return 'ddnet.org'

    async def player(self, player_name: str) -> DDPlayer:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate(
            f"{self.url}players/?json2={quote(player_name)}",
            DDPlayer,
            emoji=await self._get_emoji(player_name)
        )

    async def players(self, player_names: list[str]) -> tuple[DDPlayer]:
        """Fetch data for multiple players from the API and return it as a list of dictionaries."""
        tasks = [self.player(player_name) for player_name in player_names]
        return await asyncio.gather(*tasks)

    async def status(self) -> Union[DDStatus, None]:
        return await self._generate(
            f"{self.url}status/json/stats.json",
            DDStatus
        )

    async def query(self, player: str) -> Union[Query, None]:
        return await self._generate(
            f"{self.url}players/?query={quote(player)}",
            Query,
            "data",
            emoji=await self._get_emoji(player)
        )

    async def master(self) -> Union[Master, None]:
        return await self._generate(
            "https://master1.ddnet.org/ddnet/15/servers.json",
            Master
        )

    async def map(self, map_name: str) -> Union[DMap, None]:
        return await self._generate(
            f"{self.url}maps/?json={quote(map_name)}",
            DMap
        )


class DDstats(API):
    @staticmethod
    def powered() -> str:
        return 'ddstats.tw'
