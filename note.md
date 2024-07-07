# API: getRecentMatchHistory

At the moment, a working API is the following:

```https://aoe-api.worldsedgelink.com/community/leaderboard/getRecentMatchHistory?title=age2&profile_names=[%22/steam/{STEAM_ID}%22]```

for example
[https://aoe-api.worldsedgelink.com/community/leaderboard/getRecentMatchHistory?title=age2&profile_names=[%22/steam/76561198342887481%22]](https://aoe-api.worldsedgelink.com/community/leaderboard/getRecentMatchHistory?title=age2&profile_names=[%22/steam/76561198342887481%22]&id=192039891).

This api will return information about 'recent' matches of a given Steam ID. It includes for sure Ranked games and Quickplay.
It remains unclear whether the search results include private lobbies. Additionally, the absence of chronological ordering makes it uncertain if all recent games are displayed.

# API response description

A request to the getRecentMatchHistory API, will return a JSON with the following structure:

```json
    {
        "result": {...},  # an error code and a info on whether the request was successful or not
        "matchHistoryStats": [...],  # a list of matches, from many leaderboard, with all the details about them
        "profiles": [...]  # A list of all the profiles seen in the matches returned, with details for each profile
    }
```

In this page, we described each element of the JSON response, for documentation

## result

This is simply metadata about the API request placed.

```json
    "result": {
        "code": 0,  # 0 if successful, 5 if steam ID not found
        "message": "SUCCESS", # 'UNREGISTERED_PROFILE_NAME' if
    },
```

## matchHistoryStats

This is a list of matches. Each match is a dictionary with many fields, described below.

```json
 {
            "id": 192039891,
            "creator_profile_id": 1302836,
            "mapname": "AfricanClearing.rms",
            "maxplayers": 4,
            "matchtype_id": 19,  # Unranked 2v2. Below, full description of other matchtype_id
            "options": "eNo9UstuwyAQ/Jd8QWzHSD2S4lRpuyCnoNY9xqos4Ta21EY2fH0XWMxpxD5mZnd3l6Hl+Eqwk+cLIsEZ5D8/348BitErC0uKN+ya4gcl5jr9nRm0VKOn5RiQ6BZleROg0hxrIMBCWXMNQGpgppjnt4/jSbu/38v7ft/fZgXj8+PL/vtu9P4h9e4YcBNrUWOVtUmN2iLPUCLPKfF07FU3iVP07CtpqpTti9RryDoL6SdHOkt1G2ONtKEm6qyVPcc/QO3AuwBX9LZKMRJXy0ATFibwEm43DdJufKXSU5H4epyLSXHfYDx6q9DbSj5X8FMBPNYh37SmHTQ4u345DhGj58bJlnI85sTezUHZgXSP2HtIvTEOgi/U04HIOzqv2CfqBntmkvYFFvAGohaH/CX5r4IWsIbyDYMtv8s+HGopaUdOicmTZ9Q+PKXcMdQRP1T5RqTv8r5qsHm3gH5olr7Pd1dIm/22Lu9J6e0uq3CXxFtvu9W4i+T/AGK7nXW7Ubxh1VLc43zizE2tfj7d7h/XevIh",
            "slotinfo": "eNq9k11PgzAUhv0tvUZDKQ5c4s3cukBEx1dlM14UKIHwGagmc/G/C6gxxK/hBVfn7TlvT5Mnb6Ek3B9AVZdRkjGtiMqzJARzBM9VWVQF0HDKk7LQlm1PAJzRvJOiACIafAzaU00D1kmIOl2k1+yJZe+TIjUoD2JnX/WWU9juSXK2YTWuac4Mu/cljcVouG9XvD362PTtnHG6pJyCOdBSjCwXL0wXI5P0dUWI1dUFcfRbf61zq8hi8pxZ2zRc35Bqa6dV4hO92bkYdz7TwVd9dXe2jzPPWOn9fecuuNjY2iV4Eb7CgEiUVDQbwICfMOBPMGbTsjDHsvDC71l4v7BAkoQUBQ5YyMcEQ5kWhjUaRvyvYIiyJA5gSEcEQxanheGO/iWLP5LxcPIKdwlTJA==",
            "description": "AUTOMATCH",
            "startgametime": 1669212769, # start time in unix timestamp
            "completiontime": 1669213867, # start time in unix timestamp
            "observertotal": 0,
            "matchhistoryreportresults": [...] # list of players with profile_id, civ, team_id, win/loss
            "matchhistoryitems": [],
            "matchurls": [],
            "matchhistorymember": [...]  # list of players with profile_id, civ, team_id, win/loss. Don't know the difference with matchhistoryreportresults. It includes some player stats.
        }
```

More detailed info on [libreMatch wiki](https://wiki.librematch.org/rlink/community/leaderboard/getavailableleaderboards)

| **matchtype_id** |                       |
|:----------------:|-----------------------|
| 6                | Ranked RM 1v1         |
| 7                | Ranked RM team (2v2?) |
| 19               | Quickplay 2v2         |
| 20               | Quickplay 3v3         |
| 21               | Quickplay 4v4         |

## profiles

This contains a list (an array in JSON) of all the profiles found in matches from *matchHistoryStats*. Below, an example of one element from the list:

```json
{
    "profile_id": 1300420,
    "name": "/steam/76561198342887481",
    "alias": "cC.ilBuonFabio",
    "personal_statgroup_id": 1094840,
    "xp": 1283,
    "level": 1,
    "leaderboardregion_id": 0,
    "country": "it"
}
```
