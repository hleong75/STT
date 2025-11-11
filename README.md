# 🎙️ Ultra-Powerful Speech-to-Text System

A robust, multi-language speech-to-text system powered by OpenAI's Whisper with advanced noise reduction capabilities.

## ✨ Features

- **🌍 Multi-language Support**: Supports 99+ languages including English, French, Spanish, Chinese, Arabic, Japanese, and many more
- **🔇 Noise Robustness**: Advanced noise reduction preprocessing for handling noisy audio
- **🎯 High Accuracy**: Uses OpenAI's Whisper models with state-of-the-art accuracy
- **⚡ Multiple Model Sizes**: From tiny (fast) to large (most accurate)
- **🕐 Timestamp Support**: Get word-level timestamps for your transcriptions
- **🌐 Translation**: Translate any language to English
- **🔧 Easy to Use**: Simple command-line interface and Python API

## 🚀 Installation

### Prerequisites

- Python 3.8 or higher
- FFmpeg (for audio processing)

### Install FFmpeg

**Ubuntu/Debian:**
```bash
sudo apt update && sudo apt install ffmpeg
```

**macOS:**
```bash
brew install ffmpeg
```

**Windows:**
Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

## 📖 Usage

### Basic Usage

Transcribe an audio file with automatic language detection:

```bash
python stt.py audio.wav
```

### Process Directory (Batch Mode)

Process all audio files in a directory:

```bash
python stt.py audio_directory/
```

Save transcriptions to an output directory:

```bash
python stt.py audio_directory/ --output transcripts/
```

The program will automatically:
- Find all audio files (WAV, MP3, FLAC, OGG, M4A, etc.)
- Process each file
- Save individual transcripts (when `--output` is specified)
- Show progress for each file

### Specify Language

Transcribe with a specific language:

```bash
python stt.py audio.wav --language fr
```

### Different Model Sizes

Use a larger model for better accuracy (but slower):

```bash
python stt.py audio.wav --model medium
```

Available models:
- **Multilingual**: `tiny`, `base`, `small`, `medium`, `large`, `large-v1`, `large-v2`, `large-v3`, `large-v3-turbo`, `turbo`
- **English-only (faster)**: `tiny.en`, `base.en`, `small.en`, `medium.en`

Use `.en` models for English audio to get faster transcription with similar accuracy.

### Translation

Translate any language to English:

```bash
python stt.py audio.wav --translate
```

### Timestamps

Get segment-level timestamps:

```bash
python stt.py audio.wav --timestamps
```

### Save Output

Save transcription to a file:

```bash
python stt.py audio.wav --output transcript.txt
```

### Disable Noise Reduction

For clean audio, you can disable noise reduction:

```bash
python stt.py audio.wav --no-noise-reduction
```

### GPU Acceleration

Automatically uses CUDA if available. Force CPU:

```bash
python stt.py audio.wav --device cpu
```

## 🐍 Python API

You can also use the STT system programmatically:

```python
from stt import PowerfulSTT

# Initialize the system
stt = PowerfulSTT(model_size='base', enable_noise_reduction=True)

# Transcribe audio
result = stt.transcribe('audio.wav')
print(result['text'])

# Transcribe with timestamps
result = stt.transcribe_with_timestamps('audio.wav', language='fr')
for segment in result['segments']:
    print(f"[{segment['start']:.2f}s - {segment['end']:.2f}s] {segment['text']}")
```

## 🌍 Supported Languages

The system supports 99+ languages including:

- **European**: English, French, Spanish, German, Italian, Portuguese, Dutch, Polish, Russian, Ukrainian, Greek, Czech, Romanian, Swedish, Danish, Norwegian, Finnish, Turkish, and more
- **Asian**: Chinese (Mandarin), Japanese, Korean, Hindi, Thai, Vietnamese, Indonesian, Malay, Tamil, Telugu, and more
- **Middle Eastern**: Arabic, Hebrew, Persian, Urdu, and more
- **African**: Swahili, Afrikaans, Yoruba, Somali, and more
- **Others**: Latin, Hawaiian, Maori, and many more

## 🎯 Model Comparison

