#!/usr/bin/env python3
"""
Test script to verify exit codes are correct in various scenarios
"""

import subprocess
import sys
import os
from pathlib import Path

def test_exit_code(description, command, expected_exit_code):
    """Run a command and check its exit code."""
    print(f"\nTesting: {description}")
    print(f"Command: {' '.join(command)}")
    
    result = subprocess.run(command, capture_output=True, text=True)
    
    actual_exit_code = result.returncode
    passed = actual_exit_code == expected_exit_code
    
    status = "✓ PASS" if passed else "✗ FAIL"
    print(f"Expected exit code: {expected_exit_code}, Actual: {actual_exit_code} - {status}")
    
    if not passed:
        print("STDOUT:", result.stdout[:200])
        print("STDERR:", result.stderr[:200])
    
    return passed

def main():
    """Run all exit code tests."""
    print("=" * 80)
    print("Testing Exit Codes for stt.py")
    print("=" * 80)
    
    all_passed = True
    
    # Test 1: Help command should exit with 0
    all_passed &= test_exit_code(
        "Help command (should succeed)",
        ["python3", "stt.py", "--help"],
        0
    )
    
    # Test 2: Missing dependencies should exit with 1
    # This already exits with 1 due to missing dependencies
    all_passed &= test_exit_code(
        "Missing file (should fail)",
        ["python3", "stt.py", "nonexistent_file.wav"],
        1
    )
    
    # Test 3: Non-existent directory should exit with 1
    all_passed &= test_exit_code(
        "Non-existent directory (should fail)",
        ["python3", "stt.py", "nonexistent_directory/"],
        1
    )
    
    # Test 4: Empty directory (if dependencies installed)
    # Create empty test directory
    test_dir = Path("/tmp/empty_audio_test")
    test_dir.mkdir(exist_ok=True)
    
    all_passed &= test_exit_code(
        "Empty directory with no audio files (should fail)",
        ["python3", "stt.py", str(test_dir)],
        1
    )
    
    # Clean up
    test_dir.rmdir()
    
    # Test 5: demo.py should succeed
    all_passed &= test_exit_code(
        "demo.py (should succeed)",
        ["python3", "demo.py"],
        0
    )
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✓ All exit code tests PASSED")
        return 0
    else:
        print("✗ Some exit code tests FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
