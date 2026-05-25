# Content Digest Self-Scheduler

Background runner for content-digest that doesn't require cron access. Runs daily at 8 AM UTC.

## Files

- `daily_runner.py` - Main runner loop
- `start_daily_runner.sh` - Start runner in background
- `stop_daily_runner.sh` - Stop background runner
- `content-runner.log` - Runtime logs (in workspace/memory/)

## Usage

Start the runner:
```bash
bash start_daily_runner.sh
```

Stop the runner:
```bash
bash stop_daily_runner.sh
```

Check status:
```bash
ps aux | grep daily_runner
```

View logs:
```bash
tail -f ~/.openclaw/workspace/memory/content-runner.log
```

## How it works

1. Runner starts in background via nohup
2. Immediately runs content-digest
3. Waits until 8 AM UTC next day
4. Repeats forever
5. Logs all activity to workspace/memory/

## Auto-restart

If runner crashes, manually restart with start_daily_runner.sh. For persistence, add to ~/.bashrc or systemd user service.