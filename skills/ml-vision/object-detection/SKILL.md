---
name: object-detection
description: YOLO-based object detection for dora-rs. Use when user needs bounding box detection, object recognition, or wants to detect objects in images/video.
---

# Object Detection with YOLO

Detect objects in images using YOLO models within dora-rs dataflow.

## Node Configuration

```yaml
- id: yolo
  build: pip install dora-yolo
  path: dora-yolo
  inputs:
    image: camera/image
  outputs:
    - bbox
  env:
    MODEL: yolov8n.pt       # Model variant
    CONFIDENCE: "0.5"       # Detection threshold
    DEVICE: cuda            # cuda, mps, or cpu
```

## Model Options

| Model | Size | Speed | Accuracy |
|-------|------|-------|----------|
| `yolov8n.pt` | Nano | Fastest | Lower |
| `yolov8s.pt` | Small | Fast | Good |
| `yolov8m.pt` | Medium | Balanced | Better |
| `yolov8l.pt` | Large | Slower | High |
| `yolov8x.pt` | XLarge | Slowest | Highest |

## Input Format

The node expects BGR8 encoded images:

```python
# Image metadata
metadata = {
    "width": "640",
    "height": "480",
    "encoding": "bgr8"
}

# Image data: flattened numpy array (H * W * 3)
image_data = pa.array(image.flatten())
```

## Output Format

Bounding boxes as Arrow StructArray:

```python
# Output structure
bbox = {
    "bbox": [x, y, w, h],      # Box coordinates (xywh format)
    "confidence": 0.95,         # Detection confidence
    "class": 0,                 # Class ID (COCO classes)
    "label": "person"           # Class name
}
```

## Complete Example Dataflow

```yaml
nodes:
  # Camera capture
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

  # YOLO detection
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

  # Visualization
  - id: plot
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      image: camera/image
      boxes2d: yolo/bbox
```

## Processing Detections in Custom Node

```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT" and event["id"] == "bbox":
        # Get detections
        detections = event["value"]

        for detection in detections:
            bbox = detection["bbox"]  # [x, y, w, h]
            confidence = detection["confidence"]
            label = detection["label"]

            print(f"Detected {label} at {bbox} ({confidence:.2f})")

            # Filter by class
            if label == "person":
                # Do something with person detection
                pass
```

## Custom Model Training

Use a custom-trained YOLO model:

```yaml
env:
  MODEL: /path/to/custom_model.pt
  # or use Ultralytics hub
  MODEL: yolov8n-custom.pt
```

## COCO Class Labels

Default COCO classes (80 categories):
- 0: person, 1: bicycle, 2: car, 3: motorcycle
- 4: airplane, 5: bus, 6: train, 7: truck
- ... (see full list in COCO dataset)

## Performance Optimization

### Real-time Processing

```yaml
inputs:
  image:
    source: camera/image
    queue_size: 1  # Process only latest frame
```

### GPU Selection

```yaml
env:
  DEVICE: cuda:0   # Specific GPU
  DEVICE: cuda:1   # Second GPU
  DEVICE: mps      # Apple Silicon
```

### Reduce Resolution

```yaml
# In camera node
env:
  IMAGE_WIDTH: "320"
  IMAGE_HEIGHT: "240"
```

## Integration with Other Nodes

### With Segmentation (SAM2)

```yaml
- id: sam2
  build: pip install dora-sam2
  path: dora-sam2
  inputs:
    image: camera/image
    bbox: yolo/bbox  # Use YOLO boxes as prompts
  outputs:
    - mask
```

### With Tracking

```yaml
- id: tracker
  build: pip install dora-cotracker
  path: dora-cotracker
  inputs:
    image: camera/image
    bbox: yolo/bbox
  outputs:
    - tracks
```

### With Robot Control

```yaml
- id: arm-controller
  path: ./arm_controller.py
  inputs:
    bbox: yolo/bbox  # React to detected objects
  outputs:
    - action
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No detections | Lower confidence threshold |
| Slow FPS | Use smaller model (yolov8n) |
| CUDA error | Check PyTorch CUDA installation |
| Wrong classes | Use custom-trained model |

## Related Skills

- `ml-vision` - Vision pipeline overview
- `segmentation` - SAM2 mask generation
- `tracking` - Point tracking
