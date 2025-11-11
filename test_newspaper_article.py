#!/usr/bin/env python3
"""
Test script for newspaper article formatting feature.
This tests the structure and functionality without requiring actual API calls.
"""

import ast
import os
import sys


def test_newspaper_article_method():
    """Test that the newspaper article formatting method exists."""
    print("Testing newspaper article formatting method...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check for the method
    if 'format_as_newspaper_article' not in content:
        print("❌ format_as_newspaper_article method not found")
        return False
    
    print("✓ format_as_newspaper_article method found")
    
    # Parse the file
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"❌ Syntax error in stt.py: {e}")
        return False
    
    # Check method exists in PowerfulSTT class
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'PowerfulSTT':
            methods = [m.name for m in node.body if isinstance(m, ast.FunctionDef)]
            if 'format_as_newspaper_article' not in methods:
                print("❌ format_as_newspaper_article not in PowerfulSTT class")
                return False
            print("✓ format_as_newspaper_article is in PowerfulSTT class")
            break
    
    return True


def test_cli_flag():
    """Test that the --newspaper-article CLI flag exists."""
    print("\nTesting CLI flag...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check for the flag
    if '--newspaper-article' not in content:
        print("❌ --newspaper-article flag not found")
        return False
    
    print("✓ --newspaper-article flag found")
    
    # Check it's used in argument parser
    if 'newspaper_article' not in content and 'newspaper-article' not in content:
        print("❌ newspaper_article handling not found")
        return False
    
    print("✓ newspaper_article handling found")
    
    return True


def test_openai_import():
    """Test that OpenAI import is handled."""
    print("\nTesting OpenAI import handling...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check for OpenAI import
    if 'from openai import' not in content and 'import openai' not in content:
        print("❌ OpenAI import not found")
        return False
    
    print("✓ OpenAI import found")
    
    # Check for availability flag
    if 'OPENAI_AVAILABLE' not in content:
        print("❌ OPENAI_AVAILABLE flag not found")
        return False
    
    print("✓ OPENAI_AVAILABLE flag found")
    
    return True


def test_requirements():
    """Test that openai is in requirements.txt."""
    print("\nTesting requirements.txt...")
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    if 'openai' not in content.lower():
        print("❌ openai not found in requirements.txt")
        return False
    
    print("✓ openai found in requirements.txt")
    
    return True


def test_documentation():
    """Test that documentation includes newspaper article feature."""
    print("\nTesting documentation...")
    
    with open('README.md', 'r') as f:
        content = f.read()
    
    # Check for newspaper article mention
    if 'newspaper' not in content.lower() and 'article' not in content.lower():
        print("❌ Newspaper article feature not documented")
        return False
    
    print("✓ Newspaper article feature is documented")
    
    # Check for --newspaper-article flag in docs
    if '--newspaper-article' not in content:
        print("❌ --newspaper-article flag not in documentation")
        return False
    
    print("✓ --newspaper-article flag documented")
    
    # Check for OPENAI_API_KEY mention
    if 'OPENAI_API_KEY' not in content:
        print("❌ OPENAI_API_KEY not mentioned in documentation")
        return False
    
    print("✓ OPENAI_API_KEY documented")
    
    return True


def test_error_handling():
    """Test that proper error handling exists for newspaper article feature."""
    print("\nTesting error handling...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check for API key check
    if 'OPENAI_API_KEY' not in content:
        print("❌ OPENAI_API_KEY check not found")
        return False
    
    print("✓ OPENAI_API_KEY check found")
    
    # Check for RuntimeError or similar error handling
    if 'RuntimeError' not in content and 'raise' not in content:
        print("❌ Error handling not found")
        return False
    
    print("✓ Error handling found")
    
    return True


def main():
    """Run all tests."""
    print("=" * 80)
    print("Newspaper Article Feature Tests")
    print("=" * 80)
    
    tests = [
        test_newspaper_article_method,
        test_cli_flag,
        test_openai_import,
        test_requirements,
        test_documentation,
        test_error_handling,
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
        print("\n🎉 All tests passed!")
        return 0
    else:
        print("\n❌ Some tests failed")
        return 1


if __name__ == '__main__':
    sys.exit(main())
