# 流程：消化信号 → 生成改动建议

## 阶段 1：加载输入

**动作**：
1. drain .codex/evolution/signals.jsonl
2. 扫 git log + git diff（近 N 个 commit）
3. 读 .codex/EVOLUTION.md 上下文

**完成**：输入就绪

## 阶段 2：消化信号

**动作**（逐条）：
1. 读信号内容
2. 抽象剥离产品专属名词
3. 判通用性（跨产品还成立吗？）
4. 判最小干预（反例 vs 长规则 vs 改现有 skill）
5. 决定：加 / 退 / 改 skill / 建新 skill

**完成**：每条信号有归类

## 阶段 3：扫现有规则

**动作**：
1. 读 AGENTS.md / 各 SKILL.md / 各 hook
2. 找：已内化（人不会犯）/ 不触发（条件太死）/ 重复（多条说同一事）
3. 提议删

**完成**：双向扫描结果

## 阶段 4：生成建议

**动作**：
- 写进 .codex/evolution/proposals.md 的 ## 待审阅 区
- 每条一行 - 开头
- 字段：依据信号 / 归类（加 / 退 / 改 / 建新）/ 落到哪个文件 / 改动摘要
- 落点按规则管什么走（AGENTS.md / SKILL.md / hook），不堆给某一个文件
- 消费掉的 signal 从 signals.jsonl 移走

**完成**：proposals.md 就绪

## 阶段 5：等用户确认

**注意**：
- evolution-runner 只消化和提议
- 主 Agent 在 session 启动时同步消化、逐条问用户
- 按回应落地：
  - 同意：改对应文件，建新 Skill 调 skill-builder
  - 全盘否定：signal + proposal 一起删
  - 一半一半：按用户认可的部分改，其余删
- 落地后从 proposals.md 移走

## 失败处理

- 信号抽象后仍产品专属 → 归用户记忆，不立规则
- 多个信号说的是同一事 → 合并为一条
- 改现有 skill 比新建更合理 → 提议改现有
