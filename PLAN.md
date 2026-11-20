# Working notes

Durable plan/progress log so a future session (or a fresh agent with no chat
history) can see what is finished, what is verified, and what is still open.

**Last updated:** 2026-11-07 (Bingo 2 points, leaderboard record, restore code v2)

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

## Bingo 2 economy research (2026-11-07)

Requested: deep research into how credit-based online games work (buying
credits, pot-funded wins, retention) and what could be built into Bingo 2.

**Status: research + design proposal only. Nothing implemented, no code
changed.** The full write-up — market findings with sources, the legal line on
purchasable/redeemable credits, the proposed credit/pot economy with numbers,
and a phased build plan — is in [`BINGO-2-ECONOMY.md`](BINGO-2-ECONOMY.md).

Headline conclusions, for a session that cannot open the doc:

- Social bingo apps (Blitz, Bash, Aloha) do **not** run player-funded pots;
  prizes are algorithmic per player. Real pots exist in regulated bingo
  (stakes − participation fee), pari-mutuel apps (Bingo Tour) and pool/poker
  (8 Ball Pool).
- Retention is driven by **competition events** (+212% YoY at Blitz) and
  drip rewards more than by features; a weak collection is revenue-negative.
- A pure bot/player pot with no sink inflates and dies; needs a rake, a stake
  ladder and top-3 payouts.
- Selling credits or letting them be redeemed = gambling (UK licence; NY/TN/WA
  enforcement). Stay single-currency, non-redeemable, free entry. The doc's §5
  now models the four switches (purchase / value out / transfer / rake) and the
  three separate robot issues (gambling test, disclosure, overlay vs
  house-banked).
- Cross-device saves are specified in the doc's §6: a self-contained restore
  code (no backend, no PII, ships with the wallet) and an optional anonymous
  sync key backed by a tiny Worker. No accounts.
- Operator grants are §7: ECDSA-signed gift tokens verified against embedded
  public keys (role caps enforced client-side), `?gift=` links, a redeem field,
  an in-room host tip, and a local-only `tools/mint.html`. Single use and
  revocation need the Worker.
- Best structural change for Bingo 2: replace "first bingo ends the round"
  with a **call budget + multiple bingos paid by rank** (55/25/12), which is
  what makes buying extra cards meaningful.

### Implemented: points, tables, pot and jackpot (2026-11-07)

Phases 1 and 2 of [`BINGO-2-ECONOMY.md`](BINGO-2-ECONOMY.md) are built.

**Files:** `games/bingo-2.html`, `bingo-2.css`, `downloads/*.zip` (regenerated).

**What shipped**

- **Points**: 1,000 to start, persisted in `gh.bingo2.wallet`. The HUD carries
  `Points` and `Pot` chips. Points are score tokens: not buyable, not
  transferable in the UI, never redeemable for anything of value.
- **Tables**: Practice (0) / Bronze 10 / Silver 50 / Gold 250 / Champion
  1,000 per card, chosen in the create form and the lobby. `Cards each` 1–3
  applies to every seat; ante = stake × cards.
- **Pot**: entries = seats × ante; 6% rake (half to the jackpot, half deleted);
  jackpot also takes 5% of entries. `Pot` and `🎰` show in the room bar.
- **Round shape**: the round no longer ends at the first bingo. It runs to a call
  budget (line 32, corners 45, blackout 75) and pays every bingo by rank —
  55 / 25 / 12, remainder rolls into the jackpot. Nobody bingos → whole pot rolls.
- **Jackpot**: seeded at 10 × stake, pays a bingo inside 12 (line) / 20 (corners)
  / 52 (blackout) calls, then resets to seed.
- **Bots** ante from their own balance but their winnings are **discarded** (the
  sink) and their balance refills to 3,000; labelled 🤖 as before.
- **Multi-card**: card tabs above the board; daub messages carry a card index
  (`{t:'daub', c, n, round}`); guests apply daubs per card.
- **Patterns**: the host picks Any line, Four corners, X, T, H, **Climb the
  ladder** (a staircase of squares), **Bullseye** (the 3×3 target around the
  centre; the centre is a live number, not a free space) or Blackout. Each
  pattern is a plain set of card indices checked by `findWin`, with its own call
  budget and jackpot window. `makeCard(freeCenter)` deals a live centre for
  Bullseye; a `0` at index 12 in the start payload still means a free centre, so
  the guest side needs no extra protocol.
  Solo play uses the same pattern list: a picker in the page head (saved in
  `gh.bingo2.soloPattern`) deals a matching card, including a live centre for
  Bullseye, and best scores are kept per pattern (`gh.bingo2.best.<pattern>`;
  an older single best migrates to any-line).
  A pattern of the day rotates through the table one step per local calendar
  day (`dailyPatternKey()`, day number from local Y/M/D in UTC), shown as a
  header chip that plays it, and offered as a `daily` shortcut in the room
  form that resolves to the concrete pattern on create.
  A streak counter (`gh.bingo2.daily`: `last`, `streak`, `best`) counts
  consecutive local days with a completed round on that day's pattern — solo
  wins and no-bingos, plus seated room rounds whose pattern matches — and shows
  as a `🔥 Streak` HUD chip in solo. It is calendar-day based, so it lapses
  silently if a day is missed and resets to 1 on the next daily play.
  The wallet record also tracks `staked` (points spent on cards in seated
  rounds) so the panel can show **Return on cards** = earned ÷ staked. That
  makes a 10-point heads-up win and a 1,000-point full-table win comparable
  instead of ranking by pot size. Restore codes are now v3 (22 bytes, 9
  four-character groups) carrying points, earned and staked plus games/wins;
  v2 and v1 codes still decode, with staked defaulting to zero.
  The record is split into `solo` and `room` standings: solo carries games,
  wins and win rate (no points move in solo), rooms carry games, wins, gross
  points won, **net** (gross − card costs) and return. Restore codes are v4
  (25 bytes, 10 four-character groups) carrying both standings; v3/v2 map their
  old flat counters onto the room side, v1 still carries points only.
  Codes are v5 (26-byte payload, 12 four-character groups) and also carry the
  daily streak: `last` as a 16-bit calendar day, streak and best as bytes. A
  restore keeps whichever streak reached the later day (longer one on a tie)
  and the highest best, so moving browsers doesn't reset the run.
  A carried streak that ended more than a day before today is called out in
  the preview and again after the restore: the best is kept, but it is not
  presented as a live run.
  A single streak freeze (`gh.bingo2.daily.freezes`, capped at 1) is earned
  by finishing a blackout in solo or winning a blackout room, and is spent
  automatically when exactly one day was missed. It rides in the code's
  formerly-reserved byte, so the v5 length is unchanged.
  The daily record also keeps `days` (last 7, `{d, t}` with t 0 played / 1
  frozen), rendered as a strip under the HUD: weekday + day number, amber for
  played, snowflake for a frozen day, dim for missed. History is local-only;
  codes carry the streak and freeze, not the strip.
  While a freeze is banked and today's pattern is still unplayed, a small
  reminder sits under the strip with a "Play today" button; it hides once the
  daily is played, the freeze is spent, or a room is entered.
  "Not today" stores `gh.bingo2.daily.snoozed = today`, so the reminder stays
  hidden for the rest of that day and returns on the next one; snoozing never
  touches the streak or the freeze itself.
  The reminder names today's pattern and its button doubles as a state cue:
  "Play today" switches to it, and once it is the selected solo pattern the
  button reads "✓ Today selected" and is disabled.
