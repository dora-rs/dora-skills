# Data Directory

This directory contains generated data files and shared reference documentation used by dora-skills.

## Reference Files

Shared documentation to reduce redundancy across skill files:

### COMMON_NODES.md

Standard node configurations used across multiple skills. Reference this file instead of duplicating node examples.

**Contents:**
- Camera, YOLO, Rerun visualization
- Microphone, VAD, Whisper, Piper TTS
- SAM2 segmentation, CoTracker tracking
- Piper robot arm nodes
- Timer patterns and queue management

**Usage in SKILL.md files:**
```markdown
See [COMMON_NODES.md](../../data/COMMON_NODES.md#camera-node)
```

### CODE_TEMPLATES.md

Reusable code patterns for custom node development. Reference these templates to avoid code duplication.

**Contents:**
- Python/Rust node boilerplate
- Image and audio handling functions
- Detection processing patterns
- Multiple input handling
- Error handling and state management

**Usage in SKILL.md files:**
```markdown
See [CODE_TEMPLATES.md](../../data/CODE_TEMPLATES.md#python-node-boilerplate)
```

### CONFIG_REFERENCE.md

Common configuration options and patterns. Reference this for standard settings.

**Contents:**
- Device configuration (GPU/CPU selection)
- Queue management patterns
- Model configurations (YOLO, SAM2, Whisper)
- Language and audio settings
- Performance optimization patterns

**Usage in SKILL.md files:**
```markdown
See [CONFIG_REFERENCE.md](../../data/CONFIG_REFERENCE.md#device-configuration)
```

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

The `nodes.json` file is an array of node objects. Each node has the following schema:

```json
[
  {
    "title": "node-name",
    "description": "Node description extracted from README",
    "preview": null,
    "author": "Author Name",
    "github": "https://github.com/dora-rs/dora-hub",
    "downloads": null,
    "last_commit": "2024-01-15T10:00:00Z",
    "last_release": null,
    "license": "Apache-2.0",
    "install": "pip install dora-node-name",
    "category": null,
    "website": "node-name",
    "source": "https://github.com/dora-rs/dora-hub/tree/main/node-hub/node-name",
    "tags": ["python", "image", "video"]
  }
]
```

#### Field Descriptions

| Field | Type | Description |
|-------|------|-------------|
| `title` | string | Node name/identifier |
| `description` | string | Brief description of node functionality |
| `preview` | string\|null | Preview image URL (currently unused) |
| `author` | string\|null | Node author name |
| `github` | string | Repository URL |
| `downloads` | number\|null | Download count (currently unused) |
| `last_commit` | string\|null | ISO 8601 timestamp of last commit |
| `last_release` | string\|null | Last release version (currently unused) |
| `license` | string\|null | SPDX license identifier |
| `install` | string\|null | Installation command (e.g., `pip install ...`) |
| `category` | string\|null | Node category (currently unused) |
| `website` | string | Node identifier/website |
| `source` | string | Direct link to node source code |
| `tags` | string[] | Array of tags for filtering (e.g., `python`, `image`, `audio`) |

### Searching with jq

[jq](https://jqlang.github.io/jq/) is a powerful command-line JSON processor that makes it easy to query and filter the nodes.json file.

#### Installation

```bash
# macOS
brew install jq

# Ubuntu/Debian
sudo apt-get install jq

# Fedora
sudo dnf install jq
```

#### Basic Queries

**List all node titles:**
```bash
jq '.[].title' data/nodes.json
```

**Count total nodes:**
```bash
jq 'length' data/nodes.json
```

**Get a specific node by title:**
```bash
jq '.[] | select(.title == "dora-yolo")' data/nodes.json
```

#### Filtering by Tags

**Find all Python nodes:**
```bash
jq '.[] | select(.tags | contains(["python"]))' data/nodes.json
```

**Find all image processing nodes:**
```bash
jq '.[] | select(.tags | contains(["image"]))' data/nodes.json
```

**Find nodes with multiple tags (Python AND audio):**
```bash
jq '.[] | select(.tags | contains(["python", "audio"]))' data/nodes.json
```

**Find nodes with any of several tags (vision OR audio):**
```bash
jq '.[] | select(.tags | any(. == "image" or . == "audio"))' data/nodes.json
```

#### Filtering by Other Fields

**Find nodes with installation commands:**
```bash
jq '.[] | select(.install != null)' data/nodes.json
```

**Find nodes by author:**
```bash
jq '.[] | select(.author == "Dora Team")' data/nodes.json
```

**Find nodes with specific license:**
```bash
jq '.[] | select(.license == "Apache-2.0")' data/nodes.json
```

**Find recently updated nodes (within last 30 days):**
```bash
jq --arg date "$(date -u -d '30 days ago' +%Y-%m-%d)" \
  '.[] | select(.last_commit != null and .last_commit > $date)' \
  data/nodes.json
```

#### Output Formatting

**Show only titles and descriptions:**
```bash
jq '.[] | {title, description}' data/nodes.json
```

**Create a compact list with titles and tags:**
```bash
jq '.[] | "\(.title): \(.tags | join(", "))"' data/nodes.json
```

**Get installation commands for all Python nodes:**
```bash
jq -r '.[] | select(.tags | contains(["python"])) | .install' data/nodes.json
```

**Generate a markdown list of nodes:**
```bash
jq -r '.[] | "- **\(.title)**: \(.description)"' data/nodes.json
```

#### Advanced Queries

**Group nodes by primary tag:**
```bash
jq 'group_by(.tags[0]) | map({tag: .[0].tags[0], nodes: map(.title)})' data/nodes.json
```

**Get all unique tags:**
```bash
jq '[.[].tags[]] | unique' data/nodes.json
```

**Count nodes by tag:**
```bash
jq '[.[].tags[]] | group_by(.) | map({tag: .[0], count: length})' data/nodes.json
```

**Find nodes matching a description keyword:**
```bash
jq '.[] | select(.description | test("detection"; "i"))' data/nodes.json
```

#### Practical Examples

**Create a quick reference list for a specific category:**
```bash
# All audio nodes with install commands
jq -r '.[] | select(.tags | contains(["audio"])) |
  "## \(.title)\n\(.description)\n```bash\n\(.install)\n```\n"' \
  data/nodes.json
```

**Export Python nodes to a new JSON file:**
```bash
jq '[.[] | select(.tags | contains(["python"]))]' \
  data/nodes.json > python_nodes.json
```

**Find nodes without installation instructions:**
```bash
jq '.[] | select(.install == null) | .title' data/nodes.json
```

**Search for nodes by partial name match:**
```bash
jq '.[] | select(.title | contains("yolo"))' data/nodes.json
```
