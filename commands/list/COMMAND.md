---
name: list
description: List and inspect running dora dataflows
---

# /list Command

List all currently running dora dataflows and inspect their status.

## Usage

```
/list [<dataflow-uuid>] [--format <format>] [--watch]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<dataflow-uuid>` | Show details for specific dataflow | - |
| `--format` | Output format (table, json, yaml) | table |
| `--watch` | Continuous monitoring mode | false |

## What It Shows

The list command displays:
- Dataflow UUIDs
- Custom names (if set)
- Current status
- Uptime
- Node count and health
- Resource usage (CPU, memory)

## Examples

### List all dataflows

```
/list
```

Shows overview of all running dataflows:
```bash
$ dora list

UUID            Name       Status    Uptime    Nodes  CPU%   MEM
abc-123-def     robot      Running   01:30:45  3/3    12.5   256M
def-456-ghi     vision     Running   00:45:20  5/5    8.2    512M
ghi-789-jkl     audio      Running   00:15:10  4/4    5.1    128M

Total: 3 dataflows running
```

### Show specific dataflow

```
/list abc-123-def
```

Detailed view of a single dataflow:
```bash
$ dora list abc-123-def

Dataflow: robot
UUID: abc-123-def
Status: Running
Started: 2024-01-15 13:00:00
Uptime: 01:30:45
File: /home/user/robot/dataflow.yml

Nodes (3):
  ID            Status     CPU%   MEM     Uptime
  camera        Running    5.2    128M    01:30:45
  detector      Running    15.8   512M    01:30:45
  visualize     Running    8.5    256M    01:30:45

Connections:
  camera/image → detector/image
  camera/image → visualize/image
  detector/bbox → visualize/boxes2d

Resources:
  Total CPU:    29.5%
  Total Memory: 896M
  Network I/O:  15 MB/s
```

### JSON format

```
/list --format json
```

Machine-readable output:
```json
{
  "dataflows": [
    {
      "uuid": "abc-123-def",
      "name": "robot",
      "status": "running",
      "started_at": "2024-01-15T13:00:00Z",
      "uptime": "01:30:45",
      "nodes": [
        {
          "id": "camera",
          "status": "running",
          "cpu_percent": 5.2,
          "memory_mb": 128,
          "uptime": "01:30:45"
        }
      ],
      "total_cpu": 29.5,
      "total_memory_mb": 896
    }
  ],
  "total_count": 1
}
```

### Watch mode

```
/list --watch
```

Continuous monitoring with auto-refresh:
```bash
$ dora list --watch

[Updating every 2s, press Ctrl+C to exit]

UUID            Name       Status    Uptime    Nodes  CPU%   MEM
abc-123-def     robot      Running   01:30:47  3/3    13.1   258M
def-456-ghi     vision     Running   00:45:22  5/5    7.8    510M
ghi-789-jkl     audio      Running   00:15:12  4/4    5.3    130M

[Last updated: 2024-01-15 14:30:47]
```

## Status Types

| Status | Description | Color |
|--------|-------------|-------|
| Running | All nodes active | 🟢 Green |
| Starting | Nodes launching | 🟡 Yellow |
| Degraded | Some nodes failed | 🟠 Orange |
| Stopping | Shutting down | 🔵 Blue |
| Failed | Critical error | 🔴 Red |

### Status examples

```
UUID            Status      Nodes
abc-123-def     Running     3/3    # All healthy
def-456-ghi     Degraded    4/5    # One node down
ghi-789-jkl     Starting    2/4    # Still launching
```

## Node Information

For each node, the detailed view shows:

### Basic info
- **ID**: Node identifier
- **Status**: Current state
- **Uptime**: How long running

### Resource usage
- **CPU%**: CPU utilization
- **MEM**: Memory usage
- **Disk I/O**: Read/write activity
- **Network**: Network traffic

### Health indicators
- ✓ Running normally
- ⚠ High resource usage
- ✗ Crashed or failed
- ⏸ Paused or idle

## Filtering and Sorting

### Filter by status
```bash
dora list | grep Running
dora list | grep Degraded
```

### Sort by uptime
```bash
dora list | sort -k4
```

### Sort by memory usage
```bash
dora list | sort -k7 -h
```

### Filter by name pattern
```bash
dora list | grep robot
```

