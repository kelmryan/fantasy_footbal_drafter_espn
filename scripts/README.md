# Draft Automation Scripts

Scripts to automate player research during the draft.

## Quick Start

**Queue-based research (recommended - works reliably):**

```bash
# Terminal 1: Run Claude Code for the draft
# (your main session)

# Terminal 2: Start the queue monitor
./scripts/queue-research.sh state/mock-draft.md &
# Monitors picks, checks cache, queues missing players

# When Terminal 2 shows "To process queue, type in Claude Code:"
# Just type this in Terminal 1:
process research queue
```

**Full auto-research (researches everything, ignores cache):**

```bash
# Terminal 2: Start the auto-research monitor with auto-dispatch
./scripts/auto-research.sh state/mock-draft.md --auto-dispatch &
# Researches all new picks regardless of cache
```

**Manual mode (if you prefer copy/paste control):**

```bash
# Terminal 2: Start the monitor without auto-dispatch
./scripts/auto-research.sh state/mock-draft.md &

# Terminal 3: When you see "Trigger file updated", run:
./scripts/generate-research-prompt.sh
# Then copy the output and paste it to Claude Code
```

---

## Scripts

### `queue-research.sh` ⭐ **Recommended**

Queue-based research monitor that works reliably without CLI issues.

**Usage:**
```bash
./scripts/queue-research.sh [draft-file]
```

**Example:**
```bash
./scripts/queue-research.sh state/mock-draft.md &
```

**What it does:**
- Watches for new picks in the draft file
- Checks if each player already exists in `state/news/*.md` files
- ✅ **Player in cache** → Skip (you already have intel)
- ❌ **Player NOT in cache** → Add to queue file (`/tmp/ff-research-queue.txt`)
- Tells you when to process the queue

**When you see "process queue" message:**
Just type in your Claude Code session:
```
process research queue
```

Claude will:
1. Read all queued players
2. Research each one
3. Update `state/news/` files
4. Clear the queue

**Why use this:**
- **Reliable**: No CLI piping issues
- **Smart**: Only researches players not in cache
- **Control**: You decide when to process (batch during breaks, or continuously)
- **Fast**: Queue builds up during fast picks, process when you have time

**Example output:**
```
[17:20:15] 🆕 4 new pick(s) detected
   📝 Queued: Tyler Allgeier
   📝 Queued: Jordan Addison
   ✅ Cached: 2 | ⏳ Queued: 2 | 📊 Total in queue: 5

   💡 To process queue, type in Claude Code: process research queue
```

---

### `smart-research.sh`

Smart research monitor that checks the local news cache before triggering web research.

**Usage:**
```bash
./scripts/smart-research.sh [draft-file]
```

**Example:**
```bash
./scripts/smart-research.sh state/mock-draft.md &
```

**What it does:**
- Watches for new picks in the draft file
- Extracts player names from recent picks
- **Checks if each player already exists in `state/news/*.md` files**
- ✅ **Player in cache** → Skip research (use existing intel)
- ❌ **Player NOT in cache** → Send research request to Claude Code
- Only researches players you don't have intel on yet, saving time during fast drafts

**Why use this:**
- **Faster**: Doesn't re-research players you already have data on
- **Efficient**: Only queries the web for genuinely new players
- **Smart**: Leverages your pre-draft research in `state/news/`

**Example output:**
```
[17:15:22] 🆕 3 new pick(s) detected (total: 72)
📚 Already in news cache:
   ✓ Bijan Robinson
   ✓ Nico Collins
🔍 Need research (not in cache):
   ❌ Tyler Allgeier
   ❌ Jordan Addison

🔍 Requesting research for 2 player(s)...
✅ Research request sent to Claude Code
```

---

### `auto-research.sh`

Monitors the draft board file for new picks and triggers research (automatically or manually).

**Usage:**
```bash
# Automatic mode (sends directly to Claude Code)
./scripts/auto-research.sh [draft-file] --auto-dispatch

# Manual mode (prints prompts for you to copy/paste)
./scripts/auto-research.sh [draft-file]
```

**Examples:**
```bash
# Auto mode - recommended for draft day
./scripts/auto-research.sh state/draft-board.md --auto-dispatch &

# Manual mode - if you want control over when research happens
./scripts/auto-research.sh state/mock-draft.md &
```

**What it does:**
- Watches for new picks in the draft file
- Extracts player names from recent picks
- **Auto mode (`--auto-dispatch`)**: Automatically sends research requests to your active Claude Code session via the `claude` CLI
- **Manual mode**: Writes to `/tmp/ff-research-trigger.txt` and prints a prompt for you to copy/paste

**Options:**
- `--auto-dispatch`: Enable automatic research dispatch (requires `claude` CLI)
- Edit `CHECK_INTERVAL` in the script to change polling frequency (default: 5 seconds)

---

### `generate-research-prompt.sh`

Reads the trigger file and generates a formatted research prompt for Claude Code.

**Usage:**
```bash
./scripts/generate-research-prompt.sh
```

**What it does:**
- Reads `/tmp/ff-research-trigger.txt`
- Formats a Claude-ready research prompt
- Clears the trigger file after generating the prompt

**Workflow:**
1. `auto-research.sh` detects new picks → writes to trigger file
2. You run `generate-research-prompt.sh` → get formatted prompt
3. Copy/paste prompt to Claude Code
4. Claude researches players and updates `state/news/*.md` files

---

## Typical Draft Day Setup

**Smart research setup (recommended):**

**Terminal 1: Claude Code**
```bash
cd /mnt/c/Users/swimm/programming/fantasy_football_espn
claude-code
# Your main draft session
```

**Terminal 2: Smart research monitor**
```bash
cd /mnt/c/Users/swimm/programming/fantasy_football_espn
./scripts/smart-research.sh state/draft-board.md &

# Watch it work
tail -f /tmp/ff-smart-research.log
```

That's it! Only players not in your news cache will trigger research, saving time.

---

**Manual setup (if you prefer control):**

**Terminal 1: Claude Code**
```bash
claude-code
# Your main draft session
```

**Terminal 2: Auto-research monitor**
```bash
cd /mnt/c/Users/swimm/programming/fantasy_football_espn
./scripts/auto-research.sh state/draft-board.md &
```

**Terminal 3: Generate prompts as needed**
```bash
watch -n 10 ./scripts/generate-research-prompt.sh
# Or run manually when you see trigger file updates, then copy/paste to Terminal 1
```

---

## Customization

### Change polling interval
Edit `auto-research.sh` line 11:
```bash
CHECK_INTERVAL=5  # seconds between checks
```

### Change trigger file location
Edit both scripts, replace:
```bash
RESEARCH_TRIGGER="/tmp/ff-research-trigger.txt"
```

### Auto-clear old triggers
Add to `auto-research.sh` before the while loop:
```bash
> "$RESEARCH_TRIGGER"  # Clear on start
```

---

## Stopping the monitor

```bash
# Find the process
ps aux | grep auto-research

# Kill it
kill [PID]

# Or kill all instances
pkill -f auto-research.sh
```
