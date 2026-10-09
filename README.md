# 🎮 Game Hub

Play classic arcade games free in your browser — and **download them to play offline**.

No installs. No accounts. No ads. No tracking. Just HTML, CSS and vanilla JavaScript.

**▶ Play now: <https://jiffythorn.github.io/game-hub/>**
**💬 Guestbook: <https://jiffythorn.github.io/game-hub/chat.html>**

## Guestbook

Visitors can leave messages for each other on [`chat.html`](chat.html).

Chat is hosted by **[giscus](https://giscus.app)**, which turns a GitHub
Discussions category into a comment thread — so there is no server to run and
every message is a real GitHub Discussion you can moderate from the repo.

- **Repo settings used:** `repoId` `R_kgDOVBlm5A`, category `General`
  (`DIC_kwDOVBlm5M4DHYkc`), mapping `pathname`.
- **Theme:** [`giscus-theme.css`](giscus-theme.css) — imports the official dark
  theme, then remaps GitHub Primer colours to the Game Hub palette. GitHub
  Pages serves it with `access-control-allow-origin: *`, which giscus requires.
- **Moderation:** delete, hide, lock or pin messages from
  [Discussions](https://github.com/jiffythorn/game-hub/discussions). Reports
  filed through the site's 🚩 button open an issue labelled `report`.
- **Offline:** the guestbook needs internet, so the downloaded ZIP shows a
  friendly fallback instead of the chat.

> ⚠️ One-time setup: install the **[giscus GitHub App](https://github.com/apps/giscus)**
> on this repository, otherwise the embed cannot read or write discussions.

## Games

| Game | Controls | Features |
|------|----------|----------|
| 🐍 **Snake** | Arrows / WASD / swipe | Ramp-up speed, high score |
| 🧱 **Breakout** | Mouse / touch / arrows | 3 lives, escalating levels, narrowing paddle |
| 🏓 **Pong vs AI** | W/S, ↑↓, mouse, touch | First to 7, adaptive AI, win streaks |
| 🐦 **Flappy** | Space / click / tap | Endless pipes, high score |
| 🃏 **Memory Match** | Click / tap | 4×4, 6×6, 8×8 grids, timer, best time |
| 💣 **Minesweeper** | Click to reveal, right-click / flag mode to flag | 3 levels, first click always safe |

## Play offline

Every game is a single static page — there is no server and no build step.

**Option 1 — grab the whole site**

Download [`game-hub-offline.zip`](downloads/game-hub-offline.zip), unzip it, and double-click
`index.html`. Everything works with no internet connection.

**Option 2 — one game, one file**

Each game has its own ZIP containing a single self-contained `index.html`
(CSS inlined):

```bash
# from the repo, or after cloning
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

## Run locally

```bash
git clone https://github.com/jiffythorn/game-hub.git
cd game-hub
python3 -m http.server 8000
# open http://localhost:8000
```

Opening `index.html` directly from the filesystem also works.

## Rebuild the download ZIPs

The files in [`downloads/`](downloads/) are generated. After editing any game:

```bash
python3 scripts/build_downloads.py
```

Commit the regenerated ZIPs alongside your changes.

## Deploy

GitHub Pages is configured to serve from the `main` branch, root folder.
Push to `main` and the site updates automatically.

## Project structure

```
game-hub/
├── index.html                 home page + game grid
├── chat.html                  guestbook (giscus)
├── giscus-theme.css           custom giscus theme
├── style.css                  shared theme and layout
├── games/
│   ├── snake.html
│   ├── breakout.html
│   ├── pong.html
│   ├── flappy.html
│   ├── memory.html
│   └── minesweeper.html
├── downloads/                 generated ZIPs (do not edit by hand)
├── scripts/build_downloads.py rebuilds downloads/
├── LICENSE
└── README.md
```

## Adding a game

1. Create `games/mygame.html`, copy the shell from an existing game.
2. Link `../style.css` and add a card to `index.html`.
3. Run `python3 scripts/build_downloads.py`.
4. Add a ZIP card to `index.html` and a row to this README.

## License

[MIT](LICENSE)
