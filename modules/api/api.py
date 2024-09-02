from collections.abc import Sequence
from dataclasses import dataclass
from typing import Any, Self

from pydantic import BaseModel


class ApiResult(BaseModel):
    code: int
    message: str


class ApiProfile(BaseModel):
    profile_id: int
    name: str
    alias: str
    personal_statgroup_id: int
    xp: int
    level: int
    leaderboardregion_id: int
    country: str


class MatchHistoryReportResult(BaseModel):
    matchhistory_id: int
    profile_id: int
    resulttype: int
    teamid: int
    race_id: int
    xpgained: int
    counters: str
    matchstartdate: int
    civilization_id: int


class Matchurls(BaseModel):
    profile_id: int
    url: str
    size: int
    datatype: int


class MatchHistoryMember(BaseModel):
    matchhistory_id: int
    profile_id: int
    race_id: int
    statgroup_id: int
    teamid: int
    wins: int
    losses: int
    streak: int
    arbitration: int
    outcome: int
    oldrating: int
    newrating: int
    reporttype: int
    civilization_id: int


class matchHistoryElement(BaseModel):
    id: int
    creator_profile_id: int
    mapname: str
    maxplayers: int
    matchtype_id: int
    options: str
    slotinfo: str
    description: str
    startgametime: int
    completiontime: int
    observertotal: int
    matchhistoryreportresults: Sequence[MatchHistoryReportResult]
    matchhistoryitems: list
    matchurls: Sequence[Matchurls]
    matchhistorymember: Sequence[MatchHistoryMember]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        matchhistoryreportresults = [
            MatchHistoryReportResult(**x) for x in data["matchhistoryreportresults"]
        ]
        matchurls = [Matchurls(**x) for x in data["matchurls"]]
        matchhistorymember = [
            MatchHistoryMember(**x) for x in data["matchhistorymember"]
        ]
        to_drop = ["matchhistoryreportresults", "matchurls", "matchhistorymember"]
        new_data = {key: value for key, value in data.items() if key not in to_drop}
        return cls(
            matchhistoryreportresults=matchhistoryreportresults,
            matchurls=matchurls,
            matchhistorymember=matchhistorymember,
            **new_data,
        )


@dataclass
class ApiResponse:
    result: ApiResult
    matchHistoryStats: list[matchHistoryElement]
    profiles: list[ApiProfile]

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> Self:
        match_history_stats = [
            matchHistoryElement.from_dict(x) for x in data["matchHistoryStats"]
        ]
        profiles = [ApiProfile(**profile) for profile in data["profiles"]]
        return cls(
            result=ApiResult(**data["result"]),
            matchHistoryStats=match_history_stats,
            profiles=profiles,
        )
