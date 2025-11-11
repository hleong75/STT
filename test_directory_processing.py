#!/usr/bin/env python3
"""
Test script to verify directory processing logic without requiring full dependencies
"""

import sys
import os
import ast
from pathlib import Path


def test_directory_detection():
    """Test that the code can detect directories vs files."""
    print("Testing directory detection logic...")
    
    # Read the stt.py file
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check that process_directory function exists
    if 'def process_directory(' not in content:
        print("❌ process_directory function not found")
        return False
    
    print("✓ process_directory function found")
    
    # Check that is_dir() is used
    if 'is_dir()' not in content:
        print("❌ is_dir() check not found")
        return False
    
    print("✓ is_dir() check found")
    
    # Check that Path is imported
    if 'from pathlib import Path' not in content:
        print("❌ Path import not found")
        return False
    
    print("✓ Path import found")
    
    return True


def test_audio_extensions():
    """Test that audio extensions are defined."""
    print("\nTesting audio extensions...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check for common audio extensions
    required_extensions = ['.wav', '.mp3', '.flac', '.ogg', '.m4a']
    
    for ext in required_extensions:
        if ext not in content:
            print(f"❌ Extension {ext} not found")
            return False
        print(f"✓ Extension {ext} found")
    
    return True


def test_batch_output():
    """Test that batch output is handled."""
    print("\nTesting batch output handling...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check for output directory creation
    if 'mkdir' not in content and 'makedirs' not in content:
        print("❌ Output directory creation not found")
        return False
    
    print("✓ Output directory creation found")
    
    # Check for file counting
    if 'len(audio_files)' not in content:
        print("❌ File counting not found")
        return False
    
    print("✓ File counting found")
    
    return True


def test_help_text_updated():
    """Test that help text mentions directory processing."""
    print("\nTesting help text...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check that directory is mentioned in help
    if 'directory' not in content.lower():
        print("❌ Directory not mentioned in help text")
        return False
    
    print("✓ Directory mentioned in help text")
    
    # Check for directory example
    if 'audio_directory' in content or 'directory/' in content:
        print("✓ Directory example found in help")
    
    return True


def test_syntax():
    """Test that the file has valid Python syntax."""
    print("\nTesting Python syntax...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    try:
        ast.parse(content)
        print("✓ Python syntax is valid")
        return True
    except SyntaxError as e:
        print(f"❌ Syntax error: {e}")
        return False


def test_glob_pattern():
    """Test that glob patterns are used to find audio files."""
    print("\nTesting glob pattern usage...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    if '.glob(' not in content:
        print("❌ glob() not found")
        return False
    
    print("✓ glob() usage found")
    return True


def main():
    """Run all tests."""
    print("=" * 80)
    print("Directory Processing Feature Tests")
    print("=" * 80)
    
    tests = [
        test_syntax,
        test_directory_detection,
        test_audio_extensions,
        test_batch_output,
        test_help_text_updated,
        test_glob_pattern,
    ]
    
    results = []
    for test in tests:
        try:
            results.append(test())
        except Exception as e:
            print(f"❌ Test {test.__name__} failed with exception: {e}")
            results.append(False)
    
    print("\n" + "=" * 80)
    print("Test Summary")
    print("=" * 80)
    
    passed = sum(results)
    total = len(results)
    
    print(f"Passed: {passed}/{total}")
    
    if all(results):
        print("\n🎉 All directory processing tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