## Watch Mode Features

Watch mode provides real-time monitoring:

### Update frequency
```bash
# Update every 1 second
dora list --watch --interval 1

# Update every 5 seconds (default: 2)
dora list --watch --interval 5
```

### Highlight changes
Changes flash briefly:
- New dataflows: Green highlight
- Status changes: Yellow highlight
- Stopped dataflows: Red highlight

### Keyboard shortcuts
- `q` - Quit watch mode
- `r` - Force refresh
- `s` - Sort by column
- `f` - Filter by pattern

## Detailed Node View

Get more info about specific node:

```bash
# List with node details
dora list abc-123-def --nodes
```

Output:
```
Node: camera
Path: opencv-video-capture
Status: Running
Uptime: 01:30:45

Inputs:
  tick: dora/timer/millis/33

Outputs:
  image: 640x480x3 (30 fps)

Environment:
  CAPTURE_PATH: 0
  IMAGE_WIDTH: 640
  IMAGE_HEIGHT: 480

Resources:
  CPU: 5.2% (avg: 4.8%)
  Memory: 128M (peak: 145M)
  FPS: 30.2

Recent logs (last 10 lines):
  [INFO] Frame captured: 54123
  [INFO] Frame captured: 54124
  [INFO] Frame captured: 54125
```

## Empty State

When no dataflows are running:

```bash
$ dora list

No dataflows running

To start a dataflow:
  dora start dataflow.yml

To view stopped dataflows:
  dora list --all
```

## Historical Data

### List all (including stopped)
```bash
dora list --all
```

Output:
```
UUID            Status     Uptime    Stopped
abc-123-def     Stopped    -         2m ago
def-456-ghi     Running    01:30:45  -
ghi-789-jkl     Failed     00:05:00  5m ago
```

### List only stopped
```bash
dora list --status stopped
```

### Clear history
```bash
dora list --clear-history
```

## Export Options

### Save to file
```bash
# Table format
dora list > dataflows.txt

# JSON format
dora list --format json > dataflows.json

# YAML format
dora list --format yaml > dataflows.yaml
```

### Export for analysis
```bash
# CSV format for spreadsheet
dora list --format csv > dataflows.csv
```

CSV output:
```csv
uuid,name,status,uptime,cpu_percent,memory_mb
abc-123-def,robot,running,5445,12.5,256
def-456-ghi,vision,running,2720,8.2,512
```

## Integration Examples

### Shell script
```bash
#!/bin/bash
# check-health.sh

# Get dataflow count
COUNT=$(dora list | grep Running | wc -l)

if [ $COUNT -eq 0 ]; then
  echo "⚠ No dataflows running!"
  exit 1
fi

echo "✓ $COUNT dataflows healthy"
```

### Python monitoring
```python
import subprocess
import json

def get_dataflows():
    """Get list of running dataflows"""
    result = subprocess.run(
        ['dora', 'list', '--format', 'json'],
        capture_output=True,
        text=True
    )
    return json.loads(result.stdout)

def check_health():
    """Check if all dataflows are healthy"""
    data = get_dataflows()

    for df in data['dataflows']:
        if df['status'] != 'running':
            print(f"⚠ {df['name']}: {df['status']}")
            return False

        # Check resource usage
        if df['total_cpu'] > 80:
            print(f"⚠ {df['name']}: High CPU ({df['total_cpu']}%)")

        if df['total_memory_mb'] > 8000:
            print(f"⚠ {df['name']}: High memory ({df['total_memory_mb']}M)")

    return True

if __name__ == "__main__":
    healthy = check_health()
    exit(0 if healthy else 1)
```

### Prometheus metrics
```python
from prometheus_client import Gauge, start_http_server
import subprocess
import json
import time

# Define metrics
cpu_gauge = Gauge('dora_cpu_percent', 'CPU usage', ['dataflow', 'node'])
mem_gauge = Gauge('dora_memory_mb', 'Memory usage', ['dataflow', 'node'])

def collect_metrics():
    """Collect metrics from dora list"""
    result = subprocess.run(
        ['dora', 'list', '--format', 'json'],
        capture_output=True,
        text=True
    )
    data = json.loads(result.stdout)

    for df in data['dataflows']:
        for node in df['nodes']:
            cpu_gauge.labels(
                dataflow=df['name'],
                node=node['id']
            ).set(node['cpu_percent'])

            mem_gauge.labels(
                dataflow=df['name'],
                node=node['id']
            ).set(node['memory_mb'])

if __name__ == "__main__":
    start_http_server(8000)
    while True:
        collect_metrics()
        time.sleep(5)
```

