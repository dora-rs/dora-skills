---
name: install
description: Install dora-cli using the best method for your system
---

# /install Command

Install dora-cli by automatically detecting available tools on your system and choosing the optimal installation method.

## Usage

```
/install [--method <method>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--method` | Force specific installation method: `cargo`, `pip`, `uv`, `github`, `source` | auto-detect |

## What It Does

The install command:
1. **Detects available tools** on your system (cargo, pip, uv, curl, etc.)
2. **Chooses the best installation method** based on what's available
3. **Installs dora-cli** using the selected method
4. **Verifies installation** with `dora --version`

## Auto-Detection Logic

The command intelligently selects the installation method based on your environment:

### Priority Order

1. **cargo** (Rust projects)
   - ✅ No Python required
   - ✅ Best for Rust-only workflows
   - ✅ Compiles from source
   - ⚠️ Requires Rust toolchain

2. **uv** (Python projects - fastest)
   - ✅ 10-100x faster than pip
   - ✅ Modern Python package manager
   - ⚠️ Requires Python and virtual environment

3. **pip** (Python projects - most compatible)
   - ✅ Most widely available
   - ✅ Works with any Python installation
   - ⚠️ Requires Python and virtual environment

4. **github** (Standalone installer)
   - ✅ No Python or Rust required
   - ✅ Pre-built binaries
   - ✅ Works on any system

5. **source** (Development/custom builds)
   - ✅ Latest features
   - ⚠️ Requires Rust toolchain
   - ⚠️ Longer installation time

### Detection Rules

```
IF cargo is installed:
  → Use cargo (ideal for Rust projects)

ELSE IF Python venv is active AND uv is installed:
  → Use uv (fastest for Python projects)

ELSE IF Python venv is active AND pip is available:
  → Use pip (compatible for Python projects)

ELSE IF curl/powershell is available:
  → Use github installer (no dependencies)

ELSE:
  → Prompt user to install cargo or Python
```

## Examples

### Auto-detect (Recommended)

```
/install
```

**For Rust-only projects:**
```bash
# System has cargo installed
$ /install
Detecting available tools...
  ✓ Found: cargo 1.75.0

Installing dora-cli via cargo...
$ cargo install dora-cli
    Updating crates.io index
   Compiling dora-cli v0.3.5
    Finished release [optimized] target(s) in 2m 15s
  Installing ~/.cargo/bin/dora
   Installed package `dora-cli v0.3.5`

Verifying installation...
$ dora --version
dora 0.3.5

✓ Installation complete!
```

**For Python projects:**
```bash
# User has venv active and uv installed
$ source .venv/bin/activate
$ /install
Detecting available tools...
  ✓ Found: Python venv active
  ✓ Found: uv 0.4.0

Installing dora-cli via uv (fastest)...
$ uv pip install dora-rs-cli
Resolved 12 packages in 234ms
   Installed dora-rs-cli v0.3.5

Verifying installation...
$ dora --version
dora 0.3.5

✓ Installation complete!
```

**For systems without cargo or Python:**
```bash
$ /install
Detecting available tools...
  ✗ cargo not found
  ✗ Python venv not active
  ✓ Found: curl

Installing dora-cli via GitHub installer...
$ curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh
Downloading dora-cli...
  ✓ dora-cli installed to ~/.cargo/bin/dora

Verifying installation...
$ dora --version
dora 0.3.5

✓ Installation complete!
```

### Force Specific Method

#### Rust Projects (No Python)

```
/install --method cargo
```

Install dora-cli using cargo:
```bash
$ cargo install dora-cli
    Updating crates.io index
   Compiling dora-cli v0.3.5
    Finished release [optimized] target(s) in 2m 15s
  Installing ~/.cargo/bin/dora

$ dora --version
dora 0.3.5
```

**When to use:**
- Pure Rust projects
- No Python dependency desired
- Want to compile from source
- Have Rust toolchain installed

#### Python Projects (uv - Fastest)

```
/install --method uv
```

Install using uv (requires active venv):
```bash
# Activate venv first
$ python -m venv .venv
$ source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Then install
$ /install --method uv
$ uv pip install dora-rs-cli
Resolved 12 packages in 234ms
   Installed dora-rs-cli v0.3.5

$ dora --version
dora 0.3.5
```

**When to use:**
- Python-based workflows
- Want fastest installation
- Already using uv

#### Python Projects (pip - Compatible)

```
/install --method pip
```

Install using pip (requires active venv):
```bash
# Activate venv first
$ python -m venv .venv
$ source .venv/bin/activate  # Linux/macOS
# or: .venv\Scripts\activate  # Windows

# Then install
$ /install --method pip
$ pip install dora-rs-cli
Collecting dora-rs-cli
...
Successfully installed dora-rs-cli-0.3.5

$ dora --version
dora 0.3.5
```

**When to use:**
- Python-based workflows
- Don't have uv installed
- Maximum compatibility

#### Standalone (No Dependencies)

```
/install --method github
```

Install using GitHub installer (no Python or Rust needed):

**macOS/Linux:**
```bash
$ curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh
```

