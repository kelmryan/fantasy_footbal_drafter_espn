#!/bin/bash

# Auto-research script for fantasy football draft
# Monitors draft picks and triggers Claude to research/update player intel
#
# Usage:
#   Manual mode:    ./scripts/auto-research.sh [draft-file]
#   Auto mode:      ./scripts/auto-research.sh [draft-file] --auto-dispatch
#
# Example:
#   ./scripts/auto-research.sh state/mock-draft.md --auto-dispatch &

# Parse arguments
AUTO_DISPATCH=false
DRAFT_FILE=""

for arg in "$@"; do
    if [ "$arg" = "--auto-dispatch" ]; then
        AUTO_DISPATCH=true
    elif [ -z "$DRAFT_FILE" ]; then
        DRAFT_FILE="$arg"
    fi
done

DRAFT_FILE="${DRAFT_FILE:-state/mock-draft.md}"
RESEARCH_TRIGGER="/tmp/ff-research-trigger.txt"
LAST_PICK_COUNT=0
CHECK_INTERVAL=5  # seconds between checks

echo "🏈 Auto-research monitor started"
echo "📋 Watching: $DRAFT_FILE"
echo "🔄 Check interval: ${CHECK_INTERVAL}s"
if [ "$AUTO_DISPATCH" = true ]; then
    echo "🤖 Auto-dispatch: ENABLED (will send directly to Claude Code)"
else
    echo "📋 Manual mode (copy/paste prompts yourself)"
fi
echo ""

# Create trigger file if it doesn't exist
touch "$RESEARCH_TRIGGER"

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
            grep -v "Player" | \
            grep -v "^$" | \
            sort -u)

        if [ -n "$RECENT_PLAYERS" ]; then
            echo "📝 Players to research:"
            echo "$RECENT_PLAYERS" | sed 's/^/   - /'
            echo ""

            # Write to trigger file with timestamp
            {
                echo "# Research triggered at $(date)"
                echo "# New picks detected: $NEW_PICKS"
                echo "# Players:"
                echo "$RECENT_PLAYERS"
                echo ""
            } >> "$RESEARCH_TRIGGER"

            if [ "$AUTO_DISPATCH" = true ]; then
                # Build research message
                PLAYER_LIST=$(echo "$RECENT_PLAYERS" | tr '\n' ',' | sed 's/,$//' | sed 's/,/, /g')

                echo "🤖 Auto-dispatching to Claude Code..."

                # Build the research prompt
                RESEARCH_PROMPT="Research and update state/news/ intel files for these recently drafted players: $PLAYER_LIST

For each player:
1. Check their position (RB/WR/TE/QB)
2. Look up current 2026 injury status, role, recent stats/news
3. Update the appropriate state/news/[position]-intel.md file with a concise 2-3 line entry
4. Keep entries brief and focused on fantasy-relevant info (target share, injury status, role changes)

Format each entry like:
**Player Name (TEAM)** - [brief intel]. [Key stat or concern]. [Fantasy impact]."

                # Send to Claude Code via CLI (pipe to stdin)
                echo "$RESEARCH_PROMPT" | claude 2>/dev/null

                if [ $? -eq 0 ]; then
                    echo "✅ Research request sent to Claude Code"
                else
                    echo "❌ Failed to send to Claude Code (is claude CLI available?)"
                    echo "   Manual prompt:"
                    echo "   Research and update intel for: $PLAYER_LIST"
                fi
            else
                echo "✅ Trigger file updated: $RESEARCH_TRIGGER"
                echo "   Copy this prompt to Claude Code:"
                echo ""
                echo "   Research and update intel for these players:"
                for player in $RECENT_PLAYERS; do
                    echo "   - $player"
                done
                echo ""
            fi
        fi

        LAST_PICK_COUNT=$CURRENT_PICKS
    fi

    sleep $CHECK_INTERVAL
done
