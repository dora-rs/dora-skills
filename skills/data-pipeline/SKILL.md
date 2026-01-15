---
name: data-pipeline
description: Data collection and management for dora-rs. Use when user asks about data recording, replay, dataset creation, or training data collection.
---

# Data Pipeline

Data collection, storage, and replay for robot learning.

## Overview

Build data pipelines for training robot learning models:

| Stage | Purpose | Nodes |
|-------|---------|-------|
| Collection | Capture demonstrations | dora-record |
| Storage | Save to dataset format | LeRobot, Parquet |
| Replay | Playback for training | dora-replay |
| Training | Train policies | LeRobot, RDT |

## Data Collection Architecture

```yaml
nodes:
  # Sensor inputs
  - id: camera
    path: opencv-video-capture
    outputs:
      - image

  # Robot state
  - id: arm
    path: dora-piper
    outputs:
      - jointstate

  # Teleoperation
  - id: leader
    path: dora-piper
    outputs:
      - action

  # Recorder
  - id: recorder
    build: pip install dora-lerobot-recorder
    path: dora-lerobot-recorder
    inputs:
      image: camera/image
      observation: arm/jointstate
      action: leader/action
    env:
      DATASET_PATH: ./my_dataset
      EPISODE_PREFIX: episode
```

## Data Formats

### LeRobot Format

```
my_dataset/
├── meta_data/
│   └── info.json
├── videos/
│   └── observation.image.mp4
└── data/
    ├── episode_0/
    │   ├── observation.state.parquet
    │   └── action.parquet
    └── episode_1/
        └── ...
```

### Raw Parquet

```
recordings/
├── episode_001.parquet
├── episode_002.parquet
└── ...
```

## Recording Workflow

### 1. Setup Teleoperation

```yaml
nodes:
  - id: leader
    path: dora-piper
    env:
      MODE: passive
      CAN_BUS: can0

  - id: follower
    path: dora-piper
    inputs:
      joint_action: leader/jointstate
    env:
      MODE: active
      CAN_BUS: can1
```

### 2. Add Camera

```yaml
  - id: camera
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - image
```

### 3. Add Recorder

```yaml
  - id: recorder
    path: dora-lerobot-recorder
    inputs:
      image: camera/image
      observation: follower/jointstate
      action: leader/jointstate
    env:
      DATASET_PATH: ./pick_and_place
```

## Replay Workflow

### Load Dataset

```yaml
- id: replay
  build: pip install dora-replay
  path: dora-replay
  inputs:
    tick: dora/timer/millis/50
  outputs:
    - observation
    - action
    - image
  env:
    DATASET_PATH: ./pick_and_place
    EPISODE: "0"
    SPEED: "1.0"
```

### Execute on Robot

```yaml
nodes:
  - id: replay
    path: dora-replay
    outputs:
      - action

  - id: robot
    path: dora-piper
    inputs:
      joint_action: replay/action
```

## Complete Recording Pipeline

```yaml
nodes:
  # Wrist camera
  - id: wrist_camera
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - image
    env:
      CAPTURE_PATH: "0"
      IMAGE_WIDTH: "640"
      IMAGE_HEIGHT: "480"

  # External camera
  - id: external_camera
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - image
    env:
      CAPTURE_PATH: "2"

  # Leader arm
  - id: leader
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
    outputs:
      - jointstate
    env:
      CAN_BUS: can0
      MODE: passive

  # Follower arm
  - id: follower
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
      joint_action: leader/jointstate
    outputs:
      - jointstate
    env:
      CAN_BUS: can1
      MODE: active

  # Recorder
  - id: recorder
    build: pip install dora-lerobot-recorder
    path: dora-lerobot-recorder
    inputs:
      wrist_image: wrist_camera/image
      external_image: external_camera/image
      observation: follower/jointstate
      action: leader/jointstate
    env:
      DATASET_PATH: ./manipulation_dataset
      TASK_NAME: pick_and_place
```

## Episode Management

```python
# Keyboard control for episodes
# Space: Start/stop recording
# Enter: Save episode
# Escape: Discard episode
```

## Data Synchronization

All data is timestamped using UHLC (Unique Hybrid Logical Clock):

```python
for event in node:
    timestamp = event["metadata"]["timestamp"]
    # Nanosecond precision
```

## Storage Tips

### Compression

```yaml
env:
  VIDEO_CODEC: h264    # Compressed video
  QUALITY: "23"        # CRF (lower = better quality)
```

### Downsampling

```yaml
env:
  RECORD_HZ: "10"      # Record at 10 Hz instead of 50 Hz
```

## Quality Checks

```python
# Verify recorded data
import pandas as pd

df = pd.read_parquet("dataset/episode_0/observation.parquet")
print(f"Samples: {len(df)}")
print(f"Duration: {df['timestamp'].max() - df['timestamp'].min()}")
print(f"Columns: {df.columns.tolist()}")
```

## Related Skills

- `recording` - Detailed recording workflow
- `replay` - Data playback
- `lerobot` - LeRobot integration