| Model  | Speed | Memory | Accuracy | Best For |
|--------|-------|--------|----------|----------|
| tiny / tiny.en   | ⚡⚡⚡  | 1 GB   | Good     | Quick transcription, real-time |
| base / base.en   | ⚡⚡    | 1 GB   | Better   | General use (default) |
| small / small.en  | ⚡     | 2 GB   | Great    | Better accuracy |
| medium / medium.en | 🐌    | 5 GB   | Excellent| Professional use |
| large / large-v3  | 🐌🐌  | 10 GB  | Best     | Maximum accuracy |
| turbo  | ⚡⚡⚡  | 6 GB   | Excellent| Fast + accurate balance |

**Note**: Models with `.en` suffix are English-only and ~2x faster than their multilingual counterparts with similar accuracy for English audio. The `turbo` and `large-v3` models are the latest versions with improved performance.

## 🔧 Advanced Features

### Noise Reduction

The system includes advanced noise reduction that:
- Removes stationary background noise
- Improves transcription quality for noisy recordings
- Works well with environmental noise, fans, AC, etc.

### Multi-format Support

Supports all common audio formats:
- WAV, MP3, FLAC, OGG, M4A, WMA, AAC, etc.

### Batch Processing

Process an entire directory of audio files:

```bash
# Process all audio files in a directory
python stt.py my_audio_files/ --output transcripts/

# Process with specific options
python stt.py recordings/ --output transcripts/ --language en --model medium
```

The built-in directory processing will:
- Automatically detect all audio files (WAV, MP3, FLAC, OGG, M4A, WMA, AAC)
- Process each file sequentially
- Save individual transcripts to the output directory
- Show progress and success/failure status for each file

Alternatively, for shell-based batch processing:

```bash
for file in *.wav; do
    python stt.py "$file" --output "${file%.wav}.txt"
done
```

## 📝 Examples

### Example 1: Transcribe a French audio file

```bash
python stt.py french_audio.mp3 --language fr --output transcript_fr.txt
```

### Example 2: Process an entire directory of meetings

```bash
python stt.py meeting_recordings/ --output transcripts/ --language en --model medium
```

### Example 3: Transcribe noisy English audio with timestamps

```bash
python stt.py noisy_meeting.wav --language en --timestamps --model medium
```

### Example 4: Translate Chinese to English

```bash
python stt.py chinese_podcast.m4a --language zh --translate
```

## 🛠️ Troubleshooting

**Issue**: "No module named 'whisper'"
- **Solution**: Run `pip install -r requirements.txt`

**Issue**: Slow transcription
- **Solution**: Use a smaller model with `--model tiny` or ensure CUDA is available

**Issue**: Poor accuracy on noisy audio
- **Solution**: Ensure noise reduction is enabled (default) and try a larger model

**Issue**: Out of memory error
- **Solution**: Use a smaller model or run on CPU with `--device cpu`

## 📄 License

This project uses OpenAI's Whisper model. Please refer to [Whisper's license](https://github.com/openai/whisper) for usage terms.

## 🤝 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests.

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - The powerful STT model
- [noisereduce](https://github.com/timsainb/noisereduce) - Noise reduction library

## 🇫🇷 En Français

Ce système offre un programme **ultra puissant** de reconnaissance vocale (speech-to-text) qui:

- ✅ **Supporte tous les langages**: Plus de 99 langues supportées incluant le français, l'anglais, l'espagnol, le chinois, l'arabe, et bien d'autres
- ✅ **Ultra robuste aux bruits**: Prétraitement avancé de réduction de bruit pour gérer les environnements bruyants
- ✅ **Haute précision**: Propulsé par Whisper d'OpenAI, le modèle de pointe en reconnaissance vocale
- ✅ **Facile à utiliser**: Interface en ligne de commande simple et API Python

**Utilisation rapide:**
```bash
pip install -r requirements.txt
python stt.py audio.wav --language fr
```

Pour plus d'informations, consultez le [Guide de démarrage rapide](QUICKSTART.md).

## 📚 Additional Resources

- [Whisper Paper](https://arxiv.org/abs/2212.04356)
- [Whisper Model Card](https://github.com/openai/whisper/blob/main/model-card.md)