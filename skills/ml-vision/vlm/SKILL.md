---
name: vlm
description: Vision-Language Models (InternVL, Qwen VL) for dora-rs. Use when user needs image understanding, visual question answering, image captioning, or multimodal AI.
---

# Vision-Language Models

Integrate Vision-Language Models (VLM) for image understanding and visual reasoning.

## Available VLM Nodes

| Node | Model | Best For |
|------|-------|----------|
| `dora-internvl` | InternVL | General VQA, detailed descriptions |
| `dora-qwenvl` | Qwen2-VL | Chinese/English, multi-image |
| `dora-qwen` | Qwen2.5 | Text-only LLM (pair with vision) |

## InternVL Configuration

```yaml
- id: vlm
  build: pip install dora-internvl
  path: dora-internvl
  inputs:
    image: camera/image
    text: prompt/question
  outputs:
    - text
  env:
    MODEL: InternVL2-2B        # Model size
    DEVICE: cuda               # cuda, mps, or cpu
    MAX_NEW_TOKENS: "512"
```

## Qwen VL Configuration

```yaml
- id: vlm
  build: pip install dora-qwenvl
  path: dora-qwenvl
  inputs:
    image: camera/image
    text: prompt/question
  outputs:
    - text
  env:
    MODEL: Qwen2-VL-2B-Instruct
    DEVICE: cuda
```

## Model Options

### InternVL

| Model | Size | VRAM |
|-------|------|------|
| `InternVL2-1B` | 1B | ~4GB |
| `InternVL2-2B` | 2B | ~6GB |
| `InternVL2-4B` | 4B | ~10GB |
| `InternVL2-8B` | 8B | ~18GB |

### Qwen VL

| Model | Size | VRAM |
|-------|------|------|
| `Qwen2-VL-2B-Instruct` | 2B | ~6GB |
| `Qwen2-VL-7B-Instruct` | 7B | ~16GB |

## Complete VLM Pipeline

```yaml
nodes:
  # Camera input
  - id: camera
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/500  # Slow for VLM
    outputs:
      - image
    env:
      CAPTURE_PATH: "0"

  # Prompt generator (static or dynamic)
  - id: prompt
    path: ./prompt_generator.py
    inputs:
      tick: dora/timer/millis/1000
    outputs:
      - question

  # Vision-language model
  - id: vlm
    build: pip install dora-internvl
    path: dora-internvl
    inputs:
      image: camera/image
      text: prompt/question
    outputs:
      - text

  # Output handler
  - id: output
    path: ./output_handler.py
    inputs:
      text: vlm/text
```

## Prompt Generator Examples

### Static Prompt

```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT" and event["id"] == "tick":
        question = "Describe what you see in this image."
        node.send_output("question", pa.array([question]))
```

### Scene Understanding

```python
prompts = [
    "What objects are visible in this image?",
    "Describe the scene in detail.",
    "Are there any people? What are they doing?",
    "What is the main activity happening?",
]

prompt_index = 0

for event in node:
    if event["type"] == "INPUT":
        question = prompts[prompt_index % len(prompts)]
        prompt_index += 1
        node.send_output("question", pa.array([question]))
```

### Robot Task Planning

```python
# Ask VLM to help with robot tasks
task_prompts = {
    "identify": "What objects can you see that I could pick up?",
    "locate": "Where is the red cup located in the image?",
    "plan": "How should I approach to pick up the nearest object?",
    "safety": "Are there any obstacles or hazards in the scene?",
}

def get_task_prompt(task_type):
    return task_prompts.get(task_type, "Describe what you see.")
```

## Processing VLM Output

```python
from dora import Node

node = Node()

for event in node:
    if event["type"] == "INPUT" and event["id"] == "text":
        response = event["value"][0].as_py()
        print(f"VLM says: {response}")

        # Parse structured responses
        if "pick up" in response.lower():
            # Extract object name
            # Send robot command
            pass
```

## Multi-Image Reasoning

Some VLMs support multiple images:

```yaml
- id: vlm
  path: dora-qwenvl
  inputs:
    image1: camera1/image
    image2: camera2/image
    text: prompt/question
  outputs:
    - text
```

```python
# Prompt for comparing images
question = "Compare these two images. What changed between them?"
```

## VLM + Detection Pipeline

Combine VLM with object detection:

```yaml
nodes:
  - id: camera
    # ... camera config

  - id: yolo
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  - id: prompt-generator
    path: ./detection_to_prompt.py
    inputs:
      bbox: yolo/bbox
    outputs:
      - question

  - id: vlm
    build: pip install dora-internvl
    path: dora-internvl
    inputs:
      image: camera/image
      text: prompt-generator/question
    outputs:
      - text
```

**detection_to_prompt.py:**
```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["id"] == "bbox":
        detections = event["value"]
        labels = [d["label"] for d in detections]

        if labels:
            objects = ", ".join(set(labels))
            question = f"I detected: {objects}. Can you describe what they are doing?"
        else:
            question = "Describe what you see in this image."

        node.send_output("question", pa.array([question]))
```

## Performance Optimization

### Reduce Inference Frequency

```yaml
inputs:
  tick: dora/timer/millis/1000  # 1 FPS for VLM
```

### Use Smaller Models

```yaml
env:
  MODEL: InternVL2-1B  # Smallest, fastest
```

### Quantization

```yaml
env:
  QUANTIZATION: int4   # 4-bit quantization
```

## Use Cases

### Scene Description

```python
prompt = "Describe this scene in one sentence."
# Output: "A person sitting at a desk working on a laptop computer."
```

### Object Counting

```python
prompt = "How many people are in this image?"
# Output: "There are 3 people in the image."
```

### Action Recognition

```python
prompt = "What action is the person performing?"
# Output: "The person is waving their hand."
```

### Safety Assessment

```python
prompt = "Is it safe for a robot to move forward based on this view?"
# Output: "No, there is an obstacle directly ahead."
```

## Related Skills

- `object-detection` - Combine with YOLO
- `speech-to-text` - Voice-controlled VLM queries
- `arm-control` - Execute VLM-planned actions
