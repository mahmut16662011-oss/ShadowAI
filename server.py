import os
import re
from datetime import datetime, timezone
from typing import Any

import httpx
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("ShadowAI Chess.com", json_response=True)
mcp.settings.host = os.getenv("HOST", "0.0.0.0")
mcp.settings.port = int(os.getenv("PORT", "8000"))

CHESS_API = "https://api.chess.com/pub"
HEADERS = {
    "User-Agent": os.getenv("CHESSCOM_USER_AGENT", "ShadowAI-Chess-Finder/0.1 (public game archive lookup)"),
    "Accept": "application/json",
}

def normalize_username(value: str) -> str:
    value = value.strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{2,30}", value):
        raise ValueError("Invalid Chess.com username.")
    return value.lower()

async def get_json(client: httpx.AsyncClient, url: str) -> dict[str, Any]:
    response = await client.get(url, headers=HEADERS, timeout=20.0)
    response.raise_for_status()
    return response.json()

@mcp.tool()
async def find_chesscom_games(opponent: str, username: str = "shadowmahmud", limit: int = 10) -> dict[str, Any]:
    """Find a user's public Chess.com games against a named opponent and return PGNs for analysis.

    Use this when the user asks to find a game they played against an opponent.
    Only public games are available; private messages and private account data are not accessed.
    """
    me = normalize_username(username)
    rival = normalize_username(opponent)
    limit = max(1, min(int(limit), 25))
    async with httpx.AsyncClient(follow_redirects=True) as client:
        archives_data = await get_json(client, f"{CHESS_API}/player/{me}/games/archives")
        archives = archives_data.get("archives", [])
        matches = []
        errors = []
        # Newest months first, stopping once enough matches are found.
        for archive_url in reversed(archives):
            try:
                data = await get_json(client, archive_url)
            except Exception as exc:
                errors.append(f"{archive_url.rsplit('/', 2)[-2:]}: {type(exc).__name__}")
                continue
            for game in data.get("games", []):
                white = (game.get("white") or {}).get("username", "").lower()
                black = (game.get("black") or {}).get("username", "").lower()
                if rival not in (white, black):
                    continue
                me_is_white = white == me
                mine = game.get("white" if me_is_white else "black", {})
                theirs = game.get("black" if me_is_white else "white", {})
                end_time = game.get("end_time")
                matches.append({
                    "date": datetime.fromtimestamp(end_time, timezone.utc).isoformat() if end_time else None,
                    "url": game.get("url"),
                    "opponent": theirs.get("username", opponent),
                    "color": "White" if me_is_white else "Black",
                    "result": mine.get("result"),
                    "my_rating": mine.get("rating"),
                    "opponent_rating": theirs.get("rating"),
                    "time_class": game.get("time_class"),
                    "pgn": game.get("pgn"),
                })
            if len(matches) >= limit:
                break
    matches.sort(key=lambda g: g.get("date") or "", reverse=True)
    return {
        "username": me,
        "opponent_query": rival,
        "count": min(len(matches), limit),
        "matches": matches[:limit],
        "note": "Public Chess.com archive only. A game is returned only when present in the public archive.",
        "archive_errors": errors[:3],
    }

@mcp.tool()
async def get_chesscom_player_profile(username: str = "shadowmahmud") -> dict[str, Any]:
    """Get public Chess.com profile details for a player."""
    user = normalize_username(username)
    async with httpx.AsyncClient(follow_redirects=True) as client:
        return await get_json(client, f"{CHESS_API}/player/{user}")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
