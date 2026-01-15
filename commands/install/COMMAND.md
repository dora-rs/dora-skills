---
name: install
description: Install dora-cli with the best method for your platform
---

# /install Command

Install dora-cli using the most appropriate method for your system. The command intelligently detects your platform and available tools to recommend the best installation approach.

## Prerequisites

### Virtual Environment (Recommended)

**IMPORTANT**: Before installing dora-cli with pip or uv, activate a virtual environment to isolate your Python packages:

```bash
# Create virtual environment (first time only)
python -m venv .venv

# Activate virtual environment
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
```

**Why virtual environments matter:**
- Prevents conflicts with system Python packages
- Ensures dora-cli dependencies are isolated
- Makes it easier to manage and update packages
- Required for proper uv integration with dora commands

After activation, you'll see `(.venv)` in your terminal prompt, indicating you're in the virtual environment.

## Usage

```
/install [--method <method>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--method` | Installation method: uv, pip, cargo, github, source | auto-detect |

## What It Does

The install command:
1. Detects your operating system (macOS, Linux, Windows)
2. Checks for available tools (uv, pip, cargo, curl, PowerShell)
3. Recommends the best installation method
4. Executes the installation
5. Verifies the installation with `dora --version`

## Installation Methods

### 1. uv (Recommended - Fastest)

Uses the ultra-fast uv package manager (10-100x faster than pip).

**Install uv first:**
```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# Or with pip
pip install uv
```

**Then install dora-cli:**
```bash
# Make sure virtual environment is activated!
source .venv/bin/activate  # Linux/macOS

# Install with uv
uv pip install dora-rs-cli
```

**Advantages:**
- Fastest installation (10-100x faster than pip)
- Better dependency resolution
- Compatible with all pip packages
- Works seamlessly with dora build/run commands

### 2. pip (Most Compatible)

Standard Python package installer, works everywhere.

```bash
# Make sure virtual environment is activated!
source .venv/bin/activate  # Linux/macOS

pip install dora-rs-cli
```

**Advantages:**
- Pre-installed with Python
- Most widely compatible
- Stable and reliable

### 3. GitHub Installers (Standalone)

Standalone installers that don't require Python or Rust.

**macOS/Linux:**
```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.ps1 | iex"
```

**Advantages:**
- No Python/Rust dependencies required
- Always gets latest release version
- Quick and easy for system-wide install

### 4. cargo (For Rust Developers)

Install from source using Rust's package manager.

```bash
cargo install dora-cli
```

