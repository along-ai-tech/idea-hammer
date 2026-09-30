# Product Spec — Personal Blog（个人博客 MVP）

> 按 IdeaHammer 8 步流水线 **product-spec-builder** 产出
> 锚定 demo：`examples/personal-blog/`（按方法论从零到一真跑，非后补演示）

---

## 0. Phase 0 商业可行性 5 问快筛（business-context-check）

| # | 问 | 答 | 通过？ |
|---|----|----|-------|
| 1 | **凭什么你活**（vs Hexo/Hugo/Halo/WordPress/Notion/掘金） | 个人博客赛道极度饱和。差异化 = **"演示 IdeaHammer 方法论的活工程"**（简历项目）+ 完全可控 / 一键部署 / 评论无需第三方。**不靠功能强，靠作品集价值** | ✅ |
| 2 | **付费动机** | **自我展示型博客**，非商业产品。无付费场景 → 跳过商业化深问。明确文档化"非商业、纯展示、价值在作品集" | ✅（显式标注） |
| 3 | **1 年后死在哪个原因** | (a) 懒得写 → 博客空；(b) 评论 spam → 关评论；(c) 迁移成本 → 锁死。**缓解：MVP 6 endpoint，spam 防护留 Phase 2** | ✅ |
| 4 | **是否可发布** | MVP = 发布 + 列表 + 详情 + 评论 + 点赞 + 点踩 + 置顶（**7 个端点**）。复用 FastAPI + Vue 栈。预计 30-60 分钟跑完 TDD → commit | ✅ |
| 5 | **用户量门槛** | 单用户 / 自用 / 演示。**门槛 = 0** | ✅ |

→ **Phase 0 通过**，进 Phase 1。

---

## 1. Phase 1 核心功能 + persona + job

### 1.1 Persona

**wuzhilong** — 3 年后端工程师转型 AI Native 方向，2026.07 离职红杏林研发团，准备 2026 长沙 AI Coding / 后端岗面试。

### 1.2 核心 Job

> 创建一个可即时发布 / 维护 / 与访客互动的个人博客，
> 用作**简历配套的活工程展示**（不是营销页），让面试官能在 3 分钟内看到
> "这个人真把 AI Coding 落地了"。

### 1.3 关键场景（按优先级）

| 场景 | 谁 | 做什么 |
|------|----|------|
| **写博客** | wuzhilong（作者） | Markdown 编辑 → 保存草稿 → 发布 → 可置顶 |
| **浏览列表** | 访客 | 看博客列表（分页 / 置顶置顶优先） |
| **读详情** | 访客 | 看单篇博客（含评论 + 点赞数） |
| **评论** | 访客 | 写评论（nickname + content）→ 立刻显示（无审核流，v1 加 spam 防护） |
| **点赞/点踩** | 访客 | 点按钮 → 计数 +1，按 IP 防重复 |
| **管理** | wuzhilong | 编辑 / 删除博客 / 设置置顶 / 隐藏评论 |

---

## 1.5. Phase 1.5 竞品扫描（competitive-scan，联网搜索 2026.04）

按 IdeaHammer P1 业务纪律：≥ 2 直接竞品 + ≥ 2 替代方案，每行必填"我们凭什么"。

### 1.5.1 直接竞品（同类博客系统）

| 竞品 | 类型 | 关键特征 | 缺点 / 我们凭什么 |
|------|----|---------|-----------------|
| **Hexo / Hugo / Astro / VuePress** | 静态博客生成器 | 一行命令部署、托管免费、性能极佳 | 无评论（要接入第三方 Gitalk/Disqus）、无点赞、无后台管理、不支持动态评论计数。**我们的优势：动态评论 + 点赞点踩 + 后台管理一体化** |
| **Halo 2.x** | 国产动态博客（Java + Vue3 + Spring Boot） | Docker 一键部署、200+ 插件、社区活跃 | 200+ 插件 = 学习曲线陡；Java 栈重；后台 UI 复杂。**我们的优势：纯 Python 全栈轻量（FastAPI + Vue3）、代码 < 500 行可读完、IdeaHammer 演示价值** |
| **WordPress** | 老牌 PHP 博客 | 生态最大、插件最多 | PHP / 运维重、SEO 优化强迫症、安全补丁频繁。**我们的优势：FastAPI 现代化栈、SQLite 零运维、3 分钟跑通** |
| **Typecho / Z-Blog** | 轻量 PHP 博客 | 小巧 | PHP 老生态，无 AI Coding 演示价值。**我们的优势：栈现代化，方法论可演练** |

