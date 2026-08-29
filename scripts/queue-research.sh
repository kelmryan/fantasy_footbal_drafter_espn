#!/bin/bash

# Queue-based research monitor
# Monitors picks, checks cache, writes missing players to a queue file
# You manually trigger research when ready
#
# Usage: ./scripts/queue-research.sh [draft-file]

DRAFT_FILE="${1:-state/mock-draft.md}"
NEWS_DIR="state/news"
QUEUE_FILE="/tmp/ff-research-queue.txt"
LAST_PICK_COUNT=0
CHECK_INTERVAL=5

# Snake draft position tracking (click clack league: 14 teams, Kelly is slot 1)
TEAMS=14
SLOT=1
LAST_ALERTED_PICK=0

echo "🏈 Queue-based research monitor started"
echo "📋 Watching: $DRAFT_FILE"
echo "📁 News cache: $NEWS_DIR"
echo "📝 Queue file: $QUEUE_FILE"
echo "🔄 Check interval: ${CHECK_INTERVAL}s"
echo ""
echo "When you see players queued, run in Claude Code:"
echo "  process research queue"
echo ""

# Compute the next pick number belonging to Kelly (slot $SLOT of $TEAMS, snake order)
next_kelly_pick() {
    local current="$1"
    local r=1
    local pick
    while true; do
        if (( r % 2 == 1 )); then
            pick=$(( (r - 1) * TEAMS + SLOT ))
        else
            pick=$(( r * TEAMS - SLOT + 1 ))
        fi
        if (( pick > current )); then
            echo "$pick"
            return
        fi
        r=$((r + 1))
    done
}

# Initialize queue
> "$QUEUE_FILE"

# Function to check if a player exists in any news file
player_in_news() {
    local player="$1"
    if grep -iq "$player" "$NEWS_DIR"/*.md 2>/dev/null; then
        return 0
    else
        return 1
    fi
}

while true; do
    if [ ! -f "$DRAFT_FILE" ]; then
        sleep $CHECK_INTERVAL
        continue
    fi

    CURRENT_PICKS=$(grep -c "^\| [0-9]" "$DRAFT_FILE" 2>/dev/null || echo "0")

    if [ "$CURRENT_PICKS" -gt "$LAST_PICK_COUNT" ]; then
        NEW_PICKS=$((CURRENT_PICKS - LAST_PICK_COUNT))
        echo "[$(date '+%H:%M:%S')] 🆕 $NEW_PICKS new pick(s) detected"

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
            CACHED_COUNT=0
            QUEUED_COUNT=0

            while IFS= read -r player; do
                if player_in_news "$player"; then
                    ((CACHED_COUNT++))
                else
                    echo "$player" >> "$QUEUE_FILE"
                    ((QUEUED_COUNT++))
                    echo "   📝 Queued: $player"
                fi
            done <<< "$RECENT_PLAYERS"

            TOTAL_QUEUED=$(sort -u "$QUEUE_FILE" | wc -l)
            echo "   ✅ Cached: $CACHED_COUNT | ⏳ Queued: $QUEUED_COUNT | 📊 Total in queue: $TOTAL_QUEUED"

            if [ $QUEUED_COUNT -gt 0 ]; then
                echo ""
                echo "   💡 To process queue, type in Claude Code: process research queue"
                echo ""
            fi
        fi

        LAST_PICK_COUNT=$CURRENT_PICKS
    fi

    NEXT_PICK=$(next_kelly_pick "$CURRENT_PICKS")
    PICKS_AWAY=$(( NEXT_PICK - CURRENT_PICKS ))

    if [ "$PICKS_AWAY" -le 4 ] && [ "$NEXT_PICK" != "$LAST_ALERTED_PICK" ]; then
        echo ""
        echo "⚠️  $PICKS_AWAY pick(s) until your turn (pick $NEXT_PICK)!"
        echo "   Ask Claude Code to check for fallers: any player better than the current"
        echo "   top-5 forecast who's still on the board and worth researching."
        echo ""
        LAST_ALERTED_PICK=$NEXT_PICK
    fi

    sleep $CHECK_INTERVAL
done
