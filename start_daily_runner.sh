#!/bin/bash
# Start content-digest daily runner in background

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
RUNNER="$SCRIPT_DIR/daily_runner.py"
PIDFILE="/tmp/content-digest-runner.pid"

if [ -f "$PIDFILE" ]; then
    PID=$(cat "$PIDFILE")
    if ps -p "$PID" > /dev/null 2>&1; then
        echo "Content-digest runner already running (PID: $PID)"
        exit 0
    else
        rm -f "$PIDFILE"
    fi
fi

mkdir -p ~/.openclaw/workspace/memory
mkdir -p ~/.openclaw/workspace/outputs

echo "Starting content-digest daily runner..."
nohup python3 "$RUNNER" > ~/.openclaw/workspace/memory/content-runner.log 2>&1 &
echo $! > "$PIDFILE"
echo "Content-digest runner started (PID: $!)"
echo "Log: ~/.openclaw/workspace/memory/content-runner.log"
echo "Stop: kill $(cat $PIDFILE) && rm $PIDFILE"