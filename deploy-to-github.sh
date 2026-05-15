#!/usr/bin/env bash
# Deployment helper for Content Pipeline CLI
# Usage: ./deploy-to-github.sh [version]

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

VERSION=${1:-$(grep 'version = ' pyproject.toml | head -1 | cut -d'"' -f2)}

echo "Deploying Content Pipeline CLI v${VERSION} to GitHub..."

# Clean and build
echo "Building distribution packages..."
rm -rf dist/ build/ *.egg-info squad_content_digest.egg-info
python -m build

# Create and push git tag
echo "Creating git tag v${VERSION}..."
git tag -a "v${VERSION}" -m "Release v${VERSION}" || echo "Tag v${VERSION} already exists"
git push origin main --tags

echo "Done! Create a GitHub release at:"
echo "https://github.com/OpenSeneca/squad-content-pipeline/releases/new?tag=v${VERSION}"
echo ""
echo "Upload the following files from dist/:"
ls -lh dist/