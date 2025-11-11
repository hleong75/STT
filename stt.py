#!/usr/bin/env python3
"""
Ultra-Powerful Speech-to-Text System
Supports all languages and is robust to audio noise
"""

import argparse
import os
import sys
import time
import warnings
from pathlib import Path

# Try to import required dependencies with helpful error messages
try:
    import whisper
except ImportError:
    print("❌ Error: OpenAI Whisper is not installed.", file=sys.stderr)
    print("\nTo fix this issue, please install the required dependencies:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    print("\nOr install just the missing package:", file=sys.stderr)
    print("  pip install openai-whisper", file=sys.stderr)
    print("\nFor more information, see README.md or QUICKSTART.md", file=sys.stderr)
    sys.exit(1)

try:
    import numpy as np
except ImportError:
    print("❌ Error: NumPy is not installed.", file=sys.stderr)
    print("\nTo fix this issue, please install the required dependencies:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    print("\nFor more information, see README.md or QUICKSTART.md", file=sys.stderr)
    sys.exit(1)

try:
    import soundfile as sf
except ImportError:
    print("❌ Error: soundfile is not installed.", file=sys.stderr)
    print("\nTo fix this issue, please install the required dependencies:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    print("\nFor more information, see README.md or QUICKSTART.md", file=sys.stderr)
    sys.exit(1)

try:
    import noisereduce as nr
except ImportError:
    print("❌ Error: noisereduce is not installed.", file=sys.stderr)
    print("\nTo fix this issue, please install the required dependencies:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    print("\nFor more information, see README.md or QUICKSTART.md", file=sys.stderr)
    sys.exit(1)

try:
    import torch
except ImportError:
    print("❌ Error: PyTorch is not installed.", file=sys.stderr)
    print("\nTo fix this issue, please install the required dependencies:", file=sys.stderr)
    print("  pip install -r requirements.txt", file=sys.stderr)
    print("\nFor more information, see README.md or QUICKSTART.md", file=sys.stderr)
    sys.exit(1)

warnings.filterwarnings("ignore")


def load_model_with_retry(model_size, device, max_retries=3, initial_delay=1):
    """
    Load Whisper model with retry logic for handling transient failures.
    
    Args:
        model_size: Whisper model size to load
        device: Device to load model on ('cuda' or 'cpu')
        max_retries: Maximum number of retry attempts (default: 3)
        initial_delay: Initial delay in seconds before first retry (default: 1)
        
    Returns:
        Loaded Whisper model
        
    Raises:
        Exception: If model loading fails after all retries
    """
    # Validate model name before attempting to load
    valid_models = [
        'tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en',
        'medium', 'medium.en', 'large', 'large-v1', 'large-v2', 
        'large-v3', 'large-v3-turbo', 'turbo'
    ]
    
    if model_size not in valid_models:
        raise ValueError(
            f"Invalid model name '{model_size}'. "
            f"Valid options are: {', '.join(valid_models)}"
        )
    
    last_exception = None
    delay = initial_delay
    
    for attempt in range(max_retries):
        try:
            print(f"Loading Whisper model '{model_size}' on {device}...")
            if attempt > 0:
                print(f"  (Attempt {attempt + 1}/{max_retries})")
            
            model = whisper.load_model(model_size, device=device)
            print("Model loaded successfully!")
            return model
            
        except Exception as e:
            last_exception = e
            error_msg = str(e)
            
            # Check for common error types and provide helpful messages
            if "No such file or directory" in error_msg or "FileNotFoundError" in str(type(e)):
                print(f"⚠ Warning: Model file not found. Attempting to download...", file=sys.stderr)
            elif "Connection" in error_msg or "Network" in error_msg or "HTTP" in error_msg:
                print(f"⚠ Warning: Network error while downloading model. Will retry...", file=sys.stderr)
            elif "Out of memory" in error_msg or "CUDA out of memory" in error_msg:
                print(f"❌ Error: Out of memory. Try using a smaller model or --device cpu", file=sys.stderr)
                raise  # Don't retry for OOM errors
            else:
                print(f"⚠ Warning: Error loading model: {error_msg}", file=sys.stderr)
            
            # If this isn't the last attempt, wait before retrying
            if attempt < max_retries - 1:
                print(f"  Retrying in {delay} seconds...", file=sys.stderr)
                time.sleep(delay)
                delay *= 2  # Exponential backoff
            else:
                # Last attempt failed, raise the exception
                print(f"❌ Error: Failed to load model after {max_retries} attempts", file=sys.stderr)
                raise last_exception


class PowerfulSTT:
    """
    A powerful Speech-to-Text system with multi-language support
    and noise reduction capabilities.
    """
    
    # Supported languages by Whisper (99+ languages)
    SUPPORTED_LANGUAGES = [
        'en', 'zh', 'de', 'es', 'ru', 'ko', 'fr', 'ja', 'pt', 'tr', 'pl', 'ca',
        'nl', 'ar', 'sv', 'it', 'id', 'hi', 'fi', 'vi', 'he', 'uk', 'el', 'ms',
        'cs', 'ro', 'da', 'hu', 'ta', 'no', 'th', 'ur', 'hr', 'bg', 'lt', 'la',
        'mi', 'ml', 'cy', 'sk', 'te', 'fa', 'lv', 'bn', 'sr', 'az', 'sl', 'kn',
        'et', 'mk', 'br', 'eu', 'is', 'hy', 'ne', 'mn', 'bs', 'kk', 'sq', 'sw',
        'gl', 'mr', 'pa', 'si', 'km', 'sn', 'yo', 'so', 'af', 'oc', 'ka', 'be',
        'tg', 'sd', 'gu', 'am', 'yi', 'lo', 'uz', 'fo', 'ht', 'ps', 'tk', 'nn',
        'mt', 'sa', 'lb', 'my', 'bo', 'tl', 'mg', 'as', 'tt', 'haw', 'ln', 'ha',
        'ba', 'jw', 'su'
    ]
    
    def __init__(self, model_size='base', device=None, enable_noise_reduction=True):
        """
        Initialize the STT system.
        
        Args:
            model_size: Whisper model size. Options: 'tiny', 'tiny.en', 'base', 'base.en',
                       'small', 'small.en', 'medium', 'medium.en', 'large', 'large-v1', 
                       'large-v2', 'large-v3', 'large-v3-turbo', 'turbo'.
                       Models with .en suffix are English-only and faster.
            device: Device to run on ('cuda', 'cpu', or None for auto)
            enable_noise_reduction: Whether to apply noise reduction
        """
        self.model_size = model_size
        self.enable_noise_reduction = enable_noise_reduction
        
        # Auto-detect device
        if device is None:
            self.device = 'cuda' if torch.cuda.is_available() else 'cpu'
        else:
            self.device = device
        
        # Load model with retry logic
        self.model = load_model_with_retry(model_size, self.device)
    
    def reduce_noise(self, audio, sample_rate):
        """
        Apply noise reduction to audio signal.
        
        Args:
            audio: Audio signal as numpy array
            sample_rate: Sample rate of the audio
            
        Returns:
            Noise-reduced audio signal
        """
        print("Applying noise reduction...")
        # Use noisereduce library for stationary noise reduction
        reduced_audio = nr.reduce_noise(
            y=audio,
            sr=sample_rate,
            stationary=True,
            prop_decrease=1.0
        )
        return reduced_audio
    
    def transcribe(self, audio_path, language=None, task='transcribe', verbose=True):
        """
        Transcribe audio file to text.
        
        Args:
            audio_path: Path to audio file
            language: Language code (None for auto-detection)
            task: 'transcribe' or 'translate' (translate to English)
            verbose: Whether to print progress
            
        Returns:
            Dictionary containing transcription results
        """
        if not os.path.exists(audio_path):
            raise FileNotFoundError(f"Audio file not found: {audio_path}")
        
        print(f"\nProcessing: {audio_path}")
        
        # Load audio file
        audio, sample_rate = sf.read(audio_path)
        
        # Convert stereo to mono if necessary
        if len(audio.shape) > 1:
            audio = np.mean(audio, axis=1)
        
        # Apply noise reduction if enabled
        if self.enable_noise_reduction:
            audio = self.reduce_noise(audio, sample_rate)
        
        # Save preprocessed audio temporarily
        temp_audio_path = "/tmp/preprocessed_audio.wav"
        sf.write(temp_audio_path, audio, sample_rate)
        
        # Transcribe with Whisper
        print(f"Transcribing with Whisper ({self.model_size} model)...")
        
        options = {
            'task': task,
            'verbose': verbose,
        }
        
        if language:
            options['language'] = language
            print(f"Language: {language}")
        else:
            print("Language: Auto-detect")
        
        result = self.model.transcribe(temp_audio_path, **options)
        
        # Clean up temporary file
        if os.path.exists(temp_audio_path):
            os.remove(temp_audio_path)
        
        return result
    
    def transcribe_with_timestamps(self, audio_path, language=None):
        """
        Transcribe audio with word-level timestamps.
        
        Args:
            audio_path: Path to audio file
            language: Language code (None for auto-detection)
            
        Returns:
            Dictionary containing transcription with timestamps
        """
        result = self.transcribe(audio_path, language=language, verbose=False)
        
        # Extract segments with timestamps
        segments = []
        for segment in result.get('segments', []):
            segments.append({
                'start': segment['start'],
                'end': segment['end'],
                'text': segment['text'].strip()
            })
        
        return {
            'text': result['text'],
            'language': result.get('language', 'unknown'),
            'segments': segments
        }


def process_directory(stt, directory_path, args):
    """
    Process all audio files in a directory.
    
    Args:
        stt: PowerfulSTT instance
        directory_path: Path to directory containing audio files
        args: Command-line arguments
        
    Returns:
        Number of failed files (0 if all succeeded)
    """
    # Supported audio extensions
    audio_extensions = {'.wav', '.mp3', '.flac', '.ogg', '.m4a', '.wma', '.aac'}
    
    # Find all audio files
    audio_files = []
    directory = Path(directory_path)
    for ext in audio_extensions:
        audio_files.extend(directory.glob(f'*{ext}'))
        audio_files.extend(directory.glob(f'*{ext.upper()}'))
    
    if not audio_files:
        print(f"No audio files found in {directory_path}")
        return 1  # Return 1 to indicate failure (no files to process)
    
    print(f"\nFound {len(audio_files)} audio files to process")
    print("=" * 80)
    
    # Create output directory if output path is specified
    output_dir = None
    if args.output:
        output_dir = Path(args.output)
        output_dir.mkdir(parents=True, exist_ok=True)
        print(f"Output directory: {output_dir}\n")
    
    # Process each file
    task = 'translate' if args.translate else 'transcribe'
    success_count = 0
    
    for i, audio_file in enumerate(audio_files, 1):
        print(f"\n[{i}/{len(audio_files)}] Processing: {audio_file.name}")
        print("-" * 80)
        
        try:
            if args.timestamps:
                result = stt.transcribe_with_timestamps(str(audio_file), language=args.language)
                
                # Format output
                output_lines = []
                output_lines.append(f"File: {audio_file.name}")
                output_lines.append(f"Language: {result['language']}")
                output_lines.append(f"\nFull transcription:\n{result['text']}\n")
                output_lines.append("\nSegments with timestamps:")
                
                for segment in result['segments']:
                    start_time = f"{int(segment['start'] // 60):02d}:{segment['start'] % 60:05.2f}"
                    end_time = f"{int(segment['end'] // 60):02d}:{segment['end'] % 60:05.2f}"
                    output_lines.append(f"[{start_time} -> {end_time}] {segment['text']}")
                
                output = '\n'.join(output_lines)
            else:
                result = stt.transcribe(str(audio_file), language=args.language, task=task, verbose=False)
                
                # Format output
                output_lines = []
                output_lines.append(f"File: {audio_file.name}")
                if 'language' in result:
                    output_lines.append(f"Language: {result['language']}")
                output_lines.append(f"\nTranscription:\n{result['text']}")
                output = '\n'.join(output_lines)
            
            # Output results
            if output_dir:
                output_file = output_dir / f"{audio_file.stem}.txt"
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"✓ Saved to: {output_file}")
            else:
                print(output)
            
            success_count += 1
            
        except Exception as e:
            print(f"✗ Error: {e}")
            continue
    
    print("\n" + "=" * 80)
    print(f"Processing complete: {success_count}/{len(audio_files)} files succeeded")
    
    failure_count = len(audio_files) - success_count
    if failure_count > 0:
        print(f"⚠ {failure_count} files failed")
    else:
        print("✓ All files processed successfully!")
    
    return failure_count


def main():
    """Main CLI interface for the STT system."""
    parser = argparse.ArgumentParser(
        description='Ultra-Powerful Speech-to-Text System',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic transcription with auto-language detection
  python stt.py audio.wav
  
  # Transcribe all audio files in a directory
  python stt.py audio_directory/
  
  # Transcribe directory and save outputs to another directory
  python stt.py audio_directory/ --output transcripts/
  
  # Transcribe with specific language
  python stt.py audio.wav --language fr
  
  # Translate to English
  python stt.py audio.wav --translate
  
  # Use larger model for better accuracy
  python stt.py audio.wav --model medium
  
  # Use English-only model for faster processing
  python stt.py english_audio.wav --model base.en
  
  # Use latest model for best accuracy
  python stt.py audio.wav --model large-v3
  
  # Use turbo model for speed + accuracy balance
  python stt.py audio.wav --model turbo
  
  # Disable noise reduction for clean audio
  python stt.py audio.wav --no-noise-reduction
  
  # Get timestamps
  python stt.py audio.wav --timestamps
  
Supported languages: English, Chinese, German, Spanish, Russian, Korean, French,
Japanese, Portuguese, Turkish, Polish, Catalan, Dutch, Arabic, Swedish, Italian,
Indonesian, Hindi, Finnish, Vietnamese, Hebrew, Ukrainian, Greek, Malay, Czech,
Romanian, Danish, Hungarian, Tamil, Norwegian, Thai, Urdu, Croatian, Bulgarian,
Lithuanian, Latin, Maori, Malayalam, Welsh, Slovak, Telugu, Persian, Latvian,
Bengali, Serbian, Azerbaijani, Slovenian, Kannada, Estonian, Macedonian, Breton,
Basque, Icelandic, Armenian, Nepali, Mongolian, Bosnian, Kazakh, Albanian,
Swahili, Galician, Marathi, Punjabi, Sinhala, Khmer, Shona, Yoruba, Somali,
Afrikaans, Occitan, Georgian, Belarusian, Tajik, Sindhi, Gujarati, Amharic,
Yiddish, Lao, Uzbek, Faroese, Haitian Creole, Pashto, Turkmen, Norwegian Nynorsk,
Maltese, Sanskrit, Luxembourgish, Burmese, Tibetan, Tagalog, Malagasy, Assamese,
Tatar, Hawaiian, Lingala, Hausa, Bashkir, Javanese, Sundanese, and many more!
        """
    )
    
    parser.add_argument(
        'audio_file',
        help='Path to audio file or directory (supports WAV, MP3, FLAC, OGG, etc.)'
    )
    
    parser.add_argument(
        '--model',
        choices=['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en', 
                 'medium', 'medium.en', 'large', 'large-v1', 'large-v2', 'large-v3', 
                 'large-v3-turbo', 'turbo'],
        default='base',
        help='Whisper model size (default: base). Models with .en are English-only and faster. '
             'Larger models are more accurate but slower. v3 and turbo are the latest versions.'
    )
    
    parser.add_argument(
        '--language',
        help='Language code (e.g., en, fr, es, zh). Auto-detected if not specified.'
    )
    
    parser.add_argument(
        '--translate',
        action='store_true',
        help='Translate to English instead of transcribing'
    )
    
    parser.add_argument(
        '--no-noise-reduction',
        action='store_true',
        help='Disable noise reduction (for clean audio)'
    )
    
    parser.add_argument(
        '--timestamps',
        action='store_true',
        help='Include timestamps for each segment'
    )
    
    parser.add_argument(
        '--output',
        help='Output file path (for single file) or directory (for batch processing)'
    )
    
    parser.add_argument(
        '--device',
        choices=['cuda', 'cpu'],
        help='Device to run on (auto-detected if not specified)'
    )
    
    args = parser.parse_args()
    
    # Check if input is a directory or file
    input_path = Path(args.audio_file)
    
    if not input_path.exists():
        print(f"Error: Path not found: {args.audio_file}", file=sys.stderr)
        sys.exit(1)
    
    is_directory = input_path.is_dir()
    
    # Initialize STT system
    try:
        stt = PowerfulSTT(
            model_size=args.model,
            device=args.device,
            enable_noise_reduction=not args.no_noise_reduction
        )
    except ValueError as e:
        # Handle invalid model names
        print(f"\n❌ Invalid model configuration: {e}", file=sys.stderr)
        print(f"\nAvailable models:", file=sys.stderr)
        print(f"  - Multilingual: tiny, base, small, medium, large, large-v1, large-v2, large-v3, large-v3-turbo, turbo", file=sys.stderr)
        print(f"  - English-only: tiny.en, base.en, small.en, medium.en", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        # Handle other errors during initialization
        print(f"\n❌ Error initializing STT system: {e}", file=sys.stderr)
        print(f"\nTroubleshooting tips:", file=sys.stderr)
        print(f"  1. Check your internet connection (models are downloaded on first use)", file=sys.stderr)
        print(f"  2. Ensure you have enough disk space (~1-10GB depending on model)", file=sys.stderr)
        print(f"  3. Try a smaller model: --model tiny", file=sys.stderr)
        print(f"  4. Try forcing CPU: --device cpu", file=sys.stderr)
        print(f"  5. Check the model cache directory has write permissions", file=sys.stderr)
        sys.exit(1)
    
    # Process directory or single file
    try:
        if is_directory:
            failure_count = process_directory(stt, args.audio_file, args)
            if failure_count > 0:
                sys.exit(1)  # Exit with error if any files failed
        else:
            # Original single file processing
            task = 'translate' if args.translate else 'transcribe'
            
            if args.timestamps:
                result = stt.transcribe_with_timestamps(args.audio_file, language=args.language)
                
                # Format output
                output_lines = []
                output_lines.append(f"Language: {result['language']}")
                output_lines.append(f"\nFull transcription:\n{result['text']}\n")
                output_lines.append("\nSegments with timestamps:")
                
                for segment in result['segments']:
                    start_time = f"{int(segment['start'] // 60):02d}:{segment['start'] % 60:05.2f}"
                    end_time = f"{int(segment['end'] // 60):02d}:{segment['end'] % 60:05.2f}"
                    output_lines.append(f"[{start_time} -> {end_time}] {segment['text']}")
                
                output = '\n'.join(output_lines)
            else:
                result = stt.transcribe(args.audio_file, language=args.language, task=task)
                
                # Format output
                output_lines = []
                if 'language' in result:
                    output_lines.append(f"Language: {result['language']}")
                output_lines.append(f"\nTranscription:\n{result['text']}")
                output = '\n'.join(output_lines)
            
            # Output results
            if args.output:
                with open(args.output, 'w', encoding='utf-8') as f:
                    f.write(output)
                print(f"\nResults saved to: {args.output}")
            else:
                print("\n" + "=" * 80)
                print(output)
                print("=" * 80)
            
            print("\n✓ Transcription completed successfully!")
        
    except Exception as e:
        print(f"Error during transcription: {e}", file=sys.stderr)
        sys.exit(1)
    
    # Explicitly exit with success code
    sys.exit(0)


if __name__ == '__main__':
    main()
