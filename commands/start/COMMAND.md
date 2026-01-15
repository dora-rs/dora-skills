---
name: start
description: Start a dora dataflow in daemon mode (background)
---

# /start Command

Start a dora dataflow in daemon mode, allowing it to run in the background.

## Usage

```
/start [<dataflow-file>] [--hot-reload] [--name <name>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<dataflow-file>` | Path to dataflow YAML | ./dataflow.yml |
| `--hot-reload` | Auto-restart on code changes | false |
| `--name` | Custom name for the dataflow | auto |

## What It Does

The start command:
1. Starts the dora daemon (if not running)
2. Launches the dataflow in detached mode
3. Returns a UUID for managing the dataflow
4. Runs nodes in the background

## Prerequisites

Before starting, ensure the daemon is running:
```bash
dora up
```

## Examples

### Basic start

```
/start
```

Starts the dataflow in `./dataflow.yml`:
```bash
$ dora up
Daemon started successfully

$ dora start dataflow.yml
Dataflow started: 550e8400-e29b-41d4-a716-446655440000

Use 'dora stop 550e8400-e29b-41d4-a716-446655440000' to stop
Use 'dora list' to view status
Use 'dora logs 550e8400-e29b-41d4-a716-446655440000' to view logs
```

### Start with hot reload

```
/start --hot-reload
```

Auto-restarts when you modify Python files:
```bash
$ dora start dataflow.yml --hot-reload
Dataflow started: abc-123-def (hot-reload enabled)

Watching for changes...
  - *.py
  - dataflow.yml

File changed: processor.py
Restarting dataflow...
Dataflow restarted successfully
```

### Start specific dataflow

```
/start robot/dataflow.yml
```

Starts a dataflow from a specific path.

### Start with custom name

```
/start --name my-robot
```

Easier to identify in listings:
```bash
$ dora list
UUID                                    Name        Status    Uptime
abc-123-def                            my-robot    Running   00:05:32
```

## Daemon Management

### Start daemon
```bash
dora up
```

Starts the dora daemon and coordinator:
```
Starting dora daemon...
  ✓ Coordinator started on port 53290
  ✓ Daemon ready

Daemon running at: http://localhost:53290
```

### Check daemon status
```bash
dora list
```

Shows all running dataflows.

### Stop daemon
```bash
dora destroy
```

Stops the daemon and all dataflows:
```
Stopping all dataflows...
  ✓ my-robot stopped
Shutting down daemon...
  ✓ Daemon stopped
```

## Start vs Run

### `/start` (Daemon Mode)
- **Detached**: Runs in background
- **Persistent**: Survives terminal close
- **Production**: Best for deployments
- **Management**: Use UUID to control
- **Monitoring**: View logs separately

```bash
dora start dataflow.yml
dora list  # Check status
dora logs <uuid>  # View logs
dora stop <uuid>  # Stop when done
```

### `/run` (Attached Mode)
- **Attached**: Runs in foreground
- **Temporary**: Stops when terminal closes
- **Development**: Best for debugging
- **Output**: Direct console output
- **Control**: Ctrl+C to stop

```bash
dora run dataflow.yml  # Blocks until stopped
```

## Workflow Examples

### Development Workflow
```bash
# Quick iterations with attached mode
/build --uv
/run  # See output immediately, Ctrl+C to stop
```

### Production Workflow
```bash
# Long-running deployment with daemon mode
dora up
/build --uv
/start
# Returns UUID: abc-123-def

# Later, check status
dora list

# View logs
dora logs abc-123-def --follow

# Stop when needed
dora stop abc-123-def
```

### Hot Reload Workflow
```bash
# Rapid development with auto-restart
dora up
/start --hot-reload

# Edit code, watch it restart automatically
nano processor.py  # Save changes
# Dataflow automatically restarts
```

## Monitoring Running Dataflows

### List all dataflows
```bash
dora list
```

Output:
```
UUID            Status   Uptime   Nodes  CPU%  MEM
abc-123-def    Running  01:30:45  3/3   12.5  256M
def-456-ghi    Running  00:15:20  5/5   8.2   512M
```

### View logs
```bash
# All logs
dora logs abc-123-def

# Follow logs (live)
dora logs abc-123-def --follow

# Specific node logs
dora logs abc-123-def --node camera

# Last N lines
dora logs abc-123-def --tail 100
```

