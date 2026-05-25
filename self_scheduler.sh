#!/bin/bash
# Content Digest Self-Scheduler
# Runs content-digest and schedules next run via atd (no cron access required)

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MAIN_PY="$SCRIPT_DIR/main.py"
LOG_DIR="$HOME/.openclaw/workspace/memory"
LOG_FILE="$LOG_DIR/$(date +%Y-%m-%d).md"
OUTPUT_DIR="$HOME/.openclaw/workspace/outputs"

mkdir -p "$LOG_DIR" "$OUTPUT_DIR"

echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] Running content-digest..." >> "$LOG_FILE"

# Run content-digest
if python3 "$MAIN_PY" --daily >> "$LOG_FILE" 2>&1; then
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] Content-digest completed successfully" >> "$LOG_FILE"
    
    # Schedule next run (8 AM UTC tomorrow)
    NEXT_RUN=$(date -u -d "tomorrow 08:00" +"%Y-%m-%d %H:%M:%S")
    echo "$0" | at -t "$(date -d "tomorrow 08:00" +"%Y%m%d%H%M")" 2>/dev/null || echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] Warning: atd not available, manual run required" >> "$LOG_FILE"
    
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] Next run scheduled for $NEXT_RUN UTC" >> "$LOG_FILE"
    exit 0
else
    echo "[$(date -u +"%Y-%m-%d %H:%M:%S UTC")] ERROR: Content-digest failed" >> "$LOG_FILE"
    exit 1
fi