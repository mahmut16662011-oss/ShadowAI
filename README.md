# ShadowAI Chess.com agent backend

This repository contains a public-game search tool for ChatGPT/MCP integration.

## Tool
- `find_chesscom_games(opponent, username="shadowmahmud", limit=10)`: searches public monthly Chess.com archives newest-first and returns matching game metadata and PGN.
- `get_chesscom_player_profile(username="shadowmahmud")`: retrieves public profile data.

No password, session cookie, or OAuth token is used. It does not read inbox messages or private account data.

## Run locally
```bash
pip install -r requirements.txt
python server.py
```
The MCP Streamable HTTP server listens on port 8000 by default.

## Important deployment status
The source code is prepared, but it is **not hosted or connected to ChatGPT yet**. A reachable HTTPS deployment is required before ChatGPT can call these tools. The repository alone is not a live backend. Use a hosting provider that supports a persistent Python web service and set the service start command to `python server.py`.

## API behavior
The tool reads public archives from Chess.com's Published Data API and returns PGN records where available. Requests may fail if Chess.com rate-limits or denies access. In that case, the tool reports the request failure instead of inventing results.
