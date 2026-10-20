#!/usr/bin/env python3
"""
Pull the live free-agent pool and Kelly's roster for the "click clack" ESPN league.

The league is private, so ESPN's fantasy API needs two cookies from a logged-in
browser session: `espn_s2` and `SWID`. Put them in a `.env` file at the repo root
(see `.env.example`) or export them as environment variables.

Usage:
  scripts/espn-free-agents.py                  # roster + top free agents at every position
  scripts/espn-free-agents.py --pos RB WR      # only these positions
  scripts/espn-free-agents.py --limit 20       # more names per position
  scripts/espn-free-agents.py --sort proj      # sort by this-week projection (default: %owned)
  scripts/espn-free-agents.py --next           # upcoming week (waivers run before ESPN rolls over on Tue)
  scripts/espn-free-agents.py --week 4         # override the scoring week ESPN reports
  scripts/espn-free-agents.py --no-roster      # skip the roster section
  scripts/espn-free-agents.py --json           # raw JSON instead of markdown (for piping)

Output is markdown so it can be pasted straight into a Claude Code session.
"""

import argparse
import json
import os
import sys
from pathlib import Path

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("python3 -m pip install requests")

LEAGUE_ID = 453244
TEAM_ID = 10          # SlickDaddy Club
SEASON = 2026
BASE = f"https://lm-api-reads.fantasy.espn.com/apis/v3/games/ffl/seasons/{SEASON}"
LEAGUE_URL = f"{BASE}/segments/0/leagues/{LEAGUE_ID}"

POSITIONS = {1: "QB", 2: "RB", 3: "WR", 4: "TE", 5: "K", 16: "D/ST"}
POS_SLOT = {"QB": 0, "RB": 2, "WR": 4, "TE": 6, "K": 17, "DST": 16}
LINEUP_SLOTS = {0: "QB", 2: "RB", 4: "WR", 6: "TE", 23: "FLEX", 16: "D/ST", 17: "K", 20: "BE", 21: "IR"}
PRO_TEAMS = {
    0: "FA", 1: "ATL", 2: "BUF", 3: "CHI", 4: "CIN", 5: "CLE", 6: "DAL", 7: "DEN", 8: "DET",
    9: "GB", 10: "TEN", 11: "IND", 12: "KC", 13: "LV", 14: "LAR", 15: "MIA", 16: "MIN",
    17: "NE", 18: "NO", 19: "NYG", 20: "NYJ", 21: "PHI", 22: "ARI", 23: "PIT", 24: "LAC",
    25: "SF", 26: "SEA", 27: "TB", 28: "WSH", 29: "CAR", 30: "JAX", 33: "BAL", 34: "HOU",
}
INJURY_SHORT = {
    "ACTIVE": "", "QUESTIONABLE": "Q", "DOUBTFUL": "D", "OUT": "OUT",
    "INJURY_RESERVE": "IR", "SUSPENSION": "SUSP", "PROBABLE": "P",
}
DEFAULT_LIMIT = {"QB": 8, "RB": 15, "WR": 15, "TE": 10, "DST": 8, "K": 6}


# ---------------------------------------------------------------- auth / http

def load_cookies():
    """espn_s2 + SWID from the environment, falling back to a repo-root .env file."""
    s2, swid = os.environ.get("ESPN_S2"), os.environ.get("SWID")
    if not (s2 and swid):
        env_path = Path(__file__).resolve().parent.parent / ".env"
        if env_path.exists():
            for line in env_path.read_text().splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                k, v = line.split("=", 1)
                k, v = k.strip(), v.strip().strip('"').strip("'")
                if k == "ESPN_S2" and not s2:
                    s2 = v
                elif k == "SWID" and not swid:
                    swid = v
    if not (s2 and swid):
        sys.exit(
            "Missing ESPN cookies. The click clack league is private, so this needs\n"
            "ESPN_S2 and SWID in the repo-root .env (copy .env.example) or the environment.\n"
            "Get them: log into fantasy.espn.com -> DevTools -> Application -> Cookies ->\n"
            "copy the values of `espn_s2` and `SWID` (SWID keeps its curly braces)."
        )
    if not swid.startswith("{"):
        swid = "{" + swid.strip("{}") + "}"
    return {"espn_s2": s2, "SWID": swid}


