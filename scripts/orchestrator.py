#!/usr/bin/env python3
"""
orchestrator.py — IdeaHammer 路由图编排器

按路由图定义执行 skill 调用，支持：
- 拓扑排序
- 条件路由（基于 state 表达式）
- 并发节点（parallel）
- spike 探查（不更新 state）
- 终止判定
- dry-run 模式（不实际调 skill，只走图）

用法：
  python3 scripts/orchestrator.py run --graph <route-graph.json> --state <state.json> [--dry-run]
  python3 scripts/orchestrator.py validate --graph <route-graph.json>
  python3 scripts/orchestrator.py plan --graph <route-graph.json>  # 打印执行计划
"""

import argparse
import json
import sys
from collections import defaultdict, deque
from pathlib import Path


def load_graph(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _validate_nodes_exist(graph):
    """校验所有节点和 entry 存在，edge from/to 都引用存在的节点。"""
    errors = []
    node_ids = {n["id"] for n in graph.get("nodes", [])}
    if "entry" not in graph:
        errors.append("缺 entry 节点")
    elif graph["entry"] not in node_ids:
        errors.append(f"entry 节点 '{graph['entry']}' 不存在")
    for edge in graph.get("edges", []):
        if edge["from"] not in node_ids:
            errors.append(f"edge from '{edge['from']}' 不存在")
        targets = edge["to"] if isinstance(edge["to"], list) else [edge["to"]]
        for t in targets:
            if t not in node_ids:
                errors.append(f"edge to '{t}' 不存在")
    return errors


def _detect_cycle(graph):
    """检测环（loop=true 的边允许）。返回 (是否环, 错误信息)。"""
    in_degree = defaultdict(int)
    adj = defaultdict(list)
    for e in graph.get("edges", []):
        if e.get("loop"):
            continue
        targets = e["to"] if isinstance(e["to"], list) else [e["to"]]
        for t in targets:
            adj[e["from"]].append(t)
            in_degree[t] += 1
    queue = deque([n for n in adj if in_degree[n] == 0])
    visited = sum(1 for _ in queue)
    while queue:
        n = queue.popleft()
        for t in adj[n]:
            in_degree[t] -= 1
            if in_degree[t] == 0:
                queue.append(t)
                visited += 1
    return visited != len(adj), "路由图存在环"


def validate_graph(graph):
    """校验节点存在 + 检测环。"""
    errors = _validate_nodes_exist(graph)
    has_cycle, cycle_err = _detect_cycle(graph)
    if has_cycle:
        # 排除 loop=true 的边后再测一次
        loop_edges = [e for e in graph.get("edges", []) if e.get("loop")]
        if loop_edges:
            saved = graph["edges"]
            graph["edges"] = [e for e in saved if not e.get("loop")]
            still_has_cycle, _ = _detect_cycle(graph)
            graph["edges"] = saved
            if still_has_cycle:
                errors.append(f"{cycle_err}（loop 边之外的环）")
        else:
            errors.append(cycle_err)
    return errors


def topological_plan(graph):
    """返回执行计划（线性序列）。"""
    in_degree = defaultdict(int)
    adj = defaultdict(list)
    for e in graph.get("edges", []):
        targets = e["to"] if isinstance(e["to"], list) else [e["to"]]
        for t in targets:
            adj[e["from"]].append(t)
            in_degree[t] += 1

    queue = deque([graph["entry"]])
    plan = []
    visited = set()
    while queue:
        n = queue.popleft()
        if n in visited:
            continue
        visited.add(n)
        plan.append(n)
        for t in adj[n]:
            in_degree[t] -= 1
            if in_degree[t] == 0:
                queue.append(t)
    return plan


def eval_condition(expr, state):
    """评估条件表达式。state 注入到表达式命名空间。"""
    if not expr:
        return True
    try:
        # 只允许访问 state，不允许其他
        return bool(eval(expr, {"__builtins__": {}}, {"state": state}))
    except Exception as e:
        print(f"[warn] 条件评估失败 '{expr}': {e}", file=sys.stderr)
        return False


def find_next_nodes(graph, current_id, state):
    """根据条件找下一节点（多个目标按 priority 排序）。"""
    next_nodes = []
    for e in graph.get("edges", []):
        if e["from"] != current_id:
            continue
        if eval_condition(e.get("condition"), state):
            targets = e["to"] if isinstance(e["to"], list) else [e["to"]]
            for t in targets:
                next_nodes.append((t, e.get("priority", 0)))

    # 按 priority 降序
    next_nodes.sort(key=lambda x: -x[1])
    return [n for n, _ in next_nodes]


def _resolve_inputs(node, state):
    """从 state 解析节点 inputs。"""
    resolved = {}
    for key, path_str in (node.get("inputs") or {}).items():
        if path_str.startswith("state."):
            resolved[key] = state.get(path_str[len("state."):])
    return resolved


def _execute_node(node, resolved_inputs, dry_run, state):
    """执行单个节点（dry_run 只 print，实际跑模拟 outputs）。"""
    mode = node.get("mode", "default")
    tag = "dry-run" if dry_run else "run"
    print(f"[{tag}] {node['skill']} (mode={mode}) inputs={list(resolved_inputs.keys())}")
    if not dry_run and not node.get("spike"):
        for state_key in (node.get("outputs") or {}).keys():
            state[state_key] = f"<from {node['skill']}>"


def _next_step(graph, current, state):
    """决定下一步：检查 terminal / 无出边 / 下一节点。"""
    if current in graph.get("terminal", []):
        print(f"[done] 到达终止节点 {current}")
        return None
    next_nodes = find_next_nodes(graph, current, state)
    if not next_nodes:
        print(f"[done] {current} 无出边")
        return None
    if len(next_nodes) > 1 and graph["nodes"][[n["id"] for n in graph["nodes"]].index(current)].get("parallel"):
        print(f"[parallel] 下一节点: {next_nodes}")
    return next_nodes[0]


def run(graph, initial_state, dry_run=False):
    """按路由图执行 skill 调用。"""
    state = dict(initial_state)
    current = graph["entry"]
    visited = set()
    path = []

    while current:
        if current in visited:
            print(f"[error] 循环访问 {current}", file=sys.stderr)
            break
        visited.add(current)
        path.append(current)

        node = next(n for n in graph["nodes"] if n["id"] == current)
        resolved_inputs = _resolve_inputs(node, state)
        _execute_node(node, resolved_inputs, dry_run, state)
        current = _next_step(graph, current, state)

    return state, path


def cmd_run(args):
    graph = load_graph(args.graph)
    errors = validate_graph(graph)
    if errors:
        print("路由图校验失败：", errors, file=sys.stderr)
        sys.exit(1)

    if args.state:
        s = args.state
        # 如果以 { 开头或 [ 开头，当作 JSON 字符串
        if s.startswith("{") or s.startswith("["):
            state = json.loads(s)
        else:
            # 否则当作文件路径
            state = json.loads(Path(s).read_text(encoding="utf-8"))
    else:
        state = {}

    final_state, path = run(graph, state, dry_run=args.dry_run)
    print(f"\n执行路径: {' → '.join(path)}")
    print(f"\n最终 state:")
    print(json.dumps(final_state, indent=2, ensure_ascii=False))


def cmd_validate(args):
    graph = load_graph(args.graph)
    errors = validate_graph(graph)
    if errors:
        print("❌ 错误：")
        for e in errors:
            print(f"  - {e}")
        sys.exit(1)
    print(f"✓ 路由图 '{graph.get('name')}' 校验通过")


def cmd_plan(args):
    graph = load_graph(args.graph)
    errors = validate_graph(graph)
    if errors:
        print("路由图有问题：", errors, file=sys.stderr)
        sys.exit(1)
    plan = topological_plan(graph)
    print(f"路由图 '{graph.get('name')}' 执行计划：")
    for i, node_id in enumerate(plan, 1):
        node = next(n for n in graph["nodes"] if n["id"] == node_id)
        marker = "🔀" if node.get("parallel") else "🧪" if node.get("spike") else "▶"
        print(f"  {i:2d}. {marker} {node_id:20s} → {node['skill']}")


def main():
    parser = argparse.ArgumentParser(description="IdeaHammer 路由图编排器")
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_run = sub.add_parser("run", help="执行路由图")
    p_run.add_argument("--graph", required=True)
    p_run.add_argument("--state", help="初始 state JSON")
    p_run.add_argument("--dry-run", action="store_true", help="只走图不实际调 skill")
    p_run.set_defaults(func=cmd_run)

    p_val = sub.add_parser("validate", help="校验路由图")
    p_val.add_argument("--graph", required=True)
    p_val.set_defaults(func=cmd_validate)

    p_plan = sub.add_parser("plan", help="打印执行计划")
    p_plan.add_argument("--graph", required=True)
    p_plan.set_defaults(func=cmd_plan)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
