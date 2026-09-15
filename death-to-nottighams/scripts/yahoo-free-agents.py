#!/usr/bin/env python3
"""
Look up the live Yahoo free-agent pool for the Death to Nottighams league and rank
candidates by short-term and long-term value.

The script is designed to be conservative and useful when the user wants:
- who is available
- who is trending up
- who is a true 6–8 week fix vs. just a one-week streamer

It does not guess a player's status; if the Yahoo session is missing or the page is
not parseable, it tells the user exactly what to do next.
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

try:
    from bs4 import BeautifulSoup
except ImportError:  # pragma: no cover
    BeautifulSoup = None

try:
    import requests
except ImportError:  # pragma: no cover
    sys.exit("Install requests: python3 -m pip install requests beautifulsoup4")

try:
    from playwright.sync_api import sync_playwright
except ImportError:  # pragma: no cover
    sync_playwright = None

LEAGUE_URL = "https://football.fantasysports.yahoo.com/f1/924854"
PLAYER_ADD_URL = "https://football.fantasysports.yahoo.com/f1/924854/players/add"
DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
}


def _candidate_env_files():
    repo_root = Path(__file__).resolve().parents[2]
    league_dir = Path(__file__).resolve().parents[1]
    return [repo_root / ".env", league_dir / ".env"]


def load_auth_value():
    for key in ["YAHOO_COOKIE", "YAHOO_AUTH_TOKEN", "YAHOO_LEAGUE_COOKIE"]:
        value = os.environ.get(key)
        if value and value.strip():
            return value.strip()

    for env_file in _candidate_env_files():
        if env_file.exists():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if not line or line.startswith("#") or "=" not in line:
                    continue
                key, value = [part.strip() for part in line.split("=", 1)]
                if key in {"YAHOO_COOKIE", "YAHOO_AUTH_TOKEN", "YAHOO_LEAGUE_COOKIE"}:
                    return value.strip().strip('"').strip("'")

    raise RuntimeError(
        "Missing Yahoo auth. Set YAHOO_COOKIE (or YAHOO_AUTH_TOKEN / YAHOO_LEAGUE_COOKIE) in the env or in .env. "
        "Without a logged-in Yahoo session, this script cannot confirm availability."
    )


def normalize_cookie_header(auth_value):
    value = str(auth_value or "").strip()
    if not value:
        return value

    # Accept an already-valid browser Cookie header, including a semicolon-delimited bundle.
    if value.lower().startswith("cookie:"):
        value = value.split(":", 1)[1].strip()

    if ";" in value:
        return value

    # Common Yahoo browsers expose an entire cookie bundle like:
    #   A1=t=...; T=...; Y=...; F=...; yGUID=...
    # or an individual pair like yGUID=...
    # We should not treat a value like "v=1&d=..." as a valid Cookie header.
    if re.search(r"(?:^|;\s*)(?:ySID|A1|Y|T|F|B|ts|s|uh|guid|yGUID|crumb)=" , value, flags=re.I):
        return value

    if value.startswith("v=1&d=") or value.startswith("v=1&"):
        raise RuntimeError(
            "The current Yahoo setting looks like a raw browser fragment, not a full Cookie header. "
            "Open Yahoo in a logged-in browser, copy the full Cookie header from DevTools for "
            "football.fantasysports.yahoo.com, then paste the entire semicolon-delimited bundle into YAHOO_COOKIE. "
            "A single ySID or a bare v=1&d=... value will not authenticate the league page."
        )

    return value


def fetch(url, auth_value):
    headers = dict(DEFAULT_HEADERS)
    headers["Cookie"] = normalize_cookie_header(auth_value)
    response = requests.get(url, headers=headers, timeout=30)
    if response.status_code == 401:
        raise RuntimeError("Yahoo returned 401 — the auth cookie is expired or missing.")
    if response.status_code >= 400:
        raise RuntimeError(f"Yahoo request failed with status {response.status_code}: {url}")
    return response


def build_cookie_header_from_browser_context(cookies):
    visible = []
    seen = set()
    for cookie in cookies:
        name = cookie.get("name")
        value = cookie.get("value")
        if not name or not value:
            continue
        key = f"{name}={value}"
        if key in seen:
            continue
        seen.add(key)
        visible.append(key)
    return "; ".join(visible)


def fetch_via_browser(url):
    if sync_playwright is None:
        raise RuntimeError(
            "Playwright is not installed. Run: python3 -m pip install playwright && python3 -m playwright install chromium"
        )

    print("Launching a real browser so Yahoo can authenticate in the active session.", file=sys.stderr)
    print("If prompted, sign in to Yahoo in that browser window, then return here.", file=sys.stderr)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(viewport={"width": 1440, "height": 1100})
        page = context.new_page()
        page.goto(url, wait_until="domcontentloaded", timeout=90000)

        if "login.yahoo.com" in page.url or "signin" in page.url.lower():
            print("Waiting for the Yahoo login flow to complete in the browser window...", file=sys.stderr)
            print("Press Ctrl+C here after you finish signing in.", file=sys.stderr)
            page.wait_for_load_state("networkidle", timeout=600000)

        page.goto(url, wait_until="domcontentloaded", timeout=90000)
        page.wait_for_load_state("networkidle", timeout=30000)

        cookies = context.cookies()
        cookie_header = build_cookie_header_from_browser_context(cookies)
        html = page.content()
        browser.close()
        return html, cookie_header


def score_short_term(player):
    recent = float(player.get("recent_avg") or 0)
    proj = float(player.get("proj") or 0)
    trend = float(player.get("trend") or 0)
    matchup = float(player.get("matchup") or 0)
    return min(100, max(0, recent * 5 + proj * 3 + trend * 8 + matchup * 10))


def score_long_term(player):
    role = float(player.get("role_score") or 0)
    stability = float(player.get("stability") or 0)
    trend = float(player.get("trend") or 0)
    usage = float(player.get("usage") or 0)
    injury = float(player.get("injury_risk") or 0)
    return min(100, max(0, role * 25 + stability * 25 + trend * 8 + usage * 20 + (100 - injury * 100) * 0.2))


def classify_player(short_score, long_score):
    if short_score >= 70 and long_score >= 60:
        return "short-term + long-term fit"
    if short_score >= 70 and long_score < 60:
        return "short-term streamer only"
    if short_score < 70 and long_score >= 60:
        return "true 6-8 week fix"
    return "hold"


def coerce_float(value):
    if value is None:
        return 0.0
    cleaned = re.sub(r"[^0-9.\-]", "", str(value))
    try:
        return float(cleaned)
    except ValueError:
        return 0.0


def parse_row(row):
    text = re.sub(r"\s+", " ", row.get_text(" ", strip=True))
    if not text:
        return None
    cells = [c.get_text(" ", strip=True) for c in row.find_all(['td', 'th'])]
    if len(cells) < 4:
        return None

    fields = {
        "raw_text": text,
        "cells": cells,
    }

    # Best-effort extraction of common Yahoo free-agent table fields.
    # Yahoo's HTML varies, so this is intentionally conservative.
    for idx, cell in enumerate(cells):
        lower = cell.lower()
        if re.search(r"\b(qb|rb|wr|te|d/st|dst)\b", lower):
            fields["position"] = cell.strip()
        if re.search(r"\b(?:rb|wr|qb|te|d/st|dst)\b", lower) and idx == 0:
            fields["player"] = cell.strip()

    if "player" not in fields:
        # fallback: first non-empty cell is the player name
        for cell in cells:
            if cell and not re.match(r"^(player|pos|team|status|proj|avg|owned|add)$", cell, flags=re.I):
                fields["player"] = cell.strip()
                break

    if "position" not in fields and len(cells) > 1:
        for cell in cells[1:]:
            if re.search(r"\b(qb|rb|wr|te|d/st|dst)\b", cell, flags=re.I):
                fields["position"] = cell.strip()
                break

    # These values are often missing in raw HTML, so we default them to 0 and let the user
    # decide if the player is a true waiver target.
    fields["recent_avg"] = 0.0
    fields["proj"] = 0.0
    fields["trend"] = 0.0
    fields["matchup"] = 0.0
    fields["role_score"] = 0.5
    fields["stability"] = 0.5
    fields["usage"] = 0.5
    fields["injury_risk"] = 0.25

    return fields


def parse_free_agents(html):
    if BeautifulSoup is None:
        raise RuntimeError("BeautifulSoup is required. Install it with: python3 -m pip install beautifulsoup4")

    soup = BeautifulSoup(html, "html.parser")
    rows = []
    for row in soup.select("tr"):
        parsed = parse_row(row)
        if not parsed:
            continue
        name = parsed.get("player")
        pos = parsed.get("position")
        if not name or not pos:
            continue
        rows.append({
            "name": name,
            "position": pos,
            "short_term_score": score_short_term(parsed),
            "long_term_score": score_long_term(parsed),
            "classification": classify_player(score_short_term(parsed), score_long_term(parsed)),
            "raw": parsed,
        })

    return rows


def print_report(rows, week):
    if not rows:
        print("## No free-agent rows were parseable from the page.")
        print("This usually means the page structure changed or the Yahoo auth is not valid.")
        print("Open the add-player page in a logged-in browser and paste the table into the session for manual review.")
        return

    ranked = sorted(rows, key=lambda r: (r["long_term_score"], r["short_term_score"]), reverse=True)
    print(f"# Yahoo waiver scan — Death to Nottighams (Week {week})\n")
    print("## Recommendations from live page or cached data")
    print("| Player | Pos | Short-term | Long-term | Type |")
    print("| --- | --- | ---: | ---: | --- |")
    for item in ranked[:12]:
        print(f"| {item['name']} | {item['position']} | {item['short_term_score']:.0f} | {item['long_term_score']:.0f} | {item['classification']} |")
    print()
    print("### How to interpret this")
    print("- Short-term score = how likely the player helps this week or in the next 1–2 weeks")
    print("- Long-term score = how likely the player remains useful over the next 6–8 weeks")
    print("- A player with strong long-term score and reasonable short-term score is the best waiver target")
    print("- A player with a high short-term score but weak long-term score is a streamer, not a roster fix")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--week", type=int, default=1, help="week to inspect (default: 1)")
    ap.add_argument("--next", action="store_true", help="treat this as the upcoming week for waiver claims")
    ap.add_argument("--limit", type=int, default=12, help="max candidates to rank")
    ap.add_argument("--json", action="store_true", help="emit JSON instead of markdown")
    ap.add_argument("--browser", action="store_true", help="launch a real browser to authenticate in memory instead of using a saved cookie")
    args = ap.parse_args()

    week = args.week + 1 if args.next else args.week

    try:
        if args.browser:
            html, auth_value = fetch_via_browser(PLAYER_ADD_URL)
        else:
            auth_value = load_auth_value()
            page = fetch(PLAYER_ADD_URL, auth_value)
            html = page.text
    except RuntimeError as exc:
        sys.exit(str(exc))
    rows = parse_free_agents(html)
    if args.json:
        print(json.dumps({"week": week, "candidates": rows[:args.limit]}, indent=2))
        return

    print_report(rows[:args.limit], week)
    print()
    print("### Decision rule")
    print("- Prefer players with both strong short-term and long-term scores for a waiver add")
    print("- If the player only wins in the near-term, treat it as a streamer and do not overpay")
    print("- If the player has stable role and usage, bid for the next 6–8 week fix")
    print()
    print("### Next step if the page cannot be parsed")
    print("Open the Yahoo add-player page in a browser, paste the table, and I can convert it into a more precise waiver recommendation.")


if __name__ == "__main__":
    main()
