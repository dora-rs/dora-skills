---
name: core-development
description: Dataflow building fundamentals for dora-rs. Use when user asks about dataflow YAML, node configuration, input/output wiring, or timer inputs.
---

# Core Development

Foundation for building dataflow applications with dora-rs.

## Dataflow YAML Structure

A dataflow is defined in YAML with nodes and their connections:

```yaml
nodes:
  - id: sender              # Unique node identifier
    path: sender.py         # Path to executable or package name
    build: pip install ...  # Optional build command
    inputs:
      tick: dora/timer/millis/100  # Timer input
    outputs:
      - message             # Output port names
    env:
      CONFIG: value         # Environment variables

  - id: receiver
    path: receiver.py
    inputs:
      data: sender/message  # Subscribe to sender's output
    outputs:
      - result
```

## Node Configuration Options

### Basic Fields

| Field | Required | Description |
|-------|----------|-------------|
| `id` | Yes | Unique identifier for the node |
| `path` | Yes | Package name or path to executable |
| `build` | No | Build command (e.g., `pip install package`) |
| `inputs` | No | Input mappings |
| `outputs` | No | List of output port names |
| `env` | No | Environment variables |

### Input Mapping Syntax

```yaml
inputs:
  # Subscribe to another node's output
  input_name: source_node/output_name

  # Timer input (triggers every N milliseconds)
  tick: dora/timer/millis/100

  # Multiple inputs
  image: camera/image
  command: controller/action
```

### Output Declaration

```yaml
outputs:
  - image      # Simple output name
  - bbox       # Another output
  - text
```

## Timer Inputs

Dora provides built-in timer inputs for periodic triggering:

```yaml
inputs:
  # Trigger every 100 milliseconds (10 Hz)
  tick: dora/timer/millis/100

  # Trigger every 33 milliseconds (~30 Hz)
  tick: dora/timer/millis/33

  # Trigger every 1000 milliseconds (1 Hz)
  tick: dora/timer/millis/1000
```

## Environment Variables

Configure nodes with environment variables:

```yaml
env:
  # Model configuration
  MODEL_PATH: /path/to/model.pt
  DEVICE: cuda

  # Camera settings
  CAPTURE_PATH: "0"
  IMAGE_WIDTH: "640"
  IMAGE_HEIGHT: "480"

  # Serial ports
  SERIAL_PORT: /dev/ttyUSB0
  BAUD_RATE: "115200"
```

## Complete Example: Camera Pipeline

```yaml
nodes:
  # Camera capture node
  - id: camera
    build: pip install opencv-video-capture
    path: opencv-video-capture
    inputs:
      tick: dora/timer/millis/33
    outputs:
      - image
    env:
      CAPTURE_PATH: "0"
      IMAGE_WIDTH: "640"
      IMAGE_HEIGHT: "480"

  # Object detection
  - id: detector
    build: pip install dora-yolo
    path: dora-yolo
    inputs:
      image: camera/image
    outputs:
      - bbox
    env:
      MODEL: yolov8n.pt

  # Visualization
  - id: plot
    build: pip install dora-rerun
    path: dora-rerun
    inputs:
      image: camera/image
      boxes2d: detector/bbox
```

## Node Source Options

### Python Package (pip installable)
```yaml
- id: yolo
  build: pip install dora-yolo
  path: dora-yolo
```

### Local Python File
```yaml
- id: custom
  path: ./my_node.py
```

### Rust Executable
```yaml
- id: rust-node
  build: cargo build --release
  path: ./target/release/my_node
```

### Dynamic Nodes

Dynamic nodes are spawned manually (not by the framework):

```yaml
- id: dynamic-node
  path: dynamic-node-python
  inputs:
    tick: dora/timer/millis/100
  outputs:
    - output
  _unstable_dynamic: true  # Mark as dynamic
```

## Queue Size Configuration

Control input buffering:

```yaml
inputs:
  image:
    source: camera/image
    queue_size: 1  # Only keep latest (drop old frames)
```

## Multiple Dataflow Files

Split complex applications into modules:

```yaml
# main-dataflow.yml
nodes:
  - id: perception
    path: perception-dataflow.yml  # Include another dataflow

  - id: control
    path: control-dataflow.yml
```

## Best Practices

1. **Use descriptive node IDs**: `camera`, `object-detector`, `arm-controller`
2. **Set appropriate timer frequencies**: Match your processing rate
3. **Configure queue sizes**: Use `queue_size: 1` for real-time applications
4. **Use environment variables**: Keep configuration separate from code
5. **Organize large dataflows**: Split into multiple YAML files

## Related Skills

- `custom-node` - Create custom nodes in Python/Rust
- `cli-workflow` - Run and manage dataflows
