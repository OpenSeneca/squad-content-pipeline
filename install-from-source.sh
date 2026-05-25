#!/bin/bash
# Install content-digest CLI directly from GitHub source
# No PyPI required - installs as editable package

set -e

echo "=== Installing content-digest CLI from GitHub ==="

# Clone or update the repo
if [ -d "$HOME/.openclaw/workspace/tools/content-pipeline" ]; then
    echo "Updating existing repository..."
    cd "$HOME/.openclaw/workspace/tools/content-pipeline"
    git pull origin main
else
    echo "Cloning repository..."
    git clone https://github.com/OpenSeneca/squad-content-pipeline.git \
        "$HOME/.openclaw/workspace/tools/content-pipeline"
    cd "$HOME/.openclaw/workspace/tools/content-pipeline"
fi

# Install as editable package
echo "Installing package..."
pip3 install -e . --user

# Verify installation
if command -v content-digest &> /dev/null; then
    echo "✅ content-digest installed successfully!"
    echo ""
    echo "Usage:"
    echo "  content-digest --help"
    echo ""
    echo "To start daily runner:"
    echo "  bash ~/.openclaw/workspace/tools/content-pipeline/start_daily_runner.sh"
else
    echo "❌ Installation failed"
    exit 1
fi