**Prerequisites:**
- Rust toolchain (install from [rustup.rs](https://rustup.rs))

**Advantages:**
- Compiles for your specific system
- Always latest version from crates.io
- No Python dependencies

### 5. source (For Development)

Build from source for development or customization.

```bash
git clone https://github.com/dora-rs/dora.git
cd dora
cargo build --release -p dora-cli
export PATH=$PATH:$(pwd)/target/release
```

**Prerequisites:**
- Rust toolchain
- Git

**Advantages:**
- Full control over build
- Can modify source code
- Access to unreleased features

## Examples

### Auto-detect best method

```
/install
```

The command will check your system and recommend:
```bash
# If uv is available and venv is active
$ /install
Detected: Python 3.11, uv 0.1.15, virtual environment active
Recommended method: uv (fastest)

Installing dora-cli with uv...
  ✓ uv pip install dora-rs-cli
  ✓ dora-cli 0.3.7 installed

Installation complete!
Verify: dora --version
```

### Install with specific method

```
/install --method uv
```

```
/install --method pip
```

```
/install --method github
```

### First-time setup workflow

```bash
# 1. Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate

# 2. Install uv (optional but recommended)
pip install uv

# 3. Install dora-cli
/install --method uv

# 4. Verify installation
dora --version

# 5. Start using dora
dora new my-robot --lang python
```

## Installation Priority

The auto-detect logic follows this priority order:

1. **uv** (if installed and venv active) - Fastest
2. **pip** (if venv active) - Most compatible
3. **github** (standalone installers) - No dependencies
4. **cargo** (if Rust installed) - For developers
5. **source** (requires git + cargo) - For customization

## Platform-Specific Notes

### macOS
- GitHub installer works on Apple Silicon and Intel
- Homebrew support: `brew install dora-cli` (if available)
- May need to add to PATH: `export PATH=$PATH:$HOME/.dora/bin`

### Linux
- GitHub installer supports x86_64 and aarch64
- May need to add to PATH: `export PATH=$PATH:$HOME/.dora/bin`
- Some distributions require `libssl-dev` for cargo builds

### Windows
- Use PowerShell for GitHub installer
- Python from Microsoft Store or python.org both work
- May need to restart terminal after installation

## Verification

After installation, verify dora-cli is working:

```bash
# Check version
dora --version

# Show help
dora --help

# Test with new project
dora new test-project --lang python
cd test-project
dora run dataflow.yml
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `dora: command not found` | Add to PATH or restart terminal |
| `pip install fails` | Activate virtual environment first |
| `uv not found` | Install uv with pip or curl installer |
| `Permission denied` | Use virtual environment, not sudo |
| `SSL certificate error` | Update certificates: `pip install --upgrade certifi` |
| `Cargo not found` | Install Rust from [rustup.rs](https://rustup.rs) |
| `Build from source fails` | Check Rust version: `rustc --version` (need 1.70+) |

### Common Virtual Environment Issues

**Forgot to activate venv:**
```bash
# Error: pip install installs globally
$ pip install dora-rs-cli
# Fix: Activate venv first
$ source .venv/bin/activate
(.venv) $ pip install dora-rs-cli
```

**Virtual environment not found:**
```bash
# Create it first
python -m venv .venv
source .venv/bin/activate
```

**Wrong Python version in venv:**
```bash
# Recreate with specific Python version
python3.11 -m venv .venv
source .venv/bin/activate
```

## Updating dora-cli

### With pip/uv
```bash
source .venv/bin/activate
pip install --upgrade dora-rs-cli
# OR
uv pip install --upgrade dora-rs-cli
```

### With cargo
```bash
cargo install dora-cli --force
```

### With GitHub installers
```bash
# Re-run the installer script
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh
```

## Uninstalling

### With pip/uv
```bash
source .venv/bin/activate
pip uninstall dora-rs-cli
```

### With cargo
```bash
cargo uninstall dora-cli
```

### GitHub installers
```bash
# Remove binary
rm ~/.dora/bin/dora  # Linux/macOS
# Remove from PATH in ~/.bashrc or ~/.zshrc
```

## Method Comparison

| Method | Speed | Dependencies | Use Case |
|--------|-------|--------------|----------|
| uv | ⚡⚡⚡ (fastest) | Python, venv | Production, CI/CD |
| pip | ⚡⚡ (medium) | Python, venv | Standard installs |
| github | ⚡⚡⚡ (fast) | None | System-wide, no Python |
| cargo | ⚡ (slow) | Rust | Rust developers |
| source | ⚡ (slow) | Rust, git | Development, custom builds |

## Integration with Workflow

### Development Setup
```bash
# 1. Setup environment
python -m venv .venv
source .venv/bin/activate

# 2. Install tools
pip install uv
uv pip install dora-rs-cli

# 3. Create project
dora new my-robot --lang python
cd my-robot

# 4. Build and run
dora build --uv
dora run
```

### CI/CD Pipeline
```yaml
# .github/workflows/test.yml
- name: Setup Python
  uses: actions/setup-python@v4
  with:
    python-version: '3.11'

- name: Create venv
  run: python -m venv .venv

- name: Install dora-cli
  run: |
    source .venv/bin/activate
    pip install uv
    uv pip install dora-rs-cli

- name: Build and test
  run: |
    source .venv/bin/activate
    dora build --uv
    dora run dataflow.yml
```

## Security Notes

### GitHub Installers
- Always use HTTPS protocol
- Verify installer signatures (if available)
- Review script before piping to shell
- Use `--version` tag for reproducible installs

### pip/uv Installation
- Install in virtual environment (never use sudo)
- Verify package on PyPI: https://pypi.org/project/dora-rs-cli/
- Check package integrity with `pip hash`

### Source Builds
- Verify git repository: https://github.com/dora-rs/dora
- Review source code before building
- Use official releases, not random branches

## Next Steps

After installing dora-cli:

1. **Create your first project:**
   ```bash
   dora new my-first-robot --lang python
   ```

2. **Explore example dataflows:**
   ```bash
   git clone https://github.com/dora-rs/dora.git
   cd dora/examples
   ```

3. **Read the documentation:**
   - [Dora Documentation](https://dora-rs.ai/docs)
   - [Getting Started Guide](https://dora-rs.ai/docs/getting-started)
   - [Node Hub](https://github.com/dora-rs/dora/tree/main/node-hub)

4. **Use other commands:**
   - `/build` - Build dataflow dependencies
   - `/run` - Run your dataflow
   - `/new-dataflow` - Create new dataflow
   - `/add-node` - Add nodes to dataflow

## Related Commands

- `/build` - Build and install node dependencies
- `/run` - Run dataflow with automatic building
- `/new-dataflow` - Create new dataflow project
- `/start` - Start dataflow in daemon mode
- `/visualize` - Generate dataflow diagram

## Environment Variables

```bash
# Use uv by default for dora commands
export DORA_USE_UV=1

# Custom installation path
export DORA_HOME=$HOME/.local/dora

# pip configuration
export PIP_INDEX_URL=https://pypi.org/simple
```

## See Also

- [Dora CLI Documentation](https://dora-rs.ai/docs/cli)
- [Python Virtual Environments](https://docs.python.org/3/tutorial/venv.html)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Rust Installation](https://rustup.rs)
- [PyPI dora-rs-cli](https://pypi.org/project/dora-rs-cli/)
