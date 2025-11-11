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


def test_rule_based_formatting():
    """Test that rule-based formatting is implemented."""
    print("\nTesting rule-based formatting...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check that OpenAI is NOT required
    if 'OPENAI_AVAILABLE' in content:
        print("❌ Code still references OPENAI_AVAILABLE")
        return False
    
    print("✓ OpenAI dependency removed")
    
    # Check for rule-based implementation markers
    if 're.split' not in content or 'sentences' not in content:
        print("❌ Rule-based text processing not found")
        return False
    
    print("✓ Rule-based text processing found")
    
    return True


def test_requirements():
    """Test that openai is NOT in requirements.txt."""
    print("\nTesting requirements.txt...")
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    # Check that openai package (not openai-whisper) is NOT in requirements
    lines = content.lower().split('\n')
    has_openai_package = any(line.startswith('openai>=') or line.startswith('openai==') 
                               for line in lines)
    
    if has_openai_package:
        print("❌ openai package still in requirements.txt")
        return False
    
    print("✓ openai package removed from requirements.txt")
    
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
    
    # Check that OPENAI_API_KEY is NOT mentioned (since we removed API dependency)
    if 'OPENAI_API_KEY' in content:
        print("❌ OPENAI_API_KEY still mentioned in documentation")
        return False
    
    print("✓ OPENAI_API_KEY removed from documentation")
    
    return True


def test_error_handling():
    """Test that proper error handling exists for newspaper article feature."""
    print("\nTesting error handling...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check that API key check is NOT present (since we removed API dependency)
    if 'OPENAI_API_KEY' in content:
        print("❌ OPENAI_API_KEY check still present")
        return False
    
    print("✓ OPENAI_API_KEY check removed")
    
    # Check for basic error handling
    if 'try:' not in content or 'except' not in content:
        print("❌ Basic error handling not found")
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
        test_rule_based_formatting,
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
