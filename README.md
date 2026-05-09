# Content Pipeline CLI - README

Scans Marcus/Galen learnings/ for tweet drafts and blog angles,
outputs daily digest to workspace/outputs/.

## Installation

### From PyPI (recommended after publishing)
```bash
pip install squad-content-pipeline
```

### From GitHub
```bash
pip install git+https://github.com/OpenSeneca/squad-content-pipeline.git
```

### Manual installation
```bash
cd ~/.openclaw/workspace/tools/content-pipeline
python3 main.py
```

## Usage

```bash
# Generate digest (default: scans ~/.openclaw/learnings)
content-pipeline

# Custom directories
content-pipeline --learnings-dir /path/to/learnings --output-dir /path/to/outputs

# Or use python directly
python3 main.py
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
0 8 * * * content-pipeline >> /var/log/content-pipeline.log 2>&1
```

Or if using manual installation:
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
**GitHub:** https://github.com/OpenSeneca/squad-content-pipeline
**Version:** 1.2.0
**PyPI:** 📋 Built and ready for publishing (requires PyPI token)
**Last Published:** GitHub (2026-05-09)
**Output:** Daily content digests

## PyPI Publishing

The package is built and ready to publish:
```bash
# 1. Configure PyPI token (one-time setup)
./setup-pypi-token.sh <your-pypi-token>

# 2. Publish to PyPI
./deploy.sh
```

After publishing, users can install with:
```bash
pip install squad-content-pipeline
```

Last updated: 2026-05-09
