---
name: custom-node
description: Create custom nodes for dora-rs in Python, Rust, or C++. Use when user wants to implement their own node, write processing logic, or create new node types.
---

# Custom Node Development

Guide for creating custom nodes in Python, Rust, or C++.

## Python Node

### Basic Structure

```python
from dora import Node
import pyarrow as pa

def main():
    node = Node()

    for event in node:
        if event["type"] == "INPUT":
            # Get input data
            input_id = event["id"]
            data = event["value"]  # PyArrow array
            metadata = event["metadata"]

            # Process data
            result = process(data)

            # Send output
            node.send_output("output_name", pa.array(result), metadata)

        elif event["type"] == "STOP":
            break

if __name__ == "__main__":
    main()
```

### Event Types

| Type | Description | Fields |
|------|-------------|--------|
| `INPUT` | Data received | `id`, `value`, `metadata` |
| `INPUT_CLOSED` | Input stream closed | `id` |
| `STOP` | Shutdown signal | - |
| `ERROR` | Error occurred | `error` |

### Handling Multiple Inputs

```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT":
        if event["id"] == "image":
            # Handle image input
            image_data = event["value"].to_numpy()
            # Process image...

        elif event["id"] == "command":
            # Handle command input
            command = event["value"][0].as_py()
            # Execute command...

        # Send result
        node.send_output("result", pa.array([result]))
```

### Working with Image Data

```python
import numpy as np
import pyarrow as pa

# Receive image
def handle_image(event):
    metadata = event["metadata"]
    width = int(metadata["width"])
    height = int(metadata["height"])
    encoding = metadata.get("encoding", "bgr8")

    # Convert to numpy array
    flat_array = event["value"].to_numpy()

    if encoding in ["bgr8", "rgb8"]:
        image = flat_array.reshape((height, width, 3))
    elif encoding == "gray8":
        image = flat_array.reshape((height, width))

    return image

# Send image
def send_image(node, image, encoding="bgr8"):
    metadata = {
        "width": str(image.shape[1]),
        "height": str(image.shape[0]),
        "encoding": encoding
    }
    flat = image.flatten()
    node.send_output("image", pa.array(flat), metadata)
```

### Working with Audio Data

```python
import numpy as np
import pyarrow as pa

# Receive audio
def handle_audio(event):
    metadata = event["metadata"]
    sample_rate = int(metadata.get("sample_rate", 16000))
    audio = event["value"].to_numpy().astype(np.float32)
    return audio, sample_rate

# Send audio
def send_audio(node, audio, sample_rate=16000):
    metadata = {"sample_rate": str(sample_rate)}
    node.send_output("audio", pa.array(audio.astype(np.float32)), metadata)
```

### Using Timeout for Non-blocking

```python
from dora import Node

node = Node()

while True:
    event = node.next(timeout=0.1)  # 100ms timeout

    if event is None:
        # No event received, do background work
        do_background_task()
        continue

    if event["type"] == "INPUT":
        process(event)
    elif event["type"] == "STOP":
        break
```

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

```rust
use dora_node_api::{DoraNode, Event};
use eyre::Result;

fn main() -> Result<()> {
    let (mut node, mut events) = DoraNode::init_from_env()?;

    while let Some(event) = events.recv() {
        match event {
            Event::Input { id, metadata, data } => {
                // Process input
                let result = process(&data);

                // Send output
                node.send_output(
                    "output".into(),
                    metadata.parameters,
                    result.into(),
                )?;
            }
            Event::Stop => break,
            _ => {}
        }
    }

    Ok(())
}
```

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

### Working with Arrow Data

```rust
use arrow::array::{Float32Array, UInt8Array};
use dora_node_api::arrow::array::ArrayRef;

fn process_image(data: &ArrayRef) -> Vec<f32> {
    let array = data.as_any()
        .downcast_ref::<UInt8Array>()
        .expect("Expected UInt8Array");

    // Process image data
    let result: Vec<f32> = array.values()
        .iter()
        .map(|&v| v as f32 / 255.0)
        .collect();

    result
}
```

## C++ Node

### Basic Structure

```cpp
#include "dora-node-api.h"
#include <iostream>

int main() {
    auto dora_node = init_dora_node();
    auto merged_events = dora_events_into_combined(std::move(dora_node.events));

    while (true) {
        auto event = merged_events->next();

        if (event->is_stop()) {
            break;
        }

        if (event->is_input()) {
            auto input = event->input();
            std::string id(input.id.ptr, input.id.len);

            // Process input
            // ...

            // Send output
            std::vector<uint8_t> result = process(input.data);
            auto output = dora_node.send_output(
                {"output", 6},
                result.data(),
                result.size()
            );
        }
    }

    return 0;
}
```

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
