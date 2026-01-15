---
name: lerobot
description: LeRobot integration for dora-rs. Use when user needs to work with LeRobot datasets, train imitation learning policies, or deploy trained models.
---

# LeRobot Integration

Integrate with LeRobot for imitation learning and robot policy training.

## Overview

LeRobot is a library for robot learning that provides:
- Standardized dataset format
- Pre-trained policies
- Training pipelines (ACT, Diffusion Policy)
- Hugging Face Hub integration

## Dataset Recording

### LeRobot Format Recorder

```yaml
- id: recorder
  build: pip install dora-lerobot-recorder
  path: dora-lerobot-recorder
  inputs:
    observation.images.wrist: wrist_camera/image
    observation.images.top: top_camera/image
    observation.state: robot/jointstate
    action: leader/action
  env:
    DATASET_PATH: ./lerobot_dataset
    REPO_ID: my-org/my-dataset
    TASK_NAME: pick_and_place
    ROBOT_TYPE: piper
    FPS: "20"
```

## Dataset Structure

```
lerobot_dataset/
├── meta_data/
│   ├── info.json          # Dataset metadata
│   ├── stats.json         # Normalization statistics
│   └── episodes.json      # Episode list
├── videos/
│   ├── observation.images.wrist_episode_000000.mp4
│   └── observation.images.top_episode_000000.mp4
└── data/
    └── chunk-000/
        └── episode_000000.parquet
```

## Configuration Options

| Option | Description |
|--------|-------------|
| `REPO_ID` | HuggingFace repo ID |
| `TASK_NAME` | Task description |
| `ROBOT_TYPE` | Robot model name |
| `FPS` | Recording frequency |
| `VIDEO_CODEC` | Video compression |

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

  # Teleoperation
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
    outputs:
      - jointstate
    env:
      CAN_BUS: can1

  # LeRobot recorder
  - id: recorder
    build: pip install dora-lerobot-recorder
    path: dora-lerobot-recorder
    inputs:
      observation.images.wrist: wrist_cam/image
      observation.images.top: top_cam/image
      observation.state: follower/jointstate
      action: leader/jointstate
    env:
      DATASET_PATH: ./aloha_pick_place
      REPO_ID: my-org/aloha-pick-place
      TASK_NAME: "Pick up the cube and place it in the bowl"
      ROBOT_TYPE: aloha
      FPS: "20"
```

## Training with LeRobot

### ACT (Action Chunking Transformer)

```bash
# Install LeRobot
pip install lerobot

# Train ACT policy
python -m lerobot.scripts.train \
    policy=act \
    env=aloha \
    dataset_repo_id=my-org/aloha-pick-place \
    hydra.run.dir=outputs/act_pick_place
```

### Diffusion Policy

```bash
python -m lerobot.scripts.train \
    policy=diffusion \
    env=aloha \
    dataset_repo_id=my-org/aloha-pick-place \
    hydra.run.dir=outputs/diffusion_pick_place
```

## Policy Deployment

### Load Trained Policy

```yaml
- id: policy
  build: pip install dora-lerobot-policy
  path: dora-lerobot-policy
  inputs:
    observation.images.wrist: wrist_cam/image
    observation.images.top: top_cam/image
    observation.state: robot/jointstate
  outputs:
    - action
  env:
    POLICY_PATH: ./outputs/act_pick_place/checkpoints/last.ckpt
    # Or from HuggingFace Hub
    REPO_ID: my-org/act-pick-place
    DEVICE: cuda
```

### Complete Deployment Pipeline

```yaml
nodes:
  # Cameras
  - id: wrist_cam
    path: opencv-video-capture
    outputs:
      - image

  - id: top_cam
    path: opencv-video-capture
    outputs:
      - image

  # Robot
  - id: robot
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
      joint_action: policy/action
    outputs:
      - jointstate

  # Policy inference
  - id: policy
    path: dora-lerobot-policy
    inputs:
      observation.images.wrist: wrist_cam/image
      observation.images.top: top_cam/image
      observation.state: robot/jointstate
    outputs:
      - action
    env:
      REPO_ID: my-org/act-pick-place
```

## Using Pre-trained Models

### From Hugging Face Hub

```yaml
env:
  REPO_ID: lerobot/act_aloha_sim_transfer_cube_human
```

### Available Models

| Model | Task | Robot |
|-------|------|-------|
| `lerobot/act_aloha_sim_transfer_cube_human` | Cube transfer | ALOHA |
| `lerobot/diffusion_pusht` | Push-T | 2D pusher |
| `lerobot/tdmpc_simxarm` | Various | xArm |

## Custom Policy Node

```python
# policy_node.py
from dora import Node
import torch
from lerobot.common.policies.act import ACTPolicy
import pyarrow as pa

node = Node()

# Load policy
policy = ACTPolicy.from_pretrained("my-org/act-pick-place")
policy.eval()
policy.to("cuda")

# Observation buffer
obs_buffer = {}

for event in node:
    if event["type"] == "INPUT":
        obs_buffer[event["id"]] = event["value"]

        # Check if all observations are ready
        if all(k in obs_buffer for k in ["observation.state", "observation.images.wrist"]):
            # Prepare observation dict
            observation = {
                "observation.state": torch.tensor(obs_buffer["observation.state"].to_numpy()),
                "observation.images.wrist": preprocess_image(obs_buffer["observation.images.wrist"]),
            }

            # Get action from policy
            with torch.no_grad():
                action = policy.select_action(observation)

            # Send action
            node.send_output("action", pa.array(action.cpu().numpy()))

            # Clear buffer
            obs_buffer.clear()
```

## Dataset Statistics

```python
from lerobot.common.datasets.lerobot_dataset import LeRobotDataset

dataset = LeRobotDataset("my-org/aloha-pick-place")

print(f"Episodes: {dataset.num_episodes}")
print(f"Total frames: {len(dataset)}")
print(f"FPS: {dataset.fps}")
print(f"Features: {dataset.features}")
```

## Upload to Hub

```python
from huggingface_hub import HfApi

api = HfApi()
api.upload_folder(
    folder_path="./aloha_pick_place",
    repo_id="my-org/aloha-pick-place",
    repo_type="dataset",
)
```

## Evaluation

```python
# Evaluate policy success rate
from lerobot.scripts.eval import eval_policy

results = eval_policy(
    policy_path="outputs/act_pick_place",
    env_name="aloha",
    num_episodes=50,
)
print(f"Success rate: {results['success_rate']:.1%}")
```

## Best Practices

1. **Collect diverse demos**: 50-100 episodes minimum
2. **Quality over quantity**: Filter bad demonstrations
3. **Consistent setup**: Same camera positions, lighting
4. **Task variation**: Include different object positions
5. **Normalization**: Let LeRobot compute statistics

## Related Skills

- `data-pipeline` - Pipeline overview
- `recording` - Data collection
- `replay` - Data playback
- `arm-control` - Robot execution
