---
name: run
description: Run a dora dataflow in foreground (attached mode)
---

# /run Command

Run a dora dataflow in foreground mode with direct console output.

## Usage

```
/run [<dataflow-file>] [--uv] [--attach <node>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<dataflow-file>` | Path to dataflow YAML | ./dataflow.yml |
| `--uv` | Use uv package manager | false |
| `--attach` | Attach to specific node output | all |

## What It Does

The run command:
1. Builds dependencies (if needed)
2. Starts the dataflow in foreground
3. Shows output directly in console
4. Blocks until stopped (Ctrl+C)
5. Cleans up on exit

## Examples

### Basic run

```
/run
```

Runs `./dataflow.yml` in foreground:
```bash
$ dora run dataflow.yml
[INFO] Starting dataflow...
[INFO] camera: Opened video device 0
[INFO] detector: Loaded model yolov8n.pt
[INFO] visualize: Started Rerun viewer

[camera] Frame 0 captured
[detector] Detected 3 objects
[camera] Frame 1 captured
[detector] Detected 2 objects
...

^C
[INFO] Stopping dataflow...
[INFO] All nodes stopped
```

### Run with uv

```
/run --uv
```

Builds with uv before running:
```bash
$ dora run dataflow.yml --uv
Building with uv...
  ✓ opencv-video-capture installed
  ✓ dora-yolo installed
  ✓ dora-rerun installed

Starting dataflow...
[camera] Ready
[detector] Ready
[visualize] Ready
...
```

### Run specific dataflow

```
/run robot/dataflow.yml
```

Runs a dataflow from specific path.

### Attach to specific node

```
/run --attach camera
```

Shows only camera node output:
```bash
$ dora run dataflow.yml --attach camera
[camera] Frame 0 captured
[camera] Frame 1 captured
[camera] Frame 2 captured
...
```

## Run vs Start

| Feature | /run (Foreground) | /start (Background) |
|---------|-------------------|---------------------|
| **Output** | Direct to console | Saved to logs |
| **Terminal** | Blocks terminal | Returns immediately |
| **Control** | Ctrl+C to stop | Need UUID to stop |
| **Use case** | Development | Production |
| **Survival** | Dies with terminal | Survives terminal close |
| **Daemon** | Not required | Requires daemon |

### When to use /run
- ✓ During development
- ✓ For debugging
- ✓ Quick testing
- ✓ Seeing immediate output
- ✓ Interactive development

### When to use /start
- ✓ Production deployment
- ✓ Long-running services
- ✓ Multiple dataflows
- ✓ Remote servers
- ✓ Background processing

## Output Modes

### All nodes (default)
```bash
$ dora run dataflow.yml
[camera] Frame 0
[detector] Detected 3 objects
[visualize] Rendered
[camera] Frame 1
[detector] Detected 2 objects
[visualize] Rendered
```

### Single node
```bash
$ dora run dataflow.yml --attach detector
[detector] Detected 3 objects (person, car, dog)
[detector] Detected 2 objects (person, cat)
[detector] Detected 4 objects (person, person, car, bike)
```

### Multiple specific nodes
```bash
$ dora run dataflow.yml --attach camera,detector
[camera] Frame 0
[detector] Detected 3 objects
[camera] Frame 1
[detector] Detected 2 objects
```

## Keyboard Controls

While running:
- `Ctrl+C` - Graceful stop
- `Ctrl+Z` - Pause (suspend)
- `Ctrl+\` - Force quit

## Log Levels

### Set log level
```bash
# Debug level (verbose)
RUST_LOG=debug dora run dataflow.yml

# Info level (default)
RUST_LOG=info dora run dataflow.yml

# Warn level (quiet)
RUST_LOG=warn dora run dataflow.yml

# Error level (silent)
RUST_LOG=error dora run dataflow.yml
```

### Per-node log levels
```bash
RUST_LOG=camera=debug,detector=info dora run dataflow.yml
```

## Development Workflow

### Rapid iteration
```bash
# 1. Edit code
nano processor.py

# 2. Run immediately
/run

# 3. See output, test
# Press Ctrl+C when done

# 4. Repeat
```

### Debug specific node
```bash
# Add debug prints to node
echo "print(f'DEBUG: {data}')" >> camera.py

# Run and watch output
/run --attach camera
```

### Test changes
```bash
# Quick test loop
while true; do
  /run
  read -p "Test again? (y/n) " answer
  [[ $answer != "y" ]] && break
