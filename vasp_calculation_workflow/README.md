# {{crew_name}} Crew

Welcome to the {{crew_name}} Crew project, powered by [crewAI](https://crewai.com). This template is designed to help you set up a multi-agent AI system with ease, leveraging the powerful and flexible framework provided by crewAI. Our goal is to enable your agents to collaborate effectively on complex tasks, maximizing their collective intelligence and capabilities.

## 安装

确保你的linux系统上安装了 Python >=3.10 <3.13 版本。本项目使用 [UV](https://docs.astral.sh/uv/) 进行依赖项管理和包处理，提供无缝的安装和执行体验。

首先，如果您还没有安装 uv，请安装

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh              #linux
```

接下来，导航到您的项目目录并安装依赖项：

（可选）锁定依赖项并使用 CLI 命令安装它们：
```bash
crewai install
```

开发时，如果有其他要安装的软件包，可以通过运行以下命令来实现：
```bash
uv add <package-name>
```

### 环境变量设置

**若有需要，将您的 `ACCESS_KEY` 添加到 `.env` 文件中，这样能在borium上看到计算执行情况。不修改`ACCESS_KEY`，针对生成的文件调试也行。遇到计算任务提交失败问题请查看[bohrium命令行工具安装](https://bohrium-doc.dp.tech/docs/bohrctl/install/)**



- 开发指南：[crewai文档](https://docs.crewai.com/introduction)
- 修改 'src/vasp_calculation_workflow/config/agents.yaml' 以定义您的代理
- 修改 'src/vasp_calculation_workflow/config/tasks.yaml' 来定义你的任务
- 修改 'src/vasp_calculation_workflow/crew.py' 以添加您自己的逻辑、工具和特定参数
- 修改 'src/vasp_calculation_workflow/main.py' 以为您的代理和任务添加自定义输入

## 运行项目

要启动流程并开始执行，请从项目的根文件夹运行以下命令：

```bash
crewai flow kickoff
```

此命令将按照配置中的定义初始化 vasp_calculation_workflow Flow。


## Understanding Your Crew

VASP 计算工作流程团队由多个 AI 代理组成，每个代理具有独特的角色、目标和工具。这些代理在`config/tasks.yaml`中定义的一系列任务上进行协作，利用他们的集体技能实现复杂目标。`config/agents.yaml`文件概述了您团队中每个代理的能力和配置。



## Support

For support, questions, or feedback regarding the {{crew_name}} Crew or crewAI.

- Visit our [documentation](https://docs.crewai.com)
- Reach out to us through our [GitHub repository](https://github.com/joaomdmoura/crewai)
- [Join our Discord](https://discord.com/invite/X4JWnZnxPb)
- [Chat with our docs](https://chatg.pt/DWjSBZn)

Let's create wonders together with the power and simplicity of crewAI.
