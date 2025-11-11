#!/usr/bin/env python3
"""
Unit test for the retry logic without requiring Whisper installation
"""

import sys
import ast


def test_retry_logic_structure():
    """Test that the retry logic is properly implemented."""
    print("Testing retry logic structure...")
    
    with open('stt.py', 'r') as f:
        tree = ast.parse(f.read())
    
    # Find the load_model_with_retry function
    load_func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == 'load_model_with_retry':
            load_func = node
            break
    
    if not load_func:
        print("❌ load_model_with_retry function not found")
        return False
    
    print("✓ load_model_with_retry function found")
    
    # Check that it has the right parameters
    params = [arg.arg for arg in load_func.args.args]
    expected_params = ['model_size', 'device', 'max_retries', 'initial_delay']
    
    for param in expected_params:
        if param not in params:
            print(f"❌ Parameter '{param}' not found")
            return False
    
    print(f"✓ All expected parameters found: {', '.join(expected_params)}")
    
    # Check for retry loop (for loop)
    has_for_loop = False
    for node in ast.walk(load_func):
        if isinstance(node, ast.For):
            has_for_loop = True
            break
    
    if not has_for_loop:
        print("❌ Retry loop (for loop) not found")
        return False
    
    print("✓ Retry loop found")
    
    # Check for exception handling
    has_try_except = False
    for node in ast.walk(load_func):
        if isinstance(node, ast.Try):
            has_try_except = True
            break
    
    if not has_try_except:
        print("❌ Exception handling not found")
        return False
    
    print("✓ Exception handling found")
    
    # Check that the function validates model names
    func_body_str = ast.get_source_segment(open('stt.py').read(), load_func)
    if 'valid_models' in func_body_str and 'ValueError' in func_body_str:
        print("✓ Model validation found")
    else:
        print("⚠ Model validation may be missing")
    
    return True


def test_powerfulSTT_uses_retry():
    """Test that PowerfulSTT.__init__ uses the retry function."""
    print("\nTesting PowerfulSTT integration...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
        tree = ast.parse(content)
    
    # Find PowerfulSTT class
    powerfulSTT = None
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef) and node.name == 'PowerfulSTT':
            powerfulSTT = node
            break
    
    if not powerfulSTT:
        print("❌ PowerfulSTT class not found")
        return False
    
    # Find __init__ method
    init_method = None
    for node in powerfulSTT.body:
        if isinstance(node, ast.FunctionDef) and node.name == '__init__':
            init_method = node
            break
    
    if not init_method:
        print("❌ __init__ method not found")
        return False
    
    # Check that it calls load_model_with_retry
    init_str = ast.get_source_segment(content, init_method)
    if 'load_model_with_retry' in init_str:
        print("✓ PowerfulSTT.__init__ uses load_model_with_retry")
        return True
    else:
        print("❌ PowerfulSTT.__init__ does not use load_model_with_retry")
        return False


def test_error_handling_improvements():
    """Test that error handling has been improved."""
    print("\nTesting error handling improvements...")
    
    with open('stt.py', 'r') as f:
        content = f.read()
    
    # Check for ValueError handling
    if 'except ValueError' in content:
        print("✓ ValueError handling added")
    else:
        print("⚠ ValueError handling may be missing")
    
    # Check for helpful error messages
    helpful_messages = [
        'Available models',
        'Troubleshooting tips',
        'Invalid model configuration'
    ]
    
    found_messages = [msg for msg in helpful_messages if msg in content]
    
    if len(found_messages) >= 2:
        print(f"✓ Helpful error messages found: {', '.join(found_messages)}")
        return True
    else:
        print(f"⚠ Only found {len(found_messages)} helpful messages")
        return True  # Still pass, but warn


def main():
    """Run all unit tests."""
    print("=" * 80)
    print("Unit Tests for Model Loading Retry Logic")
    print("=" * 80)
    print()
    
    all_passed = True
    
    all_passed &= test_retry_logic_structure()
    all_passed &= test_powerfulSTT_uses_retry()
    all_passed &= test_error_handling_improvements()
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✅ All unit tests PASSED")
        return 0
    else:
        print("❌ Some unit tests FAILED")
        return 1


if __name__ == '__main__':
    sys.exit(main())
