# Content Digest CLI - README

Scans Marcus/Galen learnings/ for tweet drafts and blog angles,
outputs daily digest to workspace/outputs/.

## Installation

### From PyPI (recommended after publishing)
```bash
pip install squad-content-digest
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
content-digest

# Custom directories
content-digest --learnings-dir /path/to/learnings --output-dir /path/to/outputs

# Filter by date
content-digest --date 2026-05-20

# Or use python directly
python3 main.py
python3 main.py --learnings-dir /path/to/learnings --output-dir /path/to/outputs
```

## Output

Generates daily digest: `content-digest-YYYY-MM-DD.md`

Sections:
- Tweet Drafts (extracted from "## Tweet Draft" sections or "Tweet Draft:" lines)
- Blog Angles (extracted from "BLOG ANGLE:" lines)

## Deployment

Cron job (daily at 8 AM UTC):
```bash
0 8 * * * content-digest >> /var/log/content-digest.log 2>&1
```

Current setup uses: `bash ~/.openclaw/scripts/run-content-digest.sh`
which runs the installed package via `content-digest` command.

## Version History

- **v1.4.1** (2026-05-20): Fix pyproject.toml entry point to use `main:main` instead of non-existent `content_pipeline.main`
- **v1.4.0** (2026-05-20): Broken release - incorrect entry point
- **v1.3.0** (2026-05-14): Initial published version

## License

MIT License - See LICENSE file
