---
name: voice-activity
description: Voice activity detection and microphone input for dora-rs. Use when user needs VAD, microphone capture, or audio input filtering.
---

# Voice Activity Detection

Capture audio and detect speech using VAD (Voice Activity Detection).

## Node Configuration

**Microphone:** See [COMMON_NODES.md](../../../data/COMMON_NODES.md#microphone-node).

**VAD:** See [COMMON_NODES.md](../../../data/COMMON_NODES.md#vad-voice-activity-detection-node).

**Configuration:** See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#audio-configuration) for sample rates and [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#vad-sensitivity) for VAD threshold tuning.

## Complete VAD Pipeline

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
      - speaking

  - id: whisper
    # See COMMON_NODES.md#whisper-speech-to-text-node
    build: pip install dora-distil-whisper
    path: dora-distil-whisper
    inputs:
      audio: vad/audio
    outputs:
      - text

  - id: indicator
    path: ./speaking_indicator.py
    inputs:
      speaking: vad/speaking
```

## Handling VAD Output

### Speech Audio

See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#audio-handling-python) for audio handling.

### Speaking Indicator

```python
is_speaking = event["value"][0].as_py()
if is_speaking:
    print("Speech detected")
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

See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#vad-sensitivity) for threshold configuration based on environment.

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