done
```

## Output Redirection

### Save to file
```bash
dora run dataflow.yml > output.log 2>&1
```

### Filter output
```bash
# Only errors
dora run dataflow.yml 2>&1 | grep ERROR

# Only specific node
dora run dataflow.yml 2>&1 | grep "\[camera\]"
```

### Tail recent output
```bash
dora run dataflow.yml 2>&1 | tail -f
```

### Split output
```bash
# Stdout to file, stderr to console
dora run dataflow.yml > output.log
```

## Running in Background

### Using nohup
```bash
nohup dora run dataflow.yml > output.log 2>&1 &
```

### Using screen
```bash
screen -dmS dora dora run dataflow.yml
screen -r dora  # Reattach
```

### Using tmux
```bash
tmux new -d -s dora 'dora run dataflow.yml'
tmux attach -t dora  # Reattach
```

**Note**: For proper background execution, use `/start` instead.

## Error Handling

### Build failures
```bash
$ dora run dataflow.yml
Error: Failed to build node 'detector'
  Package 'dora-yolo' not found

Solution: Check package name or build manually:
  pip install dora-yolo
```

### Node startup failures
```bash
$ dora run dataflow.yml
[INFO] Starting dataflow...
[ERROR] camera: Failed to open video device

Error: Node 'camera' failed to start

Solution: Check device availability:
  ls /dev/video*
```

### Runtime errors
```bash
[camera] Frame 0
[detector] Error: CUDA out of memory
[ERROR] detector crashed

Dataflow stopped due to node failure
```

## Testing and Validation

### Dry run
```bash
# Validate without running
dora check dataflow.yml
```

### Time-limited run
```bash
# Run for 10 seconds then stop
timeout 10 dora run dataflow.yml
```

### Run until condition
```bash
# Stop after specific output
dora run dataflow.yml | grep -m1 "Ready" && killall dora
```

### Automated testing
```bash
#!/bin/bash
# test-dataflow.sh

# Run and check output
OUTPUT=$(timeout 5 dora run dataflow.yml 2>&1)

if echo "$OUTPUT" | grep -q "Error"; then
  echo "✗ Test failed"
  exit 1
else
  echo "✓ Test passed"
  exit 0
fi
```

## Performance Monitoring

### With time
```bash
time dora run dataflow.yml
```

### With resource monitoring
```bash
# Monitor CPU/memory while running
pidstat -p $(pgrep -f "dora run") 1
```

### With profiling
```bash
# Python profiling
PYTHONPROFILE=1 dora run dataflow.yml
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Won't start | Check build with `/build` first |
| No output | Check log level: `RUST_LOG=debug` |
| Slow startup | Build separately with `/build --uv` |
| Stops immediately | Check logs for errors |
| High CPU | Profile nodes, check for loops |
| Port conflicts | Stop other dataflows |

## Best Practices

1. **Build separately for faster runs**
   ```bash
   /build --uv  # Once
   /run         # Fast startup
   ```

2. **Use appropriate log level**
   ```bash
   # Development
   RUST_LOG=debug /run

   # Production testing
   RUST_LOG=warn /run
   ```

3. **Attach to specific nodes when debugging**
   ```bash
   /run --attach problematic-node
   ```

4. **Save output for analysis**
   ```bash
   /run 2>&1 | tee output-$(date +%Y%m%d-%H%M%S).log
   ```

5. **Use /start for long-running tasks**
   ```bash
   # For > 5 minutes, use daemon mode
   /start
   ```

6. **Clean terminal on exit**
   ```bash
   dora run dataflow.yml; clear
   ```

## Related Commands

- `/build` - Build dependencies before running
- `/start` - Run in background (daemon mode)
- `/stop` - Stop daemon mode dataflows
- `/list` - List running dataflows
- `/visualize` - Visualize dataflow structure

## Environment Variables

```bash
# Auto-build before run
export DORA_AUTO_BUILD=true

# Use uv by default
export DORA_USE_UV=true

# Default log level
export RUST_LOG=info

# Colored output
export DORA_COLORED_OUTPUT=true

# Node output format
export DORA_OUTPUT_FORMAT=pretty
```

## See Also

- [Dora CLI Documentation](https://dora-rs.ai/docs/cli)
- [Debugging Guide](https://dora-rs.ai/docs/debugging)
- [Development Workflow](https://dora-rs.ai/docs/workflow)
