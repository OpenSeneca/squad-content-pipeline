#!/usr/bin/env python3
"""
Content Pipeline CLI for Seneca
Scans Marcus/Galen learnings/ for tweet drafts and blog angles,
outputs daily digest to workspace/outputs/
Updated to handle Marcus/Galen format:
- ## Tweet Draft (singular) followed by paragraph
- ## Blog Angle followed by **BLOG ANGLE: Priority — Title**
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
    in_blog_angle = False
    
    for i, line in enumerate(lines):
        # Detect Marcus/Galen format: ## Tweet Draft (singular)
        if re.match(r'^##\s*Tweet Draft\s*$', line):
            # Save previous tweet if exists (start of new tweet block)
            if in_tweet_block and current_tweet:
                tweet_text = ' '.join(current_tweet)
                if tweet_text.strip():
                    tweets.append({
                        'text': tweet_text,
                        'source': source_file,
                        'line': i + 1 - len(current_tweet)
                    })
                current_tweet = []
            in_tweet_block = True
            in_blog_angle = False
            continue
        
        # Detect legacy format: ## Tweet Drafts (plural)
        if re.match(r'^##\s*Tweet Drafts\s*$', line) or re.match(r'^###\s*Tweet Drafts\s*$', line):
            in_tweet_block = True
            in_blog_angle = False
            continue
        
        # Detect Marcus/Galen format: ## Blog Angle
        if re.match(r'^##\s*Blog Angle\s*$', line):
            # Save any accumulated tweet before switching to blog angle mode
            if in_tweet_block and current_tweet:
                tweet_text = ' '.join(current_tweet)
                if tweet_text.strip():
                    tweets.append({
                        'text': tweet_text,
                        'source': source_file,
                        'line': i + 1 - len(current_tweet)
                    })
                current_tweet = []
            in_blog_angle = True
            in_tweet_block = False
            current_angle = None
            continue
        
        # Detect legacy format: Tweet Draft: prefix
        if 'Tweet Draft:' in line:
            tweet_text = line.replace('Tweet Draft:', '').strip()
            tweet_text = re.sub(r'^#+\s*', '', tweet_text)
            if tweet_text:
                tweets.append({
                    'text': tweet_text,
                    'source': source_file,
                    'line': i + 1
                })
        
        # Pattern 2: List items under ## Tweet Drafts section (legacy)
        elif in_tweet_block and line.strip().startswith('-'):
            tweet_text = line.strip().lstrip('-').strip()
            if tweet_text:
                tweets.append({
                    'text': tweet_text,
                    'source': source_file,
                    'line': i + 1
                })
        
        # Pattern 3: Marcus/Galen Tweet Draft (paragraph under ## Tweet Draft)
        elif in_tweet_block and line.strip() and not line.startswith('#'):
            # Accumulate tweet text until we hit another section
            current_tweet.append(line.strip())
        
        # Detect Marcus/Galen format: **BLOG ANGLE: Title** (no priority field)
        if in_blog_angle and '**BLOG ANGLE:' in line:
            match = re.search(r'\*\*BLOG ANGLE:\s*(.+)\*\*', line)
            if match:
                title = match.group(1).strip()
                # Default to High priority for squad format
                angles.append({
                    'title': title,
                    'priority': 'High',
                    'source': source_file,
                    'line': i + 1
                })
        
        # Detect legacy BLOG ANGLE format with priority field
        elif in_blog_angle and 'BLOG ANGLE:' in line and '**BLOG ANGLE:' not in line:
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
        
        # Detect legacy format with bold markers and priority (old squad format)
        elif in_blog_angle and '**BLOG ANGLE:' in line and 'Priority —' in line:
            match = re.search(r'\*\*BLOG ANGLE:\s*(High|Medium|Low)\s*Priority\s*—\s*(.+)\*\*', line)
            if match:
                priority = match.group(1)
                title = match.group(2).strip()
                angles.append({
                    'title': title,
                    'priority': priority,
                    'source': source_file,
                    'line': i + 1
                })
        
        # End of tweet block - save accumulated tweet
        if in_tweet_block and line.startswith('## ') and not re.match(r'^##\s*Tweet', line):
            if current_tweet:
                tweet_text = ' '.join(current_tweet)
                if tweet_text.strip():
                    tweets.append({
                        'text': tweet_text,
                        'source': source_file,
                        'line': i + 1 - len(current_tweet)
                    })
                current_tweet = []
            in_tweet_block = False
        
        # End of blog angle block
        if in_blog_angle and line.startswith('## ') and not re.match(r'^##\s*Blog Angle', line):
            in_blog_angle = False
    
    # Save any accumulated tweet at end of file
    if in_tweet_block and current_tweet:
        tweet_text = ' '.join(current_tweet)
        if tweet_text.strip():
            tweets.append({
                'text': tweet_text,
                'source': source_file,
                'line': i + 1 - len(current_tweet)
            })
    
    return tweets, angles

def scan_learnings_directory(learnings_dir, target_date=None):
    """Scan markdown files in learnings/ for content. If target_date is provided, only scan files from that date."""
    all_tweets = []
    all_angles = []
    
    for filepath in Path(learnings_dir).glob('*.md'):
        # Filter by date if specified
        if target_date:
            # Check if filename starts with the target date
            filename = os.path.basename(filepath)
            if not filename.startswith(target_date):
                continue
        
        tweets, angles = extract_tweets_and_angles(filepath)
        all_tweets.extend(tweets)
        all_angles.extend(angles)
    
    return all_tweets, all_angles

def generate_digest(tweets, angles, output_file):
    """Generate daily digest markdown file."""
    # Extract date from output_file filename (format: content-digest-YYYY-MM-DD.md)
    basename = os.path.basename(output_file)
    match = re.search(r'content-digest-(\d{4}-\d{2}-\d{2})', basename)
    if match:
        date_str = match.group(1)
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Content Digest — {date_str}\n\n")
        f.write(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}\n\n")
        
        # Key Themes Section (from Marcus research)
        f.write("## Key Themes\n\n")
        f.write("1. **Agentic stack crystallizing into 5 layers** - Orchestration, memory, tools, runtime, deployment\n")
        f.write("2. **Supply chain security** - WordPress plugins + NPM + Mercor vulnerabilities\n")
        f.write("3. **Inference cost revolution (I-DLM)** - Dramatic cost reductions across providers\n")
        f.write("4. **Multi-provider resilience post-Anthropic OAuth** - Enterprises avoiding single-provider lock-in\n\n")
        
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
        
        # Funding Correction Note (from Seneca inbox)
        f.write("## Funding Data Correction\n\n")
        f.write("**VERIFIED:** $5.8M total funding across verification builders\n")
        f.write("- OpenGradient: $0.5M\n")
        f.write("- Inference Labs: $0.3M\n\n")
        f.write("**NOT verification builders:**\n")
        f.write("- Guildhawk: AI translation (NOT verification)\n")
        f.write("- Bigspin AI: Stanford research project (NOT funded builder)\n\n")
        
        # Summary
        f.write("---\n\n")
        f.write(f"**Summary:** {len(tweets)} tweet drafts, {len(angles)} blog angles\n")

def main():
    parser = argparse.ArgumentParser(description='Content Pipeline CLI for Seneca')
    parser.add_argument('--learnings-dir',
                        default='~/.openclaw/learnings',
                        help='Path to learnings directory')
    parser.add_argument('--output-dir',
                        default='~/.openclaw/workspace/intel',
                        help='Path to output directory (default: intel/)')
    parser.add_argument('--date',
                        default=None,
                        help='Filter learnings files by date (YYYY-MM-DD), default scans all files')
    
    args = parser.parse_args()
    
    # Expand paths
    learnings_dir = os.path.expanduser(args.learnings_dir)
    output_dir = os.path.expanduser(args.output_dir)
    
    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate output filename
    if args.date:
        date_str = args.date
    else:
        date_str = datetime.now().strftime('%Y-%m-%d')
    output_file = os.path.join(output_dir, f'content-digest-{date_str}.md')
    
    # Scan and generate
    if args.date:
        print(f"Scanning {learnings_dir} for content from {args.date}...")
        tweets, angles = scan_learnings_directory(learnings_dir, target_date=args.date)
    else:
        print(f"Scanning {learnings_dir} for content (all dates)...")
        tweets, angles = scan_learnings_directory(learnings_dir)
    print(f"Found {len(tweets)} tweet drafts, {len(angles)} blog angles")
    
    print(f"Generating digest at {output_file}...")
    generate_digest(tweets, angles, output_file)
    
    print(f"✅ Digest generated successfully!")

if __name__ == '__main__':
    main()
