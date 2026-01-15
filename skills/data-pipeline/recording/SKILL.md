---
name: recording
description: Data recording workflow for dora-rs. Use when user needs to record demonstrations, capture sensor data, or create training datasets.
---

# Data Recording

Record demonstrations and sensor data for robot learning.

## Basic Recording Node

```yaml
- id: recorder
  build: pip install dora-record
  path: dora-record
  inputs:
    image: camera/image
    state: robot/jointstate
    action: controller/action
  env:
    OUTPUT_DIR: ./recordings
    FORMAT: parquet
```

## LeRobot Recorder

```yaml
- id: recorder
  build: pip install dora-lerobot-recorder
  path: dora-lerobot-recorder
  inputs:
    image: camera/image
    observation: robot/jointstate
    action: leader/action
  env:
    DATASET_PATH: ./my_dataset
    TASK_NAME: pick_object
    ROBOT_TYPE: piper
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `OUTPUT_DIR` | Save directory | ./recordings |
| `FORMAT` | parquet, ario, lerobot | parquet |
| `EPISODE_PREFIX` | Episode name prefix | episode |
| `AUTO_EPISODE` | Auto-increment episodes | true |
| `RECORD_HZ` | Recording frequency | 20 |

## Complete Recording Pipeline

```yaml
nodes:
  # Cameras
  - id: wrist_cam
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

  - id: top_cam
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - image
    env:
      CAPTURE_PATH: "2"

  # Robot arms (teleoperation)
  - id: leader
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
    outputs:
      - jointstate
      - gripper_state
    env:
      CAN_BUS: can0
      MODE: passive

  - id: follower
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
      joint_action: leader/jointstate
      gripper_action: leader/gripper_state
    outputs:
      - jointstate
    env:
      CAN_BUS: can1
      MODE: active

  # Recording
  - id: recorder
    build: pip install dora-lerobot-recorder
    path: dora-lerobot-recorder
    inputs:
      wrist_image: wrist_cam/image
      top_image: top_cam/image
      observation.state: follower/jointstate
      action: leader/jointstate
    env:
      DATASET_PATH: ./pick_and_place_dataset
      TASK_NAME: pick_and_place

  # Keyboard control for episodes
  - id: keyboard
    build: pip install dora-keyboard
    path: dora-keyboard
    outputs:
      - keypress

  - id: episode_controller
    path: ./episode_controller.py
    inputs:
      keypress: keyboard/keypress
    outputs:
      - control
```

## Episode Controller

```python
# episode_controller.py
from dora import Node
import pyarrow as pa

node = Node()

is_recording = False

print("Episode controls:")
print("  SPACE: Start/stop recording")
print("  ENTER: Save episode")
print("  ESC: Discard episode")
print("  Q: Quit")

for event in node:
    if event["id"] == "keypress":
        key = event["value"][0].as_py()

        if key == " ":
            is_recording = not is_recording
            if is_recording:
                print("Recording started...")
                node.send_output("control", pa.array(["start"]))
            else:
                print("Recording paused.")
                node.send_output("control", pa.array(["pause"]))

        elif key == "enter":
            print("Saving episode...")
            node.send_output("control", pa.array(["save"]))
            is_recording = False

        elif key == "escape":
            print("Discarding episode...")
            node.send_output("control", pa.array(["discard"]))
            is_recording = False

        elif key == "q":
            print("Quitting...")
            break
```

## Custom Recording Node

```python
# custom_recorder.py
from dora import Node
import pandas as pd
import numpy as np
import os

node = Node()

episode_data = []
episode_count = 0
is_recording = False
output_dir = os.environ.get("OUTPUT_DIR", "./recordings")

os.makedirs(output_dir, exist_ok=True)

for event in node:
    if event["id"] == "control":
        cmd = event["value"][0].as_py()

        if cmd == "start":
            is_recording = True
            episode_data = []

        elif cmd == "pause":
            is_recording = False

        elif cmd == "save":
            if episode_data:
                df = pd.DataFrame(episode_data)
                path = f"{output_dir}/episode_{episode_count:04d}.parquet"
                df.to_parquet(path)
                print(f"Saved {len(df)} samples to {path}")
                episode_count += 1
            episode_data = []
            is_recording = False

        elif cmd == "discard":
            episode_data = []
            is_recording = False

    elif is_recording:
        # Record data
        sample = {
            "timestamp": event["metadata"]["timestamp"],
            "input_id": event["id"],
        }

        if event["id"] == "image":
            # Store image path or reference
            sample["image_path"] = save_image(event["value"])
        else:
            sample["data"] = event["value"].to_numpy().tolist()

        episode_data.append(sample)
```

## Multi-Camera Recording

```python
# Synchronize multiple camera streams
buffers = {
    "wrist": None,
    "top": None,
    "state": None,
}

for event in node:
    if event["id"] == "wrist_image":
        buffers["wrist"] = event["value"]
    elif event["id"] == "top_image":
        buffers["top"] = event["value"]
    elif event["id"] == "observation":
        buffers["state"] = event["value"]

    # Only record when all data is available
    if all(v is not None for v in buffers.values()):
        record_sample(buffers)
        buffers = {k: None for k in buffers}
```

## Video Recording

```yaml
env:
  VIDEO_ENABLED: "true"
  VIDEO_CODEC: h264
  VIDEO_FPS: "30"
  VIDEO_QUALITY: "23"  # CRF value
```

## Data Validation

```python
def validate_episode(episode_path):
    """Check episode data quality."""
    df = pd.read_parquet(episode_path)

    # Check for gaps
    timestamps = df["timestamp"].values
    gaps = np.diff(timestamps)
    expected_gap = 1 / 20  # 20 Hz

    if np.any(gaps > expected_gap * 2):
        print(f"Warning: Large gaps in data")

    # Check for NaN
    if df.isnull().any().any():
        print(f"Warning: NaN values found")

    # Check duration
    duration = (timestamps[-1] - timestamps[0])
    print(f"Episode duration: {duration:.1f}s")
    print(f"Samples: {len(df)}")

    return True
```

## Best Practices

1. **Consistent frequency**: Use timer inputs for steady recording rate
2. **Episode length**: Keep episodes focused (30-60 seconds)
3. **Quality over quantity**: Delete failed demonstrations
4. **Metadata**: Record task name, date, operator
5. **Backup**: Save data incrementally

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Dropped frames | Reduce image resolution or recording rate |
| Large files | Enable video compression |
| Sync issues | Use timestamps for alignment |
| Disk space | Monitor available storage |

## Related Skills

- `data-pipeline` - Pipeline overview
- `replay` - Playback recorded data
- `lerobot` - LeRobot format integration
