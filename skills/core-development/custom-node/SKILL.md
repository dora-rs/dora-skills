---
name: custom-node
description: Create custom nodes for dora-rs in Python, Rust, or C++. Use when user wants to implement their own node, write processing logic, or create new node types.
---

# Custom Node Development

Guide for creating custom nodes in Python, Rust, or C++.

## Python Node

### Basic Structure

See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#python-node-boilerplate) for the standard Python node template.

### Event Types

| Type | Description | Fields |
|------|-------------|--------|
| `INPUT` | Data received | `id`, `value`, `metadata` |
| `INPUT_CLOSED` | Input stream closed | `id` |
| `STOP` | Shutdown signal | - |
| `ERROR` | Error occurred | `error` |

### Handling Multiple Inputs

See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#multiple-input-handling-python).

### Working with Image Data

See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#image-handling-python).

### Working with Audio Data

See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#audio-handling-python).

### Using Timeout for Non-blocking

See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#non-blocking-event-loop-python).

### Package Structure

```
my-node/
├── pyproject.toml
├── my_node/
│   ├── __init__.py
│   ├── __main__.py
│   └── main.py
└── tests/
    └── test_node.py
```

**pyproject.toml:**
```toml
[project]
name = "my-node"
version = "0.1.0"
dependencies = [
    "dora-rs>=0.3.9",
    "pyarrow>=5.0.0",
    "numpy",
]

[project.scripts]
my-node = "my_node.main:main"
```

**__main__.py:**
```python
from .main import main

if __name__ == "__main__":
    main()
```

## Rust Node

### Basic Structure

See [CODE_TEMPLATES.md](../../../data/CODE_TEMPLATES.md#rust-node-boilerplate).

### Cargo.toml

```toml
[package]
name = "my-node"
version = "0.1.0"
edition = "2021"

[dependencies]
dora-node-api = "0.3"
eyre = "0.6"
```

## C++ Node

C++ nodes follow a similar pattern to Rust. Contact dora-rs documentation for C++ API details.

## Node Testing

### Python Unit Test

```python
import pytest
from dora import Node
import pyarrow as pa

def test_node_processing():
    # Create test input
    test_data = pa.array([1, 2, 3, 4, 5])

    # Process
    result = process(test_data)

    # Verify
    assert len(result) == 5
```

### Integration Test with Dora

```python
from dora import Node

def test_integration():
    # Run in interactive mode for testing
    node = Node()

    # Send test input
    node.send_output("test", pa.array([1, 2, 3]))

    # Check output
    # ...
```

## Best Practices

1. **Handle all event types**: Don't ignore INPUT_CLOSED or ERROR
2. **Use metadata**: Pass image dimensions, sample rates, encodings
3. **Proper cleanup**: Handle STOP event gracefully
4. **Error handling**: Catch exceptions and log errors
5. **Type hints**: Use Python type hints for clarity

## Related Skills

- `core-development` - Dataflow YAML configuration
- `cli-workflow` - Running and testing nodes
