#!/bin/bash
# Pre-push script: updates chapter numbers before git push
# This can be called manually or set up as a git hook

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "Running pre-push checks..."
echo "Updating chapter numbers from placeholders..."

"$SCRIPT_DIR/update_chapter_numbers.sh"

echo "Pre-push checks complete."
echo "You can now push your changes."

