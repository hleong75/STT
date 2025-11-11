#!/usr/bin/env python3
"""
Test script to verify model loading with retry logic
"""

import subprocess
import sys
import os

def test_model_loading(description, command, should_succeed=False):
    """Run a command and check if it handles model loading correctly."""
    print(f"\nTesting: {description}")
    print(f"Command: {' '.join(command)}")
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    # Check stderr for expected error messages
    stderr = result.stderr
    
    if should_succeed:
        passed = result.returncode == 0
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Expected: Success, Actual: {'Success' if passed else 'Failure'} - {status}")
    else:
        # For failure cases, check if we get helpful error messages
        has_helpful_message = any(keyword in stderr for keyword in [
            "Invalid model", "Available models", "Troubleshooting tips",
            "Error initializing STT system"
        ])
        passed = result.returncode != 0 and has_helpful_message
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Expected: Failure with helpful message, Actual: Exit code {result.returncode} - {status}")
    
    if not passed or "--verbose" in sys.argv:
        if result.stdout:
            print("STDOUT:", result.stdout[:500])
        if result.stderr:
            print("STDERR:", result.stderr[:500])
    
    return passed

def main():
    """Run all model loading tests."""
    print("=" * 80)
    print("Testing Model Loading with Retry Logic")
    print("=" * 80)
    
    all_passed = True
    
    # Test 1: Invalid model name should give helpful error
    all_passed &= test_model_loading(
        "Invalid model name (should fail with helpful message)",
        ["python3", "stt.py", "test_audio.wav", "--model", "invalid_model"],
        should_succeed=False
    )
    
    # Test 2: Valid model name but missing file should give helpful error
    all_passed &= test_model_loading(
        "Valid model but missing file (should fail with helpful message)",
        ["python3", "stt.py", "nonexistent_file.wav", "--model", "tiny"],
        should_succeed=False
    )
    
    # Test 3: Help should always work
    all_passed &= test_model_loading(
        "Help command (should succeed)",
        ["python3", "stt.py", "--help"],
        should_succeed=True
    )
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✓ All model loading tests PASSED")
        return 0
    else:
        print("✗ Some model loading tests FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
