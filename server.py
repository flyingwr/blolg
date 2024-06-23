from api.routes import Match, Players, PlayersPage

from aiohttp import ClientSession, web

import asyncio
import os

async def main():
    app = web.Application()
    app["session"] = ClientSession(headers={
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36"
    })
    app["leaguepedia_url"] = "https://lol.fandom.com/api.php"

    # API routes
    app.router.add_get("/api/match", Match)
    app.router.add_get("/api/players", Players)

    # Common routes
    app.router.add_static("/public", "./public")
    app.router.add_get("/players", PlayersPage)

    runner = web.AppRunner(app)
    await runner.setup()

    try:
        SERVER_PORT = os.getenv("PORT", 8080)
        
        site = web.TCPSite(runner, "0.0.0.0", SERVER_PORT)
        await site.start()

        print(f"Servidor iniciado. Porta: {SERVER_PORT}")
        
        while True:
            await asyncio.sleep(3600.0)
    finally:
        await runner.cleanup()

if __name__ == "__main__":
    asyncio.run(main())