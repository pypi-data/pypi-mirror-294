# pylint: disable-all
from collections import Counter
from datetime import datetime
from typing import Optional, Union, Any, AsyncGenerator
from pydantic import BaseModel, Field

rm_list = ["DD-Persian", "/vDQMHSss8W"]


# DDStats


class QE(BaseModel):
    sql: str
    params: dict


class DDStatsSql(BaseModel):
    ok: bool = Field(default=None)
    database: str = Field(default=None)
    table: str = Field(default=None)
    is_view: bool = Field(default=None)
    human_description_en: str = Field(default=None)
    rows: list[list] = Field(default=None)
    truncated: bool = Field(default=None)
    filtered_table_rows_count: int = Field(default=None)
    expanded_columns: list = Field(default=None)
    expandable_columns: list = Field(default=None)
    columns: list = Field(default=None)
    primary_keys: list = Field(default=None)
    units: dict = Field(default=None)
    query: QE = Field(default=None)
    facet_results: dict = Field(default=None)
    suggested_facets: list = Field(default=None)
    next: int | None = Field(default=None)
    next_url: str | None = Field(default=None)
    error: str = Field(default='')
    private: bool = Field(default=None)
    allow_execute_sql: bool = Field(default=None)
    query_ms: float = Field(default=None)


# ddnet
class DPoints(BaseModel):
    total: Optional[int] = Field(default=None)
    points: Optional[int] = Field(default=None)
    rank: Optional[int] = Field(default=None)


class MaxFinishes(BaseModel):
    rank: Optional[int] = Field(default=None)
    player: Optional[str] = Field(default=None)
    num: Optional[int] = Field(default=None)
    time: Optional[float] = Field(default=None)
    min_timestamp: Optional[int] = Field(default=None)
    max_timestamp: Optional[int] = Field(default=None)


class DDRanks(BaseModel):
    rank: Optional[int] = Field(default=None)
    player: Union[str, list[str]] = Field(default=None)
    time: Optional[float] = Field(default=None)
    timestamp: Optional[int] = Field(default=None)
    country: Optional[str] = Field(default=None)


class DDTMRanks(BaseModel):
    rank: Optional[int] = Field(default=None)
    players: Union[str, list[str]] = Field(default=None)
    time: Optional[float] = Field(default=None)
    timestamp: Optional[int] = Field(default=None)
    country: Optional[str] = Field(default=None)


class DMap(BaseModel):
    name: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    thumbnail: Optional[str] = Field(default=None)
    web_preview: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)
    points: Optional[int] = Field(default=None)
    difficulty: Optional[int] = Field(default=None)
    mapper: Optional[str] = Field(default=None)
    release: Optional[int] = Field(default=None)
    median_time: Optional[float] = Field(default=None)
    first_finish: Optional[int] = Field(default=None)
    last_finish: Optional[int] = Field(default=None)
    finishes: Optional[int] = Field(default=None)
    finishers: Optional[int] = Field(default=None)
    biggest_team: Optional[int] = Field(default=None)
    width: Optional[int] = Field(default=None)
    height: Optional[int] = Field(default=None)
    tiles: Optional[list] = Field(default=None)
    team_ranks: Optional[list[DDTMRanks]] = Field(default=None)
    ranks: Optional[list[DDRanks]] = Field(default=None)
    max_finishes: Optional[list[MaxFinishes]] = Field(default=None)


class DRank(BaseModel):
    points: Optional[int] = Field(default=None)
    rank: Optional[int] = Field(default=None)


class FirstFinish(BaseModel):
    timestamp: Optional[float] = Field(default=None)
    map: Optional[str] = Field(default=None)
    time: Optional[float] = Field(default=None)


class LastFinish(BaseModel):
    timestamp: Optional[float] = Field(default=None)
    map: Optional[str] = Field(default=None)
    time: Optional[float] = Field(default=None)
    country: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default=None)


