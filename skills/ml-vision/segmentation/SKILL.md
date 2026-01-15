---
name: segmentation
description: SAM2 (Segment Anything Model 2) for dora-rs. Use when user needs instance segmentation, mask generation, or object segmentation from bounding boxes or points.
---

# Segmentation with SAM2

Generate precise segmentation masks using SAM2 (Segment Anything Model 2).

## Node Configuration

```yaml
- id: sam2
  build: pip install dora-sam2
  path: dora-sam2
  inputs:
    image: camera/image
    bbox: detector/bbox      # Bounding box prompts
  outputs:
    - mask
  env:
    MODEL: sam2-hiera-small  # Model variant
    DEVICE: cuda             # cuda, mps, or cpu
```

## Model Options

| Model | Size | Speed | Quality |
|-------|------|-------|---------|
| `sam2-hiera-tiny` | Tiny | Fastest | Good |
| `sam2-hiera-small` | Small | Fast | Better |
| `sam2-hiera-base` | Base | Balanced | High |
| `sam2-hiera-large` | Large | Slower | Best |

## Input Prompts

### From Bounding Boxes

```yaml
inputs:
  image: camera/image
  bbox: yolo/bbox  # YOLO detection boxes
```

### From Points

```yaml
inputs:
  image: camera/image
  points: click/points  # User-selected points
```

## Output Format

Segmentation masks as Arrow arrays:

```python
# Mask metadata
metadata = {
    "width": "640",
    "height": "480",
    "encoding": "mask"  # Binary mask
}

# Mask data: flattened boolean array (H * W)
# 1 = object, 0 = background
```

## Complete Pipeline: Detection + Segmentation

```yaml
nodes:
  # Camera
  - id: camera
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/33
    outputs:
      - image
    env:
      CAPTURE_PATH: "0"

  # Object detection
  - id: yolo
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  # Segmentation from detections
  - id: sam2
    build: pip install dora-sam2
    path: dora-sam2
    inputs:
      image: camera/image
      bbox: yolo/bbox
    outputs:
      - mask

  # Visualization
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

Create point prompts from user input:

```yaml
nodes:
  # Click handler node
  - id: click
    path: ./click_handler.py
    inputs:
      tick: dora/timer/millis/100
    outputs:
      - points

  # Segment from clicks
  - id: sam2
    build: pip install dora-sam2
    path: dora-sam2
    inputs:
      image: camera/image
      points: click/points
    outputs:
      - mask
```

**click_handler.py:**
```python
import cv2
import pyarrow as pa
from dora import Node

clicked_points = []

def mouse_callback(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        clicked_points.append((x, y, 1))  # 1 = foreground
    elif event == cv2.EVENT_RBUTTONDOWN:
        clicked_points.append((x, y, 0))  # 0 = background

node = Node()
cv2.namedWindow("Click to segment")
cv2.setMouseCallback("Click to segment", mouse_callback)

for event in node:
    if event["type"] == "INPUT" and event["id"] == "image":
        # Display image
        # ...

        if clicked_points:
            points = pa.array(clicked_points)
            node.send_output("points", points)
            clicked_points.clear()
```

## Multi-Object Segmentation

Handle multiple objects:

```python
# Each bbox produces a separate mask
for i, detection in enumerate(detections):
    mask = masks[i]
    # Process each object mask
```

## Performance Tips

### GPU Memory

```yaml
env:
  # Use smaller model for limited GPU memory
  MODEL: sam2-hiera-tiny
  # Or use CPU
  DEVICE: cpu
```

### Batch Processing

```yaml
inputs:
  image:
    source: camera/image
    queue_size: 1  # Latest frame only
```

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
