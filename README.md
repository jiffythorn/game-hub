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
| 🔢 **2048 Merge** | Arrows / WASD / swipe | 4×4 sliding puzzle, undo, best score and top tile |
| 🟪 **Block Drop** | Arrows / WASD, Space hard drop | 7-bag pieces, ghost preview, 10 lines per level |
| 👾 **Star Swarm** | ← → / A D, Space to fire | Waves, 3 lives, destructible bunkers, best score |
| 🔴 **Four in a Row** | Click / tap a column | 7×6 board, 3 AI levels, 2-player mode |
| 📦 **Sokoban** | Arrows / WASD / swipe | 8 hand-built levels, undo, hints, move & push counters |
| 🎟️ **Bingo** | Click / tap to dab, `B` to claim | 75-ball caller, 5×5 cards with free centre, smart bots, **multiplayer rooms with invite links** |

## Play offline

Every game is a single static page — there is no server and no build step.

> Bingo's solo mode (you against bots) works offline. Its multiplayer rooms
> need an internet connection, because players connect to each other directly.

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

## Bingo rooms

Bingo can be played alone or with friends. No account, no game server to run:

- **Solo** — pick 0–5 bots. Bots track every line on their card, dab with
  human-like reaction times, and shout bingo once a line is complete. There are
  three speeds: *Casual* (slow and forgiving), *Sharp* (a fair race) and
  *Ruthless* (spots a line almost instantly).
- **Host a room** — you get a 4-character code plus an invite link. Whoever
  opens the link lands in your lobby; you choose the bot count, difficulty and
  call speed, then press start.
- **Join a room** — type a friend's code, or just open the invite link.
- **Room chat** — everyone in the room can talk while waiting and during a
  round. Guests' messages are relayed by the host, the same way game state is.

How it works: the host's browser is authoritative — it draws the numbers,
validates every claim against the numbers actually called, runs the bots and
broadcasts state. Players connect directly via WebRTC using
[PeerJS](https://peerjs.com)'s free public signalling server, so there is still
nothing to host and the site stays a static GitHub Pages deploy. If the host
closes the tab, guests are told the room is gone.

Only the host's connection to the signalling server is required; no messages go
through Game Hub itself.

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
│   ├── minesweeper.html
│   ├── 2048.html
│   ├── blocks.html
│   ├── swarm.html
│   ├── connect4.html
│   ├── sokoban.html
│   └── bingo.html
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
