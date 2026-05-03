# Content Pipeline CLI - README

Scans Marcus/Galen learnings/ for tweet drafts and blog angles,
outputs daily digest to workspace/outputs/.

## Installation

### From GitHub (recommended)
```bash
pip install git+https://github.com/OpenSeneca/squad-content-pipeline.git
```

### From local wheel (build first)
```bash
cd ~/.openclaw/workspace/.publish-staging/content-pipeline
pyproject-build
pip install dist/squad_content_pipeline-1.0.0-py3-none-any.whl
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
**Published:** ✅ GitHub: https://github.com/OpenSeneca/squad-content-pipeline (PUBLIC)
**PyPI:** 📋 Ready for publishing - requires PyPI token
**Last Run:** 2026-05-03 10:41:59 UTC
**Output:** Daily content digests

## PyPI Publishing

To publish to PyPI:
```bash
# 1. Install twine
pipx install twine

# 2. Set PyPI token in ~/.pypirc or use --token flag
# 3. Publish
twine upload dist/squad_content_pipeline-*.tar.gz dist/squad_content_pipeline-*.whl
```

Last updated: 2026-05-03