def get(session, url, params=None, headers=None):
    r = session.get(url, params=params, headers=headers, timeout=30)
    if r.status_code == 401:
        sys.exit("ESPN returned 401 — cookies are missing/expired. Re-copy espn_s2 and SWID into .env.")
    r.raise_for_status()
    return r.json()


# ---------------------------------------------------------------- data pulls

def league_status(session):
    data = get(session, LEAGUE_URL, params={"view": "mSettings"})
    status = data.get("status", {})
    return {
        "week": data.get("scoringPeriodId") or status.get("latestScoringPeriod") or 1,
        "faab_budget": data.get("settings", {}).get("acquisitionSettings", {}).get("acquisitionBudget", 100),
    }


def bye_weeks(session):
    """proTeamId -> bye week. Best-effort; returns {} if the endpoint changes shape."""
    try:
        data = get(session, BASE, params={"view": "proTeamSchedules_wl"})
        return {t["id"]: t.get("byeWeek") for t in data["settings"]["proTeams"]}
    except Exception:
        return {}


def my_roster(session, week):
    data = get(session, LEAGUE_URL, params={"view": ["mRoster", "mTeam"], "scoringPeriodId": week})
    team = next(t for t in data["teams"] if t["id"] == TEAM_ID)
    spent = team.get("transactionCounter", {}).get("acquisitionBudgetSpent", 0)
    entries = []
    for e in team.get("roster", {}).get("entries", []):
        p = e["playerPoolEntry"]["player"]
        entries.append((e.get("lineupSlotId", 20), p))
    slot_order = [0, 2, 4, 6, 23, 16, 17, 20, 21]
    entries.sort(key=lambda x: (slot_order.index(x[0]) if x[0] in slot_order else 99))
    return {
        "name": team.get("name") or f"{team.get('location','')} {team.get('nickname','')}".strip(),
        "faab_spent": spent,
        "entries": entries,
    }


def free_agents(session, pos, week, limit):
    flt = {
        "players": {
            "filterStatus": {"value": ["FREEAGENT", "WAIVERS"]},
            "filterSlotIds": {"value": [POS_SLOT[pos]]},
            "limit": limit,
            "offset": 0,
            "sortPercOwned": {"sortPriority": 1, "sortAsc": False},
            "sortDraftRanks": {"sortPriority": 100, "sortAsc": True, "value": "PPR"},
            # stat rows to include: season actual, season projected, this-week projected, last-week actual
            "filterStatsForTopScoringPeriodIds": {
                "value": 2,
                "additionalValue": [f"00{SEASON}", f"10{SEASON}", f"11{SEASON}{week}", f"01{SEASON}{week - 1}"],
            },
        }
    }
    data = get(
        session, LEAGUE_URL,
        params={"view": "kona_player_info", "scoringPeriodId": week},
        headers={"X-Fantasy-Filter": json.dumps(flt)},
    )
    return [(pe.get("status", ""), pe["player"]) for pe in data.get("players", [])]


# ---------------------------------------------------------------- shaping

def stat(player, source, split, season=SEASON, period=None):
    """appliedTotal for a stats row. source 0=actual 1=projected; split 0=season 1=single week."""
    for s in player.get("stats", []):
        if s.get("statSourceId") == source and s.get("statSplitTypeId") == split and s.get("seasonId") == season:
            if period is None or s.get("scoringPeriodId") == period:
                return s.get("appliedTotal"), s.get("appliedAverage")
    return None, None


def shape(player, week, byes):
    own = player.get("ownership", {}) or {}
    season_total, season_avg = stat(player, 0, 0)
    week_proj, _ = stat(player, 1, 1, period=week)
    last_actual, _ = stat(player, 0, 1, period=week - 1) if week > 1 else (None, None)
    return {
        "name": player.get("fullName"),
        "pos": POSITIONS.get(player.get("defaultPositionId"), "?"),
        "team": PRO_TEAMS.get(player.get("proTeamId"), "?"),
        "bye": byes.get(player.get("proTeamId")),
        "injury": INJURY_SHORT.get(player.get("injuryStatus", "ACTIVE"), player.get("injuryStatus", "")),
        "pct_owned": own.get("percentOwned"),
        "pct_change": own.get("percentChange"),
        "pct_started": own.get("percentStarted"),
        "week_proj": week_proj,
        "last_week": last_actual,
        "season_pts": season_total,
        "season_avg": season_avg,
        "ppr_rank": (player.get("draftRanksByRankType", {}).get("PPR") or {}).get("rank"),
    }


