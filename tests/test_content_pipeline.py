#!/usr/bin/env python3
"""
Unit tests for content-pipeline tool
"""

import unittest
import tempfile
import os
from pathlib import Path
import sys

# Add the parent directory to path so we can import main
sys.path.insert(0, str(Path(__file__).parent.parent))

from main import extract_tweet_drafts_and_blog_angles, process_learning_file

class TestContentPipeline(unittest.TestCase):
    
    def test_extract_tweet_drafts_and_blog_angles(self):
        """Test extraction of tweet drafts and blog angles"""
        content = '''
## Tweet Drafts
Tweet Draft: This is a test tweet
Tweet Draft: Another test tweet

## BLOG ANGLE:
This is a test blog angle
'''
        
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        
        self.assertEqual(len(tweets), 2)
        self.assertEqual(tweets[0], "This is a test tweet")
        self.assertEqual(tweets[1], "Another test tweet")
        self.assertEqual(len(angles), 1)
        self.assertEqual(angles[0], "This is a test blog angle")
    
    def test_extract_tweet_drafts_case_insensitive(self):
        """Test that extraction is case insensitive"""
        content = '''
## Tweet Drafts

tweet draft: lowercase test
TWEET DRAFT: uppercase test
Tweet Draft: mixed case test

## BLOG ANGLE:
blog angle test
'''
        
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        
        self.assertEqual(len(tweets), 3)
        self.assertEqual(tweets[0], "lowercase test")
        self.assertEqual(tweets[1], "uppercase test")
        self.assertEqual(tweets[2], "mixed case test")
        self.assertEqual(len(angles), 1)
        self.assertEqual(angles[0], "blog angle test")
    
    def test_extract_no_matches(self):
        """Test extraction when no matches are found"""
        content = '''
# Some other content
## RANDOM SECTION
Some random content
'''
        
        tweets, angles = extract_tweet_drafts_and_blog_angles(content)
        
        self.assertEqual(len(tweets), 0)
        self.assertEqual(len(angles), 0)
    
    def test_process_learning_file_success(self):
        """Test processing a valid file"""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('''
## Tweet Drafts

Tweet Draft: Test tweet from temp file

## BLOG ANGLE:
Test blog angle from temp file
''')
            temp_path = f.name
        
        try:
            tweets, angles = process_learning_file(Path(temp_path))
            self.assertEqual(len(tweets), 1)
            self.assertEqual(tweets[0], "Test tweet from temp file")
            self.assertEqual(len(angles), 1)
            self.assertEqual(angles[0], "Test blog angle from temp file")
        finally:
            os.unlink(temp_path)
    
    def test_process_learning_file_not_found(self):
        """Test processing a non-existent file"""
        tweets, angles = process_learning_file(Path("/non/existent/file.md"))
        self.assertEqual(len(tweets), 0)
        self.assertEqual(len(angles), 0)
    
    def test_process_learning_file_permission_denied(self):
        """Test processing a file with no read permissions"""
        # Skip this test on systems where we can't easily test permissions
        # or if we're running as root
        if os.geteuid() == 0:
            self.skipTest("Running as root, cannot test permission denied")
            return
            
        with tempfile.NamedTemporaryFile(mode='w', suffix='.md', delete=False) as f:
            f.write('Test content')
            temp_path = f.name
        
        try:
            # Remove read permissions
            os.chmod(temp_path, 0o000)
            tweets, angles = process_learning_file(Path(temp_path))
            # Should return empty lists, not raise exception
            self.assertEqual(len(tweets), 0)
            self.assertEqual(len(angles), 0)
        finally:
            # Restore permissions so we can delete
            os.chmod(temp_path, 0o644)
            os.unlink(temp_path)

if __name__ == '__main__':
    unittest.main()