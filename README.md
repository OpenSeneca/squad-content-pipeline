# Content Pipeline CLI - README

Scans Marcus/Galen learnings/ for tweet drafts and blog angles,
outputs daily digest to workspace/outputs/.

## Installation

```bash
cd ~/.openclaw/workspace/tools/content-pipeline
chmod +x main.py
```

## Usage

```bash
# Generate digest (default: scans ~/.openclaw/learnings)
python3 main.py

# Custom directories
python3 main.py --learnings-dir /path/to/learnings --output-dir /path/to/outputs

# Send digest to Telegram (requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in ~/.config/openclaw/secrets.env)
python3 main.py --telegram
```

## Output

Generates daily digest: `content-digest-YYYY-MM-DD.md`

Sections:
- Tweet Drafts (extracted from "Tweet Draft:" lines or under ## Tweet Drafts)
- Blog Angles (extracted from "BLOG ANGLE: [High/Medium/Low] Priority — ...")

## Deployment

Cron job (daily at 8 AM UTC):
```bash
# Without Telegram notification
0 8 * * * cd ~/.openclaw/workspace/tools/content-pipeline && python3 main.py >> /var/log/content-pipeline.log 2>&1

# With Telegram notification
0 8 * * * cd ~/.openclaw/workspace/tools/content-pipeline && python3 main.py --telegram >> /var/log/content-pipeline.log 2>&1
```

## Features

- ✅ Scans all .md files in learnings directory
- ✅ Extracts tweet drafts (two patterns supported)
- ✅ Extracts blog angles with priority levels
- ✅ Sorts blog angles by priority (High > Medium > Low)
- ✅ Tracks source file and line number
- ✅ Generates timestamped daily digest
- ✅ **Telegram Notifications**: Sends digest to Telegram bot when `--telegram` flag is used (requires TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID in ~/.config/openclaw/secrets.env)

## Testing

```bash
# Run manually
python3 main.py

# Check output
cat ~/.openclaw/workspace/outputs/content-digest-$(date +%Y-%m-%d).md
```

## Status

**Tool Status:** ✅ Built, tested, deployed, Telegram notification support added
**Last Run:** 2026-03-16 15:55 UTC
**Output:** 107 learning files processed, 14 tweets, 0 blog angles

## Telegram Notifications

The content pipeline now supports sending digest notifications to Telegram via bot.

### Setup

Add to `~/.config/openclaw/secrets.env`:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
TELEGRAM_CHAT_ID=your_chat_id_here
```

### Usage

```bash
# Generate and send digest to Telegram
python3 main.py --telegram

# Generate digest but skip Telegram notification
python3 main.py --no-telegram
```

The notification includes:
- Date of digest
- Number of tweets found
- Number of blog angles found
- Output file path
- Digest status

Last updated: 2026-03-16
