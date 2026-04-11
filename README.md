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
```

## Output

Generates daily digest: `content-digest-YYYY-MM-DD.md`

Sections:
- Tweet Drafts (extracted from "Tweet Draft:" lines or under ## Tweet Drafts)
- Blog Angles (extracted from "BLOG ANGLE: [High/Medium/Low] Priority — ...")

## Deployment

Cron job (daily at 8 AM UTC):
```bash
0 8 * * * cd ~/.openclaw/workspace/tools/content-pipeline && python3 main.py >> /var/log/content-pipeline.log 2>&1
```

## Features

- ✅ Scans all .md files in learnings directory
- ✅ Extracts tweet drafts (two patterns supported)
- ✅ Extracts blog angles with priority levels
- ✅ Sorts blog angles by priority (High > Medium > Low)
- ✅ Tracks source file and line number
- ✅ Generates timestamped daily digest

## Testing

```bash
# Run manually
python3 main.py

# Check output
cat ~/.openclaw/workspace/outputs/content-digest-$(date +%Y-%m-%d).md
```

## Status

**Tool Status:** ✅ Built, tested, deployed
**Last Run:** 2026-03-10 09:29 UTC
**Output:** 15 tweets, 84 blog angles

Last updated: 2026-03-10
