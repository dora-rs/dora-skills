---
name: speech-to-text
description: Whisper-based speech recognition for dora-rs. Use when user needs speech-to-text, voice transcription, or audio transcription.
---

# Speech-to-Text with Whisper

Transcribe speech to text using Whisper models.

## Node Configuration

```yaml
- id: whisper
  build: pip install dora-distil-whisper
  path: dora-distil-whisper
  inputs:
    audio: vad/audio
  outputs:
    - text
  env:
    MODEL: distil-whisper-large-v3
    LANGUAGE: en
    DEVICE: cuda
```

## Model Options

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `distil-whisper-small` | Small | Fast | Good |
| `distil-whisper-medium` | Medium | Balanced | Better |
| `distil-whisper-large-v3` | Large | Slower | Best |
| `whisper-tiny` | Tiny | Fastest | Basic |
| `whisper-base` | Base | Fast | Good |
| `whisper-small` | Small | Balanced | Better |
| `whisper-medium` | Medium | Slower | High |
| `whisper-large-v3` | Large | Slowest | Best |

## Platform-Specific Models

### macOS (MLX)

```yaml
env:
  MODEL: mlx-community/distil-whisper-large-v3
  BACKEND: mlx  # Apple Silicon optimized
```

### Linux (Transformers)

```yaml
env:
  MODEL: distil-whisper-large-v3
  BACKEND: transformers
  DEVICE: cuda
```

## Language Configuration

```yaml
env:
  # Single language (faster, more accurate)
  LANGUAGE: en    # English
  LANGUAGE: zh    # Chinese
  LANGUAGE: ja    # Japanese
  LANGUAGE: ko    # Korean

  # Auto-detect (slower)
  LANGUAGE: auto
```

## Input Format

Audio chunks from VAD or microphone:

```python
# Expected format
metadata = {
    "sample_rate": "16000"  # 16kHz required
}

# Audio: float32 array
audio = np.array([...], dtype=np.float32)
```

## Output Format

Transcribed text:

```python
for event in node:
    if event["id"] == "text":
        transcription = event["value"][0].as_py()
        print(f"Heard: {transcription}")
```

## Complete STT Pipeline

```yaml
nodes:
  # Microphone input
  - id: microphone
    build: pip install dora-microphone
    path: dora-microphone
    outputs:
      - audio
    env:
      SAMPLE_RATE: "16000"

  # Voice activity detection
  - id: vad
    build: pip install dora-vad
    path: dora-vad
    inputs:
      audio: microphone/audio
    outputs:
      - audio
    env:
      THRESHOLD: "0.5"

  # Speech to text
  - id: whisper
    build: pip install dora-distil-whisper
    path: dora-distil-whisper
    inputs:
      audio: vad/audio
    outputs:
      - text
    env:
      MODEL: distil-whisper-large-v3
      LANGUAGE: en

  # Process transcription
  - id: handler
    path: ./text_handler.py
    inputs:
      text: whisper/text
```

## Processing Transcriptions

```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT" and event["id"] == "text":
        text = event["value"][0].as_py()

        # Clean transcription
        text = text.strip().lower()

        # Command detection
        if "hello" in text:
            print("Greeting detected!")

        # Keyword extraction
        keywords = extract_keywords(text)

        # Send processed text
        node.send_output("processed", pa.array([text]))
```

## Filtering and Cleaning

```python
def clean_transcription(text):
    """Clean Whisper output."""
    # Remove filler words
    fillers = ["um", "uh", "er", "ah"]
    for filler in fillers:
        text = text.replace(f" {filler} ", " ")

    # Remove repeated words
    words = text.split()
    cleaned = []
    for word in words:
        if not cleaned or word != cleaned[-1]:
            cleaned.append(word)

    return " ".join(cleaned)
```

## Streaming Mode

For real-time transcription:

```yaml
env:
  STREAMING: "true"
  CHUNK_LENGTH: "5"  # Seconds
```

## Timestamps

Get word-level timestamps:

```yaml
env:
  RETURN_TIMESTAMPS: "true"
```

```python
# Output includes timestamps
output = {
    "text": "Hello world",
    "timestamps": [
        {"word": "Hello", "start": 0.0, "end": 0.5},
        {"word": "world", "start": 0.6, "end": 1.0}
    ]
}
```

## Translation Mode

Translate non-English audio to English:

```yaml
env:
  TASK: translate  # Translate to English
  # or
  TASK: transcribe  # Keep original language
```

## Performance Optimization

### GPU Acceleration

```yaml
env:
  DEVICE: cuda
  # Specific GPU
  DEVICE: cuda:0
```

### Batch Processing

```yaml
env:
  BATCH_SIZE: "4"  # Process multiple chunks
```

### Memory Optimization

```yaml
env:
  MODEL: distil-whisper-small  # Smaller model
  FP16: "true"                 # Half precision
```

## Accuracy Tips

1. **Use VAD**: Filter silence before sending to Whisper
2. **16kHz audio**: Resample if necessary
3. **Specify language**: Don't use auto-detect if you know the language
4. **Clean audio**: Use noise reduction when possible

## Integration Examples

### With LLM

```yaml
- id: llm
  inputs:
    text: whisper/text
```

### With Command Parser

```python
def parse_command(text):
    text = text.lower()
    if "turn on" in text:
        return {"action": "turn_on", "target": extract_target(text)}
    elif "turn off" in text:
        return {"action": "turn_off", "target": extract_target(text)}
    return None
```

## Related Skills

- `voice-activity` - VAD for filtering
- `text-to-speech` - Generate speech response
- `audio` - Audio pipeline overview
