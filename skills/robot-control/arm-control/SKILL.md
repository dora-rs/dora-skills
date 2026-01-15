---
name: arm-control
description: Robotic arm control for dora-rs. Use when user needs to control Piper, Aloha, Reachy, or other robotic arms, including joint control and end-effector positioning.
---

# Robotic Arm Control

Control robotic arms including Piper, Aloha, and Reachy.

## Piper Arm Configuration

```yaml
- id: piper
  build: pip install dora-piper
  path: dora-piper
  inputs:
    tick: dora/timer/millis/50        # 20 Hz state update
    joint_action: controller/action   # Joint commands
    end_pose: controller/pose         # End-effector pose
    gripper_action: controller/grip   # Gripper control
  outputs:
    - jointstate     # Current joint positions
    - end_pose       # Current end-effector pose
    - gripper_state  # Gripper state
  env:
    CAN_BUS: can0              # CAN interface
    RATE_LIMIT_HZ: "20"        # Command rate limit
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `CAN_BUS` | CAN interface name | can0 |
| `RATE_LIMIT_HZ` | Max command rate | 20 |
| `JOINT_LIMITS` | Enable joint limits | true |
| `VELOCITY_SCALE` | Max velocity (0-1) | 0.5 |

## Input Formats

### Joint Action

```python
import pyarrow as pa

# 6-DOF arm joint positions (radians)
joint_positions = [0.0, 0.5, -0.3, 1.0, 0.0, 0.0]
node.send_output("joint_action", pa.array(joint_positions))
```

### End-Effector Pose

```python
# Position (x, y, z) in meters + Quaternion (qx, qy, qz, qw)
pose = [0.3, 0.0, 0.2, 0.0, 0.0, 0.0, 1.0]
node.send_output("end_pose", pa.array(pose))
```

### Gripper Action

```python
# Gripper position: 0.0 = closed, 1.0 = open
gripper_position = 0.5  # Half open
node.send_output("gripper_action", pa.array([gripper_position]))
```

## Output Formats

### Joint State

```python
for event in node:
    if event["id"] == "jointstate":
        joints = event["value"].to_numpy()
        # [joint1, joint2, joint3, joint4, joint5, joint6]
        print(f"Joint positions: {joints}")
```

### End-Effector Pose

```python
for event in node:
    if event["id"] == "end_pose":
        pose = event["value"].to_numpy()
        position = pose[:3]      # [x, y, z]
        orientation = pose[3:]   # [qx, qy, qz, qw]
        print(f"Position: {position}")
```

## Complete Arm Control Pipeline

```yaml
nodes:
  # Camera for visual feedback
  - id: camera
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/33
    outputs:
      - image

  # Object detection
  - id: detector
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  # Motion planner
  - id: planner
    path: ./motion_planner.py
    inputs:
      bbox: detector/bbox
      jointstate: arm/jointstate
    outputs:
      - action

  # Arm controller
  - id: arm
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/50
      joint_action: planner/action
    outputs:
      - jointstate
      - end_pose
    env:
      CAN_BUS: can0
```

## Motion Planner Example

```python
from dora import Node
import numpy as np
import pyarrow as pa

node = Node()

# Home position
HOME_POSITION = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

current_target = None
current_joints = None

for event in node:
    if event["id"] == "jointstate":
        current_joints = event["value"].to_numpy()

    elif event["id"] == "bbox":
        # Calculate target from detection
        detections = event["value"]
        if len(detections) > 0:
            bbox = detections[0]["bbox"]
            current_target = calculate_target(bbox)

    elif event["id"] == "tick":
        if current_target is not None and current_joints is not None:
            # Interpolate towards target
            action = interpolate(current_joints, current_target, step=0.1)
            node.send_output("action", pa.array(action))
```

## Inverse Kinematics

Use dora-pytorch-kinematics for IK:

```yaml
- id: ik
  build: pip install dora-pytorch-kinematics
  path: dora-pytorch-kinematics
  inputs:
    current_joints: arm/jointstate
    target_pose: planner/target_pose
  outputs:
    - joint_action
  env:
    URDF_PATH: /path/to/piper.urdf
```

## Teleoperation Setup

### Leader-Follower

```yaml
nodes:
  # Leader arm (human control)
  - id: leader
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
    outputs:
      - jointstate
    env:
      CAN_BUS: can0
      MODE: passive  # No motor control

  # Follower arm (robot)
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
```

### Recording Teleoperation

```yaml
- id: recorder
  path: ./teleoperation_recorder.py
  inputs:
    leader_joints: leader/jointstate
    follower_joints: follower/jointstate
    image: camera/image
```

## Aloha Bimanual Setup

```yaml
nodes:
  # Left arm
  - id: left_arm
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
      joint_action: planner/left_action
    outputs:
      - jointstate
    env:
      CAN_BUS: can0
      ARM_ID: left

  # Right arm
  - id: right_arm
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
      joint_action: planner/right_action
    outputs:
      - jointstate
    env:
      CAN_BUS: can1
      ARM_ID: right

  # Bimanual planner
  - id: planner
    path: ./bimanual_planner.py
    inputs:
      left_state: left_arm/jointstate
      right_state: right_arm/jointstate
    outputs:
      - left_action
      - right_action
```

## Safety Features

### Joint Limits

```python
JOINT_LIMITS = [
    (-3.14, 3.14),   # Joint 1
    (-1.57, 1.57),   # Joint 2
    (-2.0, 2.0),     # Joint 3
    (-3.14, 3.14),   # Joint 4
    (-1.57, 1.57),   # Joint 5
    (-3.14, 3.14),   # Joint 6
]

def clip_joints(joints):
    """Enforce joint limits."""
    clipped = []
    for i, j in enumerate(joints):
        low, high = JOINT_LIMITS[i]
        clipped.append(np.clip(j, low, high))
    return clipped
```

### Velocity Limiting

```python
def limit_velocity(current, target, max_velocity=0.5):
    """Limit joint velocity."""
    diff = np.array(target) - np.array(current)
    velocity = np.linalg.norm(diff)

    if velocity > max_velocity:
        diff = diff * (max_velocity / velocity)

    return current + diff
```

## Debugging

```python
# Print arm state
for event in node:
    if event["id"] == "jointstate":
        joints = event["value"].to_numpy()
        print(f"Joints (deg): {np.degrees(joints)}")

    elif event["id"] == "end_pose":
        pose = event["value"].to_numpy()
        print(f"End position: {pose[:3]}")
```

## Related Skills

- `robot-control` - Control overview
- `actuators` - Servo control
- `data-pipeline/recording` - Record demonstrations
