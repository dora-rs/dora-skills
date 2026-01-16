# Code Templates

Reusable code patterns for dora-rs custom nodes. Reference these templates to avoid duplication.

## Python Node Boilerplate

```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT":
        input_id = event["id"]
        data = event["value"]
        metadata = event["metadata"]

        # Process data here
        result = process(data)

        # Send output
        node.send_output("output_name", pa.array(result), metadata)

    elif event["type"] == "STOP":
        break
```

---

## Image Handling (Python)

### Receive Image
```python
def handle_image(event):
    """Extract image from dora event."""
    metadata = event["metadata"]
    width = int(metadata["width"])
    height = int(metadata["height"])
    encoding = metadata.get("encoding", "bgr8")

    flat_array = event["value"].to_numpy()

    if encoding in ["bgr8", "rgb8"]:
        image = flat_array.reshape((height, width, 3))
    elif encoding == "gray8":
        image = flat_array.reshape((height, width))

    return image
```

### Send Image
```python
def send_image(node, image, encoding="bgr8"):
    """Send image as dora output."""
    metadata = {
        "width": str(image.shape[1]),
        "height": str(image.shape[0]),
        "encoding": encoding
    }
    flat = image.flatten()
    node.send_output("image", pa.array(flat), metadata)
```

---

## Audio Handling (Python)

### Receive Audio
```python
def handle_audio(event):
    """Extract audio from dora event."""
    metadata = event["metadata"]
    sample_rate = int(metadata.get("sample_rate", 16000))
    audio = event["value"].to_numpy().astype(np.float32)
    return audio, sample_rate
```

### Send Audio
```python
def send_audio(node, audio, sample_rate=16000):
    """Send audio as dora output."""
    metadata = {"sample_rate": str(sample_rate)}
    node.send_output("audio", pa.array(audio.astype(np.float32)), metadata)
```

---

## Detection Processing (Python)

```python
def process_detections(event):
    """Process YOLO bbox output."""
    detections = event["value"]

    for detection in detections:
        bbox = detection["bbox"]  # [x, y, w, h]
        confidence = detection["confidence"]
        label = detection["label"]

        print(f"Detected {label} at {bbox} ({confidence:.2f})")

        # Filter by class
        if label == "person":
            # React to person detection
            pass
```

---

## Multiple Input Handling (Python)

```python
from dora import Node
import pyarrow as pa

node = Node()

for event in node:
    if event["type"] == "INPUT":
        if event["id"] == "image":
            image = handle_image(event)
            # Process image

        elif event["id"] == "command":
            command = event["value"][0].as_py()
            # Execute command

        elif event["id"] == "bbox":
            detections = event["value"]
            # Process detections
```

---

## Non-blocking Event Loop (Python)

```python
from dora import Node

node = Node()

while True:
    event = node.next(timeout=0.1)  # 100ms timeout

    if event is None:
        # No event, do background work
        do_background_task()
        continue

    if event["type"] == "INPUT":
        process(event)
    elif event["type"] == "STOP":
        break
```

---

## Rust Node Boilerplate

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

---

## Common Metadata Structures

### Image Metadata
```python
metadata = {
    "width": "640",
    "height": "480",
    "encoding": "bgr8"  # or "rgb8", "gray8"
}
```

### Audio Metadata
```python
metadata = {
    "sample_rate": "16000"
}
```

### Detection Metadata
```python
bbox = {
    "bbox": [x, y, w, h],
    "confidence": 0.95,
    "class": 0,
    "label": "person"
}
```

---

## Error Handling Pattern

```python
from dora import Node
import pyarrow as pa
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

node = Node()

for event in node:
    try:
        if event["type"] == "INPUT":
            result = process(event)
            node.send_output("output", pa.array([result]))

        elif event["type"] == "ERROR":
            logger.error(f"Error: {event['error']}")

        elif event["type"] == "STOP":
            break

    except Exception as e:
        logger.error(f"Processing error: {e}")
```

---

## State Management Pattern

```python
from dora import Node
import pyarrow as pa

class StatefulNode:
    def __init__(self):
        self.node = Node()
        self.state = {}
        self.frame_count = 0

    def run(self):
        for event in self.node:
            if event["type"] == "INPUT":
                self.frame_count += 1
                result = self.process(event)
                self.node.send_output("output", pa.array([result]))

            elif event["type"] == "STOP":
                break

    def process(self, event):
        # Access self.state as needed
        pass

if __name__ == "__main__":
    node = StatefulNode()
    node.run()
```
