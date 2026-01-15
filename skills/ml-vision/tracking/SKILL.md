---
name: tracking
description: CoTracker point tracking for dora-rs. Use when user needs to track points across video frames, motion tracking, or optical flow analysis.
---

# Point Tracking with CoTracker

Track points across video frames using CoTracker for motion analysis.

## Node Configuration

```yaml
- id: cotracker
  build: pip install dora-cotracker
  path: dora-cotracker
  inputs:
    image: camera/image
    points: initial/points  # Starting points to track
  outputs:
    - tracks               # Tracked point positions
    - visibility           # Point visibility status
  env:
    MODEL: cotracker2      # Model variant
    DEVICE: cuda           # cuda, mps, or cpu
```

## Model Options

| Model | Description |
|-------|-------------|
| `cotracker2` | Latest version, best quality |
| `cotracker` | Original version |

## Input Format

### Points to Track

```python
import pyarrow as pa

# Initial points: [[x1, y1], [x2, y2], ...]
points = [
    [320, 240],  # Center of 640x480 image
    [100, 100],  # Top-left region
    [540, 380],  # Bottom-right region
]
node.send_output("points", pa.array(points))
```

### From Detection Boxes

```python
# Convert bbox centers to tracking points
def bbox_to_points(bboxes):
    points = []
    for bbox in bboxes:
        x, y, w, h = bbox
        center_x = x + w / 2
        center_y = y + h / 2
        points.append([center_x, center_y])
    return points
```

## Output Format

### Tracks

```python
# tracks: [[x1, y1], [x2, y2], ...] - current positions
tracks = event["value"].to_numpy()
for i, (x, y) in enumerate(tracks):
    print(f"Point {i}: ({x:.1f}, {y:.1f})")
```

### Visibility

```python
# visibility: [True, True, False, ...] - is point visible
visibility = event["value"].to_numpy()
for i, visible in enumerate(visibility):
    if not visible:
        print(f"Point {i} is occluded")
```

## Complete Tracking Pipeline

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

  # Initial point detection (YOLO)
  - id: yolo
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  # Convert boxes to points
  - id: points
    path: ./bbox_to_points.py
    inputs:
      bbox: yolo/bbox
    outputs:
      - points

  # Track points
  - id: tracker
    build: pip install dora-cotracker
    path: dora-cotracker
    inputs:
      image: camera/image
      points: points/points
    outputs:
      - tracks
      - visibility

  # Visualization
  - id: viz
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      image: camera/image
      points: tracker/tracks
```

## bbox_to_points.py

```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT" and event["id"] == "bbox":
        bboxes = event["value"]

        points = []
        for bbox in bboxes:
            x, y, w, h = bbox["bbox"]
            center_x = x + w / 2
            center_y = y + h / 2
            points.append([center_x, center_y])

        if points:
            node.send_output("points", pa.array(points))
```

## Motion Analysis

### Calculate Velocity

```python
import numpy as np

prev_tracks = None

def calculate_velocity(current_tracks, dt=0.033):
    global prev_tracks

    if prev_tracks is None:
        prev_tracks = current_tracks
        return None

    # Velocity in pixels per second
    velocity = (current_tracks - prev_tracks) / dt
    prev_tracks = current_tracks.copy()

    return velocity

# Usage
for event in node:
    if event["id"] == "tracks":
        tracks = event["value"].to_numpy()
        velocity = calculate_velocity(tracks)
        if velocity is not None:
            speeds = np.linalg.norm(velocity, axis=1)
            print(f"Average speed: {np.mean(speeds):.1f} px/s")
```

### Detect Motion Direction

```python
def detect_direction(velocity):
    """Classify motion direction for each point."""
    directions = []
    for vx, vy in velocity:
        if abs(vx) > abs(vy):
            direction = "right" if vx > 0 else "left"
        else:
            direction = "down" if vy > 0 else "up"
        directions.append(direction)
    return directions
```

## Grid Tracking

Track a grid of points for optical flow analysis:

```python
def create_grid_points(width, height, grid_size=20):
    """Create a grid of points to track."""
    points = []
    for y in range(grid_size, height, grid_size):
        for x in range(grid_size, width, grid_size):
            points.append([x, y])
    return points

# Create 640x480 grid with 20px spacing
grid_points = create_grid_points(640, 480, grid_size=20)
# Results in ~600 tracking points
```

## Applications

### Object Following

```python
# Track object center, calculate distance to move
target = tracks[0]  # First tracked point
image_center = [320, 240]

offset_x = target[0] - image_center[0]
offset_y = target[1] - image_center[1]

# Generate movement command
if abs(offset_x) > 50:
    action = "turn_right" if offset_x > 0 else "turn_left"
elif abs(offset_y) > 50:
    action = "tilt_down" if offset_y > 0 else "tilt_up"
else:
    action = "centered"
```

### Gesture Recognition

```python
# Track hand landmarks and recognize gestures
def recognize_gesture(hand_tracks, prev_positions):
    # Calculate movement pattern
    movement = hand_tracks - prev_positions

    # Detect swipe gestures
    avg_x = np.mean(movement[:, 0])
    avg_y = np.mean(movement[:, 1])

    if avg_x > 50:
        return "swipe_right"
    elif avg_x < -50:
        return "swipe_left"
    elif avg_y > 50:
        return "swipe_down"
    elif avg_y < -50:
        return "swipe_up"
    return None
```

## Performance Tips

### Limit Number of Points

```python
# Track fewer points for better performance
MAX_POINTS = 50
if len(points) > MAX_POINTS:
    points = points[:MAX_POINTS]
```

### Update Frequency

```yaml
# Lower frame rate for tracking
inputs:
  tick: dora/timer/millis/66  # ~15 FPS
```

## Related Skills

- `object-detection` - Generate initial tracking points
- `segmentation` - Track segmented objects
- `ml-vision` - Vision pipeline overview
