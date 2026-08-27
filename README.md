# Fantasy Football Assistant — click clack (ESPN PPR)

A Claude Code project that turns this folder into a multi-agent fantasy football assistant for your ESPN league. Open this folder in VS Code (with the Claude Code extension) or run `claude` from a terminal in this folder, and Claude will automatically read `CLAUDE.md` and know the league, your team, and how to work.

## What's here

```
CLAUDE.md                    ← the playbook Claude reads automatically every session
.claude/agents/               ← 5 specialist subagents Claude dispatches to
    rb-expert.md
    wr-expert.md
    te-expert.md
    dst-expert.md
    schedule-manager.md
state/
    draft-board.md            ← fills in live during your draft
    roster-notes.md           ← your current roster + FAAB balance, kept current across sessions
```

**Why 5 subagents instead of 8?** The position experts (RB/WR/TE/DST) and the schedule researcher are self-contained lookups — a good fit for Claude Code's subagents, which each run in their own isolated context and can even run in parallel. "Draft Manager," "Team Manager," and "Free Agent Manager" aren't subagents — they're roles Claude plays at the top level of your conversation, because they need to remember things (the draft board, your roster) across many turns, which a one-shot subagent can't do. That memory lives in the `state/` files instead, so it survives even if you close VS Code and come back later.

## Getting started

1. Open this folder in VS Code, or `cd` into it and run `claude` in a terminal.
2. Just talk to it naturally — you don't need to name a role explicitly, but it helps Claude route faster if you do. A few examples:

**On draft day:**
> "Let's start the draft — it's a 14-team snake, I'm picking 7th."

> "Team 3 took Ja'Marr Chase. Team 4 took Bijan Robinson. Who should I take at pick 7?"

> "I'm debating between two tight ends here, X and Y — who's the better pick?"

**Setting your lineup:**
> "Here's my roster: [paste it, or Claude will read it live if you've set up browser access — see below]. Who should I start at FLEX this week — X or Y?"

**Free agent / waiver decisions:**
> "Is [free agent] a better play than [my bench player] this week? How much should I bid?"

> "What's my biggest roster need right now?"

Claude will dispatch the right specialist subagent(s) behind the scenes and give you one synthesized answer — you shouldn't need to invoke `.claude/agents/rb-expert.md` etc. by name, though you can ("ask the rb-expert about...") if you want to be explicit.

## Optional: live ESPN access

Without any extra setup, Claude will ask you to paste your roster or the free-agent list when it needs current data — that works fine. If you'd rather Claude read your ESPN team page and free-agent list itself, you'd need a browser-automation MCP server (e.g. Playwright MCP) configured for Claude Code, since — unlike the Cowork session that originally built this — Claude Code in VS Code doesn't come with one built in.

This isn't set up here on purpose: adding an MCP server means installing and running an extra package on your machine, and that's a call you should make deliberately rather than something done for you silently. If you want it, the general shape is adding an entry to a `.mcp.json` file in this folder pointing at a Playwright MCP server — happy to walk you through that step-by-step (and flag exactly what the install command does) whenever you're ready. Your league is private, so either way you'll need to be logged into ESPN in whatever browser Claude ends up using.

## QB and Kicker

There's no dedicated `qb-expert` or `k-expert` subagent — `CLAUDE.md` has lightweight built-in guidance for both instead (this league's scoring mildly devalues QB relative to 6-point-passing-TD leagues, and kickers are treated as streamable, draft-last). Say the word if you want full dedicated subagents for those two positions to match the others.

## Keeping it current

If something about the league changes (a rule, your roster, a trade), just tell Claude in conversation — it'll update `state/roster-notes.md` itself. If you want to hand-edit the state files directly, that's fine too; Claude reads them fresh each session.
