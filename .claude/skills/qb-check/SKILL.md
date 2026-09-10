---
name: qb-check
description: Get a verified, round-weighted QB recommendation for the "click clack" league — dispatches qb-expert with a mandatory fresh starter-status check and the qb-value-tiers.md weighting scale, so a stale cache can never produce an unverified "he's the starter" claim again. Use whenever Kelly is deciding on a QB pick, a QB streaming option, or wants to sanity-check a QB he already has.
---

# QB Check

This skill exists because of a real miss: Anthony Richardson was recommended as a rushing-QB1 off a stale cache entry, when he'd actually been passed on the depth chart by a newly-signed starter and was fighting for his own backup job. This skill makes that specific failure structurally harder to repeat.

## When to run this

- Kelly is choosing between QB options for an upcoming pick.
- Kelly asks whether a QB streaming option is worth it.
- Kelly wants a sanity-check on a QB already on his roster (e.g., "is X actually going to play").
- Any point where a QB recommendation is about to be made and the last verification is unclear.

## Steps

1. **Identify the pick/round context.** If this is a draft decision, get Kelly's current pick number. The round window is load-bearing for `qb-value-tiers.md` — don't skip this.

2. **Dispatch `qb-expert`** (not a generic web search done inline) with:
   - The candidate name(s).
   - The current pick/round number.
   - An explicit instruction to run a fresh "who is starting" search per its research protocol — do not let it answer from cache alone.

3. **Do not accept a tier assignment (Tier A or S from `state/research/qb-value-tiers.md`) without a stated verification source and date.** If the expert's answer doesn't include one, send it back for the fresh check before using the recommendation.

4. **Cross-check the round window.** A Tier-C name should not be recommended in a Round 6-9 decision, and a Tier-S name shouldn't be reached for outside Rounds 2-4. If the expert's tier and the current round don't line up, flag that explicitly to Kelly rather than silently picking one.

5. **If this is a sanity-check on a rostered QB** (not a new pick), report the verified status plainly and, if the news is bad (buried on depth chart, traded, injured with no timeline), say so directly and recommend the practical next step — usually: treat the roster spot as needing a replacement at the next real opportunity, and note it in `state/top-10.md` if a draft is still in progress.

6. **Update `state/news/qb-intel.md`** with the freshly verified status so the next check isn't working from the same stale entry — include the verification date in the entry itself.

## Output

Report back: the tier, the round-window fit, the verification source/date, and a direct recommendation. Keep it short — this is a decision-support check, not a full report.