- **Guests** send their balance on join (honour system, per the doc §6.5), receive
  `start`/`lobby`/`end` payloads with credits, pot, payouts and jackpot, and see
  the settlement lines in the end overlay.

- **Explainer**: a collapsible "How credits work" panel sits in the room dialog
  (visible while creating, joining and waiting in the lobby) and states that
  credits have **no cash value** and that bots ante but **never collect**.
- **Terms**: new `terms.html` with a plain-language terms page and a prominent
  play-money notice (no cash value, nothing buyable, bots never collect, host
  is the bank, chat is unmoderated). Linked from the index and guestbook
  footers and from the room-dialog explainer; `build_downloads.py` rewrites the
  link to the published URL in standalone game copies.

**Verified:** `node --check` on the extracted script; a jsdom harness (fake clock,
controllable timers, stubbed `Peer` broker shared by two windows) covering solo
start, room creation, a guest joining and daubing, a full 32-ball round with pot
57, jackpot growth, settlement back to both clients, and a second round charging
the ante again — all checks passed. `python3 scripts/build_downloads.py` rebuilt.

- **Wallet**: credits persist to `gh.bingo2.wallet` in localStorage on every
  change (`setMyCredits`), and the room dialog carries a wallet panel: current
  balance, a copyable `GH2-XXXX-…` restore code (base32 over a CRC32-checked payload
  XORed with a fixed pad, points clamped to 0–10,000,000; v2 also carries
  games, wins and points earned, v1 codes still decode) and a two-step restore (parse → "replace my balance" confirm).
  Restoring is disabled inside a room, because the host's ledger is
  authoritative and would otherwise overwrite the restored wallet.

- **Mint tool**: `tools/mint.html` is a self-contained local page that signs
  `GH2G.1.<role>.<payload>.<sig>` grants with an ECDSA P-256 / SHA-256 key held
  in that browser (create, import, export, delete, SHA-256 fingerprint, JWK for
  the future verifier). Role caps promo 1,000 / op 10,000 / prize 25,000,
  expiry 1h–90d, batches of 25, gift links from a configurable game URL, CSV
  export and a verify panel. `tools/` is excluded from every ZIP.

- **Gifts / redeem**: `games/bingo-2.html` holds `GRANT_KEY` (null by default)
  and verifies `GH2G` grants with Web Crypto: signature, role cap, expiry, then
  a nonce claim ledger (`gh.bingo2.claims`, last 200) so a code works once per
  browser. `?gift=` opens a redeem overlay; the wallet panel also has a redeem
  field. Minting/redeeming is blocked inside a room, where the host ledger
  would overwrite the result. Pair a copy by pasting the snippet the mint page
  now offers (it replaces `const GRANT_KEY = null;`).

- **Points follow the player, standing stays on the board** (2026-11-07): the
  wallet keeps a record — games played, games won, points earned — next to the
  balance. `recordRound()` runs once per seated round on the host (before the
  payout is ranked) and once on each guest (from the `end` payload, which now
  carries `cardsCount` and `seatIds`). The record is rendered in the wallet
  panel and the settlement overlay, and restore code v2 carries it, so moving
  to another browser brings the points **and** the record with them. Importing
  a code merges stats upward (`Math.max` on each counter, points replaced), so a
  restore can never lower leaderboard standing. Nothing is purchasable,
  cashable or transferable; the leaderboard standing is the whole prize.

**Known gaps:** the wallet is per browser — no server sync, and a restore code
is a snapshot rather than a live link; gift codes are verified client-side (a
claim ledger, not a server), so a determined player can still edit storage; the
pot is only play money and nothing is purchasable (see doc §5).

## Mobile / visibility pass (2026-10-26)

Follow-up on the report that Four in a Row was blending into the background and
that mobile sizing was unfinished. (The earlier commit `188a790` had already
capped canvases/boards to the phone viewport for other games; Four in a Row was left
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

### Minefield (`style.css`, `.mine-grid` / `.cell`)

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
