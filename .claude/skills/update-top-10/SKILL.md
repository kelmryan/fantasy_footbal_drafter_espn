---
name: update-top-10
description: Refresh state/top-10.md against the live draft-board.md during a "click clack" draft session — drop drafted targets, backfill replacements via position experts, retarget to Kelly's next pick pair, and roll in the QB/D/ST/handcuff timing rules. Use whenever Kelly says "update the top 10" (or similar) during an active draft.
---

# Update Top 10

This skill runs the repeated "check the board, refresh the target list" loop used throughout a "click clack" draft session. It replaces the manual multi-step process of: reading `draft-board.md`, diffing it against `state/top-10.md`, dispatching position experts for replacement names, and rewriting the file.

## When to run this

Kelly says "update the top 10," "process top 10," "check the top 10," or asks a variant of "what's my top 10/5 right now" during an active offline draft (state/draft-board.md exists and is being appended to live).

## Steps

1. **Read the live board.** `grep -n "^| [0-9]" state/draft-board.md | tail -N` to see the most recent picks since the file was last updated (use the pick count noted in `top-10.md`'s header as the starting point).

2. **Diff against the current list.** For every player currently ranked in `state/top-10.md` (main ranked list, QB watch, any contingency notes), grep the board to see if they've been drafted. Use a loop like:
   ```bash
   for p in "Player One" "Player Two"; do
     result=$(grep -i "$p" state/draft-board.md)
     [ -z "$result" ] && echo "$p => still available" || echo "$p => DRAFTED: $result"
   done
   ```
   Don't trust a single "not found" as proof of availability if it matters for an imminent pick — rows can be backfilled out of chronological order (this has happened before in this league's log). Flag genuinely surprising fallers for live verification rather than asserting them as fact.

3. **Check if Kelly made his own pick(s).** If `draft-board.md` shows a new "SlickDaddy Club (Kelly)" row since the last update, the target window has closed — recompute his next pick pair using the snake formula (14 teams, Kelly is slot 1):
   - Round `r` odd: pick = `(r-1)*14 + 1`
   - Round `r` even: pick = `r*14`
   - This produces the pairs: 1, then (28,29), (56,57), (84,85), (112,113), (140,141), (168,169), (196,197), and a final single pick at 224.
   - Update the roster snapshot line with whatever Kelly just drafted, and re-derive "remaining needs" from the updated roster (starters: 1 QB, 2 RB, 2 WR, 1 TE, 1 FLEX, 1 D/ST, 1 K; 7 bench).

4. **Backfill dropped targets — prefer dispatching `overall-expert` over hand-orchestrating position experts yourself.** `overall-expert` handles the cross-positional synthesis (dispatching whichever of `rb-expert`/`wr-expert`/`te-expert`/`qb-expert`/`dst-expert` are relevant, then weighing prior-season floor against 2026-potential ceiling per its own protocol) and returns a ready-to-paste ranked table. Give it: Kelly's roster, his next pick number(s), remaining needs, and the already-drafted list (or point it at `state/draft-board.md`). Only fall back to dispatching a single position expert directly when the need is narrow and single-position (e.g., "just need one more RB name" after `overall-expert` already ran this cycle) — don't duplicate its cross-positional work. Do NOT guess a replacement name from memory either way.

5. **Apply standing rules when reordering:**
   - **PPR reweighting**: once Kelly's starting RB1/RB2 are locked, don't rank committee/early-down RBs above real target-earning WRs. Exception: a true workhorse RB with a real receiving role stays elite regardless of position. See `[[feedback_ppr_deprioritize_rb_depth]]` reasoning if present in memory.
   - **QB timing**: don't move a QB up in the ranked list unless (a) it's genuinely the target round agreed with Kelly, or (b) Kelly is down to the last team(s) needing one and a real value name is sitting there. Otherwise keep QB in a separate "watch" section, not the main ranked list.
   - **Handcuff/no-IR-slot logic**: a direct handcuff to one of Kelly's own starters (e.g., Bijan Robinson's backup) is a defensible late-round or even earlier dart specifically because this league has no IR slot — note this explicitly when it applies, and don't let it get crowded out by unrelated depth names.
   - **D/ST timing**: standard guidance is to wait until ~Round 13 (picks 168-169) and stream by matchup, per this league's points-allowed + yards-allowed scoring. If other teams start drafting D/ST unusually early (a real run, not just one or two teams), dispatch `dst-expert` to confirm whether the streaming logic still holds or whether a specific defense is worth securing early — don't assume the standard guidance still applies without checking.
   - **Don't research already-drafted, irrelevant players.** Per standing feedback, skip caching/web-searching any player who's off the board and isn't one of Kelly's own picks — this applies even during a "check the backlog" or "check for unresearched picks" ask.

6. **Rewrite `state/top-10.md` in full** (don't leave stale numbering from a partial edit — renumber the whole ranked table). Structure to preserve:
   - Title: `# Top 10 Overall — Picks X-Y` (Kelly's next pick pair)
   - Last-updated line with the current pick count
   - Roster snapshot + remaining needs
   - Any standing reweighting notes relevant to this update
   - A ranked list table (aim for ~10 rows; hold at fewer rather than force an unresearched name)
   - A "dropped since last check" / "just missed" line for anything removed
   - A QB watch / D/ST watch section when applicable, kept separate from the main ranked list per the timing rules above
   - Recommendation section (plain-language "take X at pick N, Y at pick N+1")
   - Flags section (unverified names, missing bye-week/injury data, standing rules that applied)

7. **Report back concisely**: what got dropped, what replaced it (if anything), and the current top few names — not the entire file contents restated in chat.

## Also handle "process research queue" when asked in the same breath

If Kelly also asks to process the research queue, check `/tmp/ff-research-queue.txt`. If non-empty, research each queued player (web search as needed) and append an entry to the matching `state/news/[position]-intel.md`, then clear the queue file (`> /tmp/ff-research-queue.txt`). If empty, just say so — don't proactively backfill research on names that aren't live targets (see the "don't research drafted players" rule above).
