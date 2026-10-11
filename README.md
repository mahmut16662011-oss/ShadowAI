# ShadowAI — Chess.com Game Finder

A phone-friendly prototype that searches a public Chess.com player's game archives for games against a specified opponent.

## Current status
- Uses Chess.com's public Published Data API; no password or OAuth token is requested.
- Searches the player's public monthly archives and lists matching games with links and PGN display/copy actions.
- This is currently a standalone browser prototype, **not yet connected to ChatGPT as a callable agent tool**.
- Private inbox messages are not accessed.

## Run
Open `index.html` in a browser or host it as a static site (for example, GitHub Pages). If the browser blocks API requests due to CORS, a small server-side proxy will be needed.

## Next step
To make ChatGPT respond to a request like “analyze my game against Abukamal” without manual PGN copying, connect a hosted API endpoint to a ChatGPT tool/plugin and have it return the matching game's PGN.
