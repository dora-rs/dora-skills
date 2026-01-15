# Data Directory

This directory contains generated data files used by dora-skills commands.

## nodes.json

A comprehensive catalog of all nodes available in the [dora-hub](https://github.com/dora-rs/dora-hub) node-hub.

### Generating nodes.json

```bash
# Using GitHub API (recommended)
python scripts/generate_nodes_json.py --github --output data/nodes.json

# Using local clone
git clone https://github.com/dora-rs/dora-hub.git /tmp/dora-hub
python scripts/generate_nodes_json.py --local /tmp/dora-hub/node-hub --output data/nodes.json
```

### Usage

The `/add-node` command can automatically use this file if it exists to provide:
- Complete list of available nodes
- Rich metadata (descriptions, install commands, tags)
- Smart filtering by category or tags

See:
- [scripts/README.md](../scripts/README.md) for generation details
- [docs/integrating-nodes-json.md](../docs/integrating-nodes-json.md) for integration guide

### Keeping Up-to-Date

To keep the node catalog current:

```bash
# Manual update
python scripts/generate_nodes_json.py --github --output data/nodes.json

# Or set up a cron job / GitHub Action to run weekly
```

### File Structure

```json
[
  {
    "title": "node-name",
    "description": "What the node does",
    "author": "Author name",
    "license": "Apache-2.0",
    "install": "pip install dora-node",
    "source": "https://github.com/dora-rs/dora-hub/tree/main/node-hub/node-name",
    "tags": ["python", "image", "video"]
  }
]
```
