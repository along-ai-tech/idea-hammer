# 流程：自驱整个 Phase

> 用户要把整个 Phase 交给 /goal 自驱执行时使用。

## 何时用

- 用户说"把整个 Phase 交给自驱执行"
- 用 goal-creator 生成 /goal 指令
- 完成条件 = 四步走验收

## /goal 指令内容

```
目标：完成 Phase N（来自 DEV-PLAN.md）
完成条件（四步走）：
1. 交付清单逐项贴出（DEV-PLAN.md 当前 Phase 章节）
2. tsc --noEmit 零错误输出已贴
3. code-reviewer 两阶段 PASS 已贴（spawn code-reviewer）
4. 所有 Task 已按 RED/GREEN/REFACTOR + review→fix 循环完成
5. Phase 总结报告：完成的功能 + 测试统计 + 任何偏差
```

## 注意事项

- 自驱期间用户可中断并接管
- 每个 Task commit 后建议回用户一次（汇报进度）
- 遇阻塞立即停，回用户问怎么办，不要闷头硬做
- 自驱结束必跑四步走（参考 workflow-phase-verify.md）
