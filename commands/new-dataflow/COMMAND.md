---
name: new-dataflow
description: Create a new dora dataflow project with common templates
---

# /new-dataflow Command

Create a new dora dataflow project with pre-configured templates.

## Usage

```
/new-dataflow <name> [--type <template>] [--lang <language>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<name>` | Project name | required |
| `--type` | Template type | basic |
| `--lang` | Language | python |

## Templates

### basic
Simple camera + visualization:
```yaml
nodes:
  - id: camera
  - id: visualize
```

### vision
Object detection pipeline:
```yaml
nodes:
  - id: camera
  - id: detector
  - id: visualize
```

### audio
Speech-to-speech pipeline:
```yaml
nodes:
  - id: microphone
  - id: vad
  - id: whisper
  - id: llm
  - id: tts
  - id: speaker
```

### robot
Robot teleoperation:
```yaml
nodes:
  - id: leader
  - id: follower
  - id: camera
  - id: recorder
```

### vlm
Vision-language interaction:
```yaml
nodes:
  - id: camera
  - id: vlm
  - id: visualize
```

## Workflow

1. Create project directory
2. Generate dataflow.yml from template
3. Create custom node stubs if needed
4. Print next steps

## Example

```
/new-dataflow my-robot --type vision
```

Creates:
```
my-robot/
├── dataflow.yml
└── README.md
```

With dataflow.yml:
```yaml
nodes:
  - id: camera
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/33
    outputs:
      - image
    env:
      CAPTURE_PATH: "0"
      IMAGE_WIDTH: "640"
      IMAGE_HEIGHT: "480"

  - id: detector
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox
    env:
      MODEL: yolov8n.pt

  - id: visualize
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      image: camera/image
      boxes2d: detector/bbox
```

## Next Steps

After creating:
```bash
cd my-robot
dora build dataflow.yml --uv
dora run dataflow.yml
```

## Custom Templates

Create custom templates by modifying the generated dataflow.yml:

1. Add/remove nodes
2. Adjust environment variables
3. Change connections
4. Add custom nodes
