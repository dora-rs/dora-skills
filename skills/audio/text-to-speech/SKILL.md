---
name: text-to-speech
description: Text-to-speech synthesis for dora-rs. Use when user needs TTS, voice synthesis, or converting text to audio.
---

# Text-to-Speech with Kokoro

Generate natural speech from text using Kokoro TTS.

## Node Configuration

See [COMMON_NODES.md](../../../data/COMMON_NODES.md#piper-text-to-speech-node) for standard TTS configuration.

**Kokoro TTS variant:**
```yaml
- id: tts
  build: pip install dora-kokoro-tts
  path: dora-kokoro-tts
  inputs:
    text: llm/text
  outputs:
    - audio
  env:
    VOICE: af_bella
    SPEED: "1.0"
    SAMPLE_RATE: "24000"
```

## Voice Options

### American English

| Voice | Description |
|-------|-------------|
| `af_bella` | Female, warm and clear |
| `af_sarah` | Female, professional |
| `am_adam` | Male, neutral |
| `am_michael` | Male, deep voice |

### British English

| Voice | Description |
|-------|-------------|
| `bf_emma` | Female, British accent |
| `bm_george` | Male, British accent |

### Chinese

| Voice | Description |
|-------|-------------|
| `zf_xiaoxiao` | Female, Mandarin |
| `zm_yunxi` | Male, Mandarin |

## Configuration Options

```yaml
env:
  VOICE: af_bella         # Voice selection
  SPEED: "1.0"           # Speech speed (0.5 - 2.0)
  SAMPLE_RATE: "24000"   # Output sample rate
  DEVICE: cuda           # cuda, mps, or cpu
```

## Input/Output Format

- **Input:** Text string
- **Output:** Float32 audio with sample_rate metadata. See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#audio-handling-python).

## Complete TTS Pipeline

```yaml
nodes:
  # Text source (from LLM or other)
  - id: llm
    build: pip install dora-qwen
    path: dora-qwen
    inputs:
      text: input/text
    outputs:
      - text

  # Text to speech
  - id: tts
    build: pip install dora-kokoro-tts
    path: dora-kokoro-tts
    inputs:
      text: llm/text
    outputs:
      - audio
    env:
      VOICE: af_bella
      SPEED: "1.0"

  # Audio playback
  - id: speaker
    build: pip install dora-pyaudio
    path: dora-pyaudio
    inputs:
      audio: tts/audio
```

## Text Preprocessing

```python
def preprocess_text(text):
    """Prepare text for TTS."""
    # Remove special characters
    import re
    text = re.sub(r'[^\w\s.,!?-]', '', text)

    # Expand abbreviations
    abbreviations = {
        "Dr.": "Doctor",
        "Mr.": "Mister",
        "Mrs.": "Misses",
        "etc.": "etcetera",
    }
    for abbr, full in abbreviations.items():
        text = text.replace(abbr, full)

    return text
```

## Long Text Handling

For long texts, split into sentences:

```python
import re

def split_sentences(text):
    """Split text into sentences for smoother TTS."""
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return sentences

# Send sentences one by one
for sentence in split_sentences(long_text):
    node.send_output("text", pa.array([sentence]))
    time.sleep(0.1)  # Small delay between sentences
```

## Streaming Mode

For real-time synthesis:

```yaml
env:
  STREAMING: "true"
  CHUNK_SIZE: "512"
```

## Emotion Control

Some voices support emotion:

```yaml
env:
  VOICE: af_bella
  EMOTION: happy    # happy, sad, angry, neutral
```

Or embed in text:

```python
# SSML-like markers
text = "[happy] Great news! [neutral] The weather is nice today."
```

## Alternative TTS Nodes

### Parler TTS

```yaml
- id: tts
  build: pip install dora-parler-tts
  path: dora-parler-tts
  inputs:
    text: source/text
  outputs:
    - audio
  env:
    DESCRIPTION: "A female speaker with a warm, friendly voice"
```

### OuteTTS

```yaml
- id: tts
  build: pip install dora-outetts
  path: dora-outetts
  inputs:
    text: source/text
  outputs:
    - audio
```

## Multilingual Support

Automatic language detection:

```yaml
env:
  LANGUAGE: auto  # Detect language automatically
```

Or specify:

```yaml
env:
  LANGUAGE: en    # English
  LANGUAGE: zh    # Chinese
```

## Performance Optimization

See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#device-configuration) for GPU acceleration.

## Quality Settings

### High Quality

```yaml
env:
  QUALITY: high
  SAMPLE_RATE: "48000"
```

### Low Latency

```yaml
env:
  QUALITY: fast
  SAMPLE_RATE: "16000"
```

## Saving Audio

```python
import scipy.io.wavfile as wav

def save_audio(audio, sample_rate, filename):
    """Save audio to WAV file."""
    wav.write(filename, sample_rate, audio)
```

## Integration Examples

### Voice Assistant

```yaml
nodes:
  - id: whisper    # STT
  - id: llm        # Process
  - id: tts        # TTS
  - id: speaker    # Output
```

### Notification System

```python
def announce(message):
    """Convert text notification to speech."""
    node.send_output("text", pa.array([message]))
```

## Related Skills

- `speech-to-text` - Whisper transcription
- `audio` - Audio pipeline overview
- `voice-activity` - VAD input
