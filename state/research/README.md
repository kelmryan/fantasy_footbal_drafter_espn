# Research Folder — Strategy Documentation

_Pre-written strategies for agents to reference during draft and season management_

## Purpose

This folder contains **reusable strategy documents** that agents should reference when making recommendations. Instead of regenerating the same logic every time (which wastes tokens), agents cite specific rules from these files.

**Example agent response:**
> "Recommendation: Draft **Javonte Williams (RB)** at pick 28. Per `draft-strategy-core.md`, Rounds 2-3 should prioritize RB + WR to secure positional balance. Per `bye-week-management.md`, Javonte's Week 10 bye avoids conflict with Bijan's Week 11 bye."

This saves tokens and ensures **consistent, data-driven recommendations** across all agents.

---

## File Index

### **1. draft-strategy-core.md**
**Use case:** Reference for ALL draft decisions

**Contents:**
- Draft philosophy by round (early, mid, late rounds)
- Value-based drafting (BPA vs. need)
- Risk management (red flags, yellow flags)
- Full PPR leverage (target high-reception players)
- Snake draft positional value
- Common mistakes to avoid

**When to reference:**
- Every draft pick (cite specific rules)
- User asks "who should I draft?"
- Comparing multiple players at different positions

---

### **2. positional-value-tiers.md**
**Use case:** Determine WHEN to draft each position

**Contents:**
- Round-by-round positional priority (Rounds 1-14)
- Position-by-position ADP guidelines
- Positional scarcity tiers (RB > WR > TE > QB > D/ST > K)
- 4-pt passing TD impact on QB value

**When to reference:**
- User asks "should I draft a QB now?"
- Evaluating whether to reach for a player
- Balancing roster composition (2 RBs, 2 WRs minimum by Round 5)

---

### **3. ppr-scoring-advantage.md**
**Use case:** Leverage full PPR (1 pt/reception) for draft edge

**Contents:**
- PPR vs. standard scoring value shift
- Player archetypes to target (pass-catching RBs, slot WRs, target-hog TEs)
- Key metrics (targets/game, receptions/game, target share)
- FLEX position strategy (WR > RB in PPR)

**When to reference:**
- Comparing WR vs. RB at same pick
- Evaluating FLEX options
- Choosing between high-yardage vs. high-reception players

---

### **4. bye-week-management.md**
**Use case:** Avoid bye week clustering

**Contents:**
- Definition of "cluster" (3+ starters same bye week)
- Decision rules (when to avoid, when to accept conflicts)
- Current roster bye weeks (updated during draft)
- Special cases (late-round picks, streaming positions)

**When to reference:**
- BEFORE every draft recommendation (check bye weeks)
- User asks about a specific player
- Flagging conflicts in recommendations

---

### **5. late-round-strategy.md**
**Use case:** Maximize value in Rounds 11-14

**Contents:**
- Handcuff strategy (YOUR OWN RBs, not others')
- Lottery ticket strategy (injured stashes, breakout candidates)
- Backup QB strategy (when to draft, when to skip)
- D/ST strategy (Round 13 ONLY)
- K strategy (Round 14 ONLY, literally anyone)

**When to reference:**
- Rounds 11-14 draft picks
- User asks "should I draft a defense now?"
- Balancing bench composition

---

## How Agents Should Use These Files

### **Step 1: Read the relevant strategy file(s)**
- Check `draft-strategy-core.md` for overall philosophy
- Check `positional-value-tiers.md` for round-specific priorities
- Check `ppr-scoring-advantage.md` if comparing WR/RB
- Check `bye-week-management.md` for all draft picks
- Check `late-round-strategy.md` for Rounds 11-14

### **Step 2: Apply the rules to the specific decision**
- Example: User is on the clock at pick 28 (Round 2)
  - `positional-value-tiers.md` says: "Rounds 2-3 prioritize RB + WR"
  - `draft-strategy-core.md` says: "Lock RB2 + WR1 at 28-29"
  - `bye-week-management.md` says: "Check for conflicts with Bijan (Week 11)"

### **Step 3: Cite the specific file and rule in your response**
- **Good example:**
  > "Recommendation: Draft **Javonte Williams (RB, DAL)** at pick 28. Per `positional-value-tiers.md`, Rounds 2-3 should prioritize RB + WR to secure positional balance. Javonte's Week 10 bye (per `bye-week-management.md`) avoids conflict with Bijan's Week 11 bye."

- **Bad example:**
  > "I think you should draft Javonte Williams." (no context, no strategy cited)

### **Step 4: Update files if needed**
- If you find new player intel, update `state/news/*.md` (NOT these strategy files)
- These strategy files are **principles**, not live data
- Only update if league rules change (e.g., switch from PPR to standard)

---

## Token Optimization

**Before these files existed:**
- Agent regenerates "should I draft QB early?" logic every time → 200-500 tokens per decision
- Across 14 rounds = 2,800-7,000 tokens wasted on repeating the same logic

**With these files:**
- Agent reads `positional-value-tiers.md` once (1,500 tokens)
- Agent cites specific rules in responses (50-100 tokens per decision)
- Across 14 rounds = ~2,200 tokens total (saved 60%+ tokens)

**Result:** More tokens available for real-time research, player analysis, and custom recommendations.

---

## Maintenance

**Update these files when:**
- League rules change (e.g., switch to 6-pt passing TDs → update `positional-value-tiers.md`)
- Major strategy shifts mid-season (e.g., injuries decimate RB position → update `draft-strategy-core.md`)

**Do NOT update for:**
- Individual player news (use `state/news/*.md` instead)
- One-off draft decisions (these are principles, not pick-by-pick tracking)

---

## Quick Reference for Agents

| Question | File to Check |
|----------|---------------|
| "Who should I draft at pick X?" | `draft-strategy-core.md` + `positional-value-tiers.md` |
| "Should I draft a QB now?" | `positional-value-tiers.md` |
| "Does this player have a bye week conflict?" | `bye-week-management.md` |
| "WR or RB in PPR?" | `ppr-scoring-advantage.md` |
| "Should I draft a defense now?" | `late-round-strategy.md` |
| "Handcuff or lottery ticket?" | `late-round-strategy.md` |

**Default workflow:** Read `draft-strategy-core.md` first for every draft question, then check specific files as needed.

---

**Last updated:** August 27, 2026 (post-mock draft)
