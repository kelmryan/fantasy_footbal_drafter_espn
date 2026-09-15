---
name: free-agent-check
description: Checks waiver-wire adds and drops for the Death to Nottighams Yahoo league, using the cached player intel and roster notes to recommend adds, drops, and waiver bids.
---

# Free Agent Check

This skill is for the Death to Nottighams league. It follows the same workflow as the repo's ESPN waiver skill but is tailored for the Yahoo league and the working-state files inside this folder.

## Required context to read first

1. `CLAUDE.md` in this folder
2. `state/roster-notes.md`
3. `state/player-intel.md`
4. The relevant cached position intel file under `state/news/`:
   - `state/news/rb-intel.md`
   - `state/news/wr-intel.md`
   - `state/news/te-intel.md`
   - `state/news/qb-intel.md`
   - `state/news/dst-intel.md`
5. When the league needs a formatting/model reference, read the corresponding ESPN cache files in `espn_click_clack/news/` as a style template, especially:
   - `espn_click_clack/news/rb-intel.md`
   - `espn_click_clack/news/wr-intel.md`
   - `espn_click_clack/news/te-intel.md`
   - `espn_click_clack/news/qb-intel.md`
   - `espn_click_clack/news/dst-intel.md`

## Decision workflow

1. Get the free-agent list or the exact player(s) Kelly wants evaluated.
2. Identify the roster issue: starter injury, bench depth, bye-week hole, or weak handcuff depth.
3. Read the relevant position intel file and compare the candidate to the player they would displace.
4. Check whether the move is:
   - a one-week streaming play,
   - a depth upgrade,
   - a breakout/role-change add,
   - or a true rest-of-season roster upgrade.
5. Recommend an add + drop pairing with a clear rationale.
6. Suggest a waiver bid based on the remaining budget and how much flexibility is left after the move.
7. If the recommendation is acted on, update `state/roster-notes.md` so the working roster and waiver notes stay current.

## Recommendation format

Use this structure when answering Kelly:

- Candidate to add
- Why this player fits the roster
- What roster spot or role it would replace
- Whether this is a streaming play or a long-term upgrade
- Suggested drop
- Suggested waiver bid / priority guidance
- Short caveat on risk or upside

## Position-specific notes

- RB: prioritize volume, touches, and committee/handcuff role changes; use `state/news/rb-intel.md`
- WR: prioritize target share, route volume, and weekly floor; use `state/news/wr-intel.md`
- TE: balance target volume vs. matchup leverage and usage spike; use `state/news/te-intel.md`
- QB: only use a streaming add if the starter profile is truly weak or injured; use `state/news/qb-intel.md`
- D/ST: prefer streamers by matchup and matchup-specific upside; use `state/news/dst-intel.md`

## Guardrails

- Do not recommend a player without checking the cached intel in the relevant file first.
- Do not ignore the roster pressure behind the add — a weak bench slot is not enough to justify a bad bid.
- Explicitly say whether the decision is a short-term streaming move or a real long-term upgrade, because that changes both the waiver bid and the drop decision.
- Keep the answer tailored to this Yahoo league and not to the ESPN scoring model unless the same logic clearly applies.
