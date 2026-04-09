#!/usr/bin/env python3
"""
Content Pipeline CLI for Seneca

Scans Marcus/Galen learnings/ for tweet drafts and blog angles,
outputs daily digest to workspace/outputs/content-digest-YYYY-MM-DD.md

Usage:
    python main.py [--date YYYY-MM-DD] [--agents AGENT...] [--preview]

Priority: PRIORITY 1 from HEARTBEAT.md
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple


class ContentPipeline:
    """Extract tweet drafts and blog angles from agent learnings"""

    def __init__(self, learnings_base: str = None, output_base: str = None):
        """
        Initialize content pipeline

        Args:
            learnings_base: Base path for agent learnings
            output_base: Base path for output files
        """
        self.learnings_base = Path(learnings_base) if learnings_base else Path.home() / ".openclaw" / "learnings"
        self.output_base = Path(output_base) if output_base else Path.home() / ".openclaw" / "workspace" / "outputs"

        # Agents to scan (Marcus and Galen primarily produce content)
        self.agents = ["marcus", "galen"]

        # Patterns to extract
        self.tweet_draft_pattern = re.compile(r"##\s*Tweet Draft\s*\n+(.*?)(?=##|\Z)", re.IGNORECASE | re.DOTALL)
        self.blog_angle_pattern = re.compile(r"BLOG ANGLE:\s*(.*?)(?=##|\n\n\n|\Z)", re.IGNORECASE | re.DOTALL)
        self.blog_angle_header_pattern = re.compile(r"##\s*Blog Angle\s*\n+(.*?)(?=##|\Z)", re.IGNORECASE | re.DOTALL)

    def scan_learnings_directory(self, date_filter: str = None) -> List[Path]:
        """
        Scan learnings directory for markdown files

        Args:
            date_filter: Optional date string to filter files (YYYY-MM-DD format)

        Returns:
            List of markdown file paths
        """
        if not self.learnings_base.exists():
            print(f"⚠️  Learnings directory not found: {self.learnings_base}")
            return []

        # Get all markdown files, excluding content-digest files (avoid scanning own output)
        md_files = [
            f for f in self.learnings_base.glob("*.md")
            if not f.name.startswith("content-digest-")
            and not f.name.startswith("squad-digest-")
            and not f.name.startswith("daily-quality-report-")
        ]

        # Filter by date if specified (check both filename and modification time)
        if date_filter:
            try:
                from datetime import datetime
                date_obj = datetime.strptime(date_filter, "%Y-%m-%d").date()
                md_files = [
                    f for f in md_files
                    if date_filter in f.name or
                    datetime.fromtimestamp(f.stat().st_mtime).date() == date_obj
                ]
            except ValueError:
                print(f"⚠️  Invalid date format: {date_filter}. Use YYYY-MM-DD")
                return []

        # Sort by modification time (newest first)
        md_files.sort(key=lambda p: p.stat().st_mtime, reverse=True)

        return md_files

    def extract_from_file(self, file_path: Path) -> Dict[str, List[str]]:
        """
        Extract tweet drafts and blog angles from a file

        Args:
            file_path: Path to markdown file

        Returns:
            Dictionary with 'tweet_drafts' and 'blog_angles' lists
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"⚠️  Failed to read {file_path}: {e}")
            return {"tweet_drafts": [], "blog_angles": []}

        results = {
            "tweet_drafts": [],
            "blog_angles": [],
            "source": file_path.name
        }

        # Extract tweet drafts
        tweet_matches = self.tweet_draft_pattern.findall(content)
        for match in tweet_matches:
            draft = match.strip()
            if draft:
                results["tweet_drafts"].append(draft)

        # Extract blog angles
        blog_matches = self.blog_angle_pattern.findall(content)
        for match in blog_matches:
            angle = match.strip()
            if angle:
                results["blog_angles"].append(angle)

        # Also extract ## Blog Angle headers
        blog_header_matches = self.blog_angle_header_pattern.findall(content)
        for match in blog_header_matches:
            angle = match.strip()
            if angle and angle not in results["blog_angles"]:
                results["blog_angles"].append(angle)

        return results

    def scan_all_files(self, date_filter: str = None) -> Dict[str, Dict]:
        """
        Scan all learnings files and extract content

        Args:
            date_filter: Optional date string to filter files

        Returns:
            Dictionary mapping file names to extracted content
        """
        files = self.scan_learnings_directory(date_filter)

        if not files:
            print("⚠️  No markdown files found in learnings directory")
            return {}

        print(f"📂 Scanning {len(files)} file(s) from learnings/...")

        all_results = {}

        for file_path in files:
            results = self.extract_from_file(file_path)
            if results["tweet_drafts"] or results["blog_angles"]:
                all_results[file_path.name] = results

        return all_results

    def generate_markdown_digest(self, all_results: Dict[str, Dict]) -> str:
        """
        Generate markdown digest from extracted content

        Args:
            all_results: Results from scan_all_files()

        Returns:
            Markdown digest content
        """
        date = datetime.now().strftime("%Y-%m-%d")

        # Collect all tweets and blog angles
        all_tweets = []
        all_angles = []

        for filename, results in all_results.items():
            all_tweets.extend([f"({filename}) {tweet}" for tweet in results["tweet_drafts"]])
            all_angles.extend([f"({filename}) {angle}" for angle in results["blog_angles"]])

        # Count
        total_tweets = len(all_tweets)
        total_angles = len(all_angles)

        markdown = f"""# Content Digest — {date}

**Sources Scanned:** {len(all_results)} learning(s)
**Total Tweet Drafts:** {total_tweets}
**Total Blog Angles:** {total_angles}

---

"""

        # Tweet Drafts section
        if all_tweets:
            markdown += f"## Tweet Drafts ({total_tweets})\n\n"
            for i, tweet in enumerate(all_tweets, 1):
                markdown += f"{i}. {tweet}\n\n"
        else:
            markdown += "## Tweet Drafts (0)\n\nNo tweet drafts found.\n\n"

        markdown += "---\n\n"

        # Blog Angles section
        if all_angles:
            markdown += f"## Blog Angles ({total_angles})\n\n"
            for i, angle in enumerate(all_angles, 1):
                markdown += f"{i}. {angle}\n\n"
        else:
            markdown += "## Blog Angles (0)\n\nNo blog angles found.\n\n"

        markdown += f"""
---
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")}
**Content Source:** Marcus/Galen learnings/
**Status:** Ready for Seneca review
"""

        return markdown

    def save_digest(self, markdown_content: str, date: str = None) -> str:
        """
        Save digest to output file

        Args:
            markdown_content: Markdown digest content
            date: Date string (default: today)

        Returns:
            Output file path
        """
        if not date:
            date = datetime.now().strftime("%Y-%m-%d")

        # Create output directory if needed
        self.output_base.mkdir(parents=True, exist_ok=True)

        # Generate output filename
        output_file = self.output_base / f"content-digest-{date}.md"

        # Write digest
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)

        return str(output_file)


