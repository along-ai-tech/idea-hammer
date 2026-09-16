# contracts/ — 输入输出契约

> 用 JSON Schema 描述 skill 的输入 / 输出，让行为可被机器校验。

## 命名规则

- 文件名格式：`<role>.schema.json`
- `<role>`：input / output / state / config 等
- 例：`input.schema.json`（输入契约）/ `output.schema.json`（输出契约）

## 文件结构

每个 schema 文件至少包含：

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "<SkillName><Role>",
  "type": "object",
  "required": ["必填字段"],
  "properties": {
    "字段名": {
      "type": "string|integer|boolean|object|array",
      "description": "字段说明"
    }
  },
  "additionalProperties": false
}
```

## 校验

- 文件本身必须是合法 JSON（`jq empty file` 通过）
- 至少包含 `$schema` 和 `type`
- `required` 字段在 `properties` 里都有定义

## 使用方式

- Skill 执行时读对应 schema
- 生成产出物后用 `jq` 或 `jsonschema` 工具校验
- 校验脚本：`bash scripts/check_skill_structure.sh` 会校验本目录所有 `*.json` 合法性

## 工具依赖

- `jq` — JSON 合法性校验
- `jsonschema` (Python) — 完整 JSON Schema 校验（可选，未来 TODO-005 用）
