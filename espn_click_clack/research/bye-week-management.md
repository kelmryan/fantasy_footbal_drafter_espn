# Bye Week Management Strategy

_Quick reference for agents to avoid bye week conflicts during draft_

## Rule: Track and Avoid Clustering

**Definition of "cluster":** 3+ starters with the same bye week

**Why it matters:** In a 14-team league, waiver wire is thin. If you lose 3+ starters the same week, you're forced to start bottom-tier replacements and likely lose that week.

## Current Roster Bye Weeks (Mock Draft Example)

| Player | Position | Bye Week |
|--------|----------|----------|
| Bijan Robinson | RB | 11 |
| Javonte Williams | RB | 10 |
| Nico Collins | WR | 8 |
| Rashee Rice | WR | TBD (likely 5-7) |
| Evan Engram | TE | 7 |
| Anthony Richardson | QB | TBD |
| 49ers D/ST | D/ST | 9 |

**Current clusters:** None (all spread out) ✅

## Decision Rules for Agents

### **When evaluating a player:**

1. **Check state/news/*.md** for their bye week
2. **Check current roster** for existing bye weeks
3. **Apply this logic:**

   - **0-1 players on that bye** → ✅ No conflict, OK to draft
   - **2 players on that bye, both bench** → ✅ OK to draft (bench cluster is fine)
   - **2 players on that bye, 1+ starter** → ⚠️ Flag it, but draftable if value is strong
   - **3+ players on that bye** → ❌ AVOID unless player is 2+ rounds ahead of ADP

### **Prioritize avoiding conflicts with:**
- Your RB1 (Bijan = Week 11)
- Your WR1 (Nico = Week 8)
- Your QB1 (Anthony Richardson = TBD)

**Why:** Losing your RB1 for a week is manageable. Losing RB1 + RB2 + WR1 = guaranteed loss.

## Example Agent Response Format

**Good:**
> "Recommendation: Draft **Chris Olave (WR, NO)**. Bye week 8 matches Nico Collins, but you have Rashee Rice and Wan'Dale Robinson to cover WR slots. Per bye-week-management.md, 2-player cluster is acceptable when value is strong (Olave = top-15 WR at pick 56)."

**Good (avoiding conflict):**
> "Recommendation: **Avoid Josh Jacobs (RB, GB)** — bye week 11 matches Bijan Robinson. Per bye-week-management.md, avoid creating RB1 + RB2 cluster. Take Tony Pollard (bye 9) instead."

**Bad:**
> "Draft Josh Jacobs" (doesn't mention bye week conflict at all)

## Special Cases

### **Late-round picks (Rounds 12+):**
- Bye week conflicts matter LESS for bench depth
- OK to draft a Week 11 bye if it's your 6th RB (won't start that week anyway)

### **Streaming positions (D/ST, K):**
- Bye weeks DON'T matter — you'll stream these weekly by matchup
- Never avoid a player due to D/ST/K bye week conflict

### **QB bye weeks:**
- In 4-pt passing TD league, most teams only roster 1 QB
- If you draft a QB2 backup, bye week overlap is FINE (backup exists for QB1 bye week coverage)

## Agents: When to Check This File

✅ **Check before every draft recommendation** — cite specific rules when flagging conflicts
✅ **Update the "Current Roster Bye Weeks" table** as Kelly drafts players (or reference draft-board.md)
✅ **Cite this file explicitly** when recommending/avoiding a player due to bye week (e.g., "Per bye-week-management.md...")

This ensures consistent bye week logic across all agents without regenerating the same rules every time.
