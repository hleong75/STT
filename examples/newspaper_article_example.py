#!/usr/bin/env python3
"""
Example: Newspaper Article Formatting

This example demonstrates how to use the newspaper article formatting feature
to convert audio transcriptions into well-structured newspaper articles.
"""

import os
import sys

# Add parent directory to path to import stt module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from stt import PowerfulSTT


def format_audio_as_article(audio_file, language='en'):
    """
    Transcribe audio and format it as a newspaper article.
    
    Args:
        audio_file: Path to audio file
        language: Language code (e.g., 'en', 'fr')
    """
    print("=" * 80)
    print("Newspaper Article Formatting Example")
    print("=" * 80)
    
    # Initialize STT system
    print("\n1. Initializing Speech-to-Text system...")
    stt = PowerfulSTT(model_size='base', enable_noise_reduction=True)
    
    # Transcribe audio
    print(f"\n2. Transcribing audio: {audio_file}")
    result = stt.transcribe(audio_file, language=language, verbose=False)
    
    print("\n--- Original Transcription ---")
    print(result['text'])
    print("-" * 80)
    
    # Format as newspaper article
    print("\n3. Formatting as newspaper article...")
    try:
        article = stt.format_as_newspaper_article(result['text'], language=language)
        
        print("\n" + "=" * 80)
        print("NEWSPAPER ARTICLE")
        print("=" * 80)
        
        print(f"\nHEADLINE: {article.get('title', 'Untitled')}")
        print("=" * 80)
        
        if 'lead' in article and article['lead']:
            print(f"\nLEAD PARAGRAPH:")
            print(article['lead'])
        
        print(f"\nARTICLE BODY:")
        print(article.get('body', ''))
        
        if 'sections' in article and article['sections']:
            print(f"\n\nMAIN TOPICS COVERED:")
            for i, section in enumerate(article['sections'], 1):
                print(f"  {i}. {section}")
        
        print("\n" + "=" * 80)
        print("✓ Article formatting complete!")
        
        # Optionally save to file
        output_file = audio_file.replace('.wav', '_article.txt').replace('.mp3', '_article.txt')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"HEADLINE: {article.get('title', 'Untitled')}\n")
            f.write("=" * 80 + "\n\n")
            if 'lead' in article and article['lead']:
                f.write(f"LEAD:\n{article['lead']}\n\n")
            f.write(f"ARTICLE:\n{article.get('body', '')}\n")
            if 'sections' in article and article['sections']:
                f.write("\n\nTOPICS:\n")
                for section in article['sections']:
                    f.write(f"  • {section}\n")
        
        print(f"Article saved to: {output_file}")
        
    except Exception as e:
        print(f"❌ Error formatting article: {e}")


def main():
    """Main entry point."""
    if len(sys.argv) < 2:
        print("Usage: python newspaper_article_example.py <audio_file> [language]")
        print("\nExample:")
        print("  python newspaper_article_example.py news_recording.wav en")
        print("  python newspaper_article_example.py interview.mp3 fr")
        sys.exit(1)
    
    audio_file = sys.argv[1]
    language = sys.argv[2] if len(sys.argv) > 2 else 'en'
    
    if not os.path.exists(audio_file):
        print(f"Error: Audio file not found: {audio_file}")
        sys.exit(1)
    
    format_audio_as_article(audio_file, language)


if __name__ == '__main__':
    main()
