---
name: visualize
description: Generate and display dataflow visualization
---

# /visualize Command

Generate visual representation of a dataflow.

## Usage

```
/visualize [<dataflow-file>] [--format <format>] [--output <file>]
```

## Arguments

| Argument | Description | Default |
|----------|-------------|---------|
| `<dataflow-file>` | Dataflow YAML path | ./dataflow.yml |
| `--format` | Output format | mermaid |
| `--output` | Save to file | - |

## Formats

### mermaid (default)
Mermaid diagram syntax for markdown/web:

```mermaid
graph LR
    camera[camera] --> |image| detector[detector]
    detector --> |bbox| visualize[visualize]
    camera --> |image| visualize
```

### ascii
ASCII art for terminal:

```
┌────────┐     ┌──────────┐     ┌───────────┐
│ camera │────▶│ detector │────▶│ visualize │
└────────┘     └──────────┘     └───────────┘
      │                               ▲
      └───────────────────────────────┘
```

### dot
Graphviz DOT format:

```dot
digraph dataflow {
    camera -> detector [label="image"];
    detector -> visualize [label="bbox"];
    camera -> visualize [label="image"];
}
```

## Examples

### Basic visualization

```
/visualize
```

Output (Mermaid):
```mermaid
graph LR
    subgraph Sensors
        camera[camera<br>opencv-video-capture]
    end

    subgraph Processing
        detector[detector<br>dora-yolo]
    end

    subgraph Output
        viz[visualize<br>dora-rerun]
    end

    camera -->|image| detector
    detector -->|bbox| viz
    camera -->|image| viz
```

### Save to file

```
/visualize dataflow.yml --output graph.md
```

### Graphviz PNG

```
/visualize --format dot --output graph.dot
dot -Tpng graph.dot -o graph.png
```

## Node Information

The visualization includes:
- Node ID
- Node type/path
- Input connections with labels
- Output ports
- Timer inputs (shown as dashed lines)

## Styling

### Mermaid styles by node type:

| Type | Color |
|------|-------|
| Sensor | Green |
| Processing | Blue |
| Output | Orange |
| Robot | Red |

### Example styled output:

```mermaid
graph LR
    classDef sensor fill:#90EE90
    classDef process fill:#87CEEB
    classDef output fill:#FFB347

    camera[camera]:::sensor
    detector[detector]:::process
    viz[visualize]:::output

    camera --> detector
    detector --> viz
    camera --> viz
```

## Integration

### Use with dora CLI

```bash
# Built-in visualization
dora graph dataflow.yml

# Open in browser
dora graph dataflow.yml --open
```

### Markdown embedding

Include in documentation:
````markdown
## Architecture

```mermaid
graph LR
    camera --> detector --> visualize
```
````

## Complex Example

For a speech-to-speech robot:

```mermaid
graph TB
    subgraph Audio Input
        mic[microphone]
        vad[vad]
    end

    subgraph Processing
        whisper[whisper]
        llm[llm]
        tts[tts]
    end

    subgraph Output
        speaker[speaker]
    end

    mic -->|audio| vad
    vad -->|audio| whisper
    whisper -->|text| llm
    llm -->|text| tts
    tts -->|audio| speaker
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Invalid YAML | Fix syntax errors first |
| Missing connections | Check node input sources |
| Circular dependency | Redesign data flow |
