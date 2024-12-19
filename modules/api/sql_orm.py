"""Failed attempt to derive a SQLModel form the API Base Model"""

from sqlmodel import Field, Relationship, SQLModel

from modules.api.getAvailableLeaderboards import Race
from modules.api.getRecentMatchHistory import (
    MatchhistorymemberItem,
    Matchhistoryreportresult,
    Profile,
)


class ProfileTable(SQLModel, Profile, table=True):
    __tablename__: str = "profile"
    profile_id: int = Field(primary_key=True)


class MatchhistoryitemTable(SQLModel, table=True):
    __tablename__ = "matchhistoryitem"
    matchhistory_id: int = Field(primary_key=True, foreign_key="matchhistorystat.id")
    matchhistory: "MatchhistorystatTable" = Relationship(
        back_populates="matchhistoryitems"
    )
    item_id: int = Field(primary_key=True)


class MatchurlTable(SQLModel, table=True):
    __tablename__: str = "matchurl"
    url_id: int = Field(primary_key=True)
    url: str
    matchhistory_id: int = Field(foreign_key="matchhistorystat.id")
    matchhistory: "MatchhistorystatTable" = Relationship(back_populates="matchurls")


class MatchhistorymemberItemTable(SQLModel, MatchhistorymemberItem, table=True):
    __tablename__: str = "matchhistorymemberitem"
    matchhistory_id: int = Field(primary_key=True, foreign_key="matchhistorystat.id")
    matchhistory: "MatchhistorystatTable" = Relationship(
        back_populates="matchhistorymembers"
    )
    profile_id: int = Field(primary_key=True, foreign_key="profile.profile_id")
    civilization_id: int = Field(foreign_key="race.id")


class MatchhistoryreportresultTable(SQLModel, Matchhistoryreportresult, table=True):
    __tablename__: str = "matchhistoryreportresult"
    matchhistory_id: int = Field(primary_key=True, foreign_key="matchhistorystat.id")
    matchhistory: "MatchhistorystatTable" = Relationship(
        back_populates="matchhistoryreportresults"
    )
    profile_id: int = Field(primary_key=True, foreign_key="profile.profile_id")
    civilization_id: int = Field(foreign_key="race.id")


class RaceTable(SQLModel, Race, table=True):
    __tablename__: str = "race"
    id: int = Field(primary_key=True)


# This is a redefinition of the MatchHistoryStat class from the getRecentMatchHistory.py file, because the original class includes a list, which is not compatible
class MatchhistorystatTable(SQLModel, table=True):
    __tablename__: str = "matchhistorystat"
    id: int = Field(primary_key=True)
    matchhistoryreportresults: list["MatchhistoryreportresultTable"] = Relationship(
        back_populates="matchhistory"
    )
    matchhistoryitems: list["MatchhistoryitemTable"] = Relationship(
        back_populates="matchhistory"
    )
    matchurls: list["MatchurlTable"] = Relationship(back_populates="matchhistory")
    matchhistorymembers: list["MatchhistorymemberItemTable"] = Relationship(
        back_populates="matchhistory"
    )
