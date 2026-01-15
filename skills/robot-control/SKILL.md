---
name: robot-control
description: Robot control capabilities for dora-rs. Use when user asks about robot control, arm manipulation, motor control, or robotic hardware.
---

# Robot Control

Control robotic hardware with dora-rs dataflows.

## Overview

Dora supports various robotic platforms:

| Category | Hardware | Nodes |
|----------|----------|-------|
| Arms | Piper, Aloha, Reachy, Lebai | dora-piper, dora-aloha |
| Servos | Dynamixel, Feetech | dora-dynamixel, dora-feetech |
| Mobile | Robomaster, UGV | dora-robomaster |
| Grippers | Various | Integrated with arm nodes |

## Safety Principles

1. **Rate limiting**: Limit command frequency (typically 20Hz)
2. **Position limits**: Enforce joint limits
3. **Velocity limits**: Cap maximum speeds
4. **Emergency stop**: Always have a stop mechanism
5. **Workspace limits**: Define safe operating zones

## Control Architecture

### Open-Loop Control

```yaml
nodes:
  # Command generator
  - id: planner
    path: ./planner.py
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - action

  # Robot actuator
  - id: robot
    build: pip install dora-piper
    path: dora-piper
    inputs:
      action: planner/action
```

### Closed-Loop Control

```yaml
nodes:
  # Sensor feedback
  - id: camera
    path: opencv-video-capture
    outputs:
      - image

  # Perception
  - id: detector
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  # Controller
  - id: controller
    path: ./controller.py
    inputs:
      bbox: detector/bbox
      state: robot/jointstate
    outputs:
      - action

  # Robot actuator
  - id: robot
    path: dora-piper
    inputs:
      tick: dora/timer/millis/50
      action: controller/action
    outputs:
      - jointstate
```

## Data Formats

### Joint State

```python
# Joint positions (radians)
joint_state = {
    "names": ["joint1", "joint2", "joint3", ...],
    "positions": [0.0, 1.57, -0.5, ...],
}
```

### Joint Command

```python
# Target positions
joint_command = {
    "names": ["joint1", "joint2", "joint3", ...],
    "positions": [0.5, 1.0, -0.2, ...],
}
```

### End-Effector Pose

```python
# Cartesian pose (position + quaternion)
pose = {
    "position": [x, y, z],           # meters
    "orientation": [qx, qy, qz, qw], # quaternion
}
```

## Teleoperation Example

```yaml
nodes:
  # Leader arm (human controlled)
  - id: leader
    build: pip install dora-piper
    path: dora-piper
    inputs:
      tick: dora/timer/millis/20
    outputs:
      - jointstate
    env:
      ROLE: leader
      CAN_BUS: can0

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
      ROLE: follower
      CAN_BUS: can1
```

## Kinematics Integration

```yaml
- id: kinematics
  build: pip install dora-pytorch-kinematics
  path: dora-pytorch-kinematics
  inputs:
    jointstate: robot/jointstate
    target_pose: planner/target
  outputs:
    - joint_action
  env:
    URDF_PATH: /path/to/robot.urdf
```

## Rate Limiting

Always limit control frequency:

```python
import time

MIN_INTERVAL = 0.05  # 20 Hz
last_command_time = 0

def send_command(command):
    global last_command_time
    now = time.time()

    if now - last_command_time >= MIN_INTERVAL:
        node.send_output("action", command)
        last_command_time = now
```

## Emergency Stop

```python
def emergency_stop():
    """Send stop command to robot."""
    stop_command = pa.array([0.0] * num_joints)
    node.send_output("action", stop_command, {"emergency": "true"})
```

## Related Skills

- `arm-control` - Robotic arm control
- `actuators` - Servo motor control
- `chassis` - Mobile base control
