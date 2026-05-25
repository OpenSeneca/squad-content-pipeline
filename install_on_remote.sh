#!/bin/bash
# Install content-digest on a remote agent
# Usage: ./install_on_remote.sh <agent-host>

if [ -z "$1" ]; then
    echo "Usage: $0 <agent-host>"
    echo "Example: $0 marcus-squad"
    exit 1
fi

AGENT_HOST="$1"
REMOTE_DIR="~/.openclaw/workspace/tools/content-pipeline"

echo "Installing content-digest on $AGENT_HOST..."

# Copy the tool directory
ssh "$AGENT_HOST" "mkdir -p $REMOTE_DIR"
scp main.py daily_runner.py start_daily_runner.sh stop_daily_runner.sh SELF_SCHEDULER.md "$AGENT_HOST:$REMOTE_DIR/"

# Make scripts executable
ssh "$AGENT_HOST" "chmod +x $REMOTE_DIR/start_daily_runner.sh $REMOTE_DIR/stop_daily_runner.sh"

# Start the runner
ssh "$AGENT_HOST" "bash $REMOTE_DIR/start_daily_runner.sh"

echo "Content-digest installed and started on $AGENT_HOST"