### Check node status
```bash
dora list abc-123-def
```

Detailed view:
```
Dataflow: abc-123-def
Status: Running
Uptime: 01:30:45
Started: 2024-01-15 13:00:00

Nodes:
  camera      Running  CPU: 5%   MEM: 128M
  detector    Running  CPU: 15%  MEM: 512M
  visualize   Running  CPU: 8%   MEM: 256M
```

## Multiple Dataflows

Start multiple dataflows simultaneously:

```bash
# Start robot control
dora start robot/dataflow.yml --name robot
# Returns: abc-123

# Start vision pipeline
dora start vision/dataflow.yml --name vision
# Returns: def-456

# Start audio processing
dora start audio/dataflow.yml --name audio
# Returns: ghi-789

# List all
dora list
```

Output:
```
UUID        Name     Status    Uptime
abc-123     robot    Running   00:10:00
def-456     vision   Running   00:08:30
ghi-789     audio    Running   00:05:15
```

## Hot Reload

Hot reload watches for file changes and automatically restarts:

### What triggers reload?
- Python files (*.py)
- Dataflow YAML changes
- Configuration files

### What doesn't trigger reload?
- Log files
- Temporary files
- Build artifacts
- Data files

### Custom watch patterns
```bash
# Watch specific patterns
dora start dataflow.yml --hot-reload --watch "*.py,*.yaml,config/*"
```

## Error Handling

### Daemon not running
```
Error: Failed to connect to daemon
Solution: Run 'dora up' to start daemon
```

### Port already in use
```
Error: Port 53290 already in use
Solution:
  1. Check existing daemon: dora list
  2. Stop old daemon: dora destroy
  3. Or specify different port: dora up --port 53291
```

### Node failed to start
```
Dataflow started: abc-123-def
Warning: Node 'camera' failed to start

Check logs: dora logs abc-123-def --node camera
```

## Advanced Usage

### Automatic Restart on Failure
```bash
# Start with auto-restart policy
dora start dataflow.yml --restart-policy always
```

Restart policies:
- `no`: Never restart (default)
- `on-failure`: Restart if node crashes
- `always`: Always restart, even if stopped

### Resource Limits
```bash
# Limit CPU and memory
dora start dataflow.yml --cpu-limit 2.0 --memory-limit 4G
```

### Environment Variables
```bash
# Pass environment variables
dora start dataflow.yml --env MODEL=yolov8n.pt --env DEVICE=cuda
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Daemon won't start | Check port availability, kill old processes |
| Dataflow fails immediately | Check build, verify dependencies |
| Can't connect to coordinator | Check firewall, verify daemon is running |
| Hot reload not working | Verify watch patterns, check file permissions |
| High CPU usage | Profile nodes, check for infinite loops |
| Memory leak | Monitor logs, restart periodically |

## Best Practices

1. **Always build first**
   ```bash
   /build --uv
   /start
   ```

2. **Use named dataflows**
   ```bash
   /start --name my-app  # Easier to identify
   ```

3. **Enable hot reload in dev**
   ```bash
   /start --hot-reload  # Faster iteration
   ```

4. **Monitor logs**
   ```bash
   dora logs <uuid> --follow  # Watch for issues
   ```

5. **Graceful shutdown**
   ```bash
   dora stop <uuid>  # Stop before destroy
   dora destroy      # Clean shutdown
   ```

6. **Keep daemon running**
   ```bash
   # Start daemon once
   dora up

   # Start multiple dataflows
   /start app1.yml
   /start app2.yml
   ```

## Related Commands

- `/build` - Build dependencies before starting
- `/stop` - Stop running dataflow
- `/list` - List all running dataflows
- `/run` - Run in foreground (development)

## Environment Variables

```bash
# Daemon port
export DORA_DAEMON_PORT=53290

# Coordinator address
export DORA_COORDINATOR_ADDR=localhost:53290

# Auto-restart policy
export DORA_RESTART_POLICY=on-failure

# Hot reload enabled
export DORA_HOT_RELOAD=true

# Log level
export RUST_LOG=info
```

## See Also

- [Dora Daemon Architecture](https://dora-rs.ai/docs/daemon)
- [Production Deployment Guide](https://dora-rs.ai/docs/production)
- [Hot Reload Configuration](https://dora-rs.ai/docs/hot-reload)
