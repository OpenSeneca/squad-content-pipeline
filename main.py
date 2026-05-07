#!/usr/bin/env python3
"""
Content Pipeline CLI for Seneca.
Scans Marcus and Galen learnings for tweet drafts and blog angles,
outputs daily digest to ~/workspace/outputs/content-digest-YYYY-MM-DD.md
"""
import os
import re
from datetime import datetime
from pathlib import Path

LEARNINGS_DIR = Path.home() / ".openclaw" / "learnings"
OUTPUT_DIR = Path.home() / ".openclaw" / "workspace" / "outputs"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

def extract_tweet_drafts_and_blog_angles():
    tweet_drafts = []
    blog_angles = []
    
    # Scan all .md files in learnings directory
    for md_file in LEARNINGS_DIR.glob("*.md"):
        try:
            content = md_file.read_text(encoding='utf-8')
            lines = content.splitlines()
            
            i = 0
            while i < len(lines):
                line = lines[i]
                # Look for Tweet Draft marker
                if line.strip().startswith("## Tweet Draft"):
                    # Next non-empty line is the tweet draft
                    j = i + 1
                    while j < len(lines) and not lines[j].strip():
                        j += 1
                    if j < len(lines):
                        tweet_drafts.append(lines[j].strip())
                    i = j  # Skip to next line after the draft
                # Look for Blog Angle marker
                elif "BLOG ANGLE:" in line:
                    # Extract everything after the colon
                    angle = line.split("BLOG ANGLE:", 1)[1].strip()
                    if angle:
                        blog_angles.append(angle)
                i += 1
        except Exception as e:
            print(f"Error reading {md_file}: {e}")
    
    return tweet_drafts, blog_angles

def main():
    tweet_drafts, blog_angles = extract_tweet_drafts_and_blog_angles()
    today = datetime.now().strftime("%Y-%m-%d")
    output_file = OUTPUT_DIR / f"content-digest-{today}.md"
    
    with output_file.open('w', encoding='utf-8') as f:
        f.write(f"# Content Digest for {today}\n\n")
        
        f.write("## Tweet Drafts\n")
        if tweet_drafts:
            for i, draft in enumerate(tweet_drafts, 1):
                f.write(f"{i}. {draft}\n")
        else:
            f.write("No tweet drafts found.\n")
        f.write("\n")
        
        f.write("## Blog Angles\n")
        if blog_angles:
            for i, angle in enumerate(blog_angles, 1):
                f.write(f"{i}. {angle}\n")
        else:
            f.write("No blog angles found.\n")
        f.write("\n")
    
    print(f"Content digest written to {output_file}")

if __name__ == "__main__":
    main()