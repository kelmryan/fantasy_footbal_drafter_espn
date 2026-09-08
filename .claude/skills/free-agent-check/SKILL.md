---
name: free-agent-check
description: Runs the "click clack" Free Agent Manager workflow — scans the waiver wire against Kelly's roster needs and recommends adds/drops/FAAB bids. Use when Kelly asks to check free agents/waivers, or on the scheduled Monday-night cloud routine.
---

# Free Agent Check

This formalizes the **Free Agent Manager** role defined in the project's `CLAUDE.md` so it
can be run either interactively with Kelly, or unattended on a schedule.

Read `CLAUDE.md` (league facts, bid-sizing table) and `state/roster-notes.md` (current
roster + FAAB balance) before doing anything else.

## Interactive mode (Kelly is present in the session)

1. Get the wire: ask Kelly to paste from
   `https://fantasy.espn.com/football/players/add?leagueId=453244&seasonId=2026`
   (or read it via browser MCP if one is configured), or ask which specific free agent
   he wants evaluated.
2. Identify roster weak spots from `state/roster-notes.md`: thin depth, bye-week
   clusters, injured/underperforming starters, bench spots tied up long-term with no
   IR slot to offload to.
3. Dispatch `schedule-manager` for both the free-agent candidate(s) and the roster
   player(s) they'd compete with, for matchup/injury/bye context.
4. Dispatch the relevant position expert(s) with that context included
   (`rb-expert`, `wr-expert`, `te-expert`, `dst-expert`). **There is no `qb-expert`
   agent file in `.claude/agents/` yet**, despite `CLAUDE.md` referencing one — if the
   free agent in question is a QB, say so explicitly and fall back to the `qb-check`
   skill or manual research rather than guessing.
5. Distinguish explicitly between a one-week streaming play and a rest-of-season
   roster upgrade — call out which one this is, since it changes the bid and the drop.
6. Recommend a FAAB bid against the $100 season pool per `CLAUDE.md`'s table:
   streamer (DST/TE/matchup play) $1-5, solid depth/handcuff $5-15, league-winning/
   injury-driven role change $20+ — say how much that leaves of the remaining budget.
7. If Kelly acts on the recommendation, update `state/roster-notes.md` (FAAB balance,
   any new stash/handcuff note) so it stays the source of truth across sessions.

## Unattended mode (scheduled cloud routine, no Kelly present)

There's no browser MCP and no one to paste the wire or answer questions here, so the
scan is web-research-driven rather than a live ESPN read:

1. Read `state/roster-notes.md`. If it looks stale (its own notes suggest no update
   in the last couple of weeks), say so up front in the report rather than treating
   it as current.
2. Web-search for this week's trending NFL waiver-wire adds, snap-count risers, and
   injury-driven opportunity changes, for the week implied by today's date.
3. Filter to players plausibly available in a 14-team full-PPR league, and match
   against the roster weak spots found in step 1 (thin bench, bye-week collisions,
   injured/uncertain starters, D/ST and K streaming per `CLAUDE.md`'s non-standard
   D/ST scoring).
4. Dispatch the relevant position expert(s) for the top 3-5 candidates, and
   `schedule-manager` for each candidate's upcoming matchup. Skip QB analysis (or
   flag it as unverified) since no `qb-expert` agent exists yet.
5. Write a short report: for each candidate, one line on why, a suggested FAAB bid
   range, and what roster spot it fills. Frame it as a scan for Kelly's own
   judgment call, not an automatic lineup change.
6. Email the report to kellymryan79@gmail.com via Gmail (subject line:
   `click clack — free agent scan, week of <date>`). This mode is **read-only**:
   do not edit `state/roster-notes.md` or push any commits — Kelly reconciles the
   roster himself when he reads the email.
