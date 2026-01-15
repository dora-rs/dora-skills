---
name: install
description: Install dora-cli using the best method for your platform
---

# /install Command

Automatically install dora-cli using the best method for your platform.

## Usage

```
/install [--method <method>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--method <method>` | Installation method: `uv`, `pip`, `cargo`, `github`, or `source` | Auto-detect |

## What It Does

The install command:
1. Detects your platform (macOS, Linux, Windows)
2. Checks for available package managers and tools
3. Recommends and executes the best installation method
4. Verifies the installation with `dora --version`

## Installation Methods

### 1. uv (Recommended - Fastest)

Ultra-fast Python package installer (10-100x faster than pip):

```bash
# Install with uv
/install --method uv
```

Executes:
```bash
uv pip install dora-rs-cli
```

**Advantages:**
- 10-100x faster than pip
- Better dependency resolution
- Drop-in pip replacement
- Built in Rust for performance

**Install uv first:**
```bash
pip install uv
# or
curl -LsSf https://astral.sh/uv/install.sh | sh
```

### 2. pip (Most Compatible)

Standard Python package installer:

```bash
# Install with pip
/install --method pip
```

Executes:
```bash
pip install dora-rs-cli
```

**Advantages:**
- Widely available
- No additional setup required
- Stable and reliable

### 3. cargo (For Rust Developers)

Install from crates.io:

```bash
# Install with cargo
/install --method cargo
```

Executes:
```bash
cargo install dora-cli
```

**Advantages:**
- Latest version from source
- Native Rust toolchain integration
- Full feature set

**Requires:**
- Rust toolchain installed (`rustup`)

### 4. GitHub Installer (Standalone)

Platform-specific standalone installers:

```bash
# Install from GitHub releases
/install --method github
```

**macOS/Linux:**
```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.ps1 | iex"
```

**Advantages:**
- No package manager required
- Standalone binary
- Quick setup

### 5. Source (For Development)

Build from source:

```bash
# Install from source
/install --method source
```

Executes:
```bash
git clone https://github.com/dora-rs/dora.git
cd dora
cargo build --release -p dora-cli
# Adds to PATH
```

**Advantages:**
- Latest development version
- Full source code access
- Customizable build

**Requires:**
- Rust toolchain
- Git

## Auto-Detection Logic

When no method is specified, the command automatically selects the best option:

```
Priority order:
1. uv     (if available - fastest)
2. pip    (if Python available - most compatible)
3. github (standalone installer)
4. cargo  (if Rust toolchain available)
5. source (last resort)
```

## Examples

### Auto-detect and install

```
/install
```

Output:
```bash
Detecting installation method...
✓ Found uv package manager
→ Installing dora-cli with uv (fastest method)

$ uv pip install dora-rs-cli
Installing dora-rs-cli...
✓ dora-rs-cli installed successfully

Verifying installation...
$ dora --version
dora-cli 0.3.5

✓ Installation complete!

Next steps:
  dora new my-robot --lang python
  cd my-robot
  dora run dataflow.yml
```

### Install with specific method

```
/install --method pip
```

Output:
```bash
Installing dora-cli with pip...

$ pip install dora-rs-cli
Collecting dora-rs-cli...
✓ Successfully installed dora-rs-cli-0.3.5

$ dora --version
dora-cli 0.3.5

✓ Installation complete!
```

### Upgrade existing installation

```
/install --method uv
```

If already installed:
```bash
✓ dora-cli is already installed (v0.3.4)
→ Upgrading to latest version...

$ uv pip install --upgrade dora-rs-cli
Upgrading dora-rs-cli...
✓ Upgraded to v0.3.5
```

## Platform-Specific Notes

### macOS

**Recommended:** uv or pip
```bash
# Install uv first (fastest)
curl -LsSf https://astral.sh/uv/install.sh | sh
/install --method uv

# Or use pip
/install --method pip
```

### Linux

