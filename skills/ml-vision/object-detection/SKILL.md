---
name: object-detection
description: YOLO-based object detection for dora-rs. Use when user needs bounding box detection, object recognition, or wants to detect objects in images/video.
---

# Object Detection with YOLO

Detect objects in images using YOLO models within dora-rs dataflow.

## Node Configuration

See [COMMON_NODES.md](../../../data/COMMON_NODES.md#yolo-detection-node) for the standard YOLO node configuration.

**Configuration:** Models from `yolov8n.pt` (fastest) to `yolov8x.pt` (most accurate). See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#vision-models) for details.

## Input/Output Format

- **Input:** See [COMMON_NODES.md](../../../data/COMMON_NODES.md#yolo-detection-node)
- **Output:** See [COMMON_NODES.md](../../../data/COMMON_NODES.md#yolo-detection-node)

## Complete Example Dataflow

```yaml
nodes:
  - id: camera
    # See COMMON_NODES.md#camera-node
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/33
    outputs:
      - image
    env:
      CAPTURE_PATH: "0"

  - id: yolo
    # See COMMON_NODES.md#yolo-detection-node
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox
    env:
      MODEL: yolov8n.pt
      CONFIDENCE: "0.5"

  - id: plot
    # See COMMON_NODES.md#rerun-visualization-node
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      image: camera/image
      boxes2d: yolo/bbox
```

## Processing Detections in Custom Node

See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#detection-processing-python) for processing YOLO detection outputs.

## Custom Model Training

Use a custom-trained YOLO model:

```yaml
env:
  MODEL: /path/to/custom_model.pt
```

## COCO Class Labels

Default COCO dataset has 80 categories (0: person, 1: bicycle, 2: car, etc.). See COCO dataset documentation for full list.

## Performance Optimization

See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#performance-optimization-patterns) for real-time vision optimization, including queue management, GPU selection, and resolution tuning.

## Integration with Other Nodes

### With Segmentation (SAM2)

Use YOLO boxes as prompts for SAM2. See [COMMON_NODES.md](../../../data/COMMON_NODES.md#sam2-segmentation-node).

### With Tracking

Feed detections to CoTracker. See [COMMON_NODES.md](../../../data/COMMON_NODES.md#cotracker-tracking-node).

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