### 1.5.2 替代方案（不是博客系统，但是用户写内容的方式）

| 替代 | 是什么 | 为什么不用 / 我们凭什么 |
|------|------|----------------------|
| **Notion + Super.so** | Notion 当后端，前端套壳 | 评论弱、SEO 差、内容锁 Notion、迁移困难。**我们的优势：自己后端、可导出 Markdown、纯自有** |
| **掘金 / 知乎 / CSDN / 公众号** | 平台发布 | 内容被平台绑定、不能自定义域名、审核/封号风险。**我们的优势：自有域名 + 数据 + 完全可控** |
| **GitHub Issues / Gist + Pages** | 极客方案 | 评论 = issues，技术门槛高，非技术读者看不懂。**我们的优势：原生评论，零技术门槛** |

### 1.5.3 关键差异化（来自竞品 → 我们）

1. **"作品集价值"**：不是比功能强，是**让面试官 3 分钟看到 IdeaHammer 方法论真跑过**
2. **栈现代化**：FastAPI + Vue3 + Element Plus + SQLite，全 Python 栈，面试官 1 分钟能 clone 跑通
3. **代码量极小**：MVP 7 端点 + 6 模型 + 1 service 算法 < 800 行
4. **真实 commit 链**：每个端点 = 1 commit + 1 测试，PR 描述 + Review 报告全留底

---

## 2. Phase 2 范围定义

### 2.1 用户故事

> 作为 **wuzhilong（3 年后端工程师转型 AI Native）**
> 我想要 **快速发布一篇技术博客，设置置顶，接收访客评论和点赞反馈**
> 以便 **把博客作为简历配套的活工程，给面试官 3 分钟可验证的 AI Coding 作品集**

### 2.2 功能列表（7 个核心 endpoint）

| ID | 端点 | 功能 | 验收（=测试场景） |
|----|------|-----|----------------|
| F-2.1 | `POST /api/posts` | 发布博客 | 给定 `{title, content, is_pinned: false}`；应：201 返回 `{id, slug, ...}`；title 必填 |
| F-2.2 | `GET /api/posts` | 列表（分页 + 置顶优先） | 给定 5 篇博客，1 篇置顶；当 GET ?limit=10；应：返回 5 篇，置顶在第一位 |
| F-2.3 | `GET /api/posts/{id_or_slug}` | 详情 | 给定已发布博客 id=1；应：返回完整 content + 评论数 + 点赞数 |
| F-2.4 | `PUT /api/posts/{id}` | 编辑 | 修改 title → 200，新 title 生效；update_at 刷新 |
| F-2.5 | `DELETE /api/posts/{id}` | 删除 | 应：204；之后 GET 404 |
| F-2.6 | `POST /api/posts/{id}/comments` | 写评论 | 给定 `{nickname, content}`；应：201；content 空 → 422 |
| F-2.7 | `POST /api/posts/{id}/react` | 点赞 / 点踩 | 给定 `{type: "up"\|"down"}`；应：计数 +1；同 IP 重复点赞 → 计数不变（v1 简化） |
| F-2.8 | `PATCH /api/posts/{id}/pin` | 设置/取消置顶 | 应：200，is_pinned 翻转 |
| F-2.9 | `DELETE /api/comments/{id}` | 删除评论（管理） | 应：204；评论消失 |

### 2.3 范围之外（v0 不做）

