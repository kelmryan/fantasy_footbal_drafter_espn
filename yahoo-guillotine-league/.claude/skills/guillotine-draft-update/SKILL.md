---
name: guillotine-draft-update
description: Use whenever Kelly pastes new draft-pick data for "darrell n's Superb League" (the Yahoo guillotine snake draft), or asks to "update top 5", "process research queue", or give a status update during that draft. Parses the pasted table (either a round-by-round pick log or a ranked available-players/queue sheet), updates state/draft-board.md and state/top-5.md, checks the research queue, and reports what changed. Also covers building/maintaining this skill itself if asked to extend it.
version: 0.1.0
---

# Guillotine Draft Update

Keeps `state/draft-board.md` and `state/top-5.md` in this league folder current as Kelly reports live draft picks, and gives a fast recommendation when he's on the clock. This league (`darrell n's Superb League`) is **separate** from the root "click clack" ESPN league — never mix scoring rules or state between them. Read `yahoo-guillotine-league/CLAUDE.md` for league facts if this is a fresh session.

## Inputs you'll see pasted

Kelly pastes raw copy from the Yahoo draft UI in one of two shapes — detect which one you got:

1. **Round-by-round pick log** ("Teams / Round by Round / Positions Drafted Grid") — a list of `Pick / Player / Pos / Team / Bye / Drafted-By` rows, usually the most recent N rounds, often overlapping picks you've already logged. Treat every row as an **actual completed pick** — merge new ones into `draft-board.md`, skip ones you already have.
2. **Queue / available-players sheet** (`Queue Player XRank ADP Bye Proj Pts GP Pass Yds ...`) — this is the **full remaining player pool**, ranked best-to-worst, NOT a pick-by-pick log. A `Your Turn - Nth Pick` marker is inserted at the rank position roughly matching Kelly's Nth pick — everything **above** a marker is what's realistically gone by the time that pick arrives, everything **at/below** it down to the next marker is what's more likely to actually be on the board then. Use this to build/refresh the top-5 forecast, not to log picks (nothing in this view has actually been drafted yet unless Kelly separately confirms a pick).

Kelly may also just say a player's name ("I took X" / "took Brian Robinson Jr") — that's a confirmed pick for whatever his next open pick number was.

## Every time you get an update, do this in order

1. **Check the research queue first**: `cat /tmp/ff-research-queue.txt`. If non-empty, follow the root CLAUDE.md's "Research queue processing" workflow (look up each player, add to `state/news/[position]-intel.md`, clear the queue, report counts). It's usually empty in this league since intel is pulled live — say so briefly rather than skipping silently.
2. **Read `state/draft-board.md` fresh** (it gets edited concurrently — re-read every time before writing, don't assume your last-seen copy is current; if a diff shows up that you didn't make, trust it as current state per the harness's modified-file note, don't fight it).
3. **Merge new picks** into the pick log table (`Round | Overall Pick | Player | Pos | NFL Team | Bye | Drafted By`). If a gap exists (picks not yet reported), add a `_(not reported)_` placeholder row rather than guessing.
4. **Update Kelly's roster table** in the same file whenever one of his picks lands. Recommend FLEX/bench slotting when it's a close call (e.g. a safer floor play over an existing committee-back FLEX starter) but let Kelly confirm the swap.
5. **Update the standing bye-week flag** — this roster already runs a 3-player Bye 9 cluster (Warren, Pollard, Wan'Dale Robinson). Flag any new bye collision explicitly; recommend against adding a 4th to any cluster already at 2+.
6. **Rebuild `state/top-5.md` completely** (overwrite, don't append — it's a snapshot) using whichever shortlist names are still confirmed-undrafted. Do this **every time**, even if Kelly didn't explicitly ask — that's a standing instruction, not a one-off. Structure:
   - Header: last-updated pick number, Kelly's next pick number, how many picks away.
   - Roster status: starters/FLEX/bench fill state, bench spots remaining.
   - Bye-week watch line.
   - Top 5 ranked list, each with a one-line reason + bye week + why it fits (or doesn't) roster needs.
   - A caveat line when picks in between are unconfirmed — don't imply certainty you don't have.
7. **If Kelly is live on the clock** (a `Your Turn - Nth Pick` marker matches his actual next pick, or he says "I'm up"), give a direct top-5 + one bolded recommendation fast — he's often on a 1-minute clock. Don't over-hedge; pick one and say why.

## Draft-value principles specific to this league

- **Floor over ceiling.** Guillotine format eliminates low scorers — weekly consistency beats boom/bust upside once starters are set. Reference `state/research/guillotine-strategy.md`.
- **Full PPR at TE only** (0.5 PPR everywhere else). A real target-earning TE's *effective* value is higher than a generic 0.5-PPR projection sheet shows — call this out explicitly when a decent TE is available, even if Kelly already has 2 TEs rostered (value vs. need are different questions, say both).
- **RB scarcity compounds fast.** Once starters + FLEX are set, RB depth tends to dry up well before WR — when RB options thin out, say so and weight RB depth higher than the raw projection alone would suggest.
- **IR slot is real and currently open.** A PUP/IR-tagged player with real talent is a fine target for that slot specifically — it doesn't cost a normal bench spot. Don't recommend spending it on a low-ceiling name just to fill it.
- **No trades, all season** — waivers/FAAB are the only in-season lever, so don't suggest trade-based fixes for a bad pick.

## Common failure modes to avoid (learned this draft)

- Don't assume a name from an early shortlist is still available — re-verify against the latest pasted data every single time; this room has repeatedly sniped players well ahead of their ADP.
- Don't let `draft-board.md` and `top-5.md` diverge or duplicate (a stray `top5-current.md` appeared once from a parallel process — if you ever see a second tracker file, consolidate into `top-5.md` and delete the duplicate, noting it to Kelly).
- Pick math isn't always simple snake alternation once round counts are odd/team counts create irregular reversals — trust Yahoo's own `Your Turn - Nth Pick` markers over a manually recomputed formula when they disagree.
