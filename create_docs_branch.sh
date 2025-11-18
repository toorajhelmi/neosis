#!/bin/bash
# Script to create a docs-only branch for GitBook

set -e

cd /Users/thelmi/source/Neosis

echo "Step 1: Adding and committing docs to main..."
git add docs/
git commit -m "Add documentation structure" || echo "Docs already committed or no changes"

echo "Step 2: Pushing main..."
git push origin main || echo "Already up to date"

echo "Step 3: Creating docs branch from main..."
git checkout -b docs 2>/dev/null || git checkout docs

echo "Step 4: Removing all files except docs from docs branch..."
# Get list of all tracked files except docs/
git ls-files | grep -v "^docs/" | while read file; do
    git rm "$file" 2>/dev/null || true
done

echo "Step 5: Restoring docs directory..."
git checkout HEAD -- docs/ 2>/dev/null || true

echo "Step 6: Adding README for docs branch..."
# README.md should already be created, just add it
git add README.md 2>/dev/null || true

echo "Step 7: Committing docs-only state..."
git commit -m "Create docs-only branch for GitBook" || echo "No changes to commit"

echo "Step 8: Pushing docs branch..."
git push -u origin docs || echo "Already pushed"

echo "Step 9: Switching back to main..."
git checkout main

echo "✓ Done! Docs branch created and pushed."
echo "  - main branch: full codebase + docs"
echo "  - docs branch: only docs/ directory"
echo ""
echo "In GitBook, connect to:"
echo "  - Repository: toorajhelmi/neosis"
echo "  - Branch: docs"
echo "  - Content root: docs/gitbook"

