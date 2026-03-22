# CLI 命令速查

本文件提供了 OpenSpec 原生命令行工具的常用操作备忘。

当需要底层管理时，可执行以下原生命令（按生命周期排序）：

- **安装**：`npm install -g @fission-ai/openspec@latest`
- **初始化**：`openspec init [path]` - 初始化项目。
- **更新指令**：`openspec update [path]` - 更新 OpenSpec AI 协作指令文件。
- **创建变更**：`openspec new change <name>` - 创建新的变更提案。
- **验证规格**：`openspec validate [item-name]` - 验证变更和规范文档的格式。
- **查看状态**：`openspec status` - 显示变更产物的完成状态。
- **显示详情**：`openspec show [item-name]` - 显示变更或规范的详细信息。
- **列表查询**：`openspec list` - 默认列出所有变更（使用 `--specs` 列出规范）。
- **交互大盘**：`openspec view` - 打开交互式仪表盘查看规范和变更。
- **归档变更**：`openspec archive [change-name]` - 归档已完成的变更并合并到主规格。
- **获取指令**：`openspec instructions [artifact]` - 输出用于创建产物或应用任务的增强指令。
- **配置管理**：`openspec config` - 查看和修改全局配置。
