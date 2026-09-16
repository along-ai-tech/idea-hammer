# 流程：创建新 Skill

## 阶段 1：了解需求

**动作**：
1. 新 Skill 解决什么问题？
2. 何时触发？
3. 输入输出是什么？
4. 来自进化提议？读对应 proposal 了解背景

**完成**：需求清晰

## 阶段 2：选交互模式 + 找参照

**动作**：
- 对话采集 / 自主分析 / 执行操作 / 诊断修复
- 选最接近的已有 Skill 作参照

**完成**：参照确定

## 阶段 3：读模板 + 定 Section

**动作**：
1. 读 templates/skill-template.md
2. 按 principles/structure-discipline.md 选 Section
3. 列出本 Skill 需要的 Section 清单

**完成**：Section 清单

## 阶段 4：写各 Section

**动作**：
- 逐 Section 填
- [第一性原则] 最后一条是"联网优先"
- 用 principles/writing-discipline.md 校准

**完成**：SKILL.md 草稿

## 阶段 5：创建文件

**动作**：
1. 在 `agents/skills/[skill-name]/` 建 SKILL.md
2. 有模板建 templates/
3. 跑 `scripts/check_skill_structure.py` 校验

**完成**：文件落地

## 阶段 6：登记

**动作**：
- 在 AGENTS.md 补 [Skill 调用规则]、[可用技能] 和工作流程

**完成**：登记完成

## 失败处理

- 阶段 1 需求不清 → 问用户
- 阶段 2 找不到参照 → 自己设计但遵循三层结构
- 阶段 5 check 失败 → 修
