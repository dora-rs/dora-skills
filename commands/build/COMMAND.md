---
name: build
description: Build and install dependencies for dora dataflow nodes
---

# /build Command

Build and install dependencies for nodes in a dora dataflow before running them.

## Usage

```
/build [<dataflow-file>] [--uv]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<dataflow-file>` | Path to dataflow YAML | ./dataflow.yml |
| `--uv` | Use uv package manager (faster) | false |

## What It Does

The build command:
1. Parses the dataflow YAML file
2. Executes the `build` command for each node
3. Installs Python packages (pip/uv) or compiles Rust code
4. Prepares the environment for dataflow execution

## Examples

### Basic build

```
/build
```

Builds all nodes in `./dataflow.yml`:
```bash
$ dora build dataflow.yml
Building camera...
  ✓ pip install opencv-video-capture
Building detector...
  ✓ pip install dora-yolo
Building visualize...
  ✓ pip install dora-rerun
Build completed successfully!
```

### Build with uv (faster)

```
/build --uv
```

Uses the uv package manager instead of pip:
```bash
$ dora build dataflow.yml --uv
Building camera...
  ✓ uv pip install opencv-video-capture
Building detector...
  ✓ uv pip install dora-yolo
Building visualize...
  ✓ uv pip install dora-rerun
Build completed in 2.3s (4x faster than pip)
```

### Build specific dataflow

```
/build my-robot/dataflow.yml
```

Builds nodes from a specific dataflow file.

## Node Build Configuration

In dataflow.yml, each node specifies its build command:

```yaml
nodes:
  # Python node with pip
  - id: camera
    build: pip install opencv-video-capture
    path: opencv-video-capture

  # Python node with requirements file
  - id: processor
    build: pip install -r requirements.txt
    path: ./processor

  # Rust node with cargo
  - id: controller
    build: cargo build --release
    path: ./controller

  # Custom build script
  - id: custom
    build: ./scripts/build.sh
    path: ./custom-node
```

## When to Run Build

### First Time Setup
Always run build before first execution:
```bash
/build
/run
```

### After Adding/Updating Nodes
Rebuild after modifying dataflow.yml:
```bash
# Edit dataflow.yml to add new nodes
/build
```

### Dependency Updates
When package versions change:
```bash
/build --uv  # Refresh all dependencies
```

## Package Managers

### pip (default)
Standard Python package installer:
- Widely compatible
- Stable and reliable
- Slower installation

### uv (recommended)
Fast Rust-based package installer:
- 10-100x faster than pip
- Compatible with pip packages
- Better dependency resolution

Install uv:
```bash
pip install uv
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Build Output

### Success
```
Building dataflow nodes...
  camera: ✓ opencv-video-capture installed
  detector: ✓ dora-yolo installed
  visualize: ✓ dora-rerun installed

Build completed successfully!
Time: 12.5s
```

### Partial Failure
```
Building dataflow nodes...
  camera: ✓ opencv-video-capture installed
  detector: ✗ Failed to install dora-yolo
    Error: Package not found
  visualize: ⊘ Skipped

Build failed. Fix errors and retry.
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Package not found | Check package name and version |
| Permission denied | Run with sudo or use virtual env |
| Build timeout | Increase timeout or check network |
| Dependency conflict | Use `--uv` for better resolution |
| Rust compilation fails | Install Rust toolchain: `rustup` |

## Integration with Workflow

### Development Workflow
```bash
# 1. Create project
dora new my-robot --lang python

# 2. Edit dataflow.yml
nano dataflow.yml

# 3. Build
/build --uv

# 4. Run
/run
```

### CI/CD Pipeline
```yaml
# .github/workflows/test.yml
- name: Build dataflow
  run: dora build dataflow.yml --uv

- name: Run tests
  run: dora run dataflow.yml
```

## Advanced Usage

### Parallel Builds
Build multiple dataflows in parallel:
```bash
/build robot/dataflow.yml &
/build vision/dataflow.yml &
wait
```

### Conditional Builds
Build only if dependencies changed:
```bash
# Check if build needed
if [ dataflow.yml -nt .build-timestamp ]; then
  /build
  touch .build-timestamp
fi
```

### Custom Build Scripts
For complex builds, create custom script:
```yaml
# dataflow.yml
nodes:
  - id: custom
    build: |
      pip install -r requirements.txt
      python setup.py build_ext --inplace
      chmod +x start.sh
    path: ./custom
```

## Best Practices

1. **Use Virtual Environments**
   ```bash
   python -m venv venv
   source venv/bin/activate
   /build --uv
   ```

2. **Pin Dependencies**
   ```yaml
   build: pip install opencv-video-capture==0.2.1
   ```

3. **Cache Builds**
   ```bash
   # Cache pip packages
   export PIP_CACHE_DIR=~/.cache/pip
   /build
   ```

4. **Use uv for Speed**
   ```bash
   /build --uv  # Much faster than pip
   ```

## Related Commands

- `/run` - Run dataflow after building
- `/start` - Start dataflow in daemon mode
- `/new-dataflow` - Create new dataflow project
- `/add-node` - Add nodes to dataflow

## Environment Variables

```bash
# Use uv by default
export DORA_USE_UV=1

# Custom pip index
export PIP_INDEX_URL=https://pypi.org/simple

# Build timeout
export DORA_BUILD_TIMEOUT=600

# Parallel builds
export DORA_BUILD_JOBS=4
```

## See Also

- [Dora CLI Documentation](https://dora-rs.ai/docs/cli)
- [Python Packaging Guide](https://packaging.python.org/)
- [uv Documentation](https://github.com/astral-sh/uv)
