#!/bin/bash
# Stop content-digest daily runner

PIDFILE="/tmp/content-digest-runner.pid"

if [ ! -f "$PIDFILE" ]; then
    echo "No running content-digest runner found"
    exit 0
fi

PID=$(cat "$PIDFILE")
if ps -p "$PID" > /dev/null 2>&1; then
    echo "Stopping content-digest runner (PID: $PID)..."
    kill "$PID"
    rm -f "$PIDFILE"
    echo "Stopped"
else
    echo "Stale PID file found, removing..."
    rm -f "$PIDFILE"
fi