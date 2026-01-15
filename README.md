# dora-skills

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

### Introduction

Skills for building AI agents, workflows, and embodied intelligence applications with the [dora-rs](https://github.com/dora-rs/dora) dataflow framework.

Dora is a high-performance dataflow framework that orchestrates AI models, sensors, and actuators through declarative YAML pipelines. It's ideal for scenarios requiring real-time data flow coordination — from multi-modal AI agents to robotic systems.

**Current Focus**: Embodied Intelligence (具身智能) — combining perception, language models, and physical control.

### Features

- **Core Development**: Dataflow building and custom node development
- **ML/Vision**: YOLO detection, SAM2 segmentation, VLM integration
- **Audio**: Speech-to-text, text-to-speech, voice activity detection
- **Robot Control**: Robotic arm, servo motor, mobile base control
- **Data Pipeline**: Recording, replay, LeRobot integration

### Quick Start

1. Install dora CLI:
```bash
pip install dora-rs
# or
cargo install dora-cli
```

2. Create a new project:
```bash
dora new my-robot --lang python
```

3. Run a dataflow:
```bash
dora run dataflow.yml
```

### Available Skills

| Category | Skills |
|----------|--------|
| Core | `core-development`, `custom-node`, `cli-workflow` |
| Vision | `object-detection`, `segmentation`, `tracking`, `vlm` |
| Audio | `speech-to-text`, `text-to-speech`, `voice-activity` |
| Robot | `arm-control`, `actuators`, `chassis` |
| Data | `recording`, `replay`, `lerobot` |

### Commands

- `/new-dataflow` - Create a new dataflow project
- `/add-node` - Add a node to existing dataflow
- `/visualize` - Generate dataflow visualization

### Resources

- [Dora Documentation](https://dora-rs.ai)
- [Dora GitHub](https://github.com/dora-rs/dora)
- [Node Hub](https://github.com/dora-rs/dora/tree/main/node-hub)

---

<a name="chinese"></a>
## 中文

### 简介

使用 [dora-rs](https://github.com/dora-rs/dora) 数据流框架构建 AI Agent、工作流和具身智能应用的技能集。

Dora 是一个高性能数据流框架，通过声明式 YAML 管道编排 AI 模型、传感器和执行器。适用于需要实时数据流协调的场景 —— 从多模态 AI Agent 到机器人系统。

**当前重点**: 具身智能 (Embodied Intelligence) —— 融合感知、语言模型与物理控制。

### 功能特性

- **核心开发**: 数据流构建和自定义节点开发
- **机器学习/视觉**: YOLO 检测、SAM2 分割、VLM 集成
- **音频处理**: 语音识别、语音合成、语音活动检测
- **机器人控制**: 机械臂、舵机、移动底盘控制
- **数据管道**: 数据录制、回放、LeRobot 集成

### 快速开始

1. 安装 dora CLI:
```bash
pip install dora-rs
# 或者
cargo install dora-cli
```

2. 创建新项目:
```bash
dora new my-robot --lang python
```

3. 运行数据流:
```bash
dora run dataflow.yml
```

### 可用技能

| 类别 | 技能 |
|------|------|
| 核心 | `core-development`, `custom-node`, `cli-workflow` |
| 视觉 | `object-detection`, `segmentation`, `tracking`, `vlm` |
| 音频 | `speech-to-text`, `text-to-speech`, `voice-activity` |
| 机器人 | `arm-control`, `actuators`, `chassis` |
| 数据 | `recording`, `replay`, `lerobot` |

### 命令

- `/new-dataflow` - 创建新的数据流项目
- `/add-node` - 向现有数据流添加节点
- `/visualize` - 生成数据流可视化图

### 资源

- [Dora 文档](https://dora-rs.ai)
- [Dora GitHub](https://github.com/dora-rs/dora)
- [节点仓库](https://github.com/dora-rs/dora/tree/main/node-hub)

---

## License

Apache-2.0
