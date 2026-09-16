---
name: release-builder
description: 当用户说要打包、部署、发布、上线，或项目开发完成准备交付时使用。支持 Web 部署、Desktop 打包、CLI 发布，内置隐私审计和冒烟测试。
---

# release-builder

[任务]
    根据项目类型执行构建、打包、测试、发布。确保发布产物能安装、能运行、无隐私泄露、无安全漏洞。

[依赖检测]
    基础：项目代码、git、构建工具、package.json。
    渠道：按用户选的发布渠道检测所需 CLI 和认证状态。只打包不发布则不检测部署工具。
    缺失工具你自己判断装法直接装，要登录认证才提示用户。

[使用方式]
    读 principles/ 必读 → 按 workflows/release.md 走 → 用 contracts/output.schema.json 校验。

[文件结构]
    release-builder/
    ├── SKILL.md             # 本文件（≤ 30 行）
    ├── principles/          # 发布纪律
    ├── workflows/           # 发布流程
    └── contracts/           # 输出 schema

[引用]
    原则：principles/release-discipline.md
    流程：workflows/release.md
    契约：contracts/output.schema.json
