---
name: replay
description: Data replay for dora-rs. Use when user needs to play back recorded data, test policies, or visualize demonstrations.
---

# Data Replay

Play back recorded demonstrations and datasets.

## Basic Replay Node

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
    DATASET_PATH: ./my_dataset
    EPISODE: "0"
    SPEED: "1.0"
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `DATASET_PATH` | Path to dataset | required |
| `EPISODE` | Episode number | 0 |
| `SPEED` | Playback speed | 1.0 |
| `LOOP` | Loop playback | false |
| `START_FRAME` | Starting frame | 0 |
| `END_FRAME` | Ending frame | -1 (all) |

## Playback Modes

### Single Episode

```yaml
env:
  EPISODE: "5"
  LOOP: "false"
```

### Sequential Episodes

```yaml
env:
  EPISODE: "0-10"     # Play episodes 0 through 10
  LOOP: "true"
```

### Random Episodes

```yaml
env:
  EPISODE: random
  LOOP: "true"
```

## Complete Replay Pipeline

```yaml
nodes:
  # Data replay
  - id: replay
    build: pip install dora-replay
    path: dora-replay
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - observation
      - action
      - wrist_image
      - top_image
    env:
      DATASET_PATH: ./pick_and_place_dataset
      EPISODE: "0"
      SPEED: "1.0"

  # Visualization
  - id: viz
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      wrist_image: replay/wrist_image
      top_image: replay/top_image
```

## Execute Replay on Robot

```yaml
nodes:
  - id: replay
    build: pip install dora-replay
    path: dora-replay
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - action
    env:
      DATASET_PATH: ./dataset
      EPISODE: "0"

  # Robot executes replayed actions
  - id: robot
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
      joint_action: replay/action
    outputs:
      - jointstate
    env:
      CAN_BUS: can0
```

## Custom Replay Node

```python
# replay_node.py
from dora import Node
import pandas as pd
import pyarrow as pa
import os

node = Node()

dataset_path = os.environ.get("DATASET_PATH", "./dataset")
episode = int(os.environ.get("EPISODE", "0"))
speed = float(os.environ.get("SPEED", "1.0"))

# Load episode data
episode_path = f"{dataset_path}/episode_{episode:04d}.parquet"
df = pd.read_parquet(episode_path)

current_idx = 0

for event in node:
    if event["id"] == "tick" and current_idx < len(df):
        row = df.iloc[current_idx]

        # Send observation
        if "observation" in row:
            node.send_output("observation", pa.array(row["observation"]))

        # Send action
        if "action" in row:
            node.send_output("action", pa.array(row["action"]))

        current_idx += 1

    elif current_idx >= len(df):
        print("Replay complete")
        break
```

## Speed Control

```yaml
env:
  SPEED: "0.5"   # Half speed
  SPEED: "1.0"   # Normal speed
  SPEED: "2.0"   # Double speed
```

## Interactive Replay

```python
# Keyboard-controlled replay
controls = {
    "space": "pause/resume",
    "left": "previous frame",
    "right": "next frame",
    "up": "speed up",
    "down": "slow down",
    "r": "restart",
}

paused = False
frame_idx = 0

for event in node:
    if event["id"] == "keypress":
        key = event["value"][0].as_py()

        if key == " ":
            paused = not paused
        elif key == "left" and paused:
            frame_idx = max(0, frame_idx - 1)
        elif key == "right" and paused:
            frame_idx += 1
        elif key == "r":
            frame_idx = 0

    elif event["id"] == "tick" and not paused:
        play_frame(frame_idx)
        frame_idx += 1
```

## Comparison Mode

Compare recorded actions with live policy:

```yaml
nodes:
  # Replay recorded actions
  - id: replay
    path: dora-replay
    outputs:
      - recorded_action

  # Live camera
  - id: camera
    path: opencv-video-capture
    outputs:
      - image

  # Policy generates actions from live camera
  - id: policy
    path: ./policy_node.py
    inputs:
      image: camera/image
    outputs:
      - predicted_action

  # Compare
  - id: compare
    path: ./compare_actions.py
    inputs:
      recorded: replay/recorded_action
      predicted: policy/predicted_action
```

## Data Augmentation During Replay

```python
import numpy as np

def augment_image(image):
    """Apply augmentation during replay."""
    # Random brightness
    brightness = np.random.uniform(0.8, 1.2)
    image = np.clip(image * brightness, 0, 255).astype(np.uint8)

    # Random noise
    noise = np.random.normal(0, 5, image.shape)
    image = np.clip(image + noise, 0, 255).astype(np.uint8)

    return image

def augment_action(action):
    """Add noise to actions for robustness."""
    noise = np.random.normal(0, 0.01, action.shape)
    return action + noise
```

## Statistics and Analysis

```python
# Analyze replayed data
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_parquet("dataset/episode_0.parquet")

# Plot joint positions over time
fig, axes = plt.subplots(6, 1, figsize=(10, 12))
for i in range(6):
    axes[i].plot(df["timestamp"], df[f"joint_{i}"])
    axes[i].set_ylabel(f"Joint {i}")
plt.xlabel("Time (s)")
plt.savefig("episode_analysis.png")
```

## LeRobot Dataset Replay

```yaml
- id: replay
  build: pip install dora-lerobot-replay
  path: dora-lerobot-replay
  inputs:
    tick: dora/timer/millis/50
  outputs:
    - observation.state
    - observation.image
    - action
  env:
    REPO_ID: lerobot/aloha_sim_transfer_cube_human
    EPISODE: "0"
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Timing mismatch | Check SPEED and tick rate |
| Missing frames | Verify dataset integrity |
| Robot jitter | Smooth actions with interpolation |
| Wrong format | Check dataset structure |

## Related Skills

- `data-pipeline` - Pipeline overview
- `recording` - Record new data
- `lerobot` - LeRobot integration