def fmt(v, nd=1):
    if v is None:
        return "-"
    return f"{v:.{nd}f}" if isinstance(v, float) else str(v)


def md_table(rows, week, slot_col=False):
    head = (["Slot"] if slot_col else []) + [
        "Player", "Pos", "Tm", "Bye", "Inj", "%Own", "Δ%", f"Wk{week} proj",
        f"Wk{week-1} act" if week > 1 else "Last", "Season", "Avg",
    ]
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    for r in rows:
        cells = ([r.get("slot", "")] if slot_col else []) + [
            r["name"], r["pos"], r["team"], fmt(r["bye"], 0), r["injury"] or "",
            fmt(r["pct_owned"]), fmt(r["pct_change"]), fmt(r["week_proj"]),
            fmt(r["last_week"]), fmt(r["season_pts"]), fmt(r["season_avg"]),
        ]
        lines.append("| " + " | ".join(cells) + " |")
    return "\n".join(lines)


SORT_KEYS = {
    "own": lambda r: r["pct_owned"] or 0,
    "trend": lambda r: r["pct_change"] or 0,
    "proj": lambda r: r["week_proj"] or 0,
    "avg": lambda r: r["season_avg"] or 0,
    "season": lambda r: r["season_pts"] or 0,
}


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--pos", nargs="+", choices=list(POS_SLOT), default=list(POS_SLOT),
                    help="positions to list (default: all)")
    ap.add_argument("--limit", type=int, help="names per position (default varies by position)")
    ap.add_argument("--sort", choices=list(SORT_KEYS), default="own")
    ap.add_argument("--week", type=int, help="scoring week (default: ESPN's current)")
    ap.add_argument("--next", action="store_true",
                    help="use ESPN's current week + 1 — what waiver claims are actually for on Sun night/Mon")
    ap.add_argument("--no-roster", action="store_true")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    args = ap.parse_args()

    session = requests.Session()
    session.cookies.update(load_cookies())
    session.headers.update({"User-Agent": "Mozilla/5.0 (click-clack-waiver-advisor)"})

    status = league_status(session)
    week = args.week or (status["week"] + 1 if args.next else status["week"])
    byes = bye_weeks(session)

    out = {"league_id": LEAGUE_ID, "season": SEASON, "week": week, "free_agents": {}}

    if not args.no_roster:
        roster = my_roster(session, week)
        out["roster"] = {
            "team": roster["name"],
            "faab_remaining": status["faab_budget"] - roster["faab_spent"],
            "faab_budget": status["faab_budget"],
            "players": [dict(shape(p, week, byes), slot=LINEUP_SLOTS.get(slot, str(slot)))
                        for slot, p in roster["entries"]],
        }

    for pos in args.pos:
        limit = args.limit or DEFAULT_LIMIT[pos]
        # over-fetch a bit so re-sorting by proj/avg isn't starved by the %owned cut
        fetch = limit if args.sort == "own" else limit * 2
        rows = [dict(shape(p, week, byes), waiver_status=st) for st, p in free_agents(session, pos, week, fetch)]
        rows.sort(key=SORT_KEYS[args.sort], reverse=True)
        out["free_agents"][pos] = rows[:limit]

    if args.json:
        print(json.dumps(out, indent=2))
        return

    print(f"# click clack — ESPN live pull (Week {week}, {SEASON})\n")
    if "roster" in out:
        r = out["roster"]
        print(f"## {r['team']} roster — FAAB remaining ${r['faab_remaining']} of ${r['faab_budget']}\n")
        print(md_table(r["players"], week, slot_col=True))
        print()
    for pos, rows in out["free_agents"].items():
        print(f"## Free agents — {pos} (top {len(rows)}, sorted by {args.sort})\n")
        print(md_table(rows, week) if rows else "_none returned_")
        print()
    print("_Inj: Q/D/OUT/IR. Δ% = 7-day ownership change (trending). Season/Avg = actual PPR points to date._")


if __name__ == "__main__":
    main()
