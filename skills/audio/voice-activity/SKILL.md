---
name: voice-activity
description: Voice activity detection and microphone input for dora-rs. Use when user needs VAD, microphone capture, or audio input filtering.
---

# Voice Activity Detection

Capture audio and detect speech using VAD (Voice Activity Detection).

## Microphone Node

```yaml
- id: microphone
  build: pip install dora-microphone
  path: dora-microphone
  outputs:
    - audio
  env:
    SAMPLE_RATE: "16000"
    CHANNELS: "1"
    CHUNK_SIZE: "512"
    DEVICE_INDEX: "0"
```

## VAD Node (Silero)

```yaml
- id: vad
  build: pip install dora-vad
  path: dora-vad
  inputs:
    audio: microphone/audio
  outputs:
    - audio        # Audio chunks when speech detected
    - speaking     # Boolean indicator
  env:
    THRESHOLD: "0.5"
    MIN_SPEECH_DURATION: "0.25"
    MAX_SPEECH_DURATION: "30.0"
    SPEECH_PAD_MS: "300"
```

## Configuration Options

### Microphone

| Option | Description | Default |
|--------|-------------|---------|
| `SAMPLE_RATE` | Samples per second | 16000 |
| `CHANNELS` | Audio channels | 1 |
| `CHUNK_SIZE` | Samples per chunk | 512 |
| `DEVICE_INDEX` | Microphone device | 0 |

### VAD

| Option | Description | Default |
|--------|-------------|---------|
| `THRESHOLD` | Speech detection threshold (0-1) | 0.5 |
| `MIN_SPEECH_DURATION` | Min speech length (seconds) | 0.25 |
| `MAX_SPEECH_DURATION` | Max speech length (seconds) | 30.0 |
| `SPEECH_PAD_MS` | Padding around speech (ms) | 300 |

## Complete VAD Pipeline

```yaml
nodes:
  # Audio capture
  - id: microphone
    build: pip install dora-microphone
    path: dora-microphone
    outputs:
      - audio
    env:
      SAMPLE_RATE: "16000"
      CHUNK_SIZE: "512"

  # Voice activity detection
  - id: vad
    build: pip install dora-vad
    path: dora-vad
    inputs:
      audio: microphone/audio
    outputs:
      - audio      # Filtered audio (speech only)
      - speaking   # Speaking indicator

  # Speech to text (only processes speech)
  - id: whisper
    build: pip install dora-distil-whisper
    path: dora-distil-whisper
    inputs:
      audio: vad/audio
    outputs:
      - text

  # Speaking indicator handler
  - id: indicator
    path: ./speaking_indicator.py
    inputs:
      speaking: vad/speaking
```

## Handling VAD Output

### Speech Audio

```python
from dora import Node
import numpy as np

node = Node()

for event in node:
    if event["id"] == "audio":
        # Speech audio chunk
        audio = event["value"].to_numpy()
        sample_rate = int(event["metadata"]["sample_rate"])

        # Process speech audio
        process_speech(audio, sample_rate)
```

### Speaking Indicator

```python
for event in node:
    if event["id"] == "speaking":
        is_speaking = event["value"][0].as_py()

        if is_speaking:
            print("Speech detected - listening...")
        else:
            print("Silence detected - waiting...")
```

## Speaking Indicator Node

```python
# speaking_indicator.py
from dora import Node

node = Node()
was_speaking = False

for event in node:
    if event["id"] == "speaking":
        is_speaking = event["value"][0].as_py()

        if is_speaking and not was_speaking:
            print("Started speaking")
            # Could trigger UI update, LED, etc.

        elif not is_speaking and was_speaking:
            print("Stopped speaking")
            # Could trigger processing

        was_speaking = is_speaking
```

## Threshold Tuning

```yaml
env:
  # Higher threshold = less false positives (stricter)
  THRESHOLD: "0.7"

  # Lower threshold = more sensitive (may include noise)
  THRESHOLD: "0.3"
```

## Noise Environments

### Noisy Environment

```yaml
env:
  THRESHOLD: "0.7"           # Higher threshold
  MIN_SPEECH_DURATION: "0.5" # Longer minimum
```

### Quiet Environment

```yaml
env:
  THRESHOLD: "0.3"           # Lower threshold
  MIN_SPEECH_DURATION: "0.1" # Shorter minimum
```

## Device Selection

List available microphones:

```python
import sounddevice as sd
print(sd.query_devices())
```

Select specific device:

```yaml
env:
  DEVICE_INDEX: "2"  # Use device index 2
```

## Audio Buffer Management

```python
# Accumulate speech segments
speech_buffer = []
is_speaking = False

for event in node:
    if event["id"] == "speaking":
        now_speaking = event["value"][0].as_py()

        if is_speaking and not now_speaking:
            # Speech ended, process buffer
            if speech_buffer:
                full_audio = np.concatenate(speech_buffer)
                process_complete_utterance(full_audio)
                speech_buffer.clear()

        is_speaking = now_speaking

    elif event["id"] == "audio" and is_speaking:
        # Accumulate speech audio
        audio = event["value"].to_numpy()
        speech_buffer.append(audio)
```

## Continuous Listening

```python
# Process speech continuously
for event in node:
    if event["id"] == "audio":
        # VAD already filtered - this is speech
        audio = event["value"].to_numpy()

        # Send to transcription immediately
        node.send_output("speech", event["value"], event["metadata"])
```

## Energy-Based Fallback

Simple energy-based VAD for testing:

```python
import numpy as np

def simple_vad(audio, threshold=0.01):
    """Simple energy-based VAD."""
    energy = np.sqrt(np.mean(audio ** 2))
    return energy > threshold
```

## Push-to-Talk Mode

For controlled recording:

```yaml
nodes:
  - id: keyboard
    build: pip install dora-keyboard
    path: dora-keyboard
    outputs:
      - keypress

  - id: microphone
    build: pip install dora-microphone
    path: dora-microphone
    inputs:
      trigger: keyboard/keypress  # Only record when key pressed
    outputs:
      - audio
```

## Performance Tips

1. **Sample rate**: Use 16000 Hz for speech processing
2. **Chunk size**: Smaller = lower latency, larger = more stable
3. **Threshold**: Start at 0.5, adjust based on environment
4. **Buffer**: Accumulate until speech ends for better transcription

## Debugging

```python
# Log VAD statistics
speech_segments = 0
total_audio_seconds = 0

for event in node:
    if event["id"] == "speaking":
        if event["value"][0].as_py():
            speech_segments += 1

    elif event["id"] == "audio":
        audio = event["value"].to_numpy()
        sample_rate = int(event["metadata"]["sample_rate"])
        total_audio_seconds += len(audio) / sample_rate

# Print statistics periodically
print(f"Speech segments: {speech_segments}")
print(f"Total speech: {total_audio_seconds:.1f}s")
```

## Related Skills

- `speech-to-text` - Whisper transcription
- `text-to-speech` - Kokoro TTS
- `audio` - Audio pipeline overview
