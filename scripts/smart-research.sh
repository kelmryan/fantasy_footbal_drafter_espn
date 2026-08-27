#!/bin/bash

# Smart auto-research script for fantasy football draft
# Only researches players that aren't already in state/news/ intel files
#
# Usage: ./scripts/smart-research.sh [draft-file]
# Example: ./scripts/smart-research.sh state/mock-draft.md &

DRAFT_FILE="${1:-state/mock-draft.md}"
NEWS_DIR="state/news"
RESEARCH_LOG="/tmp/ff-smart-research.log"
LAST_PICK_COUNT=0
CHECK_INTERVAL=5  # seconds between checks

echo "🏈 Smart auto-research monitor started"
echo "📋 Watching: $DRAFT_FILE"
echo "📁 News cache: $NEWS_DIR"
echo "🔄 Check interval: ${CHECK_INTERVAL}s"
echo "💡 Strategy: Only research players not already in news files"
echo ""

# Create news directory if it doesn't exist
mkdir -p "$NEWS_DIR"

# Initialize log
echo "# Smart Research Log - Started at $(date)" > "$RESEARCH_LOG"

# Function to check if a player exists in any news file
player_in_news() {
    local player="$1"
    # Check all news files for this player (case-insensitive)
    if grep -iq "$player" "$NEWS_DIR"/*.md 2>/dev/null; then
        return 0  # Found
    else
        return 1  # Not found
    fi
}

# Function to send research request to Claude Code
request_research() {
    local players="$1"
    local player_count=$(echo "$players" | wc -w)

    echo "[$(date '+%H:%M:%S')] 🔍 Requesting research for $player_count player(s)..."

    # Create a temporary file with the research prompt
    PROMPT_FILE="/tmp/ff-research-prompt-$$.txt"

    cat > "$PROMPT_FILE" <<EOF
Research and update state/news/ intel files for these recently drafted players who are NOT yet in the news cache:

$players

For each player:
1. Determine their position (RB/WR/TE/QB)
2. Look up their 2026 role, injury status, and fantasy-relevant stats
3. Add a concise entry to the appropriate state/news/[position]-intel.md file
4. Format: **Player Name (TEAM)** - [2-3 line summary covering role, injury status, and fantasy impact]

Only research players you don't already have in the news files. Skip any that are already documented.
EOF

    # Send to Claude Code via CLI
    cat "$PROMPT_FILE" | claude 2>/dev/null

    if [ $? -eq 0 ]; then
        echo "✅ Research request sent to Claude Code"
        echo "[$(date)] Research requested for: $players" >> "$RESEARCH_LOG"
    else
        echo "⚠️  Failed to send to Claude Code - falling back to manual prompt:"
        echo ""
        cat "$PROMPT_FILE"
        echo ""
        echo "   Copy the above to Claude Code manually"
    fi

    rm -f "$PROMPT_FILE"
}

while true; do
    if [ ! -f "$DRAFT_FILE" ]; then
        sleep $CHECK_INTERVAL
        continue
    fi

    # Count current picks (lines in the picks table, excluding header)
    CURRENT_PICKS=$(grep -c "^\| [0-9]" "$DRAFT_FILE" 2>/dev/null || echo "0")

    if [ "$CURRENT_PICKS" -gt "$LAST_PICK_COUNT" ]; then
        NEW_PICKS=$((CURRENT_PICKS - LAST_PICK_COUNT))
        echo "[$(date '+%H:%M:%S')] 🆕 $NEW_PICKS new pick(s) detected (total: $CURRENT_PICKS)"

        # Extract the last N picks and get unique players
        RECENT_PLAYERS=$(tail -n "$NEW_PICKS" "$DRAFT_FILE" | \
            grep "^\|" | \
            awk -F'|' '{print $4}' | \
            sed 's/^[[:space:]]*//;s/[[:space:]]*$//' | \
            sed 's/\*\*//g' | \
            grep -v "Player" | \
            grep -v "^$" | \
            grep -v "^-" | \
            sort -u)

        if [ -n "$RECENT_PLAYERS" ]; then
            NEED_RESEARCH=""
            ALREADY_CACHED=""

            while IFS= read -r player; do
                if player_in_news "$player"; then
                    ALREADY_CACHED="$ALREADY_CACHED\n   ✓ $player"
                else
                    NEED_RESEARCH="$NEED_RESEARCH $player"
                fi
            done <<< "$RECENT_PLAYERS"

            # Report status
            if [ -n "$ALREADY_CACHED" ]; then
                echo "📚 Already in news cache:"
                echo -e "$ALREADY_CACHED"
            fi

            if [ -n "$NEED_RESEARCH" ]; then
                NEED_RESEARCH=$(echo "$NEED_RESEARCH" | xargs)  # Trim whitespace
                echo "🔍 Need research (not in cache):"
                for p in $NEED_RESEARCH; do
                    echo "   ❌ $p"
                done
                echo ""

                # Send research request for missing players only
                request_research "$NEED_RESEARCH"
            else
                echo "✅ All players already documented - no research needed"
            fi

            echo ""
        fi

        LAST_PICK_COUNT=$CURRENT_PICKS
    fi

    sleep $CHECK_INTERVAL
done
