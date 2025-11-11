#!/usr/bin/env python3
"""
Unit tests for exit code logic in stt.py
Tests the process_directory function return values
"""

import sys
import os
import tempfile
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

# Add the current directory to path to import stt module
sys.path.insert(0, '/home/runner/work/STT/STT')

# Mock all the dependencies before importing stt
sys.modules['whisper'] = MagicMock()
sys.modules['numpy'] = MagicMock()
sys.modules['soundfile'] = MagicMock()
sys.modules['noisereduce'] = MagicMock()
sys.modules['torch'] = MagicMock()

# Now we can import stt
import stt

def test_process_directory_no_files():
    """Test that process_directory returns 1 when no audio files are found."""
    print("\nTest 1: Empty directory (no audio files)")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        mock_stt = Mock()
        mock_args = Mock()
        mock_args.output = None
        mock_args.timestamps = False
        mock_args.translate = False
        mock_args.language = None
        
        result = stt.process_directory(mock_stt, tmpdir, mock_args)
        
        expected = 1  # Should return 1 for no files found
        passed = result == expected
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Expected: {expected}, Got: {result} - {status}")
        return passed

def test_process_directory_all_success():
    """Test that process_directory returns 0 when all files succeed."""
    print("\nTest 2: All files succeed")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some dummy audio files
        Path(tmpdir, "test1.wav").touch()
        Path(tmpdir, "test2.mp3").touch()
        
        mock_stt = Mock()
        # Mock successful transcription
        mock_stt.transcribe.return_value = {'text': 'test', 'language': 'en'}
        
        mock_args = Mock()
        mock_args.output = None
        mock_args.timestamps = False
        mock_args.translate = False
        mock_args.language = None
        
        result = stt.process_directory(mock_stt, tmpdir, mock_args)
        
        expected = 0  # Should return 0 for all success
        passed = result == expected
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Expected: {expected}, Got: {result} - {status}")
        return passed

def test_process_directory_partial_failure():
    """Test that process_directory returns failure count when some files fail."""
    print("\nTest 3: Some files fail")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some dummy audio files
        Path(tmpdir, "test1.wav").touch()
        Path(tmpdir, "test2.mp3").touch()
        Path(tmpdir, "test3.flac").touch()
        
        mock_stt = Mock()
        
        # First call succeeds, second fails, third succeeds
        call_count = [0]
        def mock_transcribe(*args, **kwargs):
            call_count[0] += 1
            if call_count[0] == 2:
                raise Exception("Transcription failed")
            return {'text': 'test', 'language': 'en'}
        
        mock_stt.transcribe.side_effect = mock_transcribe
        
        mock_args = Mock()
        mock_args.output = None
        mock_args.timestamps = False
        mock_args.translate = False
        mock_args.language = None
        
        result = stt.process_directory(mock_stt, tmpdir, mock_args)
        
        expected = 1  # Should return 1 for 1 failure
        passed = result == expected
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Expected: {expected}, Got: {result} - {status}")
        return passed

def test_process_directory_all_failure():
    """Test that process_directory returns total count when all files fail."""
    print("\nTest 4: All files fail")
    
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create some dummy audio files
        Path(tmpdir, "test1.wav").touch()
        Path(tmpdir, "test2.mp3").touch()
        
        mock_stt = Mock()
        # Mock failed transcription
        mock_stt.transcribe.side_effect = Exception("Transcription failed")
        
        mock_args = Mock()
        mock_args.output = None
        mock_args.timestamps = False
        mock_args.translate = False
        mock_args.language = None
        
        result = stt.process_directory(mock_stt, tmpdir, mock_args)
        
        expected = 2  # Should return 2 for 2 failures
        passed = result == expected
        status = "✓ PASS" if passed else "✗ FAIL"
        print(f"Expected: {expected}, Got: {result} - {status}")
        return passed

def main():
    """Run all unit tests."""
    print("=" * 80)
    print("Unit Tests for process_directory Return Values")
    print("=" * 80)
    
    all_passed = True
    
    all_passed &= test_process_directory_no_files()
    all_passed &= test_process_directory_all_success()
    all_passed &= test_process_directory_partial_failure()
    all_passed &= test_process_directory_all_failure()
    
    print("\n" + "=" * 80)
    if all_passed:
        print("✓ All unit tests PASSED")
        return 0
    else:
        print("✗ Some unit tests FAILED")
        return 1

if __name__ == '__main__':
    sys.exit(main())
