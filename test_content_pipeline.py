#!/usr/bin/env python3
"""
Unit tests for content-pipeline tool
"""

import sys
import tempfile
import unittest
from pathlib import Path

# Add tools directory to path
tools_path = Path(__file__).parent.parent.parent.parent / "workspace" / "tools"
sys.path.append(str(tools_path))

from main import extract_tweet_drafts_and_blog_angles

class TestContentPipeline(unittest.TestCase):
    """Test cases for content-pipeline functionality"""
    
    def test_extract_tweet_drafts_single(self):
        """Test extraction of single tweet draft"""
        content = "## Tweet Draft\nThis is a test tweet"
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(tweets[0], "This is a test tweet")
        self.assertEqual(len(angles), 0)
    
    def test_extract_tweet_drafts_multiple(self):
        """Test extraction of multiple tweet drafts"""
        content = """## Tweet Drafts
Tweet Draft: First tweet here
Tweet Draft: Second tweet here
Tweet Draft: Third tweet here

## Blog Angle: This is a test angle"""
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        self.assertEqual(len(tweets), 3)
        self.assertEqual(tweets[0], "First tweet here")
        self.assertEqual(tweets[1], "Second tweet here")
        self.assertEqual(tweets[2], "Third tweet here")
        self.assertEqual(len(angles), 1)
        # Blog angles include the full section header with "## BLOG ANGLE:" prefix
        self.assertEqual(angles[0], "## Blog Angle: This is a test angle")
    
    def test_extract_blog_angles_multiple(self):
        """Test extraction of multiple blog angles"""
        content = """## BLOG ANGLE: First angle here
## BLOG ANGLE: Second angle here
## BLOG ANGLE: Third angle here"""
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        self.assertEqual(len(tweets), 0)
        self.assertEqual(len(angles), 3)
        # Blog angles include the full section header with "## BLOG ANGLE:" prefix
        self.assertEqual(angles[0], "## BLOG ANGLE: First angle here")
        self.assertEqual(angles[1], "## BLOG ANGLE: Second angle here")
        self.assertEqual(angles[2], "## BLOG ANGLE: Third angle here")
    
    def test_extract_both_tweet_and_blog(self):
        """Test extraction of both tweets and blog angles"""
        content = """## Tweet Drafts
Tweet 1 here

## BLOG ANGLE: Angle 1 here"""
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        self.assertEqual(len(tweets), 1)
        self.assertEqual(len(angles), 1)
        self.assertEqual(angles[0], "## BLOG ANGLE: Angle 1 here")
    
    def test_empty_content(self):
        """Test handling of empty content"""
        content = ""
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        self.assertEqual(len(tweets), 0)
        self.assertEqual(len(angles), 0)
    
    def test_content_without_patterns(self):
        """Test content without tweet/blog patterns"""
        content = "This is just regular content without any special markers."
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        self.assertEqual(len(tweets), 0)
        self.assertEqual(len(angles), 0)

if __name__ == "__main__":
    unittest.main()