class FavorPart(BaseModel):
    name: Optional[str] = Field(default=None)
    finishes: Optional[int] = Field(default=None)


class DData(BaseModel):
    points: Optional[DPoints] = Field(default=None)
    team_rank: Optional[DRank] = Field(default=None)
    rank: Optional[DRank] = Field(default=None)
    maps: Optional[dict] = Field(default=None)


class DDType(BaseModel):
    Novice: Optional[DData] = Field(default=None)
    Moderate: Optional[DData] = Field(default=None)
    Brutal: Optional[DData] = Field(default=None)
    Insane: Optional[DData] = Field(default=None)
    Dummy: Optional[DData] = Field(default=None)
    DDmaX_Easy: Optional[DData] = Field(default=None, validation_alias='DDmaX.Easy')
    DDmaX_Next: Optional[DData] = Field(default=None, validation_alias='DDmaX.Next')
    DDmaX_Nut: Optional[DData] = Field(default=None, validation_alias='DDmaX.Nut')
    DDmaX_Pro: Optional[DData] = Field(default=None, validation_alias='DDmaX.Pro')
    Oldschool: Optional[DData] = Field(default=None)
    Race: Optional[DData] = Field(default=None)
    Solo: Optional[DData] = Field(default=None)
    total: Optional[DData] = Field(default=None)


class DActiov(BaseModel):
    date: Optional[str] = Field(default=None)
    hours_played: Optional[int] = Field(default=None)


class DDPlayer(BaseModel):
    emoji: str = Field(default='')
    player: Optional[str] = Field(default=None)
    points: Optional[DPoints] = Field(default=None)
    team_rank: Optional[DRank] = Field(default=None)
    rank: Optional[DRank] = Field(default=None)
    points_last_month: Optional[DRank] = Field(default=None)
    points_last_week: Optional[DRank] = Field(default=None)
    first_finish: Optional[FirstFinish] = Field(default=None)
    last_finishes: Optional[list[LastFinish]] = Field(default=None)
    favorite_partners: Optional[list[FavorPart]] = Field(default=None)
    types: Optional[DDType] = Field(default=None)
    activity: Optional[list[DActiov]] = Field(default=None)
    hours_played_past_365_days: Optional[int] = Field(default=None)


# qwik

class PData(BaseModel):
    rank: int | None = None
    points: int | None = None


class PPoints(BaseModel):
    Novice: Optional[PData] = None
    Moderate: Optional[PData] = None
    Brutal: Optional[PData] = None
    Insane: Optional[PData] = None
    Dummy: Optional[PData] = None
    DDmaX_Easy: Optional[PData] = Field(default=None, validation_alias='DDmaX.Easy')
    DDmaX_Next: Optional[PData] = Field(default=None, validation_alias='DDmaX.Next')
    DDmaX_Nut: Optional[PData] = Field(default=None, validation_alias='DDmaX.Nut')
    DDmaX_Pro: Optional[PData] = Field(default=None, validation_alias='DDmaX.Pro')
    Oldschool: Optional[PData] = None
    Race: Optional[PData] = None
    Solo: Optional[PData] = None
    total: Optional[PData] = None


class PointG(BaseModel):
    date: Optional[str] | None = None
    points: Optional[int] | None = None
    rank_points: Optional[int] | None = None
    team_points: Optional[int] | None = None


class Profile(BaseModel):
    name: Optional[str] | None = None
    points: Optional[int] | None = None
    clan: Optional[str] | None = None
    country: Optional[int] | None = None
    skin_name: Optional[str] | None = None
    skin_color_body: Optional[int] | None = None
    skin_color_feet: Optional[int] | None = None


class Map(BaseModel):
    map: Optional[str] | None = None
    server: Optional[str] | None = None
    points: Optional[int] | None = None
    stars: Optional[int] | None = None
    mapper: Optional[str] | None = None
    timestamp: Optional[datetime] | None = None


