# dora-skills

[English](#english) | [中文](#chinese)

---

<a name="english"></a>
## English

Skills for building AI agents, workflows, and embodied intelligence with the [dora-rs](https://github.com/dora-rs/dora) dataflow framework.

**Focus**: Embodied Intelligence — combining perception, language models, and physical control.

### Quick Start

```bash
# Install dora CLI
pip install dora-rs

# Create a project
dora new my-robot --lang python

# Run a dataflow
dora run dataflow.yml
```

### Commands

| Command | Description | Documentation |
|---------|-------------|---------------|
| `/new-dataflow` | Create a new dataflow project | [docs](commands/new-dataflow/COMMAND.md) |
| `/add-node` | Add a node to existing dataflow | [docs](commands/add-node/COMMAND.md) |
| `/build` | Build and install dependencies | [docs](commands/build/COMMAND.md) |
| `/run` | Run dataflow in foreground | [docs](commands/run/COMMAND.md) |
| `/start` | Start dataflow in daemon mode | [docs](commands/start/COMMAND.md) |
| `/stop` | Stop running dataflow | [docs](commands/stop/COMMAND.md) |
| `/list` | List running dataflows | [docs](commands/list/COMMAND.md) |
| `/visualize` | Generate dataflow visualization | [docs](commands/visualize/COMMAND.md) |

### Available Skills

| Category | Skills |
|----------|--------|
| Core | `core-development`, `custom-node`, `cli-workflow` |
| Vision | `object-detection`, `segmentation`, `tracking`, `vlm` |
| Audio | `speech-to-text`, `text-to-speech`, `voice-activity` |
| Robot | `arm-control`, `actuators`, `chassis` |
| Data | `recording`, `replay`, `lerobot` |

### Using with Claude Code

```bash
# Clone to skills directory
git clone https://github.com/dora-rs/dora-skills.git ~/.claude-code/skills/dora-skills

# Start Claude Code in your project
cd my-robot-project
claude-code
```

Claude will automatically use these skills when you ask about dataflow pipelines, vision/audio nodes, or robot control.

### Using with Other AI Tools

Works with Cursor IDE, Continue.dev, GitHub Copilot, Aider, or any LLM via direct API integration. Reference the `SKILL.md` files as context.

### Resources

- [Dora Documentation](https://dora-rs.ai)
- [Dora GitHub](https://github.com/dora-rs/dora)
- [Node Hub](https://github.com/dora-rs/dora/tree/main/node-hub)

---

<a name="chinese"></a>
## 中文

使用 [dora-rs](https://github.com/dora-rs/dora) 数据流框架构建 AI Agent、工作流和具身智能应用的技能集。

**重点**: 具身智能 —— 融合感知、语言模型与物理控制。

### 快速开始

```bash
# 安装 dora CLI
pip install dora-rs

# 创建项目
dora new my-robot --lang python

# 运行数据流
dora run dataflow.yml
```

### 命令

| 命令 | 说明 | 文档 |
|------|------|------|
| `/new-dataflow` | 创建新的数据流项目 | [文档](commands/new-dataflow/COMMAND.md) |
| `/add-node` | 向现有数据流添加节点 | [文档](commands/add-node/COMMAND.md) |
| `/build` | 构建和安装依赖 | [文档](commands/build/COMMAND.md) |
| `/run` | 前台运行数据流 | [文档](commands/run/COMMAND.md) |
| `/start` | 后台守护模式启动数据流 | [文档](commands/start/COMMAND.md) |
| `/stop` | 停止运行中的数据流 | [文档](commands/stop/COMMAND.md) |
| `/list` | 列出运行中的数据流 | [文档](commands/list/COMMAND.md) |
| `/visualize` | 生成数据流可视化图 | [文档](commands/visualize/COMMAND.md) |

### 可用技能

| 类别 | 技能 |
|------|------|
| 核心 | `core-development`, `custom-node`, `cli-workflow` |
| 视觉 | `object-detection`, `segmentation`, `tracking`, `vlm` |
| 音频 | `speech-to-text`, `text-to-speech`, `voice-activity` |
| 机器人 | `arm-control`, `actuators`, `chassis` |
| 数据 | `recording`, `replay`, `lerobot` |

### 使用 Claude Code

```bash
# 克隆到技能目录
git clone https://github.com/dora-rs/dora-skills.git ~/.claude-code/skills/dora-skills

# 在项目中启动 Claude Code
cd my-robot-project
claude-code
```

当你询问数据流管道、视觉/音频节点或机器人控制时，Claude 会自动使用这些技能。

### 使用其他 AI 工具

支持 Cursor IDE、Continue.dev、GitHub Copilot、Aider 或通过直接 API 集成使用任何 LLM。引用 `SKILL.md` 文件作为上下文即可。

### 资源

- [Dora 文档](https://dora-rs.ai)
- [Dora GitHub](https://github.com/dora-rs/dora)
- [节点仓库](https://github.com/dora-rs/dora/tree/main/node-hub)

---

## License

Apache-2.0
