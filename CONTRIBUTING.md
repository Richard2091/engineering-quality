# 贡献指南

感谢参与 `engineering-quality` 的改进。

## 修改原则

- 先说明规则、流程或模板解决的实际工程问题。
- 保持 `SKILL.md` 简洁，详细内容放入对应参考目录。
- 新增规则时说明适用条件、证据要求和验收方式。
- 不把单一技术选型写成所有项目的强制要求。
- 修改模板、脚本或规则后，同时更新测试场景或不变量。
- 所有文本文件使用 UTF-8，文件名使用小写字母、数字和连字符。

## 提交前检查

```powershell
python -X utf8 "C:\Users\Windows\.codex\skills\.system\skill-creator\scripts\quick_validate.py" "."
python -X utf8 "scripts\validate_structure.py" "."
```

提交说明应包含变更目的、影响范围、验证结果和未验证事项。