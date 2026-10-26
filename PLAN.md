# Working notes

Durable plan/progress log so a future session (or a fresh agent with no chat
history) can see what is finished, what is verified, and what is still open.

**Last updated:** 2026-10-26

## Current task: Bingo game (multiplayer + bots)

Requested: a Bingo game for Game Hub with smart bots, multiplayer, rooms, a host
who can invite people to the game, and in-room chat.

**Status: implemented and pushed to `main` on 2026-10-26. Only the real-browser
WebRTC room test is still outstanding.**

### Files touched

| Path | What changed |
|------|--------------|
| `games/bingo.html` | New game. Live 75-ball caller, 5x5 card, dabs, smart bots, room lobby, PeerJS netcode. |
| `style.css` | New `/* ---------- bingo ---------- */` section (card, ball, roster, lobby, mobile rules) plus `.t12` card gradient. |
| `index.html` | 12th game card, game count 12, meta description. |
| `README.md` | Bingo row in the games table, "Bingo rooms" section, structure entry, offline caveat. |
| `downloads/*.zip` | Regenerated via `scripts/build_downloads.py` (all zips inline `style.css`, so they all grow together). |

### How it works (decisions already made)

- **No server, still GitHub Pages.** Multiplayer uses
  [PeerJS 1.5.5](https://peerjs.com) from a CDN, loaded lazily only when a room
  is created or joined. The free public broker (`0.peerjs.com`) does signalling;
  gameplay data flows peer-to-peer.
- **Host is authoritative.** The host draws numbers, simulates bots, validates
  every claim against the numbers actually called *and* the dab indices the
  claimer sent, then broadcasts the result. Guests never trust their own claim.
- **Room codes = peer IDs.** Host registers as `gh-bingo-<CODE>` (4 chars from
  `ABCDEFGHJKLMNPQRSTUVWXYZ23456789`), retries on `unavailable-id`. Invite link
  is `games/bingo.html?room=CODE`, which pre-fills the code on load.
- **Bots** are sim-only, three tiers (`easy`/`normal`/`hard` = Casual/Sharp/
  Ruthless) differing in dab reaction time and claim delay. Works offline.
- **Claim rule:** a line counts only if its cells are dabbed *and* those numbers
  were called. Free centre (index 12) always counts.
- **Offline:** solo vs bots works with no network. `bingo.zip` is built by the
  existing script (single self-contained `index.html`), so game CSS must stay in
  `style.css`, not in a `<style>` block in the page.

### Verified so far

- `node --check` on the extracted page script.
- Pure rules via extracted `// --- pure-logic-start/end ---` block: 3,000 cards
  (column ranges, uniqueness), all 12 lines, claim validation edge cases.
- jsdom click-through: menu, solo start, card/HUD/roster, rejected claims,
  uncalled-number rejection, return to menu, invite-link prefill.
- Round engine with a faked `Date.now`: pause blocks calls, manual call, bot
  wins, winner tag, next round resets.
- Two jsdom page instances with an in-process PeerJS stub: host code + invite
  link, guest joins, host controls hidden for guests, start reaches both,
  claims/calls broadcast, result reaches both, host leaving notifies guest.
- `downloads/bingo.zip` rebuilt, inlines the stylesheet, standalone copy boots.
- Served on `0.0.0.0:3000`: `/`, `/games/bingo.html`, `/style.css`, both zips
  return 200 with correct content types.

**Test harnesses were ad hoc (jsdom installed in `/tmp`), so they are gone.**
Recreate if needed: `npm i jsdom` in a temp dir, load the HTML with
`runScripts: 'dangerously'`, stub `window.Peer` with a Map-registry fake that
mirrors the used API (`on/once/connect/send/close/destroy`, `connection`,
`open`, `data`, `close` events).

### Open items / next steps

1. **Real-browser room test** — the only untested part is actual WebRTC:
   two browsers, one hosts, one opens the invite link, play a round. Watch for
   NAT/TURN failures (no TURN is configured; strict NATs may not connect) and
   for the signalling broker being down.
2. **Visual check on a phone** — the mobile/contrast pass below was verified by
   measurement only. Needs a real screen: Four in a Row board edge, empty
   sockets, discs, and the Bingo start menu on a short phone.
3. Not built: spectator mode, full-house mode, per-room win history.

### In-room chat (2026-10-26)

- Panel appears below the board whenever you are in a room (lobby and play).
- Guests only connect to the host, so **the host relays**: a guest's message is
  shown locally for the sender, appended on the host, then forwarded to the
  other guests (never echoed back to the sender).
- 140 chars, control characters stripped, rendered with `textContent`, 500ms
  per-player rate limit, last 80 messages kept in memory only.
- Join/leave produce system lines (`"Nova joined the room"`) broadcast by host.

## Mobile / visibility pass (2026-10-26)

Follow-up on the report that Four in a Row was blending into the background and
that mobile sizing was unfinished. (The earlier commit `188a790` had already
capped canvases/boards to the phone viewport for other games; connect4 was left
untouched then.)

### Four in a Row (`style.css`, `.c4-*`)

- Board frame lightened from `#1b2440 → #0d1322` to `#3a4877 → #1a2135`, with a
  purple border (`rgba(167,139,250,.5)`), a 26px purple halo and an inset top
  highlight. It now reads as a raised tray instead of dissolving into the
  `#05070c` stage.
- Empty sockets darkened to a radial near-black with an inset ring, so holes
  look punched out of the frame rather than being the same void as the stage.
- Discs get a top highlight and drop shadow for depth on dim screens.
- Hover/column highlight now also draws a purple ring (was a barely-visible
  `#101827` fill).
- Phone sizing: board width is capped by leftover viewport height
  (`min(100%, max(260px, calc((100dvh - 264px) * 1.166)))`) and padding/gap
  shrink, so a full board fits without scrolling on portrait phones.

Measured contrast against the stage (1.0 = identical): board top 1.32 → 2.28,
board bottom 1.09 → 1.26 (plus the purple edge), hole vs frame 1.09 → 1.27.

### Minesweeper (`style.css`, `.mine-grid` / `.cell`)

- The grid had **no frame at all**: tiles floated on the near-black `.stage`
  and opened cells were `#0b0f18` — a 1.05 ratio against the background, so
  cleared squares vanished as you played.
- Added a tray (`#2c3854 → #141b2a`) drawn with `box-shadow` instead of a
  border, deliberately: the page's `sizeCells()` measures padding only, so a
  real border would have broken its fit maths.
- Closed tiles are raised now: `#3b4767 → #242d45`, purple-tinted border, top
  highlight (1.87 against the tray, 2.03 against opened cells). Opened cells are
  flat, near-black and inset-shadowed so they read as recessed holes rather than
  background. Hover brightens; the red boom state keeps its glow.

Pattern worth keeping for the rest of the site: `.stage` is `#05070c`, so any
board built from dark tiles needs its own lighter frame or the playfield
visually disappears.

### Bingo (`style.css`, `.bingo-*`)

- The mobile block had set `min-height: 0` on the stage, which let the start
  menu's form overflow a short stage. Now `min-height: min(480px, 74dvh)`, and
  the stage overlay scrolls (with `safe center`) on very short screens.

### Blocker to remember

There is **no browser in this VM**: no chromium installed, no sudo, and the apt
mirror is stale, so Playwright's browser cannot launch (`libnss3` etc. missing).
Visual verification must be done in Freebuff's Browser panel on the preview
(`0.0.0.0:3000`), or by the user on a phone.

## Project conventions to keep

- Vanilla HTML/CSS/JS, no build step, no frameworks for the site itself.
- Game-specific CSS belongs in `style.css` (the download script inlines it).
- After any game edit: `python3 scripts/build_downloads.py` and commit the zips.
- Game pages mirror the existing shell: `.game-page`, `.game-head`, `.hud`,
  `.overlay`, `.controls-hint`; download button markup must match
  `<a class="btn btn-green btn-sm" href="../downloads/<name>.zip" download>⬇ Download</a>`
  so the offline builder can strip it.