- 用户登录 / 注册（v1：加 JWT 简单 token）
- Markdown 渲染（v1：前端 markdown-it；v0 后端存原文）
- 评论审核 / spam 防护（v1）
- 标签 / 分类 / 搜索（v1）
- SEO / RSS / sitemap（v1）
- 邮件通知（永远不做）
- 多用户 / 权限分级（永远不做，自用单作者）

### 2.4 非功能需求

| 维度 | 要求 |
|------|------|
| 性能 | 单用户场景，无 SLA；列表查询 P99 < 100ms（100 篇博客内） |
| 可用性 | 单进程，无高可用 |
| 安全 | 评论 nickname + content 用 Pydantic 校验防 SQL 注入 / XSS（v0 内容不渲染 HTML） |
| 数据迁移 | 新建空 DB；不涉及已有数据迁移 |
| 版本化 | 评论无版本化（v0）；博客编辑用 UPDATE 覆盖（单作者自用，非业务数据） |

---

## 3. Phase 3.5 pre-mortem（1 年后死因 + 监控信号）

| 1 年后死因 | 监控信号 | 缓解 |
|-----------|---------|-----|
| **1. 评论被 spam 灌满** | 24h 内 > 100 条相同关键字评论 | v1 加 IP 频次限制 + 关键字黑名单 |
| **2. SQLite 单文件变大性能崩** | 单文件 > 1GB | v1 迁移 PostgreSQL |
| **3. Markdown 渲染被 XSS 攻击** | 评论里出现 `<script>` 渲染 | v1 渲染前 sanitize（DOMPurify 或 bleach） |
| **4. 没有备份，硬盘挂了博客全没了** | 1 个月没备份 | 加 crontab 每周 sqlite3 dump |

---

## 4. 收尾多视角自检

### CEO 视角：方向对吗

- ✅ 这是真问题：开发者都要博客展示作品集
- ✅ MVP 范围合理（7 端点不多不少）
- ✅ 不与 Hexo/Halo 抢功能市场（避开红海）
- ✅ 方法论演示价值 > 产品功能价值（**这是核心定位**）

### 工程视角：能实现吗

- ✅ FastAPI + SQLAlchemy + Pydantic 已熟
- ✅ 4 张表（posts / comments / reactions / sessions）ORM 模型简单
- ✅ 评论 nesting 不做（v1 flat 评论）
- ⚠️ 点赞防刷：v0 用 IP+post_id 唯一索引；v1 加 user agent fingerprint

### QA 视角：能测吗

- ✅ 9 个端点 = 9 个测试文件
- ✅ 边界：空 title / 空 content / 不存在 id / 重复点赞
- ✅ TDD：每个端点先 RED 再 GREEN
- ✅ 集成：TestClient + in-memory SQLite

---

## 5. 验收总表（Spec → 实现可追溯）

| Spec 条目 | 实现位置（计划） | 测试位置（计划） |
|----------|----------------|----------------|
| F-2.1 ~ F-2.5 博客 CRUD | `app/api/posts.py` | `tests/test_posts.py` |
| F-2.6 评论 | `app/api/comments.py` | `tests/test_comments.py` |
| F-2.7 点赞 / 点踩 | `app/api/reactions.py` | `tests/test_reactions.py` |
| F-2.8 置顶 | `app/api/posts.py::patch_pin` | `tests/test_posts.py::test_pin` |
| F-2.9 删除评论 | `app/api/comments.py::delete` | `tests/test_comments.py::test_delete` |

---

## 6. 技术栈选型

| 层 | 选型 | 理由 |
|----|------|------|
| 后端 | Python 3.11 + FastAPI + SQLAlchemy 2.0 + SQLite + Pydantic v2 | 复用 flashcards 同栈，零依赖新增 |
| 测试 | pytest + TestClient + in-memory SQLite fixture | 复用 |
| 前端 | Vue 3.5 + Element Plus 2.8 + Vite 5 + Pinia + Vue Router | 复用 |
| 包管理 | uv / pnpm | 复用 |
| Markdown（v1） | markdown-it + DOMPurify | v1 引入 |

---

<!-- owner: product -->