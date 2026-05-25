#!/usr/bin/env python3
"""
Content Digest Daily Runner
Runs content-digest every 24 hours at 8 AM UTC
No cron required - uses sleep loop
"""

import subprocess
import time
import sys
from datetime import datetime, timedelta
import os

LOG_DIR = os.path.expanduser("~/.openclaw/workspace/memory")
OUTPUT_DIR = os.path.expanduser("~/.openclaw/workspace/outputs")

def log(message: str):
    """Log to daily memory file"""
    os.makedirs(LOG_DIR, exist_ok=True)
    now = datetime.utcnow()
    log_file = os.path.join(LOG_DIR, now.strftime("%Y-%m-%d.md"))
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S UTC")
    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {message}\n")
    print(f"[{timestamp}] {message}")

def wait_until_target(target_time: datetime):
    """Sleep until target time"""
    now = datetime.utcnow()
    if target_time < now:
        target_time += timedelta(days=1)
    
    delta = target_time - now
    seconds = delta.total_seconds()
    log(f"Waiting {delta} until next run at {target_time}")
    time.sleep(seconds)

def run_content_digest():
    """Run the content-digest script"""
    script_path = os.path.join(os.path.dirname(__file__), "main.py")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            capture_output=True,
            text=True,
            timeout=300
        )
        
        if result.returncode == 0:
            log(f"Content-digest completed: {result.stdout.strip()}")
            return True
        else:
            log(f"ERROR: Content-digest failed (exit {result.returncode}): {result.stderr}")
            return False
    except Exception as e:
        log(f"ERROR: Content-digest crashed: {e}")
        return False

def main():
    """Main loop - run daily at 8 AM UTC"""
    log("Content-digest daily runner started")
    
    while True:
        # Run content-digest
        run_content_digest()
        
        # Calculate next run time (8 AM UTC tomorrow)
        now = datetime.utcnow()
        next_run = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0, microsecond=0)
        
        # Wait until next run
        wait_until_target(next_run)

if __name__ == "__main__":
    main()