**Windows:**
```powershell
PS> powershell -ExecutionPolicy ByPass -c "irm https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.ps1 | iex"
```

**When to use:**
- Don't want Python or Rust dependencies
- Want pre-built binaries
- Quick installation on any system

#### Development (From Source)

```
/install --method source
```

Install from source (requires Rust):
```bash
$ git clone https://github.com/dora-rs/dora.git
$ cd dora
$ cargo build --release -p dora-cli
$ export PATH=$PATH:$(pwd)/target/release
# or: $env:PATH += ";$(pwd)\target\release"  # Windows

$ dora --version
dora 0.3.5-dev
```

**When to use:**
- Contributing to dora development
- Need latest unreleased features
- Custom modifications

## Installation Methods Comparison

| Method | Speed | Requirements | Use Case |
|--------|-------|--------------|----------|
| **cargo** | ⚡⚡ (2-3 min) | Rust toolchain | Rust-only projects |
| **uv** | ⚡⚡⚡ (5-10 sec) | Python + venv + uv | Python projects (fastest) |
| **pip** | ⚡⚡ (30-60 sec) | Python + venv | Python projects (compatible) |
| **github** | ⚡⚡⚡ (10-20 sec) | curl/PowerShell | No dependencies |
| **source** | ⚡ (5-10 min) | Rust toolchain + git | Development |

## Workflow Examples

### Rust-Only Project

Perfect for pure Rust robotics projects with no Python dependency:

```bash
# No Python needed!
/install --method cargo

# Use dora with Rust nodes
dora new my-robot --lang rust
cd my-robot
dora build dataflow.yml
dora run dataflow.yml
```

### Python Project

For Python-based AI/ML workflows:

```bash
# Set up Python environment
python -m venv .venv
source .venv/bin/activate

# Install dora-cli (auto-detects uv or pip)
/install

# Use dora with Python nodes
dora new my-robot --lang python
cd my-robot
dora build dataflow.yml --uv
dora run dataflow.yml
```

### Hybrid Project (Rust + Python)

Best of both worlds:

```bash
# Install via cargo (no Python dependency)
/install --method cargo

# Create hybrid dataflow
dora new my-robot --lang rust
cd my-robot

# Add Python nodes with isolated venvs per node
# Each node's build command handles its own dependencies
dora build dataflow.yml --uv
dora run dataflow.yml
```

## Platform Support

| Platform | cargo | uv | pip | github | source |
|----------|-------|----|----|--------|--------|
| **macOS** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Linux** | ✅ | ✅ | ✅ | ✅ | ✅ |
| **Windows** | ✅ | ✅ | ✅ | ✅ | ✅ |

## Virtual Environments (Python Methods Only)

### Why Virtual Environments?

Virtual environments isolate Python dependencies and prevent conflicts between projects. **Only required when using pip or uv methods.**

### When You Need a Virtual Environment

- ✅ Using `--method pip`
- ✅ Using `--method uv`
- ❌ Using `--method cargo` (no Python needed)
- ❌ Using `--method github` (no Python needed)
- ❌ Using `--method source` (no Python needed)

### Setting Up a Virtual Environment

**Linux/macOS:**
```bash
python -m venv .venv
source .venv/bin/activate
```

**Windows:**
```powershell
python -m venv .venv
.venv\Scripts\activate
```

**Verify active:**
```bash
# You should see (.venv) in your prompt
(.venv) $ which python
/path/to/project/.venv/bin/python
```

### Best Practices

1. **Rust-only projects**: Use cargo method, no venv needed
2. **Python projects**: Activate venv before using pip/uv methods
3. **Mixed projects**: Use cargo for dora-cli, venvs for node dependencies
4. **CI/CD**: Use github method or cargo for reproducible builds

## Troubleshooting

### Cargo Not Found

**Problem:** `cargo: command not found`

**Solution:** Install Rust toolchain:
```bash
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
source $HOME/.cargo/env
```

### Python/Venv Issues

**Problem:** `No active virtual environment`

**Solution:** Choose non-Python method or activate venv:
```bash
# Option 1: Use cargo (no Python needed)
/install --method cargo

# Option 2: Activate venv first
python -m venv .venv
source .venv/bin/activate
/install --method pip
```

### uv Not Found

**Problem:** `uv: command not found`

**Solution:** Install uv or use pip instead:
```bash
# Option 1: Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Option 2: Use pip
/install --method pip
```

### GitHub Installer Fails

**Problem:** Download fails or script errors

**Solution:** Use alternative method:
```bash
# Use cargo instead
/install --method cargo

# Or pip if you have Python
/install --method pip
```

### Permission Denied

**Problem:** `Permission denied` when installing

**Solution:** Check installation directory permissions:
```bash
# For cargo: check ~/.cargo/bin
ls -la ~/.cargo/bin

# For pip/uv: ensure venv is active
source .venv/bin/activate

# For github: may need sudo on Linux
sudo curl ... | sh
```

### Version Conflicts

**Problem:** Old version of dora-cli installed

**Solution:** Uninstall and reinstall:
```bash
# Cargo method
cargo uninstall dora-cli
cargo install dora-cli

# Pip/uv method
pip uninstall dora-rs-cli
pip install dora-rs-cli

# Check version
dora --version
```

