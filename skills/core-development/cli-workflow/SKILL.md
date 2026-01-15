---
name: cli-workflow
description: Dora CLI commands and workflow management. Use when user asks about dora commands, running dataflows, building nodes, or debugging.
---

# CLI Workflow

Master dora CLI commands for managing dataflow applications.

## Installation

```bash
# Install via pip (Python)
pip install dora-rs

# Install via cargo (Rust)
cargo install dora-cli

# Verify installation
dora --version
```

## Project Creation

### Create New Project

```bash
# Create Python dataflow project
dora new my-robot --lang python

# Create Rust dataflow project
dora new my-robot --lang rust

# Create Python node
dora new my-node --lang python --kind node

# Create Rust node
dora new my-node --lang rust --kind node
```

### Project Structure

```
my-robot/
├── dataflow.yml      # Dataflow definition
├── node_1/           # First node
│   ├── pyproject.toml
│   └── node_1/
│       ├── __init__.py
│       ├── __main__.py
│       └── main.py
└── node_2/           # Second node
    └── ...
```

## Building Dataflows

### Build Dependencies

```bash
# Build with pip
dora build dataflow.yml

# Build with uv (faster)
dora build dataflow.yml --uv

# Build specific nodes only
dora build dataflow.yml --nodes node1,node2
```

## Running Dataflows

### Simple Run (Attached)

```bash
# Run dataflow (blocks until completion)
dora run dataflow.yml

# Run with uv package manager
dora run dataflow.yml --uv
```

### Daemon Mode (Detached)

```bash
# Start the dora daemon and coordinator
dora up

# Start a dataflow
dora start dataflow.yml
# Returns: Dataflow UUID

# Check status
dora list

# Stop a dataflow
dora stop <dataflow-uuid>
# or stop all
dora stop --all

# Shutdown daemon
dora destroy
```

## Monitoring and Debugging

### View Logs

```bash
# View logs for all nodes
dora logs

# View logs for specific dataflow
dora logs <dataflow-uuid>

# View logs for specific node
dora logs <dataflow-uuid> --node <node-id>

# Follow logs (like tail -f)
dora logs --follow
```

### Check Status

```bash
# List running dataflows
dora list

# Show dataflow details
dora list <dataflow-uuid>
```

### Generate Visualization

```bash
# Generate Mermaid diagram
dora graph dataflow.yml

# Output to file
dora graph dataflow.yml --output graph.md

# Open in browser
dora graph dataflow.yml --open
```

## Hot Reload (Development)

```bash
# Start with hot reload enabled
dora start dataflow.yml --hot-reload

# Nodes will automatically restart when source files change
```

## Common Workflows

### Development Workflow

```bash
# 1. Create project
dora new my-project --lang python

# 2. Edit dataflow.yml and nodes

# 3. Build dependencies
dora build dataflow.yml --uv

# 4. Run
dora run dataflow.yml

# 5. Iterate: edit code, re-run
```

### Production Workflow

```bash
# 1. Start daemon
dora up

# 2. Start dataflow
dora start dataflow.yml
# Note the UUID: abc-123-def

# 3. Monitor
dora logs abc-123-def --follow

# 4. Stop when done
dora stop abc-123-def

# 5. Shutdown
dora destroy
```

### Debugging Workflow

```bash
# 1. Check dataflow syntax
dora graph dataflow.yml

# 2. Run in foreground for immediate feedback
dora run dataflow.yml 2>&1 | tee output.log

# 3. If using daemon, check logs
dora logs --follow

# 4. Check specific node
dora logs <uuid> --node problematic-node
```

## Environment Variables

```bash
# Set log level
export RUST_LOG=dora=debug

# Run with debug logging
RUST_LOG=debug dora run dataflow.yml

# Custom coordinator address
export DORA_COORDINATOR_ADDR=192.168.1.100:6012
```

## Distributed Deployment

### Multi-Machine Setup

```bash
# On coordinator machine
dora coordinator

# On each worker machine
dora daemon --coordinator-addr <coordinator-ip>:6012

# Start dataflow from any machine
dora start dataflow.yml --coordinator-addr <coordinator-ip>:6012
```

### Machine Assignment

```yaml
nodes:
  - id: camera
    path: camera-node
    deploy:
      machine: machine-1  # Run on specific machine

  - id: detector
    path: detector-node
    deploy:
      machine: machine-2
```

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Coordinator not found" | Run `dora up` first or check coordinator address |
| "Build failed" | Check pyproject.toml dependencies |
| "Node crashed" | Check `dora logs` for error messages |
| "No output" | Verify input/output connections in YAML |
| "Slow performance" | Use shared memory (default for large messages) |

### Debug Commands

```bash
# Check dora version
dora --version

# List available commands
dora --help

# Get help for specific command
dora run --help
```

## Command Reference

| Command | Description |
|---------|-------------|
| `dora new` | Create new project or node |
| `dora build` | Build dataflow dependencies |
| `dora run` | Run dataflow (attached) |
| `dora up` | Start daemon and coordinator |
| `dora start` | Start dataflow (detached) |
| `dora stop` | Stop running dataflow |
| `dora destroy` | Shutdown daemon |
| `dora list` | List running dataflows |
| `dora logs` | View node logs |
| `dora graph` | Generate visualization |

## Related Skills

- `core-development` - Dataflow YAML configuration
- `custom-node` - Creating custom nodes