### Grafana dashboard query
```sql
-- Query metrics from Prometheus
SELECT
  avg(dora_cpu_percent{dataflow="robot"})
FROM
  metrics
WHERE
  time > now() - 1h
```

## Alerts and Notifications

### High CPU alert
```bash
#!/bin/bash
# alert-cpu.sh

THRESHOLD=80

dora list --format json | jq -r '.dataflows[] |
  select(.total_cpu > '$THRESHOLD') |
  "⚠ \(.name): High CPU \(.total_cpu)%"'
```

### Slack notification
```bash
#!/bin/bash
# notify-slack.sh

WEBHOOK_URL="https://hooks.slack.com/services/YOUR/WEBHOOK"

STATUS=$(dora list --format json)
DEGRADED=$(echo $STATUS | jq '[.dataflows[] | select(.status=="degraded")] | length')

if [ $DEGRADED -gt 0 ]; then
  curl -X POST $WEBHOOK_URL \
    -H 'Content-Type: application/json' \
    -d "{\"text\": \"⚠ $DEGRADED dataflows degraded\"}"
fi
```

### Email alert
```bash
#!/bin/bash
# alert-email.sh

FAILED=$(dora list | grep Failed | wc -l)

if [ $FAILED -gt 0 ]; then
  echo "Dataflows failed: $FAILED" | \
    mail -s "Dora Alert" admin@example.com
fi
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty list but dataflows running | Daemon issue, restart with `dora destroy && dora up` |
| Wrong status shown | Stale data, force refresh |
| High memory usage | Check for memory leaks in nodes |
| Node count mismatch | Some nodes failed to start, check logs |
| Cannot connect | Daemon not running, start with `dora up` |

## Best Practices

1. **Regular monitoring**
   ```bash
   # Check status periodically
   watch -n 5 dora list
   ```

2. **Use watch mode for debugging**
   ```bash
   # Real-time monitoring
   dora list --watch
   ```

3. **Export for analysis**
   ```bash
   # Daily snapshots
   dora list --format json > logs/status-$(date +%Y%m%d).json
   ```

4. **Set up alerts**
   ```bash
   # Cron job for monitoring
   */5 * * * * /path/to/check-health.sh
   ```

5. **Name your dataflows**
   ```bash
   # Easier identification
   dora start dataflow.yml --name my-app
   ```

6. **Check before stopping**
   ```bash
   # Verify UUID before stop
   dora list
   dora stop abc-123-def
   ```

## Advanced Queries

### jq examples
```bash
# List all running dataflows
dora list --format json | jq '.dataflows[] | select(.status=="running") | .name'

# Sum total memory usage
dora list --format json | jq '[.dataflows[].total_memory_mb] | add'

# Find high CPU dataflows
dora list --format json | jq '.dataflows[] | select(.total_cpu > 50)'

# Count nodes per dataflow
dora list --format json | jq '.dataflows[] | {name: .name, nodes: .nodes | length}'
```

### awk examples
```bash
# Sum memory usage
dora list | awk '{sum+=$7} END {print sum}'

# Average CPU usage
dora list | awk '{sum+=$6; count++} END {print sum/count}'

# List high memory dataflows
dora list | awk '$7 > 500 {print $2}'
```

## Related Commands

- `/start` - Start new dataflow
- `/stop` - Stop running dataflow
- `/build` - Build before starting
- `/visualize` - Visualize dataflow structure

## Environment Variables

```bash
# Default format
export DORA_LIST_FORMAT=table

# Watch interval
export DORA_WATCH_INTERVAL=2

# Show all by default
export DORA_LIST_ALL=true

# Date format
export DORA_DATE_FORMAT="%Y-%m-%d %H:%M:%S"
```

## See Also

- [Dora Monitoring Guide](https://dora-rs.ai/docs/monitoring)
- [Metrics and Observability](https://dora-rs.ai/docs/metrics)
- [Dashboard Setup](https://dora-rs.ai/docs/dashboard)
