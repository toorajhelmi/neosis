#!/bin/bash
# Build script for GitBook documentation

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DOCS_DIR="$(dirname "$SCRIPT_DIR")"
BUILD_DIR="$DOCS_DIR/_build/gitbook"

echo "Building GitBook documentation..."

# Create build directory
mkdir -p "$BUILD_DIR"

# Copy content
echo "Copying content files..."
cp -r "$DOCS_DIR/content" "$BUILD_DIR/"
cp -r "$DOCS_DIR/gitbook"/* "$BUILD_DIR/"
cp -r "$DOCS_DIR/assets" "$BUILD_DIR/" 2>/dev/null || true

# Copy README
cp "$DOCS_DIR/README.md" "$BUILD_DIR/"

# Check if gitbook-cli is installed
if ! command -v gitbook &> /dev/null; then
    echo "Warning: gitbook-cli not found. Install with: npm install -g gitbook-cli"
    echo "Output prepared in: $BUILD_DIR"
    echo "You can manually run 'gitbook build' or 'gitbook serve' in that directory"
else
    cd "$BUILD_DIR"
    echo "Installing GitBook plugins..."
    gitbook install
    
    echo "Building GitBook..."
    gitbook build . "$BUILD_DIR/_book"
    
    echo "✓ GitBook documentation built successfully!"
    echo "Output: $BUILD_DIR/_book"
    echo "To serve locally: cd $BUILD_DIR && gitbook serve"
fi

