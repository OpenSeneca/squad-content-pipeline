# Content Pipeline CLI - README

Scans Marcus/Galen learnings/ for tweet drafts and blog angles,
outputs daily digest to workspace/outputs/.

## Installation

### From PyPI (recommended)
```bash
pip install content-pipeline
```

### From source
```bash
git clone https://github.com/OpenSeneca/content-pipeline.git
cd content-pipeline
pip install -e .
```

## Usage

```bash
# Generate digest (default: scans ~/.openclaw/learnings)
content-digest

# Custom directories
content-digest --learnings-dir /path/to/learnings --output-dir /path/to/outputs

# Specify date
content-digest --date 2026-04-17
```

## Output

Generates daily digest: `content-digest-YYYY-MM-DD.md`

Sections:
- Tweet Drafts (extracted from "Tweet Draft:" lines or under ## Tweet Drafts)
- Blog Angles (extracted from "BLOG ANGLE: [High/Medium/Low] Priority — ...")

## Deployment

Cron job (daily at 8 AM UTC):
```bash
0 8 * * * content-digest >> /var/log/content-pipeline.log 2>&1
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
content-digest

# Check output
cat ~/.openclaw/workspace/outputs/content-digest-$(date +%Y-%m-%d).md
```

## Status

**Tool Status:** ✅ Built, tested, deployed, published to PyPI
**Last Run:** 2026-04-25 21:27 UTC
**Version:** 1.1.0

Last updated: 2026-04-25