class RecentFinishes(BaseModel):
    map: Optional[Map] | None = None
    time: Optional[float] | None = None
    timestamp: Optional[datetime] | None = None
    server: Optional[str] | None = None
    cp1: Optional[float] | None = None
    cp2: Optional[float] | None = None
    cp3: Optional[float] | None = None
    cp4: Optional[float] | None = None
    cp5: Optional[float] | None = None
    cp6: Optional[float] | None = None
    cp7: Optional[float] | None = None
    cp8: Optional[float] | None = None
    cp9: Optional[float] | None = None
    cp10: Optional[float] | None = None
    cp11: Optional[float] | None = None
    cp12: Optional[float] | None = None
    cp13: Optional[float] | None = None
    cp14: Optional[float] | None = None
    cp15: Optional[float] | None = None
    cp16: Optional[float] | None = None
    cp17: Optional[float] | None = None
    cp18: Optional[float] | None = None
    cp19: Optional[float] | None = None
    cp20: Optional[float] | None = None
    cp21: Optional[float] | None = None
    cp22: Optional[float] | None = None
    cp23: Optional[float] | None = None
    cp24: Optional[float] | None = None
    cp25: Optional[float] | None = None


class FavouriteTeammates(BaseModel):
    name: str | None = None
    ranks_together: int | None = None


class Finishes(BaseModel):
    map: Map | None = None
    name: str | None = None
    time: float | None = None
    timestamp: Optional[datetime] = None
    server: str | None = None
    rank: int | None = None
    team_rank: int | None = None
    seconds_played: int | None = None


class Points(BaseModel):
    weekly_points: PData | None = None
    monthly_points: PData | None = None
    yearly_points: PData | None = None
    points: PPoints | None = None
    rank_points: PPoints | None = None
    team_points: PPoints | None = None


class RecentActivity(BaseModel):
    name: str | None = Field(default=None)
    date: str | None = Field(default=None)
    map_name: str | None = Field(default=None)
    map: Map | None = Field(default=None)
    seconds_played: int | None = Field(default=None)


class RecentPlayerInfo(BaseModel):
    name: str | None = None
    clan: str | None = None
    country: int | None = None
    skin_name: str | None = None
    skin_color_body: int | None = None
    skin_color_feet: int | None = None
    last_seen: str | None = None
    seconds_played: int | None = None


class MostPlayedMaps(BaseModel):
    map_name: str | None = None
    seconds_played: int | None = None
    map: Map | None = None


class MostPlayed(BaseModel):
    key: str | None = None
    seconds_played: int | None = None


class PlaytimePerMonth(BaseModel):
    year_month: str | None = None
    month: str | None = None
    seconds_played: int | None = None


class FavouriteRank1sTeammates(BaseModel):
    name: str
    ranks_together: int


class AllTop10s(BaseModel):
    map: Map | None = None
    name: str | None = None
    time: float | None = None
    rank: int | None = None
    team_rank: int | None = None
    team_time: float | None = None


class RecentTop10s(BaseModel):
    rank_type: str | None = None
    map: str | None = None
    time: float | None = None
    rank: int | None = None
    timestamp: datetime | None = None
    server: str | None = None


class Player(BaseModel):
    emoji: str = Field(default='')
    points_graph: Optional[list[PointG]] = None
    recent_finishes: Optional[list[RecentFinishes]] = None
    favourite_teammates: Optional[list[FavouriteTeammates]] = None
    profile: Optional[Profile] = None
    is_mapper: bool = None
    finishes: Optional[list[Finishes]] = None
    points: Points = None
    recent_activity: Optional[list[RecentActivity]] = None
    recent_player_info: Optional[list[RecentPlayerInfo]] = None
    most_played_maps: Optional[list[MostPlayedMaps]] = None
    most_played_gametypes: Optional[list[MostPlayed]] = None
    most_played_categories: Optional[list[MostPlayed]] = None
    most_played_locations: Optional[list[MostPlayed]] = None
    playtime_per_month: Optional[list[PlaytimePerMonth]] = None
    favourite_rank1s_teammates: Optional[list[FavouriteRank1sTeammates]] = None
    all_top_10s: Optional[list[AllTop10s]] = None
    recent_top_10s: Optional[list[RecentTop10s]] = None


