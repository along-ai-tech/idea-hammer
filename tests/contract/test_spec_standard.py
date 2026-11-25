"""契约测试：scripts/check_spec_standard.py 的 Phase 0 硬门禁行为。"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / "scripts" / "check_spec_standard.py"

VALID_SPEC = """# Product Spec

## 1. PRD：产品背景与用户

### 1.1 产品背景与目标

- **背景**：作者需要自持内容资产

### 1.2 用户角色与画像

| 用户类型 | 画像 | 核心需求 |
|---|---|---|
| 作者 | 工程师，长期写作 | 发布文章 |

### 1.3 用户核心问题

静态方案无评论与后台。

### 1.4 核心价值

发布到收到反馈从两天缩短到五分钟。

### 1.6 业务指标

| 指标 | 定义 | 目标 | 观察信号 |
|---|---|---|---|
| 发布闭环 | 全链路通过率 | 100% | 任一端点失败即不达标 |

## 2. 功能范围（PRD）

### 2.1 本版本范围

| 编号 | 内容 | 优先级 | 备注 |
|---|---|---|---|
| SCOPE-001 | 发布文章 | P0 | 核心 |

### 2.2 不在本版本范围

| 编号 | 内容 | 原因 |
|---|---|---|
| OUT-001 | 多用户 | 单作者自用 |

## 3. 核心业务流程（PRD）

### 3.1 用户任务（TASK）

| 编号 | 用户任务 | 用户类型 | 优先级 |
|---|---|---|---|
| TASK-001 | 发布文章 | 作者 | P0 |

### FLOW-001: 发布

作者填写标题与正文并提交。

## 4. 产品优先级（PRD）

| 编号 | 内容 | 类型 | 优先级 | 理由 |
|---|---|---|---|---|
| REQ-001 | 发布 | 功能 | P0 | 不能少 |

## 5. FRD：功能需求（REQ）

### REQ-001: 发布文章

**优先级：** P0
**关联任务：** TASK-001

**用户故事（User Story）：**

- **作为一个** 作者，
- **我希望** 发布文章，
- **以便于** 沉淀长期资产。

**目标：**
- **是什么**：发布文章

**行为：** 作者提交后入库并返回文章。

**规则：**
- MUST title 非空

**输入：**

| 字段 | 类型 | 必填 | 校验规则 |
|---|---|---:|---|
| title | string | Yes | 非空 |

**输出 / 结果：**
- 201 + 文章 id

**状态：** 无状态切换

**验收标准：**
- [ ] AC-001-01: Given 合法标题, when 提交, then 返回 201。
- [ ] AC-001-02: Given 空标题, when 提交, then 返回 422。
- [ ] AC-001-03: Given 超长标题, when 提交, then 返回 422。
"""


def run_check(tmp_path: Path, text: str) -> subprocess.CompletedProcess:
    spec = tmp_path / "Product-Spec.md"
    spec.write_text(text, encoding="utf-8")
    return subprocess.run(
        [sys.executable, str(SCRIPT), "--file", str(spec)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )


def test_example_project_passes():
    """examples/personal-blog 应符合四要素标准"""
    result = subprocess.run(
        [sys.executable, str(SCRIPT), "--project", "examples/personal-blog"],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout


def test_valid_spec_passes(tmp_path):
    result = run_check(tmp_path, VALID_SPEC)
    assert result.returncode == 0, result.stdout


def test_missing_user_story_fails(tmp_path):
    bad = VALID_SPEC.replace(
        """**用户故事（User Story）：**

- **作为一个** 作者，
- **我希望** 发布文章，
- **以便于** 沉淀长期资产。
""",
        "",
    )
    result = run_check(tmp_path, bad)
    assert result.returncode == 1
    assert "[US]" in result.stdout


def test_insufficient_ac_fails(tmp_path):
    bad = VALID_SPEC.replace(
        "- [ ] AC-001-02: Given 空标题, when 提交, then 返回 422。\n"
        "- [ ] AC-001-03: Given 超长标题, when 提交, then 返回 422。\n",
        "",
    )
    result = run_check(tmp_path, bad)
    assert result.returncode == 1
    assert "至少需要 3 条 AC" in result.stdout


def test_mismatched_ac_id_fails(tmp_path):
    bad = VALID_SPEC.replace("AC-001-02", "AC-002-02")
    result = run_check(tmp_path, bad)
    assert result.returncode == 1
    assert "编号与所属 REQ-001 不一致" in result.stdout
