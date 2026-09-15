# Death to Nottighams

This folder is a Yahoo fantasy-football league workspace for the league at:
https://football.fantasysports.yahoo.com/f1/924854/matchup?week=1&mid1=3&mid2=10

## League notes

- League name: Death to Nottighams
- Platform: Yahoo Fantasy Football
- Link: https://football.fantasysports.yahoo.com/f1/924854/matchup?week=1&mid1=3&mid2=10
- This folder mirrors the project structure used in the ESPN league, but it is intentionally separate and should not share state with the other league folders.
- The cached news files in this folder are the working source of truth for immediate waiver and lineup decisions.
- The historical intel in the ESPN project at `espn_click_clack/news/*.md` is a reference model for formatting and content style, not a live data source for this league.

## State files

- `state/roster-notes.md` — current roster, FAAB/waiver posture, and injury notes
- `state/player-intel.md` — broad summary for the current week and league context
- `state/news/*.md` — detailed player intel by position

## Waiver workflow

Use the free-agent skill in `.claude/skills/free-agent-check/SKILL.md` whenever Kelly asks about adds, drops, streaming plays, or waiver bids.

The skill should:
1. Read `state/roster-notes.md` and the relevant `state/news/*.md` file first.
2. Compare the waiver candidate against his current roster hole or bench player.
3. Distinguish one-week streaming plays from rest-of-season upgrades.
4. Recommend a add/drop decision clearly and give a bid range in line with his remaining waiver budget.
5. Reference the cached intel in this folder, and use the ESPN reference files as the formatting template for position-by-position analysis.
