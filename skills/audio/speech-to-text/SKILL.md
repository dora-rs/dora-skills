---
name: speech-to-text
description: Whisper-based speech recognition for dora-rs. Use when user needs speech-to-text, voice transcription, or audio transcription.
---

# Speech-to-Text with Whisper

Transcribe speech to text using Whisper models.

## Node Configuration

See [COMMON_NODES.md](../../../data/COMMON_NODES.md#whisper-speech-to-text-node) for standard Whisper configuration.

**Model selection:** See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#speech-models).

**Language options:** See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#language-configuration).

## Input/Output Format

- **Input:** Float32 audio at 16kHz. See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#audio-handling-python).
- **Output:** Transcribed text string.

## Complete STT Pipeline

```yaml
nodes:
  - id: microphone
    # See COMMON_NODES.md#microphone-node
    build: pip install dora-microphone
    path: dora-microphone
    outputs:
      - audio
    env:
      SAMPLE_RATE: "16000"

  - id: vad
    # See COMMON_NODES.md#vad-node
    build: pip install dora-vad
    path: dora-vad
    inputs:
      audio: microphone/audio
    outputs:
      - audio
    env:
      THRESHOLD: "0.5"

  - id: whisper
    # See COMMON_NODES.md#whisper-speech-to-text-node
    build: pip install dora-distil-whisper
    path: dora-distil-whisper
    inputs:
      audio: vad/audio
    outputs:
      - text
    env:
      MODEL: distil-whisper-large-v3
      LANGUAGE: en

  - id: handler
    path: ./text_handler.py
    inputs:
      text: whisper/text
```

## Processing Transcriptions

```python
# Basic text processing
text = event["value"][0].as_py().strip().lower()

# Command detection
if "hello" in text:
    print("Greeting detected!")
```

## Advanced Features

### Streaming Mode
```yaml
env:
  STREAMING: "true"
  CHUNK_LENGTH: "5"  # Seconds
```

### Timestamps
```yaml
env:
  RETURN_TIMESTAMPS: "true"
```

### Translation Mode
```yaml
env:
  TASK: translate  # Translate to English
```

## Performance Optimization

See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#device-configuration) for GPU acceleration and [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#performance-optimization-patterns) for memory optimization.

## Accuracy Tips

1. **Use VAD**: Filter silence before sending to Whisper (see [COMMON_NODES.md](../../../data/COMMON_NODES.md#vad-voice-activity-detection-node))
2. **16kHz audio**: Required sample rate
3. **Specify language**: Avoid auto-detect when language is known
4. **Clean audio**: Use noise reduction when possible

## Integration Examples

### With LLM
```yaml
- id: llm
  inputs:
    text: whisper/text
```

### Command Parser Example
```python
def parse_command(text):
    text = text.lower()
    if "turn on" in text:
        return {"action": "turn_on", "target": extract_target(text)}
    return None
```

## Related Skills

- `voice-activity` - VAD for filtering
- `text-to-speech` - Generate speech response
- `audio` - Audio pipeline overview
