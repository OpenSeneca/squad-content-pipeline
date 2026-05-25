#!/bin/bash
# Publish content-digest to PyPI
# Usage: bash publish-to-pypi.sh [test|production]

set -e

# Default to test PyPI
PYPI_REPO=${1:-test}
VERSION=$(grep '^version = ' pyproject.toml | head -1 | cut -d'"' -f2)

echo "=== Publishing squad-content-digest v${VERSION} to ${PYPI_REPO} PyPI ==="

# Build the package
echo "Building package..."
python3 -m build

if [ "$PYPI_REPO" = "test" ]; then
    echo "Publishing to Test PyPI..."
    python3 -m twine upload --repository testpypi dist/squad_content_digest-${VERSION}*
else
    echo "Publishing to Production PyPI..."
    python3 -m twine upload dist/squad_content_digest-${VERSION}*
fi

echo "✅ Published successfully!"
echo ""
echo "Install with:"
if [ "$PYPI_REPO" = "test" ]; then
    echo "  pip install --index-url https://test.pypi.org/simple/ squad-content-digest"
else
    echo "  pip install squad-content-digest"
fi