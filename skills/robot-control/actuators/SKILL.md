---
name: actuators
description: Servo motor control for dora-rs. Use when user needs to control Dynamixel, Feetech, or other servo motors.
---

# Servo Motor Control

Control Dynamixel and Feetech servo motors.

## Dynamixel Configuration

```yaml
- id: dynamixel
  build: pip install dora-dynamixel
  path: dora-dynamixel
  inputs:
    tick: dora/timer/millis/50    # State update rate
    position: controller/target   # Target positions
    velocity: controller/speed    # Target velocities
  outputs:
    - position   # Current positions
    - velocity   # Current velocities
    - torque     # Current torques
  env:
    SERIAL_PORT: /dev/ttyUSB0
    BAUD_RATE: "1000000"
    MOTOR_IDS: "1,2,3,4,5"
```

## Feetech Configuration

```yaml
- id: feetech
  build: pip install dora-feetech
  path: dora-feetech
  inputs:
    tick: dora/timer/millis/50
    position: controller/target
  outputs:
    - position
    - velocity
  env:
    SERIAL_PORT: /dev/ttyUSB0
    BAUD_RATE: "1000000"
    MOTOR_IDS: "1,2,3"
```

## Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| `SERIAL_PORT` | Serial port path | /dev/ttyUSB0 |
| `BAUD_RATE` | Communication speed | 1000000 |
| `MOTOR_IDS` | Comma-separated IDs | 1 |
| `PROTOCOL` | Dynamixel protocol | 2.0 |

## Position Control

### Set Position

```python
import pyarrow as pa

# Target positions for each motor (in motor units or radians)
# Motor units: 0-4095 for Dynamixel
# Radians: -π to π

positions = [2048, 2048, 2048]  # Center position for 3 motors
node.send_output("position", pa.array(positions))
```

### Read Position

```python
for event in node:
    if event["id"] == "position":
        positions = event["value"].to_numpy()
        print(f"Motor positions: {positions}")
```

## Velocity Control

```python
# Set velocity for each motor
velocities = [100, 100, 100]  # Same velocity for all
node.send_output("velocity", pa.array(velocities))
```

## Complete Servo Pipeline

```yaml
nodes:
  # Joystick or other input
  - id: input
    path: ./joystick_input.py
    inputs:
      tick: dora/timer/millis/50
    outputs:
      - command

  # Position controller
  - id: controller
    path: ./position_controller.py
    inputs:
      command: input/command
      current_pos: servos/position
    outputs:
      - target

  # Servo motors
  - id: servos
    build: pip install dora-dynamixel
    path: dora-dynamixel
    inputs:
      tick: dora/timer/millis/50
      position: controller/target
    outputs:
      - position
      - velocity
    env:
      SERIAL_PORT: /dev/ttyUSB0
      MOTOR_IDS: "1,2,3"
```

## Position Controller Example

```python
from dora import Node
import numpy as np
import pyarrow as pa

node = Node()

current_positions = None
target_positions = None

for event in node:
    if event["id"] == "current_pos":
        current_positions = event["value"].to_numpy()

    elif event["id"] == "command":
        # Command is relative motion
        command = event["value"].to_numpy()

        if current_positions is not None:
            # Add command to current position
            target_positions = current_positions + command

            # Clamp to valid range
            target_positions = np.clip(target_positions, 0, 4095)

            node.send_output("target", pa.array(target_positions))
```

## Multi-Motor Synchronization

```python
def sync_write_positions(motor_ids, positions):
    """Write positions to multiple motors simultaneously."""
    # Pack data for all motors
    data = []
    for motor_id, pos in zip(motor_ids, positions):
        data.append({"id": motor_id, "position": pos})

    node.send_output("sync_position", pa.array(data))
```

## Reading Motor State

```python
for event in node:
    if event["id"] == "position":
        positions = event["value"].to_numpy()

    elif event["id"] == "velocity":
        velocities = event["value"].to_numpy()

    elif event["id"] == "torque":
        torques = event["value"].to_numpy()

    # Print state
    print(f"Pos: {positions}, Vel: {velocities}, Torque: {torques}")
```

## Unit Conversion

### Dynamixel

```python
# Position: 0-4095 (12-bit) = 0-360 degrees
def pos_to_degrees(pos):
    return pos * 360.0 / 4095.0

def degrees_to_pos(deg):
    return int(deg * 4095.0 / 360.0)

# Velocity: units depend on model
# XM/XL series: 0.229 rpm per unit
def velocity_to_rpm(vel):
    return vel * 0.229
```

### Feetech

```python
# Position: similar to Dynamixel
# Velocity: varies by model
```

## Torque Control

```python
# Enable torque
node.send_output("torque_enable", pa.array([1, 1, 1]))  # Enable all

# Disable torque
node.send_output("torque_enable", pa.array([0, 0, 0]))  # Disable all
```

## PID Tuning

```yaml
env:
  # Position PID gains
  P_GAIN: "800"
  I_GAIN: "0"
  D_GAIN: "0"

  # Velocity limit
  VELOCITY_LIMIT: "100"
```

## Error Handling

```python
for event in node:
    if event["type"] == "ERROR":
        error = event["error"]
        print(f"Servo error: {error}")

        # Common errors:
        # - Overload: motor stalled
        # - Overheating: reduce duty cycle
        # - Communication: check cable/port
```

## Safety Features

### Position Limits

```python
MIN_POSITION = 1000
MAX_POSITION = 3000

def safe_position(target):
    return np.clip(target, MIN_POSITION, MAX_POSITION)
```

### Velocity Ramp

```python
def ramp_velocity(current_vel, target_vel, max_accel=10):
    """Gradually change velocity."""
    diff = target_vel - current_vel
    if abs(diff) > max_accel:
        diff = max_accel * np.sign(diff)
    return current_vel + diff
```

## Multiple Serial Ports

```yaml
nodes:
  # First chain
  - id: chain1
    path: dora-dynamixel
    env:
      SERIAL_PORT: /dev/ttyUSB0
      MOTOR_IDS: "1,2,3"

  # Second chain
  - id: chain2
    path: dora-dynamixel
    env:
      SERIAL_PORT: /dev/ttyUSB1
      MOTOR_IDS: "4,5,6"
```

## Debugging

### List Connected Motors

```bash
# Use Dynamixel Wizard or SDK to scan
python -m dynamixel_sdk.port_handler
```

### Check Communication

```python
# Test read
for event in node:
    if event["id"] == "position":
        print(f"Communication OK: {event['value']}")
        break
```

## Related Skills

- `robot-control` - Control overview
- `arm-control` - Arm integration
- `chassis` - Mobile base control
