---
name: audio
description: Audio processing pipeline for dora-rs. Use when user asks about audio input, speech processing, voice interaction, or audio playback.
---

# Audio Processing

Audio pipeline capabilities for dora-rs dataflows.

## Overview

Build complete audio processing pipelines:

| Stage | Nodes | Purpose |
|-------|-------|---------|
| Input | dora-microphone | Capture audio from microphone |
| VAD | dora-vad | Detect voice activity |
| STT | dora-distil-whisper | Speech to text |
| LLM | dora-qwen | Process text with LLM |
| TTS | dora-kokoro-tts | Text to speech |
| Output | dora-pyaudio | Play audio through speaker |

## Complete Speech-to-Speech Pipeline

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
      CHANNELS: "1"

  # Voice activity detection
  - id: vad
    build: pip install dora-vad
    path: dora-vad
    inputs:
      audio: microphone/audio
    outputs:
      - audio        # Only when speech detected
      - speaking     # Boolean: is speaking
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

  # Language model
  - id: llm
    build: pip install dora-qwen
    path: dora-qwen
    inputs:
      text: whisper/text
    outputs:
      - text
    env:
      MODEL: Qwen2.5-1.5B-Instruct
      SYSTEM_PROMPT: "You are a helpful assistant."

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

## Audio Data Format

All audio uses float32 arrays with metadata:

```python
# Audio metadata
metadata = {
    "sample_rate": "16000",  # Sample rate in Hz
    "channels": "1",         # Number of channels
}

# Audio data: float32 array, values in [-1.0, 1.0]
import numpy as np
import pyarrow as pa

audio = np.array([0.1, 0.2, -0.1, ...], dtype=np.float32)
node.send_output("audio", pa.array(audio), metadata)
```

## Input Options

### Microphone (Default)

```yaml
- id: mic
  build: pip install dora-microphone
  path: dora-microphone
  outputs:
    - audio
  env:
    SAMPLE_RATE: "16000"
    CHUNK_SIZE: "512"
```

### From File

```yaml
- id: audio-file
  path: ./audio_file_reader.py
  inputs:
    tick: dora/timer/millis/100
  outputs:
    - audio
  env:
    FILE_PATH: /path/to/audio.wav
```

## Output Options

### PyAudio (Speaker)

```yaml
- id: speaker
  build: pip install dora-pyaudio
  path: dora-pyaudio
  inputs:
    audio: source/audio
```

### To File

```yaml
- id: recorder
  path: ./audio_recorder.py
  inputs:
    audio: source/audio
  env:
    OUTPUT_PATH: /path/to/recording.wav
```

## Processing Tips

### Sample Rate

Most speech models expect 16000 Hz:

```yaml
env:
  SAMPLE_RATE: "16000"  # 16kHz for speech
```

### Buffer Management

```python
# Accumulate audio chunks for processing
audio_buffer = []
MIN_AUDIO_LENGTH = 16000 * 2  # 2 seconds

for event in node:
    if event["id"] == "audio":
        chunk = event["value"].to_numpy()
        audio_buffer.extend(chunk)

        if len(audio_buffer) >= MIN_AUDIO_LENGTH:
            # Process accumulated audio
            process(np.array(audio_buffer))
            audio_buffer.clear()
```

### Noise Reduction

```python
import noisereduce as nr

def clean_audio(audio, sample_rate=16000):
    cleaned = nr.reduce_noise(y=audio, sr=sample_rate)
    return cleaned
```

## Latency Optimization

### Real-time Processing

```yaml
# Smaller chunks = lower latency
env:
  CHUNK_SIZE: "256"  # Small chunks
  SAMPLE_RATE: "16000"
```

### Queue Management

```yaml
inputs:
  audio:
    source: microphone/audio
    queue_size: 1  # Drop old audio
```

## Related Skills

- `voice-activity` - VAD and microphone input
- `speech-to-text` - Whisper transcription
- `text-to-speech` - Kokoro TTS
