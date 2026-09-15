# QB Value-by-Round Weighting Scale

_How to weigh QB draft value against pick number in the "click clack" league (4-pt passing TD, standard rushing scoring)._

## Why this exists

This league's 4-pt passing TD rule (not 6) compresses the gap between an elite passer and an average one by roughly a third compared to standard leagues — see `ppr-scoring-advantage.md`. Rushing production is scored the same as any position (0.1/yd, 6/TD rush), so a QB's rushing floor is the biggest differentiator this format actually rewards. This file translates that into a concrete round-by-round weighting so a recommendation doesn't drift into "just take the best name" — the round matters as much as the player.

## Kelly's directive (Sep 14, 2026): weigh QB near-even with RB/WR

Kelly overrode the "QB is discounted" framing after Daniel Jones scored 9.0 in Week 1. **In-season, a QB's weekly output gap counts almost as much as an RB/WR gap** — a 9-point QB week is a real lineup hole, not a tolerable cost of waiting on the position. Concretely:

- **Add/drop:** compare a wire QB to Kelly's starter on projected weekly points the same way you'd compare two RBs. If the wire QB projects 4+ PPG better ROS, that's a roster upgrade worth FAAB, not a "streamer."
- **Drop confidence:** treat "one of two rostered QBs" as the drop unit — the 89% bar applies to *which* QB to cut only if the ROS gap between them is small. If one is clearly worse ROS, cut him.
- **Draft:** the round-window table below still applies, but shift each tier's window ~1 round earlier — a Tier-A QB is fine in Rounds 5-8, a Tier-B in Rounds 7-10. Don't let a 4-pt-passing-TD note talk Kelly out of a solid QB while a replacement-level RB/WR gets taken instead.
- **Rushing floor is still the top differentiator** in this scoring — that part hasn't changed.

## The weighting scale

| Tier | Round window (14-team) | What qualifies | Reach tolerance |
|---|---|---|---|
| **S — Elite rushing floor + passing volume** | Rounds 2-4 only if falling | A QB with BOTH a real weekly rushing floor (30+ rush yds/game pace) AND top-8 passing volume. Very few players qualify most seasons. | Worth reaching one round early. Otherwise let it fall. |
| **A — Rushing-driven QB1** | Rounds 5-8 (per Kelly's directive above) | Real dual-threat role, CONFIRMED as the Week 1 starter on his own team, no unresolved camp competition. | Take at value, don't reach. |
| **B — Pocket-passer QB1 / high-floor game-manager** | Rounds 7-10 (per Kelly's directive above) | Locked-in starter, high volume, but rushing floor near zero (this format's discount hits these hardest — value them a full tier below where a standard league would). | Only if the QB slot is otherwise unfilled and no Tier A option remains. |
| **C — Streamer / QB2 with a path to value** | Rounds 12+ or waivers | Backup competing for a job, a starter on a bad offense, or a QB2 with real injury-driven upside. | Never worth a proactive early pick — this tier exists for late-round flexibility or in-season streaming. |
| **Do not draft** | N/A | Confirmed backup with no starting path, active trade-block/roster-bubble situation, or a rushing-QB profile that's actually buried on a depth chart. | Zero value regardless of name recognition or draft-slot ADP hype. |

## Mandatory verification rule before assigning a tier

**A player's tier is only as good as the last time their starting/depth-chart status was actually checked.** Do not assign Tier A/B/S off a cached `state/news/qb-intel.md` entry that is more than ~2 days old, or off any entry that predates a known camp battle, trade request, or coaching change. Run a fresh, targeted web search on **current starter status** specifically (not just general player news) before naming anyone in Tier A or S — a general "he's a good player" search will miss a depth-chart demotion that a "who is starting" search will not.

This rule exists because Anthony Richardson was recommended and drafted as a Tier-A rushing QB1 based on a stale cache entry, when he was actually buried behind a newly-signed starter and fighting for his own backup job. See `[[feedback_verify_starter_status_before_recommending]]`.

## How to apply this scale

1. Determine what pick/round Kelly is actually drafting at.
2. Find the tier(s) whose round window includes that pick.
3. Only recommend a name in that tier (or better, if a higher tier has genuinely fallen) — don't recommend a Tier-C name in a Tier-A round window, and don't reach into Tier-S outside its round window even for a name-brand player.
4. Before finalizing, run the mandatory verification check above on the specific name being recommended.
5. State the tier and the verification date/source in the recommendation, e.g.: "Tier A — confirmed Week 1 starter as of [date], per [source]."
