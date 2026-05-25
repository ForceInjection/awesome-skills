# 目录与文件命名规范

## 通用原则

- 使用小写字母和短横线（kebab-case）命名目录和文件
- 避免使用空格、下划线或驼峰命名
- 文件名应简洁且能准确反映内容

## 目录命名

```
正确: agent-skill-reviewer/, deep-code-reader/, pptx-reader/
错误: AgentSkillReviewer/, deep_code_reader/, pptx reader/
```

## 文件命名

```
正确: architecture-design.md, api-reference.md, getting-started.md
错误: Architecture Design.md, api_reference.md, GettingStarted.md
```

## 中英文排版

- 中英文内容之间必须有空格：`使用 Python 编写`
- 中文与数字之间也须有空格：`延迟低于 50 μs`
- 专有名词遵循官方大小写：`vLLM`, `Redis`, `MySQL`
