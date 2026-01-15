---
name: ml-vision
description: Computer vision and ML capabilities for dora-rs. Use when user asks about vision pipelines, image processing, ML nodes, object detection, or camera integration.
---

# ML/Vision

Computer vision and machine learning capabilities for dora-rs dataflows.

## Overview

Dora provides a rich ecosystem of vision nodes for building perception pipelines:

| Category | Nodes | Purpose |
|----------|-------|---------|
| Input | opencv-video-capture, kornia-webcam, pyrealsense, pyorbbec | Camera capture |
| Detection | dora-yolo | Object detection with bounding boxes |
| Segmentation | dora-sam2 | Instance segmentation with masks |
| Tracking | dora-cotracker | Point tracking across frames |
| VLM | dora-internvl, dora-qwenvl | Vision-language understanding |
| Visualization | dora-rerun, opencv-plot | Display and debugging |

## Camera Input Options

### OpenCV Video Capture

```yaml
- id: camera
  build: pip install opencv-video-capture
  path: opencv-video-capture
  inputs:
    tick: dora/timer/millis/33  # ~30 FPS
  outputs:
    - image
  env:
    CAPTURE_PATH: "0"           # Camera index or video file
    IMAGE_WIDTH: "640"
    IMAGE_HEIGHT: "480"
```

### Intel RealSense

```yaml
- id: realsense
  build: pip install dora-pyrealsense
  path: dora-pyrealsense
  inputs:
    tick: dora/timer/millis/33
  outputs:
    - image
    - depth
```

### Orbbec Camera

```yaml
- id: orbbec
  build: pip install dora-pyorbbec
  path: dora-pyorbbec
  inputs:
    tick: dora/timer/millis/33
  outputs:
    - image
    - depth
```

## Image Format Convention

All images use flattened numpy arrays with metadata:

```python
# Metadata fields
metadata = {
    "width": "640",
    "height": "480",
    "encoding": "bgr8"  # or "rgb8", "gray8", "jpeg", etc.
}

# Supported encodings
# bgr8  - OpenCV default (3 channels, uint8)
# rgb8  - RGB format (3 channels, uint8)
# gray8 - Grayscale (1 channel, uint8)
# jpeg  - JPEG compressed
# png   - PNG compressed
```

## Complete Vision Pipeline

```yaml
nodes:
  # Camera input
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

  # Object detection
  - id: yolo
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  # Segmentation (from detection)
  - id: sam2
    build: pip install dora-sam2
    path: dora-sam2
    inputs:
      image: camera/image
      bbox: yolo/bbox
    outputs:
      - mask

  # Vision-language understanding
  - id: vlm
    build: pip install dora-internvl
    path: dora-internvl
    inputs:
      image: camera/image
      text: prompt/question
    outputs:
      - text

  # Visualization
  - id: viz
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      image: camera/image
      boxes2d: yolo/bbox
      mask: sam2/mask
```

## Visualization Options

### Rerun (3D Visualization)

```yaml
- id: rerun
  build: pip install dora-rerun
  path: dora-rerun
  inputs:
    image: camera/image
    boxes2d: detector/bbox
    depth: camera/depth
    point_cloud: lidar/points
```

### OpenCV Plot

```yaml
- id: plot
  build: pip install opencv-plot
  path: opencv-plot
  inputs:
    image: camera/image
    bbox: detector/bbox
    text: vlm/text
```

## Processing Tips

### Frame Rate Control

```yaml
# 30 FPS (33ms)
tick: dora/timer/millis/33

# 15 FPS (66ms) - for heavy processing
tick: dora/timer/millis/66

# 10 FPS (100ms) - for slow models
tick: dora/timer/millis/100
```

### Queue Size for Real-time

```yaml
inputs:
  image:
    source: camera/image
    queue_size: 1  # Drop old frames, keep latest
```

### GPU Acceleration

```yaml
env:
  DEVICE: cuda    # Use NVIDIA GPU
  # or
  DEVICE: mps     # Use Apple Silicon GPU
  # or
  DEVICE: cpu     # CPU only
```

## Related Skills

- `object-detection` - YOLO-based detection
- `segmentation` - SAM2 segmentation
- `tracking` - CoTracker point tracking
- `vlm` - Vision-language models
