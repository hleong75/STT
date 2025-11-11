#!/usr/bin/env python3
"""
Test script to validate the STT system structure without requiring dependencies
"""

import ast
import os
import sys


def test_stt_module():
    """Test the stt.py module structure."""
    print("Testing stt.py module structure...")
    
    # Check if file exists
    if not os.path.exists('stt.py'):
        print("❌ stt.py not found")
        return False
    
    # Parse the file
    with open('stt.py', 'r') as f:
        content = f.read()
    
    try:
        tree = ast.parse(content)
    except SyntaxError as e:
        print(f"❌ Syntax error in stt.py: {e}")
        return False
    
    # Check for main components
    classes = [node.name for node in ast.walk(tree) if isinstance(node, ast.ClassDef)]
    functions = [node.name for node in ast.walk(tree) if isinstance(node, ast.FunctionDef)]
    
    # Verify PowerfulSTT class exists
    if 'PowerfulSTT' not in classes:
        print("❌ PowerfulSTT class not found")
        return False
    
    print("✓ PowerfulSTT class found")
    
    # Verify key methods exist
    required_methods = ['__init__', 'reduce_noise', 'transcribe', 'transcribe_with_timestamps']
    for method in required_methods:
        if method not in functions:
            print(f"❌ Method {method} not found")
            return False
        print(f"✓ Method {method} found")
    
    # Verify main function exists
    if 'main' not in functions:
        print("❌ main function not found")
        return False
    
    print("✓ main function found")
    print("✓ stt.py structure is valid")
    return True


def test_examples():
    """Test example scripts structure."""
    print("\nTesting example scripts...")
    
    examples = ['api_usage.py', 'batch_transcribe.py', 'realtime_transcribe.py']
    
    for example in examples:
        filepath = os.path.join('examples', example)
        if not os.path.exists(filepath):
            print(f"❌ {example} not found")
            return False
        
        # Check syntax
        with open(filepath, 'r') as f:
            content = f.read()
        
        try:
            ast.parse(content)
            print(f"✓ {example} syntax is valid")
        except SyntaxError as e:
            print(f"❌ Syntax error in {example}: {e}")
            return False
    
    return True


def test_documentation():
    """Test documentation files."""
    print("\nTesting documentation...")
    
    docs = ['README.md', 'QUICKSTART.md', 'CONTRIBUTING.md', 'LICENSE']
    
    for doc in docs:
        if not os.path.exists(doc):
            print(f"❌ {doc} not found")
            return False
        
        # Check if file is not empty
        with open(doc, 'r') as f:
            content = f.read()
        
        if len(content) < 50:
            print(f"❌ {doc} is too short or empty")
            return False
        
        print(f"✓ {doc} exists and has content")
    
    return True


def test_requirements():
    """Test requirements files."""
    print("\nTesting requirements files...")
    
    if not os.path.exists('requirements.txt'):
        print("❌ requirements.txt not found")
        return False
    
    with open('requirements.txt', 'r') as f:
        content = f.read()
    
    # Check for key dependencies
    required_deps = ['whisper', 'torch', 'numpy', 'soundfile', 'noisereduce']
    
    for dep in required_deps:
        if dep.lower() not in content.lower():
            print(f"❌ Dependency {dep} not found in requirements.txt")
            return False
        print(f"✓ Dependency {dep} found")
    
    return True


def test_language_support():
    """Test that language support is comprehensive."""
    print("\nTesting language support...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check for language list
    if 'SUPPORTED_LANGUAGES' not in content:
        print("❌ SUPPORTED_LANGUAGES not found")
        return False
    
    # Extract language list
    tree = ast.parse(content)
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'PowerfulSTT':
            for item in node.body:
                if isinstance(item, ast.Assign):
                    for target in item.targets:
                        if isinstance(target, ast.Name) and target.id == 'SUPPORTED_LANGUAGES':
                            if isinstance(item.value, ast.List):
                                num_languages = len(item.value.elts)
                                print(f"✓ Found {num_languages} supported languages")
                                
                                if num_languages < 50:
                                    print(f"❌ Expected at least 50 languages, found {num_languages}")
                                    return False
                                
                                return True
    
    print("❌ Could not verify language support")
    return False


def test_noise_reduction():
    """Test that noise reduction feature exists."""
    print("\nTesting noise reduction feature...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    if 'reduce_noise' not in content:
        print("❌ reduce_noise method not found")
        return False
    
    if 'noisereduce' not in content:
        print("❌ noisereduce library not imported")
        return False
    
    if 'enable_noise_reduction' not in content:
        print("❌ enable_noise_reduction parameter not found")
        return False
    
    print("✓ Noise reduction feature is implemented")
    return True


def main():
    """Run all tests."""
    print("=" * 80)
    print("STT System Validation Tests")
    print("=" * 80)
    
    tests = [
        test_stt_module,
        test_examples,
        test_documentation,
        test_requirements,
        test_language_support,
        test_noise_reduction,
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