class Client(BaseModel):
    name: str | None = Field(default='')
    clan: str | None = Field(default='')
    country: int | None = Field(default=-1)
    score: int | None = Field(default=-9999)
    is_player: bool | None = Field(default=None)
    skin: dict | None = Field(default=None)
    afk: bool | None = Field(default=None)
    team: int | None = Field(default=0)


class Info(BaseModel):
    max_clients: int | None = Field(default=0)
    max_players: int | None = Field(default=0)
    passworded: bool | None = Field(default=None)
    game_type: str | None = Field(default=None)
    name: str | None = Field(default=None)
    map: dict | None = Field(default=None)
    version: str | None = Field(default=None)
    clients: list[Client] | None = Field(default=None)

    def __len__(self) -> int:
        return len(self.clients)


class Server(BaseModel):
    addresses: Union[list, str] = Field(default=None)
    location: str = Field(default=None)
    info: Info = Field(default=None)

    def __len__(self) -> int:
        return len(self.info.clients if self.info is not None else 0)

    def get_count_client(self) -> int:
        if self.info is not None and self.info.clients is not None:
            return len(self.info.clients)
        return 0


class Master(BaseModel):
    servers: list[Server]

    def __len__(self) -> int:
        return len(self.servers)

    async def get_info(self) -> AsyncGenerator[Info, None]:
        for i in self.servers:
            if i.info is None:
                continue
            yield i.info

    async def get_clients(self) -> AsyncGenerator[Client, None]:
        for i in self.servers:
            if i.info is None or i.info.clients is None:
                continue
            yield i.info.clients

    def get_clans(self, limit: int = 50, rm: list[str] = None) -> list[tuple[Any, int]]:
        remove_list = [] if rm is None else rm
        remove_list.extend(["DD-Persian", ''])
        if not self.servers:
            return []
        dat: Counter[Any] = Counter(client.clan
                                    for server in self.servers
                                    for client in server.info.clients
                                    if server.info is not None
                                    and server.info.clients is not None
                                    and client != '')
        for i in remove_list:
            del dat[i]
        return sorted(dat.items(), key=lambda x: x[1], reverse=True)[:limit]

    def get_count_servers(self, limit: int = 10) -> list:
        return sorted((
            (i.get_count_client(), i.addresses[0], i.info.game_type, i.info.name)
            if isinstance(i.addresses, list)
            else (i.get_count_client(), i.addresses, i.info.game_type, i.info.name)
            for i in self.servers), key=lambda x: x[0], reverse=True)[:limit]


class QueryData(BaseModel):
    points: int
    name: str


class Query(BaseModel):
    emoji: str = Field(default='')
    data: list[QueryData]


class DDStatusData(BaseModel):
    name: str | None = Field(default=None)
    type: str | None = Field(default=None)
    host: str | None = Field(default=None)
    location: str | None = Field(default=None)
    online4: bool | None = Field(default=None)
    online6: bool | None = Field(default=None)
    uptime: str | None = Field(default=None)
    load: float | None = Field(default=None)
    network_rx: int | None = Field(default=None)
    network_tx: int | None = Field(default=None)
    packets_rx: int | None = Field(default=None)
    packets_tx: int | None = Field(default=None)
    cpu: int | None = Field(default=None)
    memory_total: int | None = Field(default=None)
    memory_used: int | None = Field(default=None)
    swap_total: int | None = Field(default=None)
    swap_used: int | None = Field(default=None)
    hdd_total: int | None = Field(default=None)
    hdd_used: int | None = Field(default=None)


class DDStatus(BaseModel):
    servers: list[DDStatusData] | None = Field(default=[])
