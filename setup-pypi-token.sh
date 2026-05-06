#!/bin/bash
# setup-pypi-token.sh
# Helper script to configure PyPI token for publishing

set -euo pipefail

echo "Setting up PyPI token for squad-content-pipeline"

# Check if token is provided as argument
if [ $# -eq 0 ]; then
    echo "Please provide your PyPI token as an argument:"
    echo "  $0 <your-pypi-token>"
    echo ""
    echo "Alternatively, you can set the token manually in ~/.pypirc or via TWINE_USERNAME/__token__ and TWINE_PASSWORD environment variables."
    exit 1
fi

TOKEN=$1

# Configure .pypirc
PYPIRC_PATH="$HOME/.pypirc"

if [ -f "$PYPIRC_PATH" ]; then
    echo "Backing up existing $PYPIRC_PATH to $PYPIRC_PATH.backup"
    cp "$PYPIRC_PATH" "$PYPIRC_PATH.backup"
fi

cat > "$PYPIRC_PATH" << EOF
[distutils]
index-servers =
    pypi

[pypi]
repository = https://upload.pypi.org/legacy/
username = __token__
password = $TOKEN
EOF

chmod 600 "$PYPIRC_PATH"

echo "PyPI token configured in $PYPIRC_PATH"
echo "You can now run ./deploy.sh to publish the package"
echo ""
echo "Note: Keep your token secure. Do not share or commit this file."