**Recommended:** uv or pip
```bash
# Install uv first (fastest)
curl -LsSf https://astral.sh/uv/install.sh | sh
/install --method uv

# Or use pip
/install --method pip
```

### Windows

**Recommended:** pip or GitHub installer
```powershell
# Use pip (if Python installed)
/install --method pip

# Or GitHub installer
/install --method github
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `uv not found` | Install uv: `pip install uv` or use `--method pip` |
| `pip not found` | Install Python from python.org |
| `cargo not found` | Install Rust from rustup.rs |
| `Permission denied` | Use virtual environment or run with sudo |
| `Command not found after install` | Restart terminal or add to PATH |
| GitHub installer fails | Check network/firewall, use pip instead |

### Virtual Environment (Recommended)

Install in virtual environment to avoid conflicts:

```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # macOS/Linux
.\venv\Scripts\activate   # Windows

# Install with uv or pip
/install --method uv
```

### PATH Issues

If `dora` command not found after installation:

**pip/uv install:**
```bash
# Find installation location
pip show dora-rs-cli

# Add to PATH (add to ~/.bashrc or ~/.zshrc)
export PATH="$HOME/.local/bin:$PATH"
```

**cargo install:**
```bash
# Add cargo bin to PATH
export PATH="$HOME/.cargo/bin:$PATH"
```

**Source build:**
```bash
# Add to PATH
export PATH="$PATH:/path/to/dora/target/release"
```

## Post-Installation

After installation, verify and get started:

```bash
# Check version
dora --version

# View help
dora --help

# Create new project
dora new my-robot --lang python

# Navigate to project
cd my-robot

# Build dependencies
dora build dataflow.yml

# Run dataflow
dora run dataflow.yml
```

## Updating dora-cli

### With uv (fastest)
```bash
uv pip install --upgrade dora-rs-cli
```

### With pip
```bash
pip install --upgrade dora-rs-cli
```

### With cargo
```bash
cargo install dora-cli --force
```

### With GitHub installer
Re-run the installer script:
```bash
# macOS/Linux
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.ps1 | iex"
```

## Uninstalling

### uv/pip
```bash
uv pip uninstall dora-rs-cli
# or
pip uninstall dora-rs-cli
```

### cargo
```bash
cargo uninstall dora-cli
```

### GitHub installer/Source
```bash
# Remove binary
rm $(which dora)
```

## Comparison Table

| Method | Speed | Compatibility | Requirements | Best For |
|--------|-------|---------------|--------------|----------|
| **uv** | ⚡⚡⚡⚡⚡ | High | Python, uv | Everyone (fastest) |
| **pip** | ⚡⚡ | Very High | Python | General use |
| **cargo** | ⚡⚡⚡ | Medium | Rust | Rust developers |
| **github** | ⚡⚡⚡⚡ | High | None | Quick standalone |
| **source** | ⚡ | High | Rust, Git | Development |

## Security Notes

### uv Installation
- uv is maintained by Astral (creators of ruff)
- Verifies package signatures
- Faster and more secure than pip

### GitHub Installers
- Scripts download from official GitHub releases
- Use HTTPS (TLS 1.2+)
- Verify checksums when available

### Source Installation
- Audit source code before building
- Review build scripts
- Most transparent method

## Related Commands

- `/build` - Build dataflow dependencies (supports `--uv` flag)
- `/run` - Run dataflow
- `/new-dataflow` - Create new project

## Environment Variables

```bash
# Prefer uv for all Python operations
export DORA_USE_UV=1

# Custom installation path
export DORA_INSTALL_PATH=/usr/local/bin

# GitHub API token (for rate limiting)
export GITHUB_TOKEN=your_token_here
```

## See Also

- [Dora Documentation](https://dora-rs.ai)
- [Dora GitHub](https://github.com/dora-rs/dora)
- [uv Documentation](https://github.com/astral-sh/uv)
- [Dora PyPI Package](https://pypi.org/project/dora-rs-cli/)
- [Dora Crate](https://crates.io/crates/dora-cli)
