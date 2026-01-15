---
name: stop
description: Stop running dora dataflows
---

# /stop Command

Stop one or more running dora dataflows that were started in daemon mode.

## Usage

```
/stop [<dataflow-uuid>] [--all] [--name <name>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<dataflow-uuid>` | UUID of dataflow to stop | - |
| `--all` | Stop all running dataflows | false |
| `--name` | Stop dataflow by name | - |

## What It Does

The stop command:
1. Sends stop signal to dataflow coordinator
2. Gracefully terminates all nodes
3. Cleans up resources
4. Removes dataflow from active list

## Examples

### Stop specific dataflow

```
/stop abc-123-def
```

Stops the dataflow with UUID `abc-123-def`:
```bash
$ dora stop abc-123-def
Stopping dataflow abc-123-def...
  ✓ camera stopped
  ✓ detector stopped
  ✓ visualize stopped
Dataflow stopped successfully
```

### Stop all dataflows

```
/stop --all
```

Stops all running dataflows:
```bash
$ dora stop --all
Stopping all dataflows...

Stopping robot (abc-123-def)...
  ✓ arm-control stopped
  ✓ camera stopped
Dataflow stopped

Stopping vision (def-456-ghi)...
  ✓ detector stopped
  ✓ tracker stopped
Dataflow stopped

All dataflows stopped (2 total)
```

### Stop by name

```
/stop --name my-robot
```

Stops dataflow by its custom name:
```bash
$ dora stop --name my-robot
Found dataflow: my-robot (abc-123-def)
Stopping...
  ✓ All nodes stopped
Dataflow stopped successfully
```

## Finding Dataflow UUID

### List all dataflows
```bash
dora list
```

Output shows UUIDs:
```
UUID            Name       Status    Uptime
abc-123-def     robot      Running   01:30:00
def-456-ghi     vision     Running   00:45:00
```

### Get UUID from start command
```bash
$ dora start dataflow.yml
Dataflow started: abc-123-def
# Use this UUID to stop
```

### Save UUID for later
```bash
# Start and save UUID
DATAFLOW_UUID=$(dora start dataflow.yml | grep -oP '[0-9a-f-]{36}')
echo $DATAFLOW_UUID > .dataflow-uuid

# Stop later
dora stop $(cat .dataflow-uuid)
```

## Graceful Shutdown

The stop command performs a graceful shutdown:

1. **Send stop signal** to coordinator
2. **Wait for nodes** to finish current tasks
3. **Terminate cleanly** with timeout
4. **Release resources** (ports, memory)
5. **Remove from registry**

### Shutdown sequence
```
Stopping dataflow...
  camera: Closing video capture...     [1s]
  detector: Saving model state...      [2s]
  visualize: Flushing buffers...       [1s]
All nodes stopped gracefully
```

## Force Stop

If graceful shutdown fails:

```bash
# Try graceful stop first
dora stop abc-123-def

# If hung, force stop
dora stop abc-123-def --force
```

Force stop:
- Sends SIGKILL instead of SIGTERM
- Immediately terminates processes
- May lose unsaved data
- Use as last resort

## Stop Patterns

### Stop and restart
```bash
# Stop current version
dora stop abc-123-def

# Start new version
dora start dataflow.yml
```

### Stop all and shutdown
```bash
# Stop all dataflows
dora stop --all

# Shutdown daemon
dora destroy
```

### Conditional stop
```bash
# Stop if running for more than 1 hour
UPTIME=$(dora list abc-123-def | grep Uptime | awk '{print $2}')
if [[ $UPTIME > "01:00:00" ]]; then
  dora stop abc-123-def
fi
```

## Error Handling

### Dataflow not found
```
Error: Dataflow abc-123-def not found

Possible reasons:
  1. Dataflow already stopped
  2. UUID is incorrect
  3. Daemon was restarted

Run 'dora list' to see active dataflows
```

### Node won't stop
```
Warning: Node 'camera' not responding
Waiting... (10s timeout)
Force stopping node...
  ✓ Node terminated
```

### Daemon not running
```
Error: Cannot connect to daemon

Solution:
  1. Check if daemon is running: dora list
  2. If not, there are no dataflows to stop
```

## Monitoring Stop Process

### Watch logs during stop
```bash
# Terminal 1: Watch logs
dora logs abc-123-def --follow

# Terminal 2: Stop
dora stop abc-123-def
```

### Check final status
```bash
dora stop abc-123-def
dora list  # Verify it's gone
```

## Stopping Multiple Dataflows

### Stop by pattern
```bash
# Get all robot dataflows
for UUID in $(dora list | grep robot | awk '{print $1}'); do
  dora stop $UUID
done
```

### Stop selectively
```bash
# Stop all except one
dora list | grep -v abc-123-def | awk '{print $1}' | xargs -I {} dora stop {}
```

