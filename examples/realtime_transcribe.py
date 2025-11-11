#!/usr/bin/env python3
"""
Example script for real-time transcription from microphone
"""

import sys
import queue
import numpy as np
import sounddevice as sd
import soundfile as sf
from stt import PowerfulSTT


class RealtimeSTT:
    """Real-time speech-to-text from microphone."""
    
    def __init__(self, model_size='base', language=None):
        """Initialize real-time STT system."""
        self.stt = PowerfulSTT(model_size=model_size, enable_noise_reduction=True)
        self.language = language
        self.sample_rate = 16000
        self.chunk_duration = 5  # seconds
        self.audio_queue = queue.Queue()
    
    def audio_callback(self, indata, frames, time, status):
        """Callback for audio stream."""
        if status:
            print(status, file=sys.stderr)
        self.audio_queue.put(indata.copy())
    
    def record_and_transcribe(self, duration=None):
        """
        Record from microphone and transcribe in chunks.
        
        Args:
            duration: Recording duration in seconds (None for indefinite)
        """
        print(f"Recording from microphone (sample rate: {self.sample_rate} Hz)")
        print(f"Chunk duration: {self.chunk_duration} seconds")
        
        if duration:
            print(f"Total duration: {duration} seconds")
        else:
            print("Press Ctrl+C to stop")
        
        print("\nListening...\n")
        
        try:
            chunk_size = int(self.chunk_duration * self.sample_rate)
            
            with sd.InputStream(samplerate=self.sample_rate,
                              channels=1,
                              callback=self.audio_callback):
                
                chunk_num = 0
                audio_buffer = []
                
                while True:
                    # Collect audio for chunk duration
                    while len(audio_buffer) < chunk_size:
                        audio_buffer.extend(self.audio_queue.get())
                    
                    # Process chunk
                    chunk = np.array(audio_buffer[:chunk_size], dtype=np.float32)
                    audio_buffer = audio_buffer[chunk_size:]
                    
                    # Save chunk temporarily
                    temp_file = f"/tmp/realtime_chunk_{chunk_num}.wav"
                    sf.write(temp_file, chunk, self.sample_rate)
                    
                    # Transcribe
                    print(f"[Chunk {chunk_num}]", end=" ", flush=True)
                    result = self.stt.transcribe(
                        temp_file, 
                        language=self.language,
                        verbose=False
                    )
                    
                    text = result['text'].strip()
                    if text:
                        print(f"→ {text}")
                    else:
                        print("→ (silence)")
                    
                    chunk_num += 1
                    
                    # Check duration limit
                    if duration and chunk_num * self.chunk_duration >= duration:
                        break
        
        except KeyboardInterrupt:
            print("\n\nStopping...")
        
        print("Done!")


if __name__ == '__main__':
    import argparse
    
    parser = argparse.ArgumentParser(description='Real-time transcription from microphone')
    parser.add_argument('--model', default='base',
                       choices=['tiny', 'tiny.en', 'base', 'base.en', 'small', 'small.en',
                                'medium', 'medium.en', 'large', 'large-v1', 'large-v2', 
                                'large-v3', 'large-v3-turbo', 'turbo'],
                       help='Model size (default: base, recommend tiny.en for real-time)')
    parser.add_argument('--language', help='Language code (auto-detect if not specified)')
    parser.add_argument('--duration', type=int, help='Recording duration in seconds')
    
    args = parser.parse_args()
    
    realtime_stt = RealtimeSTT(model_size=args.model, language=args.language)
    realtime_stt.record_and_transcribe(duration=args.duration)
