#!/usr/bin/env python3
"""
Example script demonstrating API usage
"""

from stt import PowerfulSTT


def example_basic_transcription():
    """Basic transcription example."""
    print("=" * 80)
    print("Example 1: Basic Transcription")
    print("=" * 80)
    
    # Initialize STT
    stt = PowerfulSTT(model_size='base')
    
    # Transcribe audio (replace with actual audio file path)
    audio_file = 'sample_audio.wav'
    
    try:
        result = stt.transcribe(audio_file)
        print(f"\nLanguage: {result.get('language', 'unknown')}")
        print(f"Text: {result['text']}")
    except FileNotFoundError:
        print(f"Note: This is an example. Replace '{audio_file}' with an actual audio file.")


def example_with_timestamps():
    """Transcription with timestamps example."""
    print("\n" + "=" * 80)
    print("Example 2: Transcription with Timestamps")
    print("=" * 80)
    
    stt = PowerfulSTT(model_size='base')
    audio_file = 'sample_audio.wav'
    
    try:
        result = stt.transcribe_with_timestamps(audio_file)
        
        print(f"\nLanguage: {result['language']}")
        print(f"\nFull text: {result['text']}")
        print("\nSegments:")
        
        for segment in result['segments']:
            print(f"  [{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
    except FileNotFoundError:
        print(f"Note: This is an example. Replace '{audio_file}' with an actual audio file.")


def example_specific_language():
    """Transcription with specific language."""
    print("\n" + "=" * 80)
    print("Example 3: Transcription with Specific Language")
    print("=" * 80)
    
    stt = PowerfulSTT(model_size='base')
    
    # Transcribe French audio
    audio_file = 'french_audio.wav'
    
    try:
        result = stt.transcribe(audio_file, language='fr')
        print(f"\nText: {result['text']}")
    except FileNotFoundError:
        print(f"Note: This is an example. Replace '{audio_file}' with an actual audio file.")


def example_translation():
    """Translation example."""
    print("\n" + "=" * 80)
    print("Example 4: Translation to English")
    print("=" * 80)
    
    stt = PowerfulSTT(model_size='base')
    audio_file = 'spanish_audio.wav'
    
    try:
        result = stt.transcribe(audio_file, task='translate')
        print(f"\nTranslated text: {result['text']}")
    except FileNotFoundError:
        print(f"Note: This is an example. Replace '{audio_file}' with an actual audio file.")


def example_without_noise_reduction():
    """Example with noise reduction disabled."""
    print("\n" + "=" * 80)
    print("Example 5: Without Noise Reduction (for clean audio)")
    print("=" * 80)
    
    # Initialize without noise reduction
    stt = PowerfulSTT(model_size='base', enable_noise_reduction=False)
    
    audio_file = 'clean_audio.wav'
    
    try:
        result = stt.transcribe(audio_file)
        print(f"\nText: {result['text']}")
    except FileNotFoundError:
        print(f"Note: This is an example. Replace '{audio_file}' with an actual audio file.")


def example_different_model_sizes():
    """Example comparing different model sizes."""
    print("\n" + "=" * 80)
    print("Example 6: Different Model Sizes")
    print("=" * 80)
    
    audio_file = 'sample_audio.wav'
    
    for model_size in ['tiny', 'base']:
        print(f"\n--- Using {model_size} model ---")
        
        try:
            stt = PowerfulSTT(model_size=model_size)
            result = stt.transcribe(audio_file, verbose=False)
            print(f"Text: {result['text']}")
        except FileNotFoundError:
            print(f"Note: This is an example. Replace '{audio_file}' with an actual audio file.")
            break


if __name__ == '__main__':
    print("\n🎙️  STT API Usage Examples\n")
    
    # Run examples
    example_basic_transcription()
    example_with_timestamps()
    example_specific_language()
    example_translation()
    example_without_noise_reduction()
    example_different_model_sizes()
    
    print("\n" + "=" * 80)
    print("Examples completed!")
    print("=" * 80)
