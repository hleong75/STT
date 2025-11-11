# Quick Start Guide

## Installation

1. **Install FFmpeg** (required for audio processing):
   ```bash
   # Ubuntu/Debian
   sudo apt update && sudo apt install ffmpeg
   
   # macOS
   brew install ffmpeg
   ```

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## First Transcription

1. **Prepare an audio file** (e.g., `audio.wav`, `audio.mp3`, etc.)

2. **Run transcription**:
   ```bash
   python stt.py audio.wav
   ```

That's it! The system will:
- Auto-detect the language
- Apply noise reduction
- Transcribe the audio
- Display the result

## Common Usage

### Specify a language
```bash
python stt.py audio.wav --language en
```

### Use a better model
```bash
python stt.py audio.wav --model medium
```

**Model Options:**
- **Multilingual**: `tiny`, `base` (default), `small`, `medium`, `large`, `large-v3`, `turbo`
- **English-only (faster)**: `tiny.en`, `base.en`, `small.en`, `medium.en`

Use `.en` models for English audio to get 2x faster transcription!

### Get timestamps
```bash
python stt.py audio.wav --timestamps
```

### Save to file
```bash
python stt.py audio.wav --output transcript.txt
```

### Translate to English
```bash
python stt.py french_audio.wav --translate
```

## Next Steps

- Check out the [README.md](README.md) for detailed documentation
- Explore the [examples/](examples/) directory for advanced usage
- See [CONTRIBUTING.md](CONTRIBUTING.md) to contribute

## Troubleshooting

**Slow first run?**
- The first run downloads the Whisper model (~150MB for base model)
- Subsequent runs will be much faster

**Out of memory?**
- Use a smaller model: `--model tiny`
- Or run on CPU: `--device cpu`

**Low accuracy?**
- Try a larger model: `--model medium` or `--model large-v3`
- For English audio, try: `--model medium.en` (faster and accurate)
- Ensure audio quality is good

## Language Codes

Common language codes:
- `en` - English
- `fr` - French
- `es` - Spanish
- `de` - German
- `zh` - Chinese
- `ja` - Japanese
- `ar` - Arabic
- `ru` - Russian
- `pt` - Portuguese
- `it` - Italian

See README.md for the full list of 99+ supported languages!
