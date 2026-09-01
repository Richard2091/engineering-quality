# 工程质量

`engineering-quality` 是一个面向 Codex 的通用工程化 Skill，用于在开发实施阶段主动遵循工程规范，也支持对已有项目进行工程化审查、整改、验证和交付。

## 能力范围

- 前端、后端、全栈项目
- 数据处理、机器学习和模型服务
- 软件库、命令行工具和开发工具包
- 基础设施即代码、容器、持续集成和部署
- 项目画像、实施计划、质量门禁、审查报告和整改闭环
- 模块划分、文件拆分、目录规模、接口契约、测试、安全、可观测性、发布和恢复

## 设计原则

1. 以项目目标、规模、风险和生命周期决定规则，不机械强制技术选型。
2. 开发实施时主动加载适用规范；已有项目审查时默认只读并提供证据化结论。
3. 每项重要判断都应关联代码、配置、测试、运行结果或文档证据。
4. 大文件和目录规模是维护信号，拆分应服务于职责边界、测试难度和协作效率。
5. 修改、提交、推送和生产操作分别遵循明确授权边界。

## 目录说明

- `SKILL.md`：Skill 入口、模式路由和核心流程
- `references/baseline/`：通用工程基线
- `references/project-types/`：按项目类型加载的规则
- `references/workflows/`：实施、审查和整改工作流
- `references/templates/`：项目画像、实施计划、审查报告、整改、发布门禁和变更总结模板
- `scripts/`：Skill 自身结构校验脚本
- `tests/`：独立前向测试场景和行为不变量
- `references/roadmap.md`：后续增强方向

## 使用方式

将本目录作为 Codex Skill 安装到个人 Skill 目录后，可使用 `$engineering-quality` 调用。

开发任务示例：

> 使用 `$engineering-quality` 新增一个模型监控功能，在实施过程中遵循工程化规范，并输出变更总结、测试结果和剩余风险。

已有项目审查示例：

> 使用 `$engineering-quality` 审查当前项目的模块划分、文件拆分、测试、部署和可观测性，默认只读并输出整改计划。

## 验证

```powershell
python -X utf8 "C:\Users\Windows\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "."
python -X utf8 "scripts\validate_structure.py" "."
```

## 许可证

本项目采用 Apache License 2.0，详见 [LICENSE](LICENSE)。