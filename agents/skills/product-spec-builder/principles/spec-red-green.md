---
name: spec-red-green
description: 当改任何 principle / 模板 / SKILL.md 前，先用反例证明现有 spec 覆盖不到。给 spec 自身的 RED-GREEN 纪律。
---

# 原则：Spec 自身 RED-GREEN

> 改 spec 之前先跑反例，证明新 spec 真的更好。"我觉得这样改更对" 不算证据。

[定位]
    这是 spec 元纪律——改 spec 之前要先有一条**反例**（bad case）证明现行 spec 在那个用例下覆盖不到。
    借鉴 superpowers writing-skills：Writing skills IS Test-Driven Development applied to process documentation。

[反例来源]
    - 真实访谈失败案例（用户说 X 主 Agent 接受了 Y）
    - code-review 发现的"spec 写了但下游漏读"
    - 跨产品测试（同一份 spec 在 A 项目缺什么、在 B 项目暴露什么）
    - 自进化 signals 里的 spec 类抱怨

[RED 记录模板]

    ```
    RED-{{YYYY-MM-DD}}-{{N}}
    反例来源: {{访谈失败 / code-review / 跨产品 / signals}}
    现行 spec: {{引用 spec 节编号}}
    反例内容: {{具体例子，用户说了什么 / 下游漏了什么}}
    暴露的缺口: {{现行 spec 哪一节没说 / 哪一条规则缺}}
    ```

[GREEN：写新规则 / 改 spec]
    1. 跑反例验证现行 spec 真覆盖不到（不要凭感觉改）
    2. 写最小改动（不为了"顺手改进"夹带其他规则）
    3. 验证反例在新 spec 下被覆盖
    4. 记录到 CHANGELOG.md

[REFACTOR：封堵类似漏洞]
    - 找同源漏洞（同一类失败模式 3+ 次出现）
    - 把单条规则升级为通用原则
    - 更新 principle 文件，不只改模板

[纪律]
    - 反例必须是**真实发生过**的，不是假设
    - "我觉得这样改更好" 不算反例
    - 改 spec 后必须更新 CHANGELOG.md
    - 反例记录放在 `.idea-hammer/spec-red-green/` 目录（如不存在则建）