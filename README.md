# 🎮 Game Hub

Play classic arcade and card games free in your browser — and **download them to play offline**.

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
| 🧱 **Brick Breaker** | Mouse / touch / arrows | 3 lives, escalating levels, narrowing paddle |
| 🏓 **Paddle Duel** | W/S, ↑↓, mouse, touch | First to 7, adaptive AI, win streaks |
| 🐦 **Flappy** | Space / click / tap | Endless pipes, high score |
| 🃏 **Memory Match** | Click / tap | 4×4, 6×6, 8×8 grids, timer, best time |
| 💣 **Minefield** | Click to reveal, right-click / flag mode to flag | 3 levels, first click always safe |
| 🔢 **2048 Merge** | Arrows / WASD / swipe | 4×4 sliding puzzle, undo, best score and top tile |
| 🟪 **Block Drop** | Arrows / WASD, Space hard drop | 7-bag pieces, ghost preview, 10 lines per level |
| 👾 **Star Swarm** | ← → / A D, Space to fire | Waves, 3 lives, destructible bunkers, best score |
| 🔴 **Four in a Row** | Click / tap a column | 7×6 board, 3 AI levels, 2-player mode |
| 📦 **Crate Pusher** | Arrows / WASD / swipe | 8 original levels, undo, hints, move & push counters |
| ♠️ **Blackjack** | Click / tap, H / S / D / N | 6-deck shoe, hit/stand/double, 3:2 naturals, saved bankroll |
| 🎟️ **Bingo** | Click / tap to dab, `B` to claim | 75-ball caller, 5×5 cards with free centre, smart bots, **multiplayer rooms with invite links** |
| 🎱 **Bingo 2** | Click / tap to dab, card tabs for extra cards | Second table: solo players and hosts pick any line, four corners, X, T, H, climbing ladder, bullseye or blackout plus a pattern of the day with a daily streak, 0–3 smart bots, 5-character room codes, lobby and in-game chat, **points with a card cost, a shared pot and a room jackpot**, a saved balance plus separate solo and room standings (gross, net and return on card costs), a daily streak with a bankable freeze earned from blackouts a seven-day history strip, and a nudge naming today's pattern when a banked freeze is waiting on it (snoozable until tomorrow) (carried in the restore code, with a warning when the carried run has already lapsed), restore codes and signed gift codes |
| 🪲 **Thornlight** | Arrows / A D / drag | An original night-garden bug shooter: segmented thornworms that split when shot, bouncing thorn shards, breakable bloom pods, auto-fire, 3 lanterns and escalating waves |
| 🎴 **Chromaclash** | Click / tap a card, click the well to draw | An original hue-matching card game: 112 cards in four hues with shape marks, Jam, Loop, Toll, Swap, Prism and Prism Toll, SOLO last-card calls with a catch window, 1–3 smart bots, **private rooms with host-created 5-character codes and invite links**, lobby and in-game chat, bot takeover if a guest drops |

> **Chromaclash is an original game.** Its name, card faces, hue names, action names and
> rules text were made for Game Hub — no other card game's branding, wording or art is
> used. The underlying mechanics (matching, skipping, reversing, drawing) are not
> copyrightable; the expression here is our own.
>
> **Thornlight is an original game.** Its name, lantern beetle, thornworms, bloom pods,
> thorn shards, canvas art, synthesised sounds and wording were made for Game Hub. The
> fixed-shooter mechanics (a segmented enemy, breakable obstacles, ricocheting hazards)
> are not copyrightable; every piece of expression here is our own.
>
> **Paddle Duel, Brick Breaker and Crate Pusher are original presentations.** Their
> names, wording and level layouts were made for Game Hub. Paddle rallies, brick
> smashing and crate pushing are unprotected mechanics; Crate Pusher's eight maps are
> our own designs, not reproductions of another game's levels.

## Play offline

Every game is a single static page — there is no server and no build step.

> Bingo and Bingo 2 work offline against bots. Their multiplayer rooms need
> an internet connection, because players connect to each other directly.
> The two tables keep separate saved names and rooms; Bingo 2 also tracks
> its own best score.

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

## Operator tools (local only)

The local `tools/mint.html` signs Bingo 2 point grants. Open the file
directly — it has no dependencies and makes no network calls. It is ignored by
git and is not published with the site.

- **Keys:** ECDSA P-256 via Web Crypto. Create a key in the page, export it as
  JSON for backup, import it elsewhere, or delete it. The public JWK and a
  SHA-256 fingerprint are shown so a verifier can be pinned to it.
- **Grants:** `GH2G.1.<role>.<payload>.<sig>`, where the payload is base64url
  JSON `{c,r,e,i,n}` (points, role, expiry, issued, nonce) and the signature
  covers the first four dot-separated parts.
- **Caps:** promo 1,000 · operator 10,000 · prize 25,000 points per grant.
  Expiry runs from 1 hour to 90 days; a batch is up to 25 codes.
- **Pairing:** copy the game snippet the page shows and paste it over
  `const GRANT_KEY = null;` in `games/bingo-2.html`. Only that public key is
  trusted; the private key never leaves the tool.
- **Output:** a copyable code, a `…bingo-2.html?gift=<code>` link, CSV with
  `code,role,points,issued,expires,gift_link`, and a built-in verifier for
  pasted codes (it flags tampering, over-cap amounts and expiry).
- **Never deploy it.** The page is `noindex`, and
  `scripts/build_downloads.py` keeps `tools/` out of every ZIP. Anyone holding
  the private key can mint points, so keep it as private as a key.

Bingo 2 does not consume grants yet — the redeem/claim path is the next step,
so treat today's output as codes waiting for a verifier.

## Deploy

GitHub Pages is configured to serve from the `main` branch, root folder.
Push to `main` and the site updates automatically.

## Project structure

```
game-hub/
├── index.html                 home page + game grid
├── chat.html                  guestbook (giscus)
├── terms.html                 terms + points notice
├── tools/mint.html            local-only point grant signer (never shipped)
├── giscus-theme.css           custom giscus theme
├── style.css                  shared theme and layout
├── games/
│   ├── snake.html
│   ├── brick-breaker.html
│   ├── paddle.html
│   ├── flappy.html
│   ├── memory.html
│   ├── minefield.html
│   ├── 2048.html
│   ├── blocks.html
│   ├── swarm.html
│   ├── four-in-a-row.html
│   ├── crate-pusher.html
│   ├── blackjack.html
│   ├── bingo.html
│   ├── chromaclash.html
│   └── thornlight.html
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
