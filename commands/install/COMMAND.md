---
name: install
description: Install dora-cli using the best method for your platform
---

# /install Command

Install dora-cli automatically using the recommended method for your platform.

## Usage

```
/install [--method <method>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `--method` | Installation method | auto |

## Installation Methods

The command will automatically detect the best installation method for your platform:

### auto (default)
Automatically selects the best method based on:
1. **Operating System**: Detects macOS, Linux, or Windows
2. **Available Tools**: Checks for pip, cargo, curl/PowerShell
3. **User Preference**: Prioritizes ease of use and reliability

**Recommended priority:**
1. **pip** (fastest, most reliable) - `pip install dora-rs-cli`
2. **GitHub installer** (standalone, no dependencies)
   - macOS/Linux: `curl --proto '=https' --tlsv1.2 -LsSf https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh`
   - Windows: `powershell -ExecutionPolicy ByPass -c "irm https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.ps1 | iex"`
3. **cargo** (for Rust developers) - `cargo install dora-cli`
4. **source** (for development) - Build from source

### pip
Install via Python package manager:
```bash
pip install dora-rs-cli
```

**Pros:**
- Fastest installation
- Works on all platforms
- Easy to update (`pip install --upgrade dora-rs-cli`)
- No Rust toolchain required

**Cons:**
- Requires Python and pip

### cargo
Install via Rust package manager:
```bash
cargo install dora-cli
```

**Pros:**
- Native Rust installation
- Always latest from crates.io
- Good for Rust developers

**Cons:**
- Requires Rust toolchain
- Slower compilation time
- Larger download size

### github
Install using official GitHub release installers:

**macOS/Linux:**
```bash
curl --proto '=https' --tlsv1.2 -LsSf https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.sh | sh
```

**Windows:**
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://github.com/dora-rs/dora/releases/latest/download/dora-cli-installer.ps1 | iex"
```

**Pros:**
- No dependencies required
- Official standalone installers
- Pre-built binaries

**Cons:**
- Requires internet connection
- May need manual PATH configuration

### source
Build from source:
```bash
git clone https://github.com/dora-rs/dora.git
cd dora
cargo build --release -p dora-cli
PATH=$PATH:$(pwd)/target/release
```

**Pros:**
- Latest development version
- Full control over build

**Cons:**
- Requires Rust toolchain
- Longest installation time
- Manual PATH management

## Examples

### Auto-detect and install
```
/install
```

This will:
1. Detect your operating system
2. Check for available tools (pip, cargo, curl/PowerShell)
3. Choose the best method
4. Execute the installation
5. Verify installation with `dora --version`

### Install with specific method
```
/install --method pip
```

Force installation using pip.

```
/install --method cargo
```

Force installation using cargo (requires Rust toolchain).

```
/install --method github
```

Force installation using GitHub release installer.

## Workflow

1. **Detect Platform**: Identify OS (macOS, Linux, Windows)
2. **Check Prerequisites**:
   - For pip: Check if pip is available
   - For cargo: Check if cargo is available
   - For github: Check if curl/PowerShell is available
3. **Select Method**: Use explicit method or auto-select
4. **Execute Installation**: Run the appropriate command
5. **Verify**: Test with `dora --version`
6. **Report**: Show installation result and next steps

## Installation Decision Matrix

| Platform | pip available | cargo available | Recommended |
|----------|---------------|-----------------|-------------|
| Any | ✅ | ✅ | pip (fastest) |
| Any | ✅ | ❌ | pip |
| Any | ❌ | ✅ | cargo |
| macOS/Linux | ❌ | ❌ | github (curl) |
| Windows | ❌ | ❌ | github (PowerShell) |

## Post-Installation

After successful installation, the command will:
1. Verify dora is installed: `dora --version`
2. Show next steps:
   ```bash
   # Create a new project
   dora new my-robot --lang python

   # Or run an existing dataflow
   dora run dataflow.yml
   ```

## Troubleshooting

### pip installation fails
- Try upgrading pip: `pip install --upgrade pip`
- Use user install: `pip install --user dora-rs-cli`
- Check Python version (requires Python 3.8+)

### cargo installation fails
- Update Rust toolchain: `rustup update`
- Check cargo version: `cargo --version`

### GitHub installer fails
- Check internet connection
- Verify curl/PowerShell is available
- Try manual download from releases page

### Command not found after installation
- Restart terminal to refresh PATH
- Manually add to PATH:
  - macOS/Linux: Add to `~/.bashrc` or `~/.zshrc`
  - Windows: Add to System Environment Variables

## Security Notes

- All installation methods use official sources
- GitHub installers use HTTPS with TLS 1.2+
- pip installs from PyPI (https://pypi.org/project/dora-rs-cli/)
- cargo installs from crates.io (https://crates.io/crates/dora-cli)

## Related Commands

- `/new-dataflow` - Create a new dataflow project after installation
- `/add-node` - Add nodes to dataflows
- `/visualize` - Generate dataflow visualizations
