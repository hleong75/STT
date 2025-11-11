#!/usr/bin/env python3
"""
Example script demonstrating batch processing of audio files
"""

import os
import sys
from pathlib import Path
from stt import PowerfulSTT


def batch_transcribe(input_dir, output_dir, model_size='base', language=None):
    """
    Transcribe all audio files in a directory.
    
    Args:
        input_dir: Directory containing audio files
        output_dir: Directory to save transcriptions
        model_size: Whisper model size
        language: Language code (None for auto-detection)
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Initialize STT system
    print(f"Initializing STT system with {model_size} model...")
    stt = PowerfulSTT(model_size=model_size)
    
    # Supported audio extensions
    audio_extensions = {'.wav', '.mp3', '.flac', '.ogg', '.m4a', '.wma', '.aac'}
    
    # Find all audio files
    audio_files = []
    for ext in audio_extensions:
        audio_files.extend(Path(input_dir).glob(f'*{ext}'))
        audio_files.extend(Path(input_dir).glob(f'*{ext.upper()}'))
    
    if not audio_files:
        print(f"No audio files found in {input_dir}")
        return
    
    print(f"Found {len(audio_files)} audio files to transcribe\n")
    
    # Process each file
    for i, audio_file in enumerate(audio_files, 1):
        print(f"[{i}/{len(audio_files)}] Processing: {audio_file.name}")
        
        try:
            # Transcribe
            result = stt.transcribe(str(audio_file), language=language, verbose=False)
            
            # Save transcription
            output_file = Path(output_dir) / f"{audio_file.stem}.txt"
            with open(output_file, 'w', encoding='utf-8') as f:
                if 'language' in result:
                    f.write(f"Language: {result['language']}\n\n")
                f.write(result['text'])
            
            print(f"✓ Saved to: {output_file}\n")
            
        except Exception as e:
            print(f"✗ Error: {e}\n")
            continue
    
    print("Batch processing completed!")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Batch transcribe audio files')
    parser.add_argument('input_dir', help='Directory containing audio files')
    parser.add_argument('output_dir', help='Directory to save transcriptions')
    parser.add_argument('--model', default='base', 
                       choices=['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en',
                                'medium', 'medium.en', 'large', 'large-v1', 'large-v2', 
                                'large-v3', 'large-v3-turbo', 'turbo'],
                       help='Model size (default: base). .en models are English-only.')
    parser.add_argument('--language', help='Language code (auto-detect if not specified)')
    
    args = parser.parse_args()
    
    batch_transcribe(args.input_dir, args.output_dir, args.model, args.language)
