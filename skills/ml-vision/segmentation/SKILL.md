---
name: segmentation
description: SAM2 (Segment Anything Model 2) for dora-rs. Use when user needs instance segmentation, mask generation, or object segmentation from bounding boxes or points.
---

# Segmentation with SAM2

Generate precise segmentation masks using SAM2 (Segment Anything Model 2).

## Node Configuration

See [COMMON_NODES.md](../../../data/COMMON_NODES.md#sam2-segmentation-node) for standard SAM2 configuration.

**Model options:** See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#vision-models).

## Input Prompts

### From Bounding Boxes
Use YOLO detections as prompts (see [COMMON_NODES.md](../../../data/COMMON_NODES.md#sam2-segmentation-node)).

### From Points
User-selected points can be used as prompts.

## Output Format

Binary masks (1 = object, 0 = background) as flattened arrays with width/height metadata.

## Complete Pipeline: Detection + Segmentation

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

  - id: yolo
    # See COMMON_NODES.md#yolo-detection-node
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  - id: sam2
    # See COMMON_NODES.md#sam2-segmentation-node
    build: pip install dora-sam2
    path: dora-sam2
    inputs:
      image: camera/image
      bbox: yolo/bbox
    outputs:
      - mask

  - id: viz
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      image: camera/image
      mask: sam2/mask
```

## Processing Masks in Custom Node

```python
from dora import Node
import numpy as np
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT":
        if event["id"] == "mask":
            # Get mask data
            metadata = event["metadata"]
            width = int(metadata["width"])
            height = int(metadata["height"])

            # Reshape to 2D
            mask_flat = event["value"].to_numpy()
            mask = mask_flat.reshape((height, width))

            # Calculate object area
            object_area = np.sum(mask)
            total_area = width * height
            coverage = object_area / total_area

            print(f"Object covers {coverage:.1%} of frame")

            # Find object center
            if object_area > 0:
                y_coords, x_coords = np.where(mask > 0)
                center_x = np.mean(x_coords)
                center_y = np.mean(y_coords)
                print(f"Object center: ({center_x:.0f}, {center_y:.0f})")
```

## Interactive Segmentation

Create point prompts from user input (left-click = foreground, right-click = background):

```yaml
nodes:
  - id: click
    path: ./click_handler.py
    inputs:
      tick: dora/timer/millis/100
    outputs:
      - points

  - id: sam2
    build: pip install dora-sam2
    path: dora-sam2
    inputs:
      image: camera/image
      points: click/points
    outputs:
      - mask
```

## Performance Tips

See [CONFIG_REFERENCE.md](../../../data/CONFIG_REFERENCE.md#performance-optimization-patterns) for GPU memory optimization and queue management.

## Applications

### Object Removal

```python
# Create inpainting mask from segmentation
inpaint_mask = (mask * 255).astype(np.uint8)
result = cv2.inpaint(image, inpaint_mask, 3, cv2.INPAINT_TELEA)
```

### Object Extraction

```python
# Extract object from background
object_only = image.copy()
object_only[mask == 0] = 0  # Black background
```

### Collision Detection

```python
# Check if masks overlap
overlap = np.logical_and(mask1, mask2)
if np.any(overlap):
    print("Objects are colliding!")
```

## Related Skills

- `object-detection` - YOLO for bounding boxes
- `tracking` - Track segmented objects
- `ml-vision` - Vision pipeline overview
