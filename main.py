#!/usr/bin/env python3
"""
Content Pipeline CLI for Seneca
Scans Marcus/Galen learnings/ for tweet drafts and blog angles,
outputs daily digest to workspace/outputs/
"""

import os
import re
from datetime import datetime
from pathlib import Path
import argparse

def extract_tweets_and_angles(filepath):
    """Extract tweet drafts and blog angles from a markdown file."""
    tweets = []
    angles = []
    source_file = os.path.basename(filepath)
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    current_tweet = []
    current_angle = None
    in_tweet_block = False
    
    for i, line in enumerate(lines):
        # Detect tweet draft section
        if line.startswith('## Tweet Drafts') or line.startswith('### Tweet Drafts'):
            in_tweet_block = True
            continue
        
        # Detect tweet lines (two patterns)
        # Pattern 1: "Tweet Draft: ..." (anywhere in file)
        if 'Tweet Draft:' in line:
            tweet_text = line.replace('Tweet Draft:', '').strip()
            # Remove markdown headers if present
            tweet_text = re.sub(r'^#+\s*', '', tweet_text)
            if tweet_text:
                tweets.append({
                    'text': tweet_text,
                    'source': source_file,
                    'line': i + 1
                })
        
        # Pattern 2: List items under ## Tweet Drafts section
        elif in_tweet_block and line.strip().startswith('-'):
            tweet_text = line.strip().lstrip('-').strip()
            if tweet_text:
                tweets.append({
                    'text': tweet_text,
                    'source': source_file,
                    'line': i + 1
                })
        
        # End of tweet block
        if in_tweet_block and line.startswith('## ') and not line.startswith('## Tweet'):
            in_tweet_block = False
        
        # Detect blog angles
        if 'BLOG ANGLE:' in line:
            match = re.search(r'BLOG ANGLE:\s*(High|Medium|Low)\s*Priority\s*—\s*(.+)', line)
            if match:
                priority = match.group(1)
                title = match.group(2).strip()
                angles.append({
                    'title': title,
                    'priority': priority,
                    'source': source_file,
                    'line': i + 1
                })
    
    return tweets, angles

def scan_learnings_directory(learnings_dir):
    """Scan all markdown files in learnings/ for content."""
    all_tweets = []
    all_angles = []
    
    for filepath in Path(learnings_dir).glob('*.md'):
        tweets, angles = extract_tweets_and_angles(filepath)
        all_tweets.extend(tweets)
        all_angles.extend(angles)
    
    return all_tweets, all_angles

def generate_digest(tweets, angles, output_file):
    """Generate daily digest markdown file."""
    date_str = datetime.now().strftime('%Y-%m-%d')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Content Digest — {date_str}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        
        # Tweet Drafts Section
        if tweets:
            f.write(f"## Tweet Drafts ({len(tweets)} found)\n\n")
            for i, tweet in enumerate(tweets, 1):
                f.write(f"{i}. {tweet['text']}\n")
                f.write(f"   *Source: {tweet['source']} (line {tweet['line']})*\n\n")
        else:
            f.write("## Tweet Drafts\n\nNo tweet drafts found.\n\n")
        
        # Blog Angles Section
        if angles:
            # Sort by priority
            priority_order = {'High': 0, 'Medium': 1, 'Low': 2}
            angles_sorted = sorted(angles, key=lambda a: priority_order.get(a['priority'], 99))
            
            f.write(f"## Blog Angles ({len(angles)} found)\n\n")
            for i, angle in enumerate(angles_sorted, 1):
                f.write(f"{i}. **{angle['title']}** ({angle['priority']} Priority)\n")
                f.write(f"   *Source: {angle['source']} (line {angle['line']})*\n\n")
        else:
            f.write("## Blog Angles\n\nNo blog angles found.\n\n")
        
        # Summary
        f.write("---\n\n")
        f.write(f"**Summary:** {len(tweets)} tweet drafts, {len(angles)} blog angles\n")

def main():
    parser = argparse.ArgumentParser(description='Content Pipeline CLI for Seneca')
    parser.add_argument('--learnings-dir', 
                        default='~/.openclaw/learnings',
                        help='Path to learnings directory')
    parser.add_argument('--output-dir',
                        default='~/.openclaw/workspace/outputs',
                        help='Path to output directory')
    
    args = parser.parse_args()
    
    # Expand paths
    learnings_dir = os.path.expanduser(args.learnings_dir)
    output_dir = os.path.expanduser(args.output_dir)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename
    date_str = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(output_dir, f'content-digest-{date_str}.md')
    
    # Scan and generate
    print(f"Scanning {learnings_dir} for content...")
    tweets, angles = scan_learnings_directory(learnings_dir)
    print(f"Found {len(tweets)} tweet drafts, {len(angles)} blog angles")
    
    print(f"Generating digest at {output_file}...")
    generate_digest(tweets, angles, output_file)
    
    print(f"✅ Digest generated successfully!")

if __name__ == '__main__':
    main()
