# Integrating nodes.json with add-node Command

This document explains how to use the generated `nodes.json` file to enhance the `/add-node` command.

## Overview

The `generate_nodes_json.py` script creates a comprehensive metadata file for all nodes in the dora-hub. This can be used to:

1. Dynamically discover available nodes
2. Provide rich metadata (descriptions, installation, tags)
3. Enable tag-based filtering
4. Keep node list automatically updated

## Generating nodes.json

First, generate the nodes.json file:

```bash
# Using GitHub API (no clone needed)
python scripts/generate_nodes_json.py --github --output data/nodes.json

# Or using local clone
git clone https://github.com/dora-rs/dora-hub.git /tmp/dora-hub
python scripts/generate_nodes_json.py --local /tmp/dora-hub/node-hub --output data/nodes.json
```

## Using nodes.json with /add-node

### Automatic Node Discovery

Instead of maintaining a hardcoded list of nodes in `commands/add-node/COMMAND.md`, Claude Code can:

1. Read `data/nodes.json` when executing `/add-node`
2. Present all available nodes to the user
3. Use metadata to provide better descriptions

### Enhanced Command Flow

```
User: /add-node
  ↓
Claude reads data/nodes.json
  ↓
Claude presents available nodes with categories:
  - Sensors: camera, microphone, realsense, ...
  - Vision: yolo, sam2, cotracker, ...
  - Audio: vad, whisper, kokoro-tts, ...
  ↓
User selects a node
  ↓
Claude generates YAML using metadata:
  - title: node name
  - install: installation command
  - description: what the node does
  - tags: helps suggest compatible connections
```

### Tag-Based Filtering

When user wants to add a node, Claude can:

```python
# Filter by tag
vision_nodes = [n for n in nodes if "image" in n["tags"]]
audio_nodes = [n for n in nodes if "audio" in n["tags"]]
python_nodes = [n for n in nodes if "python" in n["tags"]]
```

### Smart Connection Suggestions

Using tags, Claude can suggest compatible connections:

```python
# User adds a YOLO node (tags: ["python", "image"])
# Claude suggests connecting to nodes with "image" output
camera_nodes = [n for n in existing_nodes
                if "image" in n.get("tags", [])]
```

## Example Enhanced Workflow

### Before (Manual)

```markdown
## Available Node Types

### Vision
- `yolo` - Object detection
- `sam2` - Segmentation
...
```

### After (Dynamic with nodes.json)

```python
# Claude Code can execute:
import json

# Load all available nodes
with open("data/nodes.json") as f:
    nodes = json.load(f)

# Present to user with rich information
for node in nodes:
    print(f"- {node['title']}")
    print(f"  {node['description']}")
    print(f"  Install: {node['install']}")
    print(f"  Tags: {', '.join(node['tags'])}")
```

## Implementation Strategy

### Option 1: Reference in COMMAND.md

Update `commands/add-node/COMMAND.md` to include:

```markdown
## Available Node Types

**Note**: For the complete and up-to-date list of nodes, Claude should:
1. Check if `data/nodes.json` exists
2. If yes, load and use that list
3. If no, fall back to the manual list below

To generate/update nodes.json:
\`\`\`bash
python scripts/generate_nodes_json.py --github --output data/nodes.json
\`\`\`
```

### Option 2: Automated Updates

Add a GitHub Action to automatically update nodes.json:

```yaml
# .github/workflows/update-nodes.yml
name: Update nodes.json

on:
  schedule:
    - cron: '0 0 * * 0'  # Weekly
  workflow_dispatch:

jobs:
  update:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
      - run: |
          python scripts/generate_nodes_json.py --github --output data/nodes.json
      - uses: stefanzweifel/git-auto-commit-action@v4
        with:
          commit_message: "Update nodes.json"
```

### Option 3: On-Demand Generation

Claude Code can generate nodes.json on-demand when `/add-node` is called:

```markdown
## Workflow

1. Check if `data/nodes.json` exists and is recent (< 7 days old)
2. If not, run: `python scripts/generate_nodes_json.py --github --output data/nodes.json`
3. Load nodes from JSON
4. Present available nodes to user
5. Generate node configuration
6. Add to dataflow.yml
```

## Benefits

1. **Always Up-to-Date**: Nodes are discovered from dora-hub directly
2. **Rich Metadata**: Installation instructions, descriptions, tags
3. **Better UX**: Users can search/filter nodes by category or tags
4. **Maintainability**: No need to manually update node lists
5. **Extensibility**: Easy to add new metadata fields

## Migration Path

1. Generate initial `data/nodes.json`
2. Update `commands/add-node/COMMAND.md` to reference it
3. Test with Claude Code
4. (Optional) Set up automated updates
5. Deprecate manual node list

## Example Usage

```bash
# User workflow
$ /add-node

Claude: "I found 50+ nodes in data/nodes.json. What type of node do you want to add?"
- Vision nodes (10): yolo, sam2, cotracker, ...
- Audio nodes (8): whisper, vad, kokoro-tts, ...
- Sensor nodes (6): camera, realsense, microphone, ...

User: "I want to add object detection"

Claude: "I found these vision nodes:"
1. yolo - YOLOv8 object detection (pip install dora-yolo) [python, image]
2. sam2 - SAM2 segmentation (pip install dora-sam2) [python, image]

User: "Add yolo"

Claude: *reads metadata and generates YAML*
```

## Conclusion

Integrating `nodes.json` makes the `/add-node` command more powerful, maintainable, and user-friendly. It leverages the dynamic nature of Claude Code to provide an always up-to-date catalog of available nodes.
