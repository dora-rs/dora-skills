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

### Getting Started with Claude Code

This skill package is designed to work seamlessly with [Claude Code](https://claude.ai/code) for AI-powered robotic development.

#### Using with Claude Code

1. **Install Claude Code** (if not already installed):
```bash
npm install -g @anthropic-ai/claude-code
```

2. **Clone this repository** into your Claude Code skills directory:
```bash
# Clone to the default skills location
git clone https://github.com/dora-rs/dora-skills.git ~/.claude-code/skills/dora-skills
```

3. **Start using the skills** in your conversations:
```bash
# Navigate to your dora project
cd my-robot-project

# Start Claude Code
claude-code
```

4. **Natural language commands** - Claude will automatically use these skills when you ask about:
   - Creating dataflow pipelines
   - Adding vision, audio, or robot control nodes
   - Implementing custom nodes
   - Setting up data recording/replay
   - Integrating ML models (YOLO, SAM2, VLMs)

**Example prompts:**
- "Create a new dataflow for object detection with a camera"
- "Add speech-to-text capability to my robot"
- "Help me implement a custom node for sensor processing"
- "Set up a data recording pipeline for training"

#### Alternative: Using with Other AI Tools

**Cursor IDE:**
1. Install the Cursor IDE from [cursor.sh](https://cursor.sh)
2. Clone this repository into your project
3. Use `@dora-skills` to reference these skills in your prompts

**Continue.dev:**
1. Install Continue in your IDE (VS Code/JetBrains)
2. Add this repository as a context provider in `.continue/config.json`:
```json
{
  "contextProviders": [
    {
      "name": "dora-skills",
      "type": "folder",
      "path": "path/to/dora-skills/skills"
    }
  ]
}
```

**GitHub Copilot Chat:**
1. Clone this repository alongside your project
2. Use `@workspace` to include skills context
3. Reference specific skill files when asking questions

**Aider:**
1. Install Aider: `pip install aider-chat`
2. Run Aider with skills context:
```bash
aider --read skills/**/*.md
```

**Direct API Integration:**
- Include the relevant `SKILL.md` files as context in your API calls
- The skills are structured as Markdown documentation that any LLM can understand

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

### Claude Code 入门指南

本技能包旨在与 [Claude Code](https://claude.ai/code) 无缝配合，用于 AI 驱动的机器人开发。

#### 使用 Claude Code

1. **安装 Claude Code**（如果尚未安装）:
```bash
npm install -g @anthropic-ai/claude-code
```

2. **克隆本仓库**到 Claude Code 技能目录:
```bash
# 克隆到默认技能位置
git clone https://github.com/dora-rs/dora-skills.git ~/.claude-code/skills/dora-skills
```

3. **在对话中开始使用技能**:
```bash
# 导航到你的 dora 项目
cd my-robot-project

# 启动 Claude Code
claude-code
```

4. **自然语言命令** - 当你询问以下内容时，Claude 会自动使用这些技能：
   - 创建数据流管道
   - 添加视觉、音频或机器人控制节点
   - 实现自定义节点
   - 设置数据录制/回放
   - 集成 ML 模型（YOLO、SAM2、VLM）

**示例提示词:**
- "创建一个带摄像头的目标检测数据流"
- "给我的机器人添加语音识别功能"
- "帮我实现一个用于传感器处理的自定义节点"
- "设置用于训练的数据录制管道"

#### 替代方案：使用其他 AI 工具

**Cursor IDE:**
1. 从 [cursor.sh](https://cursor.sh) 安装 Cursor IDE
2. 将本仓库克隆到你的项目中
3. 在提示词中使用 `@dora-skills` 引用这些技能

**Continue.dev:**
1. 在你的 IDE（VS Code/JetBrains）中安装 Continue
2. 在 `.continue/config.json` 中将本仓库添加为上下文提供者：
```json
{
  "contextProviders": [
    {
      "name": "dora-skills",
      "type": "folder",
      "path": "path/to/dora-skills/skills"
    }
  ]
}
```

**GitHub Copilot Chat:**
1. 将本仓库克隆到你的项目旁边
2. 使用 `@workspace` 包含技能上下文
3. 在提问时引用特定的技能文件

**Aider:**
1. 安装 Aider: `pip install aider-chat`
2. 使用技能上下文运行 Aider:
```bash
aider --read skills/**/*.md
```

**直接 API 集成:**
- 在 API 调用中包含相关的 `SKILL.md` 文件作为上下文
- 这些技能以 Markdown 文档形式组织，任何 LLM 都可以理解

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
