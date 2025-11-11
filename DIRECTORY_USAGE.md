# Directory Processing Usage Guide

## Overview

The STT program now supports processing entire directories of audio files in a single command. This feature was added to enable batch processing without requiring separate scripts or shell loops.

## Basic Usage

### Process a Directory

```bash
python stt.py /path/to/audio_directory/
```

This will:
- Scan the directory for all audio files
- Process each file with the same settings
- Display progress (e.g., "[1/5] Processing: file1.wav")
- Print transcriptions to stdout

### Save to Output Directory

```bash
python stt.py /path/to/audio_directory/ --output /path/to/transcripts/
```

This will:
- Create the output directory if it doesn't exist
- Save each transcription as `{filename}.txt`
- Show the path where each file was saved

## Supported Audio Formats

The directory processor automatically detects files with these extensions:
- `.wav`, `.WAV`
- `.mp3`, `.MP3`
- `.flac`, `.FLAC`
- `.ogg`, `.OGG`
- `.m4a`, `.M4A`
- `.wma`, `.WMA`
- `.aac`, `.AAC`

## Examples

### Example 1: Basic Directory Processing

```bash
python stt.py recordings/
```

Output:
```
Loading Whisper model 'base' on cpu...
Model loaded successfully!

Found 3 audio files to process
================================================================================

[1/3] Processing: meeting1.wav
--------------------------------------------------------------------------------
Processing: recordings/meeting1.wav
Applying noise reduction...
Transcribing with Whisper (base model)...
File: meeting1.wav
Language: en

Transcription:
This is the transcription of meeting 1...
✓ Saved to: meeting1.txt

[2/3] Processing: meeting2.mp3
...
```

### Example 2: With Custom Model and Language

```bash
python stt.py french_podcasts/ --output transcripts/ --language fr --model medium
```

### Example 3: With Timestamps

```bash
python stt.py interviews/ --output transcripts/ --timestamps --language en
```

### Example 4: Translation to English

```bash
python stt.py multilingual_audio/ --output translations/ --translate
```

## Progress and Error Handling

The processor shows clear progress:
- **Current file**: `[X/Y] Processing: filename.ext`
- **Success**: `✓ Saved to: output.txt` or displays transcription
- **Error**: `✗ Error: [error message]` (continues with next file)
- **Summary**: `Processing complete: X/Y files succeeded`

If some files fail, the processor continues with remaining files and reports the failure count at the end.

## Backward Compatibility

Single file processing still works exactly as before:

```bash
python stt.py audio.wav --output transcript.txt
```

The program automatically detects whether the input is a file or directory.

## Performance Tips

1. **Use appropriate model size**: Start with `base` for quick processing, use `medium` or `large` for better accuracy
2. **Specify language**: Auto-detection works but specifying `--language` can improve speed
3. **GPU acceleration**: The program automatically uses CUDA if available
4. **Clean audio**: Use `--no-noise-reduction` for clean recordings to save processing time

## Differences from batch_transcribe.py

The built-in directory processing in `stt.py` provides:
- Simpler command-line interface
- All CLI options available (timestamps, translation, etc.)
- Consistent with single-file usage
- Better integration with the main program

The separate `examples/batch_transcribe.py` script remains available for programmatic use and as an API example.
