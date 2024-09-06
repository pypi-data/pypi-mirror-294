import asyncio
from abc import ABC
from json import JSONDecoder
from typing import Union, Any
from urllib.parse import quote

import aiohttp
from aiohttp import ClientSession, ClientConnectorError
from aiohttp.typedefs import DEFAULT_JSON_DECODER

from .dataclass import Player


class API(ABC):
    def __init__(self,
                 session: ClientSession = None,
                 json_loads: JSONDecoder = DEFAULT_JSON_DECODER,
                 emojis: dict[str, str] = None):
        self.emojis = emojis
        if emojis is None:
            self.emojis = {"fox": "🦊"}
        self.session = session
        self.json_loads = json_loads
        self.url = "https://ddstats.qwik.space/player/json?player={0}"

    @staticmethod
    def powered() -> str:
        """Return an empty string."""
        return ''

    async def _get_emoji(self, player_name: str) -> str:
        """Return an emoji for the given player name."""
        for name, emoji in self.emojis.items():
            if name in player_name.lower():
                return emoji
        return ''

    async def _send(self, url: str) -> Union[dict, None]:
        """Send a GET request to the given URL and return the response as JSON."""
        if self.session is None:
            self.session = aiohttp.ClientSession()
        try:
            async with self.session.get(url) as req:
                if req.status == 200:
                    return await req.json(loads=self.json_loads)
                return
        except ClientConnectorError:
            return

    async def _generate(
            self,
            url: str,
            model,
            k: str = None,
            emoji: str = None
    ) -> Union[Any, None]:
        """Generate a model instance from the given URL and optional keyword arguments."""
        dat = await self._send(url)
        if dat is None:
            return
        if k is not None:
            dat = {k: dat}
        if emoji is not None:
            dat["emoji"] = emoji
        return model(**dat)

    async def close(self) -> None:
        """Close the aiohttp session."""
        if self.session:
            await self.session.close()
            self.session = None

    async def player(self, player_name: str) -> Player:
        """Fetch player data from the API and return it as a dictionary."""
        return await self._generate(
            self.url.format(quote(player_name)),
            Player,
            emoji=await self._get_emoji(player_name)
        )

    async def players(self, player_names: list[str]) -> tuple[Player]:
        """Fetch data for multiple players from the API and return it as a list of dictionaries."""
        tasks = [self.player(player_name) for player_name in player_names]
        return await asyncio.gather(*tasks)
