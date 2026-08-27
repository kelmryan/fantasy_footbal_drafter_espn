#!/bin/bash

# Generate a Claude-ready research prompt from the trigger file
# Usage: ./scripts/generate-research-prompt.sh

TRIGGER_FILE="/tmp/ff-research-trigger.txt"

if [ ! -f "$TRIGGER_FILE" ]; then
    echo "No research triggers found."
    exit 0
fi

# Get unique players from trigger file
PLAYERS=$(grep -v "^#" "$TRIGGER_FILE" | grep -v "^$" | sort -u)

if [ -z "$PLAYERS" ]; then
    echo "No players to research."
    exit 0
fi

echo "Research and update state/news/ intel files for these players:"
echo ""

# Group by position (simple heuristic - you can improve this)
for player in $PLAYERS; do
    echo "- $player"
done

echo ""
echo "For each player:"
echo "1. Dispatch schedule-manager to get current injury/role/matchup intel"
echo "2. Update the appropriate state/news/[position]-intel.md file"
echo "3. Keep entries concise - 2-3 lines per player max"

# Clear trigger file after generating prompt
> "$TRIGGER_FILE"