def main():
    """CLI interface for content pipeline"""
    parser = argparse.ArgumentParser(
        description="Content Pipeline CLI for Seneca - Extract tweet drafts and blog angles from learnings"
    )
    parser.add_argument("--date", help="Date filter (YYYY-MM-DD) - scans only files matching this date")
    parser.add_argument("--agents", nargs='+', help="Specific agents to scan (default: all)")
    parser.add_argument("--preview", action="store_true", help="Preview digest without saving")
    parser.add_argument("--output", help="Output file path (default: outputs/content-digest-YYYY-MM-DD.md)")
    parser.add_argument("--learnings-path", help="Path to learnings directory")

    args = parser.parse_args()

    # Initialize pipeline
    pipeline = ContentPipeline(
        learnings_base=args.learnings_path,
        output_base=str(Path(args.output).parent) if args.output else None
    )

    # Scan learnings
    all_results = pipeline.scan_all_files(date_filter=args.date)

    # Generate markdown digest (even if empty)
    if not all_results:
        # Create empty digest for today
        if args.preview:
            print("# Content Digest — Empty\n\n**No new content found for this date.**")
        else:
            output_path = pipeline.save_digest(
                "# Content Digest — Empty\n\n**No new content found for this date.**",
                date=args.date
            )
            print(f"✅ Content digest saved to: {output_path}")
        sys.exit(0)

    # Generate markdown digest
    markdown = pipeline.generate_markdown_digest(all_results)

    # Preview or save
    if args.preview:
        print(markdown)
    else:
        output_path = pipeline.save_digest(markdown, date=args.date)
        print(f"✅ Content digest saved to: {output_path}")

        # Print summary
        total_tweets = sum(len(r["tweet_drafts"]) for r in all_results.values())
        total_angles = sum(len(r["blog_angles"]) for r in all_results.values())

        print(f"\n📊 Summary:")
        print(f"  Sources scanned: {len(all_results)}")
        print(f"  Tweet drafts: {total_tweets}")
        print(f"  Blog angles: {total_angles}")
        print(f"  Output: {output_path}")


if __name__ == "__main__":
    main()
