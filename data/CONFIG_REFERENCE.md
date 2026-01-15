# Configuration Reference

Common configuration patterns and options used across dora-skills.

## Device Configuration

### GPU Selection
```yaml
env:
  DEVICE: cuda      # Default CUDA GPU
  DEVICE: cuda:0    # First GPU
  DEVICE: cuda:1    # Second GPU
  DEVICE: mps       # Apple Silicon (M1/M2/M3)
  DEVICE: cpu       # CPU fallback
```

**Usage:** Vision models (YOLO, SAM2), speech models (Whisper), tracking

---

## Queue Management

### Drop Old Frames (Real-time)
```yaml
inputs:
  image:
    source: camera/image
    queue_size: 1  # Only process latest frame
```

**Use case:** Real-time vision processing where latency matters more than processing every frame

### Buffer Multiple Frames
```yaml
inputs:
  image:
    source: camera/image
    queue_size: 10  # Buffer up to 10 frames
```

**Use case:** Batch processing or when you need frame history

---

## Timer Patterns

### Common Frame Rates
```yaml
inputs:
  tick: dora/timer/millis/33   # 30 FPS (camera)
  tick: dora/timer/millis/100  # 10 Hz (control loops)
  tick: dora/timer/secs/1      # 1 Hz (slow updates)
```

**Calculation:** `1000 / FPS = milliseconds`

---

## Model Configuration

### Vision Models

#### YOLO
```yaml
env:
  MODEL: yolov8n.pt       # Nano (fastest)
  MODEL: yolov8s.pt       # Small
  MODEL: yolov8m.pt       # Medium
  MODEL: yolov8l.pt       # Large
  MODEL: yolov8x.pt       # XLarge (most accurate)
  CONFIDENCE: "0.5"       # Detection threshold (0.0-1.0)
```

#### SAM2
```yaml
env:
  MODEL: sam2_hiera_tiny    # Fastest
  MODEL: sam2_hiera_small   # Balanced
  MODEL: sam2_hiera_base    # High quality
  MODEL: sam2_hiera_large   # Best quality
```

### Speech Models

#### Whisper
```yaml
env:
  # Distilled models (faster)
  MODEL: distil-whisper-small
  MODEL: distil-whisper-medium
  MODEL: distil-whisper-large-v3

  # Original models
  MODEL: whisper-tiny         # Fastest
  MODEL: whisper-base
  MODEL: whisper-small
  MODEL: whisper-medium
  MODEL: whisper-large-v3     # Best quality

  # Apple Silicon optimized
  MODEL: mlx-community/distil-whisper-large-v3
  BACKEND: mlx
```

---

## Language Configuration

### Single Language (Faster)
```yaml
env:
  LANGUAGE: en    # English
  LANGUAGE: zh    # Chinese
  LANGUAGE: ja    # Japanese
  LANGUAGE: ko    # Korean
  LANGUAGE: es    # Spanish
  LANGUAGE: fr    # French
```

### Auto-detect (Slower)
```yaml
env:
  LANGUAGE: auto
```

---

## Audio Configuration

### Sample Rates
```yaml
env:
  SAMPLE_RATE: "16000"  # Standard for speech (Whisper)
  SAMPLE_RATE: "44100"  # CD quality
  SAMPLE_RATE: "48000"  # Professional audio
```

### VAD Sensitivity
```yaml
env:
  THRESHOLD: "0.3"   # More sensitive (more false positives)
  THRESHOLD: "0.5"   # Balanced (default)
  THRESHOLD: "0.7"   # Less sensitive (may miss quiet speech)
```

---

## Image Configuration

### Resolution
```yaml
env:
  IMAGE_WIDTH: "320"   # Low res (fast)
  IMAGE_HEIGHT: "240"

  IMAGE_WIDTH: "640"   # Standard (balanced)
  IMAGE_HEIGHT: "480"

  IMAGE_WIDTH: "1280"  # High res (slow)
  IMAGE_HEIGHT: "720"
```

**Trade-off:** Higher resolution = better accuracy but slower processing

### Encoding
```yaml
metadata:
  encoding: "bgr8"   # OpenCV default (3 channels)
  encoding: "rgb8"   # Standard RGB (3 channels)
  encoding: "gray8"  # Grayscale (1 channel)
```

---

## Performance Optimization Patterns

### Real-time Vision Pipeline
```yaml
# Camera
env:
  IMAGE_WIDTH: "320"
  IMAGE_HEIGHT: "240"

# Detector
env:
  MODEL: yolov8n.pt
  DEVICE: cuda

# Queue management
inputs:
  image:
    source: camera/image
    queue_size: 1
```

### Batch Processing
```yaml
env:
  BATCH_SIZE: "4"      # Process multiple items together
  DEVICE: cuda
```

### Memory Optimization
```yaml
env:
  MODEL: yolov8n.pt    # Smaller model
  FP16: "true"         # Half precision (requires GPU)
  IMAGE_WIDTH: "416"   # Reduce input size
```

---

## Robot Control Configuration

### Serial Port
```yaml
env:
  ARM_PORT: /dev/ttyUSB0    # Linux
  ARM_PORT: /dev/tty.usbserial-XXX  # macOS
  ARM_PORT: COM3            # Windows
```

### Arm Types
```yaml
env:
  ARM_TYPE: leader      # Teleoperation leader
  ARM_TYPE: follower    # Teleoperation follower
  ARM_TYPE: standalone  # Single arm
```

---

## LLM Configuration

### Model Selection
```yaml
env:
  MODEL: gpt-4
  MODEL: claude-3-opus
  MODEL: llama-3-8b
  API_KEY: ${OPENAI_API_KEY}  # Environment variable
```

### Temperature
```yaml
env:
  TEMPERATURE: "0.0"    # Deterministic
  TEMPERATURE: "0.7"    # Balanced
  TEMPERATURE: "1.0"    # Creative
```

---

## Recording Configuration

### Output Format
```yaml
env:
  OUTPUT_DIR: ./recordings
  FORMAT: mcap          # Default dora format
  COMPRESS: "true"      # Enable compression
```

---

## Common Troubleshooting Settings

### Debug Mode
```yaml
env:
  LOG_LEVEL: debug
  VERBOSE: "true"
```

### Disable GPU (for testing)
```yaml
env:
  DEVICE: cpu
```

### Increase Timeout
```yaml
env:
  TIMEOUT: "10"  # seconds
```