### Stop with confirmation
```bash
# Interactive stop
dora list
read -p "Enter UUID to stop: " UUID
dora stop $UUID
```

## Integration Examples

### Shell script
```bash
#!/bin/bash
# stop-robot.sh

DATAFLOW_UUID=$(cat .dataflow-uuid)

echo "Stopping robot dataflow..."
dora stop $DATAFLOW_UUID

if [ $? -eq 0 ]; then
  echo "✓ Stopped successfully"
  rm .dataflow-uuid
else
  echo "✗ Failed to stop"
  exit 1
fi
```

### Python script
```python
import subprocess
import sys

def stop_dataflow(uuid):
    """Stop a dora dataflow by UUID"""
    try:
        result = subprocess.run(
            ['dora', 'stop', uuid],
            check=True,
            capture_output=True,
            text=True
        )
        print(f"✓ Stopped {uuid}")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Failed to stop {uuid}: {e.stderr}")
        return False

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python stop.py <uuid>")
        sys.exit(1)

    uuid = sys.argv[1]
    success = stop_dataflow(uuid)
    sys.exit(0 if success else 1)
```

### Systemd service
```bash
# Stop dataflow when service stops
[Service]
ExecStop=/usr/local/bin/dora stop %n
```

## Cleanup After Stop

### Remove logs
```bash
dora stop abc-123-def
rm -rf ~/.dora/logs/abc-123-def
```

### Clear temporary files
```bash
dora stop abc-123-def
rm -rf /tmp/dora-abc-123-def*
```

### Free resources
Stopping automatically frees:
- Memory used by nodes
- Network ports
- File handles
- GPU memory
- Camera devices

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Dataflow won't stop | Use `--force` flag |
| Wrong UUID | Check `dora list` for correct UUID |
| Permission denied | Run with appropriate user/permissions |
| Nodes hanging | Check node logs, may need force stop |
| Partial stop | Some nodes stopped, others hung - use force |
| Daemon crashed | No running dataflows, no action needed |

## Best Practices

1. **Save UUIDs**
   ```bash
   # Save on start
   dora start dataflow.yml | tee .dataflow-uuid

   # Use on stop
   dora stop $(cat .dataflow-uuid)
   ```

2. **Graceful shutdown first**
   ```bash
   # Try graceful
   dora stop abc-123-def

   # Force only if needed
   if [ $? -ne 0 ]; then
     dora stop abc-123-def --force
   fi
   ```

3. **Stop before modifying**
   ```bash
   # Stop before editing
   dora stop abc-123-def
   nano dataflow.yml
   dora start dataflow.yml
   ```

4. **Use names for easier management**
   ```bash
   # Start with name
   dora start dataflow.yml --name my-app

   # Stop by name
   dora stop --name my-app
   ```

5. **Monitor during stop**
   ```bash
   # Watch logs to confirm clean shutdown
   dora logs abc-123-def --follow &
   dora stop abc-123-def
   ```

6. **Clean stop all before shutdown**
   ```bash
   # Proper cleanup sequence
   dora stop --all
   sleep 2
   dora destroy
   ```

## Automated Stop Scenarios

### Stop on signal
```bash
#!/bin/bash
# trap-stop.sh

DATAFLOW_UUID=$(cat .dataflow-uuid)

trap "dora stop $DATAFLOW_UUID; exit" SIGINT SIGTERM

# Run something
while true; do
  sleep 1
done
```

### Stop on condition
```bash
# Stop if CPU usage too high
CPU=$(dora list abc-123-def | grep CPU | awk '{print $2}')
if (( $(echo "$CPU > 90" | bc -l) )); then
  echo "High CPU detected, stopping..."
  dora stop abc-123-def
fi
```

### Scheduled stop
```bash
# Cron job to stop at specific time
# crontab -e
0 22 * * * dora stop --all  # Stop all at 10 PM
```

### Stop after duration
```bash
# Stop after 1 hour
dora start dataflow.yml
sleep 3600
dora stop --all
```

## Related Commands

- `/start` - Start dataflow in daemon mode
- `/list` - List running dataflows to find UUID
- `/run` - Run in foreground (stops with Ctrl+C)
- `/build` - Rebuild before restarting

## When to Stop

### Development
- Before editing code
- When switching branches
- After testing
- Before rebuilding

### Production
- For maintenance
- To deploy updates
- When scaling down
- Before server shutdown

### Debugging
- To restart with changes
- To clear stuck state
- To free resources
- To apply new config

## Environment Variables

```bash
# Stop timeout (seconds)
export DORA_STOP_TIMEOUT=30

# Force stop by default
export DORA_FORCE_STOP=false

# Stop confirmation
export DORA_CONFIRM_STOP=true
```

## See Also

- [Dora Daemon Management](https://dora-rs.ai/docs/daemon)
- [Graceful Shutdown Guide](https://dora-rs.ai/docs/shutdown)
- [Process Management](https://dora-rs.ai/docs/processes)
