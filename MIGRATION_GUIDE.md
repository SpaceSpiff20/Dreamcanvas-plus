# Speechify TTS Migration Guide

This document outlines the migration from ElevenLabs to Speechify TTS API in the DreamCanvas+ application.

## Overview

The migration replaces the ElevenLabs TTS provider with Speechify's API while maintaining backward compatibility. The new implementation provides:

- **Enhanced multilingual support** with 23+ languages
- **Better voice quality** with advanced audio processing
- **Flexible voice selection** with filtering capabilities
- **Backward compatibility** with existing ElevenLabs integration

## Changes Made

### 1. New Files Created

- `utils/speechify_voice.py` - Core Speechify TTS implementation
- `utils/tts_wrapper.py` - Unified wrapper supporting both providers
- `test_speechify_migration.py` - Comprehensive test suite
- `test_migration_simple.py` - Simple verification script
- `MIGRATION_GUIDE.md` - This documentation

### 2. Files Modified

- `app.py` - Updated to use new TTS wrapper
- `requirements.txt` - Added `speechify-api` dependency

### 3. Files Unchanged (Backward Compatibility)

- `utils/elevenlabs_voice.py` - Original ElevenLabs implementation preserved

## Installation

### 1. Install Speechify API

```bash
pip install speechify-api
```

Or update your requirements:

```bash
pip install -r requirements.txt
```

### 2. Get Speechify API Key

1. Sign up at [Speechify Console](https://console.sws.speechify.com/signup)
2. Get your API key from the dashboard
3. Set environment variable:

```bash
export SPEECHIFY_API_KEY="your_api_key_here"
```

## Usage

### Basic Usage

The migration maintains the same interface. Your existing code will work with minimal changes:

```python
# Old ElevenLabs usage
from utils.elevenlabs_voice import elevenlabs_tts
audio_path = elevenlabs_tts(text, voice_id, api_key)

# New unified usage (recommended)
from utils.tts_wrapper import tts_convert
audio_path = tts_convert(
    text=text,
    voice_id="scott",  # Default Speechify voice
    provider="speechify"
)
```

### Advanced Usage

```python
from utils.tts_wrapper import tts_convert

# English with specific voice
audio_path = tts_convert(
    text="Hello, world!",
    voice_id="scott",
    provider="speechify",
    language="en-US",
    model="simba-english"
)

# French with multilingual model
audio_path = tts_convert(
    text="Bonjour, le monde!",
    voice_id="scott",
    provider="speechify",
    language="fr-FR",
    model="simba-multilingual"
)
```

### Voice Management

```python
from utils.speechify_voice import get_available_voices, filter_voice_models

# Get all available voices
voices = get_available_voices()

# Filter voices by criteria
male_voices = filter_voice_models(voices, gender="male")
english_voices = filter_voice_models(voices, locale="en-US")
deep_voices = filter_voice_models(voices, tags=["timbre:deep"])
```

## Configuration

### Environment Variables

- `SPEECHIFY_API_KEY` - Your Speechify API key (required)
- `TTS_PROVIDER` - Set to "speechify" or "elevenlabs" (default: "speechify")

### Provider Selection

You can switch between providers using the environment variable:

```bash
# Use Speechify (default)
export TTS_PROVIDER="speechify"

# Use ElevenLabs (if available)
export TTS_PROVIDER="elevenlabs"
```

## Testing

### Quick Test

Run the simple test script to verify the migration:

```bash
python test_migration_simple.py
```

### Comprehensive Tests

Run the full test suite:

```bash
# Install pytest if not already installed
pip install pytest

# Run all tests
pytest test_speechify_migration.py -v

# Run only unit tests (no API key required)
pytest test_speechify_migration.py -v -m "not integration"

# Run integration tests (requires API key)
pytest test_speechify_migration.py -v -m "integration"
```

## Language Support

### Fully Supported Languages

| Language              | Code  |
|-----------------------|-------|
| English               | en    |
| French                | fr-FR |
| German                | de-DE |
| Spanish               | es-ES |
| Portuguese (Brazil)   | pt-BR |
| Portuguese (Portugal) | pt-PT |

### Beta Languages

| Language   | Code  |
|------------|-------|
| Arabic     | ar-AE |
| Danish     | da-DK |
| Dutch      | nl-NL |
| Estonian   | et-EE |
| Finnish    | fi-FI |
| Greek      | el-GR |
| Hebrew     | he-IL |
| Hindi      | hi-IN |
| Italian    | it-IT |
| Japanese   | ja-JP |
| Norwegian  | nb-NO |
| Polish     | pl-PL |
| Russian    | ru-RU |
| Swedish    | sv-SE |
| Turkish    | tr-TR |
| Ukrainian  | uk-UA |
| Vietnamese | vi-VN |

## API Comparison

### ElevenLabs vs Speechify

| Feature | ElevenLabs | Speechify |
|---------|------------|-----------|
| Languages | 29+ | 23+ |
| Voice Models | 2 | 2 (simba-english, simba-multilingual) |
| Audio Formats | Multiple | 4 (aac, mp3, ogg, wav) |
| Voice Filtering | Limited | Advanced (gender, locale, tags) |
| Speech Marks | No | Yes |
| Loudness Normalization | No | Yes |
| Text Normalization | No | Yes |

### Functionality Mapping

| ElevenLabs | Speechify Equivalent |
|------------|---------------------|
| `voice_id` | `voice_id` |
| `text` | `input` |
| `model_id` | `model` |
| `output_format` | `audio_format` |
| N/A | `language` |
| N/A | `options` (loudness_normalization, text_normalization) |

## Troubleshooting

### Common Issues

1. **Import Error: No module named 'speechify'**
   ```bash
   pip install speechify-api
   ```

2. **API Key Error**
   ```bash
   export SPEECHIFY_API_KEY="your_api_key_here"
   ```

3. **Voice Not Found**
   - Use "scott" as the default voice
   - Check available voices with `get_available_voices()`

4. **Language Not Supported**
   - Use "simba-multilingual" model for beta languages
   - Omit `language` parameter for auto-detection

### Error Messages

- `"Speechify API key not provided"` - Set `SPEECHIFY_API_KEY` environment variable
- `"Unsupported TTS provider"` - Use "speechify" or "elevenlabs" as provider
- `"Voice not found"` - Use a valid voice ID from `get_available_voices()`

## Migration Checklist

- [ ] Install `speechify-api` package
- [ ] Get Speechify API key
- [ ] Set `SPEECHIFY_API_KEY` environment variable
- [ ] Run `python test_migration_simple.py`
- [ ] Test your application with `streamlit run app.py`
- [ ] Verify audio quality and voice selection
- [ ] Test multilingual functionality if needed

## Backward Compatibility

The migration maintains full backward compatibility:

- Original ElevenLabs code continues to work
- Existing voice IDs can be mapped to Speechify equivalents
- Environment variable controls provider selection
- Gradual migration is supported

## Performance Notes

- Speechify API responses include speech marks for timing information
- Audio quality is enhanced with loudness and text normalization
- Multilingual model provides better language detection
- Voice filtering enables more precise voice selection

## Support

For issues with the migration:

1. Check this migration guide
2. Run the test scripts
3. Verify your API key and environment variables
4. Check Speechify documentation at [console.sws.speechify.com](https://console.sws.speechify.com)

For Speechify API issues, contact Speechify support through their console. 