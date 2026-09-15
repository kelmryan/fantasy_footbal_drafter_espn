---
name: yahoo-waiver-advisor
description: Looks up the live Yahoo waiver pool for Death to Nottighams and advises exactly who to add, who to drop, and what budget to use for the waiver claim.
---

# Yahoo Waiver Advisor — Death to Nottighams

Produces a concrete add / drop / bid recommendation for this Yahoo league, using the live waiver pool, roster needs, and a short-term vs. long-term performance model.

## 0. Load context first

Read, in this order:
- `CLAUDE.md` in this folder
- `state/roster-notes.md`
- `state/player-intel.md`
- the relevant `state/news/*.md` file for the position under review

## 1. Pull the live Yahoo wire

Run:

```bash
python3 scripts/yahoo-free-agents.py --next --limit 25
```

This is the Yahoo equivalent of the ESPN free-agent flow, but the output is now scored for two different questions:
- Short-term: is the player likely to help this week or in the next 1–2 weeks?
- Long-term: is the player a good roster fix for the next 6–8 weeks based on role stability, usage trend, and recent production?

## 2. Evaluate the player on two axes

For each candidate, decide separately:

### Short-term signal
Look for:
- matchup quality this week
- recent output in the last 2–4 games
- target share or snap count trend if available
- injury-driven opportunity or a favorable schedule

### Long-term signal
Look for:
- stable role in the offense
- 4–8 week trend of usage or production
- workload security (starter / feature back / WR1 share)
- matchups and a clearly defined opportunity window over the next 6–8 weeks
- injury risk and whether the player is a real roster solution or just a one-week flash

Score each candidate on a simple 0–100 scale in both categories, then label it as:
- Short-term streamer
- Long-term roster fix
- Short-term only / no long-term value
- Hold

## 3. Diagnose the roster issue

Using the live roster and the notes file:
- Check starter injuries, bye-week holes, burned bench spots, and weak handcuff depth
- Compare the candidate to the player he would replace
- Separate one-week injury/streaming need from a true rest-of-season roster upgrade
- If the player is a handcuff, note the exact starter they would back up

## 4. Build a short candidate list

From the live free-agent result, pick 2–4 players at the position of need, ideally 5–8 total across the whole roster. Prefer players with:
- obvious usage trend or role change
- strong recent production in the last 2–4 games
- stable underlying role for the next 6–8 weeks
- matchup and schedule fit

Skip a player if it does not clearly beat the roster spot it would replace in at least one of the following:
- this week’s projection
- recent trend / usage
- long-term role stability over the next 6–8 weeks

## 5. Recommend the add / drop / bid

Use this pattern:

```
#1 ADD <player> (POS, TEAM) — DROP <player> — BID $N (leaves $M remaining)
Why: <2-line role/usage + roster-fit explanation>
Short-term signal: <score / read>
Long-term signal: <score / read>
Type: streamer | stable 6-8 week add | handcuff/stash | hold
```

Bid guidance for this Yahoo league:
- Streaming play: $1–5
- Depth / handcuff / useful bench stash: $5–15
- Real role change or true 6–8 week fix: $20+
- Always state how much budget remains after the bid

If nothing available is worth the move, say HOLD plainly rather than forcing a claim.

## 6. Update state after Kelly acts

If Kelly makes the claim or says which player he dropped:
- Update `state/roster-notes.md` with the new roster status and remaining budget
- Add any newly verified role/injury notes to the relevant `state/news/*.md` file so the next run doesn't waste time re-researching the same player

## 7. Unattended mode

When nobody is available to paste the wire or answer questions:
- Use the script output plus cached intel and roster notes only
- Label each call as unverified if it was not confirmed live
- Present the output as a shortlist for Kelly to confirm, not as an automatic waiver claim
