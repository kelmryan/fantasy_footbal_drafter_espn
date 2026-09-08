# Yahoo Guillotine Auction League — "darrell n's Superb League"

This folder is a **separate league** from the ESPN "click clack" league documented in the repo-root CLAUDE.md. Different platform, different format, different scoring — don't mix strategy files or state between the two.

## League facts

- League: **darrell n's Superb League**, Yahoo, leagueId `1565489`. League settings list max 18 teams, but the live draft's pick numbering confirms **16 teams are actually drafting** (round 1 = picks 1-16, round 2 starts at 17 with the same team that had pick 16 — standard snake reversal for 16 teams).
- Kelly's team name: **"Your Team"** (its literal, never-renamed display name — not a placeholder)
- Format: **Guillotine ("Death" scoring type)** — this is an elimination league, not a normal season-long/playoff format. Yahoo's settings label it "Death" scoring type and reference "guillotine elimination" in the waiver rules (1-day waiver turnaround for players dropped by an eliminated team, vs. the normal 2-day period). **Exact elimination cadence (weekly? starting what week? one team per elimination event?) is not yet confirmed — ask Kelly and record it here once known.**
- Draft: **Snake draft** (confirmed live — settings page said "Live Standard Draft" and this matched what actually happened), live **Mon Sep 7, 2026, 8:00pm EDT**, 1-minute pick clock, 16 teams drafting. Kelly's slot: **5th of 16**. (Auction/$1000-budget was an initial misread before the draft started — no bidding is happening; this is picks in order like the ESPN league.)
- Roster (14 spots): QB, WR, WR, RB, RB, TE, W/R/T (flex), BN x6, IR x1 — **no Kicker, no D/ST**. That removes two budget lines and two position-expert needs entirely versus the ESPN league.
- Trades: **not allowed**, all season (0 max trades). Waiver wire is the only in-season lever.
- Waivers: **FAAB** ("FAB" in Yahoo's UI) with continual rolling-list tiebreak. Normal waiver period is 2 days; players dropped due to guillotine elimination clear in **1 day** — expect fast, frequent waiver churn as teams get eliminated and dump talent back to the pool.
- Fractional points and negative points: both enabled.

## Scoring

Standard for QB/RB/WR: 25 pass yds/pt, 4-pt pass TD, **-1 INT**, 10 rush/rec yds/pt, 6-pt rush/rec TD, **0.5 PPR**, 2-pt conversions = 2, fumbles lost -2, return TD = 6, offensive fumble return TD = 6.

**TE gets full PPR (1.0/reception)** — every other rule is identical to QB/RB/WR. This is the one scoring quirk in the whole league, and it's a big one: a target-hog TE earns a reception bonus at *double* the rate of a target-hog RB/WR. See `state/research/positional-value-tiers.md`.

INT at -1 (not the ESPN league's -2) is slightly friendlier to volume-passing QBs than you're used to, though QB is still just one starting slot against a deep waiver pool.

## Key strategic implications

- **TE premium**: expect the true elite pass-catching TEs to go for real money early — a full-PPR TE outproduces a half-PPR RB/WR of similar target share on receptions alone. Don't assume ESPN-league TE patience applies here.
- **Guillotine rewards floor over ceiling**: a boom/bust player who can post a zero is a genuine season-ending risk if it lands on a week you're near the bottom of the standings. Depth and weekly consistency across the whole roster matter more than raw ceiling — see `state/research/guillotine-strategy.md`.
- **No trades**: FAAB and the waiver wire are the only way to fix a draft mistake in-season. Budget management (both draft-day $ and season-long FAAB) matters more here than in a trade-enabled league.
- **No K/DST**: one less thing to plan for in the auction — that budget stays in play for skill positions.

## Agent set (built fast-path — see below)

No dedicated subagents exist yet for this league (built the strategy files first since the draft was hours away when this folder was created). Until built, evaluate players using the ESPN league's `rb-expert`, `wr-expert`, `te-expert`, `qb-expert` agents but **always pass this league's scoring rules explicitly in the prompt** (0.5 PPR standard / 1.0 PPR at TE, -1 INT, guillotine format, auction not snake) — those agents default to the ESPN league's full-PPR/-2 INT rules otherwise and will misvalue players, especially TEs and QBs.

`dst-expert` and any kicker logic are **not applicable** to this league (no roster slots for either).

## Role: Draft Manager (Snake)

Same mechanics as the ESPN league's draft manager — this is a normal 18-team snake draft, Kelly picks 5th (so pick 5, then pick 32, i.e. 18+18-5+1... recompute per actual reversal each round), no bidding.

- Track every pick (round, overall pick #, player, position, NFL team, who drafted them) in `state/draft-board.md`, and update which of Kelly's roster/bench slots are filled.
- When Kelly's turn approaches, identify 2-4 realistic candidates given his remaining needs and recommend one, same pattern as the ESPN draft manager role.
- Flag the TE-premium dynamic (see `positional-value-tiers.md`) whenever a strong pass-catching TE is a live candidate — they carry more relative value here than half-PPR instincts suggest, so they may be worth taking a round or so earlier than usual.
- No auction budget tracking needed. `auction-budget-strategy.md` in `state/research/` no longer applies — ignore it (kept for reference in case a future league of Kelly's actually is an auction).

## State files

- `state/draft-board.md` — nomination/bid log + Kelly's roster-in-progress and remaining budget
- `state/roster-notes.md` — current roster, FAAB balance, standing notes
- `state/news/[position]-intel.md` — cached player intel (rb/wr/te/qb — no k/dst files needed)
- `state/research/` — strategy docs, see below

## Strategy files (state/research/)

- `draft-strategy-core.md` — auction budget philosophy for this league
- `positional-value-tiers.md` — how the TE-premium and 0.5 PPR reshape positional value vs. a standard PPR league
- `guillotine-strategy.md` — roster construction and in-season management for an elimination format
- `auction-budget-strategy.md` — $1000 budget allocation math and nomination tactics

Read the relevant file(s) before every recommendation, same discipline as the ESPN league's CLAUDE.md.
