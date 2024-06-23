from typing import Any, Dict, List

def make_cargo_query(tables: List[str], fields: List[str], where: str = "", **kwargs) -> Dict[str, Any]:
    return {
        "action": "cargoquery",
        "tables": ", ".join(tables),
        "fields": ", ".join(fields),
        "where": where,
        "limit": kwargs.get("limit", "max"),
        "format": kwargs.get("format", "json"),
        "offset": kwargs.get("offset", 0),
        "order_by": kwargs.get("order_by", "")
    }

def make_player_stats_query(player_name: str, **kwargs) -> Dict[str, Any]:
    tables = [
        "ScoreboardPlayers=sp"
    ]

    fields = [
        "sp.Name",
        "sp.Champion",
        "sp.Kills",
        "sp.Deaths",
        "sp.Assists",
        "sp.DateTime_UTC",
        "sp.OverviewPage",
        "sp.PlayerWin"
    ]

    where=f'sp.Name="{player_name}"'

    if (champion := kwargs.get("champion")) is not None:
        kwargs["order_by"] = "sp.DateTime_UTC DESC"

        where += f' and sp.Champion="{champion}"'

    return make_cargo_query(tables, fields, where, **kwargs)