## Updating dora-cli

### Cargo Method
```bash
cargo install dora-cli --force
```

### Pip/uv Method
```bash
# With pip
pip install --upgrade dora-rs-cli

# With uv
uv pip install --upgrade dora-rs-cli
```

### GitHub Method
```bash
# Re-run installer (overwrites existing)
curl --proto '=https' --tlsv1.2 -LsSf \
  https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh
```

## Uninstalling dora-cli

### Cargo Method
```bash
cargo uninstall dora-cli
```

### Pip/uv Method
```bash
# With pip
pip uninstall dora-rs-cli

# With uv
uv pip uninstall dora-rs-cli
```

### GitHub Method
```bash
# Remove binary
rm ~/.cargo/bin/dora  # macOS/Linux
# or
del %USERPROFILE%\.cargo\bin\dora.exe  # Windows
```

## Security Notes

### GitHub Installer (curl | sh)
- Downloads from official dora-rs GitHub releases
- Inspects script before running: `curl -L <url> | less`
- Installs to `~/.cargo/bin` (user directory)

### Cargo Install
- Downloads from crates.io (official Rust registry)
- Compiles from audited source
- No binary download required

### Pip/uv Install
- Downloads from PyPI (official Python registry)
- Package: `dora-rs-cli`
- Installs to virtual environment (isolated)

## CI/CD Integration

### GitHub Actions (Rust-only)
```yaml
- name: Install dora-cli
  run: cargo install dora-cli
```

### GitHub Actions (Python)
```yaml
- name: Set up Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'

- name: Install uv
  run: pip install uv

- name: Install dora-cli
  run: uv pip install dora-rs-cli
```

### Docker (Rust-only)
```dockerfile
FROM rust:1.75
RUN cargo install dora-cli
```

### Docker (Python)
```dockerfile
FROM python:3.11
RUN pip install dora-rs-cli
```

## Next Steps

After installing dora-cli:

1. **Verify installation:**
   ```bash
   dora --version
   ```

2. **Create a new project:**
   ```bash
   dora new my-robot --lang python
   # or
   dora new my-robot --lang rust
   ```

3. **Explore available nodes:**
   ```bash
   dora list
   ```

4. **Run a dataflow:**
   ```bash
   cd my-robot
   dora run dataflow.yml
   ```

5. **Learn more:**
   - [Dora Documentation](https://dora-rs.ai)
   - [dora-skills Repository](https://github.com/dora-rs/dora-skills)
   - [Node Hub](https://github.com/dora-rs/dora/tree/main/node-hub)

## Related Commands

- `/build` - Build and install dependencies for dataflow nodes
- `/run` - Run a dora dataflow
- `/new-dataflow` - Create a new dataflow project
- `/add-node` - Add a node to existing dataflow

## Common Patterns

### Pattern 1: Rust Developer (No Python)
```bash
# Install dora-cli with cargo
/install --method cargo

# Create Rust project
dora new robot --lang rust
cd robot

# Build and run
cargo build --release
dora run dataflow.yml
```

### Pattern 2: Python Developer (ML/AI)
```bash
# Set up Python environment
python -m venv .venv
source .venv/bin/activate

# Install dora-cli
/install  # Auto-detects uv or pip

# Create Python project
dora new robot --lang python
cd robot

# Build and run with uv
dora build dataflow.yml --uv
dora run dataflow.yml
```

### Pattern 3: Quick Testing (No Setup)
```bash
# Install with GitHub installer
/install --method github

# Test immediately
dora new test-project
cd test-project
dora run dataflow.yml
```

### Pattern 4: Development/Contributing
```bash
# Install from source
/install --method source

# Make changes and test
cd dora
cargo build --release -p dora-cli
./target/release/dora --version
```

## FAQ

**Q: Which method should I use?**

A: Use auto-detect (`/install`). It will choose the best method for your system:
- **Rust projects** → cargo
- **Python projects** → uv or pip
- **No dependencies** → github

**Q: Do I need Python?**

A: No! If you have cargo installed, you can use a pure Rust workflow with no Python dependency.

**Q: Can I use both cargo and pip?**

A: Yes, but install dora-cli with only one method. For hybrid projects, use cargo for dora-cli and let individual nodes manage their own Python dependencies.

**Q: What if I don't have cargo or Python?**

A: Use the GitHub installer method (`--method github`). It works on any system with no prerequisites.

**Q: How do I update dora-cli?**

A: Re-run the install command with `--force` flag, or use the update commands listed in the "Updating dora-cli" section.

**Q: Can I install different versions?**

A:
- Cargo: `cargo install dora-cli --version 0.3.4`
- Pip: `pip install dora-rs-cli==0.3.4`

**Q: Where is dora-cli installed?**

A:
- Cargo: `~/.cargo/bin/dora`
- Pip/uv: `<venv>/bin/dora` or `<venv>/Scripts/dora.exe`
- GitHub: `~/.cargo/bin/dora` (macOS/Linux) or `%USERPROFILE%\.cargo\bin\dora.exe` (Windows)
