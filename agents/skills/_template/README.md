# Skill 三层结构模板

> 把一个 skill 从单文件 markdown 拆成"行为契约"，让规则单点定义、行为可断言。

## 适用对象

为 IdeaHammer 框架创建或重构 skill 时使用本模板。

## 三层结构

```
skill-name/
├── SKILL.md                # 入口文件（≤ 50 行，仅 frontmatter + 引用列表）
├── principles/             # 第一性原则（可被多 skill 引用）
│   └── *.md
├── workflows/              # 执行流程（步骤化、含完成标准）
│   └── *.md
├── contracts/              # 输入输出 schema（机器可解析）
│   └── *.schema.json
└── assets/                 # 静态资源（图片、模板文件、参考代码等）
    └── *
```

## 各层职责

| 层 | 职责 | 写作规则 |
|---|------|---------|
| **SKILL.md** | 入口；声明何时用、依赖什么、引用哪个文件 | ≤ 50 行；只引用不展开 |
| **principles/** | 不变量、价值取向、跨 skill 共享 | 一原则一文件；可被多个 skill 引用 |
| **workflows/** | 阶段化执行步骤 + 完成标准 | 每步写目标 / 动作 / 完成；失败处理明确 |
| **contracts/** | 输入输出 JSON Schema | 机器可解析；用 `*.schema.json` 命名 |
| **assets/** | 静态资源（图、参考代码、prompt 模板） | 不参与校验；按需提供 |

## 创建新 skill

1. 复制本目录为 `agents/skills/<new-skill>/`
2. 改 SKILL.md 的 `name` 和 `description`
3. 按需填 principles/ workflows/ contracts/ assets/
4. 跑 `bash scripts/check_skill_structure.sh` 验证
5. 在 AGENTS.md 的 Skill 列表里加上

## 重构现有 skill

1. 把 SKILL.md 里"超过 30 行"的章节拆出去
2. 章节若是"为什么这样做" → principles/
3. 章节若是"步骤怎么走" → workflows/
4. 章节若是"输入输出约定" → contracts/
5. SKILL.md 只留 frontmatter + 引用列表
6. 跑 check_skill_structure.sh 验证 ≤ 50 行
