---
name: dora-skills
description: Build AI agents, workflows, and embodied intelligence applications with dora-rs dataflow framework. Use when user asks about dataflow, AI pipelines, vision, audio, robot control, or dora commands.
---

# Dora Skills

Build AI agents, workflows, and embodied intelligence applications using the dora-rs dataflow framework.

## What is Dora?

Dora is a high-performance dataflow framework that orchestrates AI models, sensors, and actuators through declarative YAML pipelines. It enables:

- **Declarative dataflows**: Define application topology in YAML
- **Isolated nodes**: Each node runs as a separate process
- **Multi-language**: Python, Rust, C/C++ nodes in one dataflow
- **Zero-copy**: Apache Arrow format for efficient data transfer
- **10-17x faster** than equivalent ROS2 workloads

## Quick Start

```bash
# Install dora CLI
pip install dora-rs
# or
cargo install dora-cli

# Create new project
dora new my-robot --lang python

# Run a dataflow
dora run dataflow.yml
```

## Available Skills

### Core Development
| Skill | Description |
|-------|-------------|
| `core-development` | Dataflow YAML syntax and node configuration |
| `custom-node` | Create Python/Rust/C++ custom nodes |
| `cli-workflow` | Dora CLI commands and workflow |

### ML/Vision
| Skill | Description |
|-------|-------------|
| `object-detection` | YOLO-based object detection |
| `segmentation` | SAM2 instance segmentation |
| `tracking` | CoTracker point tracking |
| `vlm` | InternVL/Qwen vision-language models |

### Audio
| Skill | Description |
|-------|-------------|
| `speech-to-text` | Whisper speech recognition |
| `text-to-speech` | Kokoro TTS synthesis |
| `voice-activity` | VAD + microphone input |

### Robot Control
| Skill | Description |
|-------|-------------|
| `arm-control` | Piper/Aloha robotic arm control |
| `actuators` | Dynamixel/Feetech servo control |
| `chassis` | UGV/Robomaster mobile base |

### Data Pipeline
| Skill | Description |
|-------|-------------|
| `recording` | Data collection workflow |
| `replay` | Data playback for training |
| `lerobot` | LeRobot integration |

## Example Workflows

### Vision Detection Pipeline
```yaml
nodes:
  - id: camera
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - image

  - id: yolo
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  - id: plot
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      image: camera/image
      boxes2d: yolo/bbox
```

### Speech-to-Speech Robot
```yaml
nodes:
  - id: microphone
    build: pip install dora-microphone
    path: dora-microphone
    outputs:
      - audio

  - id: vad
    build: pip install dora-vad
    path: dora-vad
    inputs:
      audio: microphone/audio
    outputs:
      - audio

  - id: whisper
    build: pip install dora-distil-whisper
    path: dora-distil-whisper
    inputs:
      audio: vad/audio
    outputs:
      - text

  - id: llm
    build: pip install dora-qwen
    path: dora-qwen
    inputs:
      text: whisper/text
    outputs:
      - text

  - id: tts
    build: pip install dora-kokoro-tts
    path: dora-kokoro-tts
    inputs:
      text: llm/text
    outputs:
      - audio

  - id: speaker
    build: pip install dora-pyaudio
    path: dora-pyaudio
    inputs:
      audio: tts/audio
```

## Key Concepts

### Dataflow YAML Structure
```yaml
nodes:
  - id: node-name           # Unique identifier
    path: node-package      # Python package or executable path
    build: pip install ...  # Build command (optional)
    inputs:
      input_name: source_node/output_name
      tick: dora/timer/millis/100  # Timer input
    outputs:
      - output_name
    env:
      CONFIG_VAR: value     # Environment variables
```

### Node Implementation Pattern (Python)
```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT":
        data = event["value"]
        # Process data
        result = process(data)
        node.send_output("output", pa.array(result))
```

### Data Format
- All data uses Apache Arrow arrays
- Images: Flattened arrays with metadata (width, height, encoding)
- Audio: Float32/Int16 arrays with sample_rate metadata
- Structured data: Arrow StructArray

## Resources

- Documentation: https://dora-rs.ai
- GitHub: https://github.com/dora-rs/dora
- Node Hub: https://github.com/dora-rs/dora/tree/main/node-hub
- Examples: https://github.com/dora-rs/dora/tree/main/examples
