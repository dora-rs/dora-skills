---
name: chassis
description: Mobile base control for dora-rs. Use when user needs to control UGV, Robomaster, or other mobile robots.
---

# Mobile Base Control

Control mobile robot platforms including UGV and Robomaster.

## Robomaster S1 Configuration

```yaml
- id: robomaster
  build: pip install dora-robomaster
  path: dora-robomaster
  inputs:
    tick: dora/timer/millis/50
    velocity: controller/cmd_vel
    gimbal: controller/gimbal
  outputs:
    - odometry
    - imu
    - image
  env:
    ROBOT_IP: 192.168.2.1
```

## UGV Configuration

```yaml
- id: ugv
  build: pip install dora-ugv
  path: dora-ugv
  inputs:
    tick: dora/timer/millis/50
    velocity: controller/cmd_vel
  outputs:
    - odometry
    - battery
  env:
    SERIAL_PORT: /dev/ttyUSB0
    BAUD_RATE: "115200"
```

## Velocity Command Format

### Differential Drive

```python
import pyarrow as pa

# Linear and angular velocity
# [linear_x, angular_z]
# linear_x: m/s (forward/backward)
# angular_z: rad/s (rotation)

cmd_vel = [0.5, 0.0]   # Forward at 0.5 m/s
cmd_vel = [0.0, 0.5]   # Rotate left
cmd_vel = [-0.5, 0.0]  # Backward

node.send_output("velocity", pa.array(cmd_vel))
```

### Mecanum/Omnidirectional

```python
# [linear_x, linear_y, angular_z]
# linear_x: forward/backward
# linear_y: left/right (strafe)
# angular_z: rotation

cmd_vel = [0.5, 0.0, 0.0]   # Forward
cmd_vel = [0.0, 0.5, 0.0]   # Strafe left
cmd_vel = [0.0, 0.0, 0.5]   # Rotate

node.send_output("velocity", pa.array(cmd_vel))
```

## Complete Mobile Robot Pipeline

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

  # Object detection
  - id: detector
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox

  # Navigation controller
  - id: nav
    path: ./navigation.py
    inputs:
      bbox: detector/bbox
      odometry: robot/odometry
    outputs:
      - cmd_vel

  # Mobile base
  - id: robot
    build: pip install dora-robomaster
    path: dora-robomaster
    inputs:
      tick: dora/timer/millis/50
      velocity: nav/cmd_vel
    outputs:
      - odometry
      - imu
```

## Navigation Controller Example

```python
from dora import Node
import numpy as np
import pyarrow as pa

node = Node()

IMAGE_CENTER_X = 320  # For 640px width

for event in node:
    if event["id"] == "bbox":
        detections = event["value"]

        if len(detections) > 0:
            # Track first detected object
            bbox = detections[0]["bbox"]
            x, y, w, h = bbox

            # Calculate object center
            obj_center_x = x + w / 2

            # Proportional control to center object
            error = obj_center_x - IMAGE_CENTER_X
            angular = -error * 0.005  # P gain

            # Move forward if object is centered
            if abs(error) < 50:
                linear = 0.3
            else:
                linear = 0.0

            cmd_vel = [linear, angular]
            node.send_output("cmd_vel", pa.array(cmd_vel))

        else:
            # No detection - stop
            node.send_output("cmd_vel", pa.array([0.0, 0.0]))
```

## Odometry Data

```python
for event in node:
    if event["id"] == "odometry":
        odom = event["value"]
        # Position: [x, y, theta]
        x = odom[0]
        y = odom[1]
        theta = odom[2]
        print(f"Position: ({x:.2f}, {y:.2f}), Heading: {np.degrees(theta):.1f}°")
```

## IMU Data

```python
for event in node:
    if event["id"] == "imu":
        imu = event["value"]
        # [accel_x, accel_y, accel_z, gyro_x, gyro_y, gyro_z]
        accel = imu[:3]
        gyro = imu[3:]
        print(f"Accel: {accel}, Gyro: {gyro}")
```

## Gimbal Control (Robomaster)

```python
# Gimbal pitch and yaw angles (degrees)
gimbal_cmd = [0.0, 30.0]  # pitch=0, yaw=30
node.send_output("gimbal", pa.array(gimbal_cmd))
```

## Keyboard Control

```yaml
nodes:
  - id: keyboard
    build: pip install dora-keyboard
    path: dora-keyboard
    outputs:
      - keypress

  - id: teleop
    path: ./keyboard_teleop.py
    inputs:
      keypress: keyboard/keypress
    outputs:
      - cmd_vel

  - id: robot
    path: dora-robomaster
    inputs:
      velocity: teleop/cmd_vel
```

**keyboard_teleop.py:**
```python
from dora import Node
import pyarrow as pa

node = Node()

LINEAR_SPEED = 0.5
ANGULAR_SPEED = 1.0

for event in node:
    if event["id"] == "keypress":
        key = event["value"][0].as_py()

        if key == "w":
            cmd = [LINEAR_SPEED, 0.0]
        elif key == "s":
            cmd = [-LINEAR_SPEED, 0.0]
        elif key == "a":
            cmd = [0.0, ANGULAR_SPEED]
        elif key == "d":
            cmd = [0.0, -ANGULAR_SPEED]
        elif key == " ":  # Space = stop
            cmd = [0.0, 0.0]
        else:
            continue

        node.send_output("cmd_vel", pa.array(cmd))
```

## Waypoint Navigation

```python
import numpy as np

waypoints = [
    [1.0, 0.0],
    [1.0, 1.0],
    [0.0, 1.0],
    [0.0, 0.0],
]
current_waypoint = 0

def navigate_to_waypoint(current_pos, target_pos):
    """Simple waypoint navigation."""
    dx = target_pos[0] - current_pos[0]
    dy = target_pos[1] - current_pos[1]
    distance = np.sqrt(dx**2 + dy**2)

    if distance < 0.1:  # Reached waypoint
        return None

    # Calculate heading to target
    target_heading = np.arctan2(dy, dx)
    heading_error = target_heading - current_pos[2]

    # Wrap to [-pi, pi]
    while heading_error > np.pi:
        heading_error -= 2 * np.pi
    while heading_error < -np.pi:
        heading_error += 2 * np.pi

    # Control
    if abs(heading_error) > 0.1:
        return [0.0, np.sign(heading_error) * 0.5]
    else:
        return [0.3, heading_error * 0.5]
```

## Safety Features

### Velocity Limits

```python
MAX_LINEAR = 1.0   # m/s
MAX_ANGULAR = 2.0  # rad/s

def limit_velocity(cmd_vel):
    linear = np.clip(cmd_vel[0], -MAX_LINEAR, MAX_LINEAR)
    angular = np.clip(cmd_vel[1], -MAX_ANGULAR, MAX_ANGULAR)
    return [linear, angular]
```

### Emergency Stop

```python
def emergency_stop():
    """Send zero velocity."""
    node.send_output("cmd_vel", pa.array([0.0, 0.0]))
```

### Obstacle Detection

```yaml
nodes:
  - id: lidar
    path: dora-lidar
    outputs:
      - scan

  - id: obstacle_avoidance
    path: ./obstacle_avoid.py
    inputs:
      scan: lidar/scan
      cmd_vel_in: nav/cmd_vel
    outputs:
      - cmd_vel_out
```

## Related Skills

- `robot-control` - Control overview
- `arm-control` - Arm manipulation
- `ml-vision` - Visual navigation
