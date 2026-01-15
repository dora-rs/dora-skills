# Scripts

Utility scripts for managing dora-skills.

## generate_nodes_json.py

Generate a `nodes.json` file with metadata for all nodes in the [dora-hub](https://github.com/dora-rs/dora-hub) repository.

### Usage

#### Using GitHub API (no clone needed)

```bash
python scripts/generate_nodes_json.py --github --output nodes.json
```

With authentication (higher rate limits):

```bash
export GITHUB_TOKEN="your_token_here"
python scripts/generate_nodes_json.py --github --output nodes.json
```

#### Using Local Clone

```bash
# Clone dora-hub first
git clone https://github.com/dora-rs/dora-hub.git /tmp/dora-hub

# Generate nodes.json
python scripts/generate_nodes_json.py --local /tmp/dora-hub/node-hub --output nodes.json
```

### Output Format

The script generates a JSON file with the following structure:

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

### Metadata Sources

The script extracts metadata from:

1. **README.md**: Title, description, installation instructions
2. **Cargo.toml**: Rust package metadata (name, description, license, authors)
3. **package.json**: Node.js package metadata
4. **pyproject.toml**: Python package metadata

### Tag Inference

Tags are automatically inferred based on:

- **Language**: `python`, `rust` (from content analysis)
- **Media Type**: `image`, `video`, `audio`, `depth` (from keywords)
- **Function**: `control` (from robotics-related keywords)

### API Rate Limits

- GitHub API without authentication: 60 requests/hour
- With authentication: 5000 requests/hour

For repositories with many nodes, authentication is recommended:

```bash
export GITHUB_TOKEN="ghp_your_token_here"
```

### Integration with add-node

The generated `nodes.json` can be used to enhance the `/add-node` command by providing:

- Complete list of available nodes
- Rich metadata for each node
- Installation instructions
- Automatic tag-based filtering

See [commands/add-node/COMMAND.md](../commands/add-node/COMMAND.md) for more information.
