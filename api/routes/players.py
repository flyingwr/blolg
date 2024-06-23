from api.helpers.leaguepedia import make_player_stats_query

from typing import Optional

from aiohttp import web

class Players(web.View):
    async def get(self):
        if (player_name := self.request.query.get("player")) is None:
            raise web.HTTPNotFound()
        
        champion = self.request.query.get("champion")
        return web.json_response(await self.get_player_stats(player_name.capitalize(), champion))
            
    async def get_player_stats(self, player_name: str, champion: Optional[str]=None):
        async with self.request.app["session"].get(self.request.app["leaguepedia_url"],
            params=make_player_stats_query(player_name, champion=champion)
        ) as response:
            data = await response.json()
            limit = data.get("limits", {}).get("cargoquery", 500)

            cargoquery = data.get("cargoquery", [])

            if len(cargoquery) == limit:
                offset = len(cargoquery)

                while True:
                    async with self.request.app["session"].get(self.request.app["leaguepedia_url"],
                        params=make_player_stats_query(player_name, champion=champion, offset=offset)
                    ) as offset_response:
                        offset_data = await offset_response.json()
                        limit = offset_data.get("limits", {}).get("cargoquery", 500)

                        offset_cargoquery = offset_data.get("cargoquery", [])
                        cargoquery.extend(offset_cargoquery)

                        if len(offset_cargoquery) < limit:
                            break
                        
                        offset += len(offset_cargoquery)

        total_games = len(cargoquery)
        wins = sum(1 for game in cargoquery if game["title"]["PlayerWin"] == "Yes")
        defeats = total_games - wins

        win_rate = round((wins / total_games) * 100 if total_games > 0 else 0, 2)

        return {
            "matches": cargoquery,
            "wins": wins,
            "defeats": defeats,
            "win_rate": win_rate
        }
    
class PlayersPage(web.View):
    async def get(self):
        return web.FileResponse("./public/players/index.html")