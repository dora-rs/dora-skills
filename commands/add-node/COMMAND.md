---
name: add-node
description: Add a pre-configured node to an existing dataflow
---

# /add-node Command

Add a node to an existing dataflow.yml file.

## Usage

```
/add-node <node-type> [--to <dataflow-file>] [--connect <source>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<node-type>` | Type of node to add | required |
| `--to` | Dataflow file path | ./dataflow.yml |
| `--connect` | Auto-connect to source | - |

## Available Node Types

### Sensors
- `camera` - OpenCV video capture
- `microphone` - Audio input
- `realsense` - Intel RealSense
- `keyboard` - Keyboard input

### Vision
- `yolo` - Object detection
- `sam2` - Segmentation
- `cotracker` - Point tracking
- `internvl` - Vision-language model
- `qwenvl` - Qwen Vision-Language

### Audio
- `vad` - Voice activity detection
- `whisper` - Speech to text
- `kokoro-tts` - Text to speech
- `speaker` - Audio output

### Language
- `qwen` - Qwen LLM

### Robot
- `piper` - Piper arm
- `dynamixel` - Dynamixel servos
- `feetech` - Feetech servos

### Visualization
- `rerun` - 3D visualization
- `opencv-plot` - OpenCV display

### Data
- `recorder` - Data recording
- `replay` - Data replay

## Examples

### Add YOLO detector

```
/add-node yolo --connect camera/image
```

Adds:
```yaml
- id: yolo
  build: pip install dora-yolo
  path: dora-yolo
  inputs:
    image: camera/image
  outputs:
    - bbox
  env:
    MODEL: yolov8n.pt
    CONFIDENCE: "0.5"
```

### Add TTS to audio pipeline

```
/add-node kokoro-tts --connect llm/text
```

Adds:
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
```

### Add visualization

```
/add-node rerun --connect camera/image,yolo/bbox
```

Adds:
```yaml
- id: rerun
  build: pip install dora-rerun
  path: dora-rerun
  inputs:
    image: camera/image
    boxes2d: yolo/bbox
```

## Workflow

1. Read existing dataflow.yml
2. Generate node configuration
3. Auto-wire connections if --connect specified
4. Append node to dataflow
5. Save updated file

## Connection Inference

Without --connect, the command will:
1. Analyze existing nodes
2. Suggest compatible sources
3. Ask user to confirm

## Validation

Before adding, the command checks:
- Node type is valid
- Source nodes exist
- Output types are compatible
- No duplicate node IDs

## Customization

After adding, you can modify:
- Node ID
- Environment variables
- Additional inputs
- Output names
