#!/bin/bash
# Setup script for git hooks
# This creates symlinks to the pre-push hook

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
HOOKS_DIR="$REPO_ROOT/.git/hooks"

echo "Setting up git hooks..."

# Create pre-push hook
cat > "$HOOKS_DIR/pre-push" << 'EOF'
#!/bin/bash
# Git pre-push hook: automatically update chapter numbers before pushing

# Get the repository root
REPO_ROOT="$(git rev-parse --show-toplevel)"
SCRIPT_PATH="$REPO_ROOT/docs/.scripts/update_chapter_numbers.sh"

# Check if we're on the docs branch or if docs files are being pushed
if [ -f "$SCRIPT_PATH" ]; then
    # Check if any docs content files are in the push
    while read local_ref local_sha remote_ref remote_sha; do
        if [ "$local_sha" != "0000000000000000000000000000000000000000" ]; then
            # Check if docs files are being pushed
            if git diff --name-only "$remote_sha" "$local_sha" | grep -q "^docs/content/chapter"; then
                echo "Updating chapter numbers before push..."
                "$SCRIPT_PATH"
                
                # Stage the updated files
                git add docs/content/chapter*/README.md 2>/dev/null || true
                
                # If files were updated, we need to amend or create a new commit
                if ! git diff --cached --quiet; then
                    echo "Chapter numbers updated. Files have been staged."
                    echo "You may want to commit these changes:"
                    echo "  git commit --amend --no-edit"
                    echo "  (or create a new commit if you prefer)"
                fi
                break
            fi
        fi
    done
fi

exit 0
EOF

chmod +x "$HOOKS_DIR/pre-push"
echo "Git pre-push hook installed successfully!"
echo ""
echo "The hook will automatically:"
echo "  1. Update chapter numbers from {CH} placeholders before pushing"
echo "  2. Stage the updated files"
echo "  3. Prompt you to commit if changes were made"

