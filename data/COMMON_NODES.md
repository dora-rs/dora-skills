# Common Node Configurations

Standard node configurations used across dora-skills. Reference these instead of duplicating examples.

## Camera Node

```yaml
- id: camera
  build: pip install opencv-video-capture
  path: opencv-video-capture
  inputs:
    tick: dora/timer/millis/33  # 30 FPS
  outputs:
    - image
  env:
    CAPTURE_PATH: "0"
    IMAGE_WIDTH: "640"
    IMAGE_HEIGHT: "480"
```

**Input Format:**
- Timer tick to trigger capture

**Output Format:**
- BGR8 encoded image (flattened numpy array)
- Metadata: `width`, `height`, `encoding`

**Common Variations:**
- `CAPTURE_PATH: "0"` - Default camera
- `CAPTURE_PATH: "rtsp://..."` - RTSP stream
- `IMAGE_WIDTH/HEIGHT` - Resolution (default: 640x480)

---

## YOLO Detection Node

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
    DEVICE: cuda
```

**Models:** `yolov8n.pt` (fastest) | `yolov8s.pt` | `yolov8m.pt` | `yolov8l.pt` | `yolov8x.pt` (most accurate)

**Output Format:**
```python
bbox = {
    "bbox": [x, y, w, h],
    "confidence": 0.95,
    "class": 0,
    "label": "person"
}
```

---

## Rerun Visualization Node

```yaml
- id: plot
  build: pip install dora-rerun
  path: dora-rerun
  inputs:
    image: camera/image
    boxes2d: yolo/bbox  # Optional
```

**Accepts:**
- Images (BGR8)
- Bounding boxes (2D boxes)
- Point tracks
- 3D scenes

---

## Microphone Node

```yaml
- id: microphone
  build: pip install dora-microphone
  path: dora-microphone
  outputs:
    - audio
  env:
    SAMPLE_RATE: "16000"
```

**Output:** Float32 audio array with `sample_rate` metadata

---

## VAD (Voice Activity Detection) Node

```yaml
- id: vad
  build: pip install dora-vad
  path: dora-vad
  inputs:
    audio: microphone/audio
  outputs:
    - audio
  env:
    THRESHOLD: "0.5"
```

**Function:** Filters out silence, only outputs audio chunks with speech

---

## Whisper Speech-to-Text Node

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

**Models:** `distil-whisper-small/medium/large-v3` | `whisper-tiny/base/small/medium/large-v3`

---

## Piper Text-to-Speech Node

```yaml
- id: tts
  build: pip install dora-piper
  path: dora-piper-tts
  inputs:
    text: llm/text
  outputs:
    - audio
  env:
    VOICE: en_US-lessac-medium
```

---

## SAM2 Segmentation Node

```yaml
- id: sam2
  build: pip install dora-sam2
  path: dora-sam2
  inputs:
    image: camera/image
    bbox: yolo/bbox  # Optional prompt
  outputs:
    - mask
  env:
    MODEL: sam2_hiera_small
    DEVICE: cuda
```

---

## CoTracker Tracking Node

```yaml
- id: tracker
  build: pip install dora-cotracker
  path: dora-cotracker
  inputs:
    image: camera/image
    bbox: yolo/bbox  # Optional
  outputs:
    - tracks
  env:
    DEVICE: cuda
```

---

## Piper Robot Arm Node

```yaml
- id: piper/leader
  build: pip install dora-piper
  path: dora-piper
  outputs:
    - joint_state
    - gripper_state
  env:
    ARM_TYPE: leader
    ARM_PORT: /dev/ttyUSB0
```

```yaml
- id: piper/follower
  build: pip install dora-piper
  path: dora-piper
  inputs:
    joint_state: piper/leader/joint_state
    gripper_state: piper/leader/gripper_state
  env:
    ARM_TYPE: follower
    ARM_PORT: /dev/ttyUSB1
```

---

## Timer (Built-in)

```yaml
inputs:
  tick: dora/timer/millis/100  # Trigger every 100ms
```

**Common rates:**
- `millis/33` → 30 FPS
- `millis/100` → 10 Hz
- `secs/1` → 1 Hz

---

## Common Configuration Patterns

### GPU Selection
```yaml
env:
  DEVICE: cuda      # Default CUDA GPU
  DEVICE: cuda:0    # Specific GPU
  DEVICE: cuda:1    # Second GPU
  DEVICE: mps       # Apple Silicon
  DEVICE: cpu       # CPU fallback
```

### Queue Management
```yaml
inputs:
  image:
    source: camera/image
    queue_size: 1  # Only process latest frame
```

### Real-time Optimization
```yaml
inputs:
  image:
    source: camera/image
    queue_size: 1  # Drop old frames
env:
  MODEL: yolov8n.pt  # Use fastest model
  IMAGE_WIDTH: "320"  # Reduce resolution
```
