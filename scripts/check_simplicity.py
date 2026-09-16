#!/usr/bin/env python3
# 代码简洁性自动校验 - 基于 simplification/ 10 条原则
import argparse
import ast
import re
import sys
from pathlib import Path


FILE_MAX_LINES = 300
FUNC_MAX_LINES = 50
CYCLOMATIC_MAX = 10
NESTED_MAX = 3
PARAMS_MAX = 4
IMPORTS_MAX = 30


def check_file_size(path):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return []
    lines = len(text.splitlines())
    if lines > FILE_MAX_LINES:
        return [{"rule": "file_size", "file": str(path), "message": f"文件 {lines} 行 (> {FILE_MAX_LINES})", "principle": "file-and-function-size.md"}]
    return []


def check_todo_fixme(path):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return []
    errors = []
    for i, line in enumerate(text.splitlines(), 1):
        if re.search(r"#\s*(TODO|FIXME|XXX)\b", line) or re.search(r"//\s*(TODO|FIXME|XXX)\b", line):
            errors.append({"rule": "todo_residue", "file": str(path), "line": i, "message": f"TODO/FIXME 残留: {line.strip()[:60]}", "principle": "yagni.md"})
    return errors


def _max_nesting(body, current=0):
    if not isinstance(body, list):
        body = [body]
    max_d = current
    for stmt in body:
        if isinstance(stmt, (ast.If, ast.For, ast.AsyncFor, ast.While, ast.With, ast.AsyncWith, ast.Try)):
            d = _max_nesting(stmt.body, current + 1)
            if hasattr(stmt, "orelse"):
                d = max(d, _max_nesting(stmt.orelse, current + 1))
            max_d = max(max_d, d)
        elif isinstance(stmt, ast.ExceptHandler):
            max_d = max(max_d, _max_nesting(stmt.body, current + 1))
    return max_d


def _function_lines(node, path, name):
    n = (node.end_lineno or 0) - (node.lineno or 0) + 1
    if n > FUNC_MAX_LINES:
        return [{"rule": "function_size", "file": str(path), "line": node.lineno, "name": name, "message": f"函数 '{name}' {n} 行 (> {FUNC_MAX_LINES})", "principle": "file-and-function-size.md"}]
    return []


def _function_params(node, path, name):
    n = len(node.args.args) + len(node.args.kwonlyargs)
    if node.args.vararg: n += 1
    if node.args.kwarg: n += 1
    if n > PARAMS_MAX:
        return [{"rule": "function_params", "file": str(path), "line": node.lineno, "name": name, "message": f"函数 '{name}' 有 {n} 个参数 (> {PARAMS_MAX})", "principle": "file-and-function-size.md"}]
    return []


COMPLEXITY_NODES = (ast.If, ast.For, ast.AsyncFor, ast.While, ast.ExceptHandler, ast.With, ast.AsyncWith, ast.Assert, ast.IfExp)


def _cyclomatic(node):
    c = 1
    for sub in ast.walk(node):
        if isinstance(sub, ast.BoolOp):
            c += len(sub.values) - 1
        elif isinstance(sub, COMPLEXITY_NODES):
            c += 1
    return c


def _function_complexity(node, path, name):
    c = _cyclomatic(node)
    if c > CYCLOMATIC_MAX:
        return [{"rule": "cyclomatic_complexity", "file": str(path), "line": node.lineno, "name": name, "message": f"函数 '{name}' 圈复杂度 {c} (> {CYCLOMATIC_MAX})", "principle": "file-and-function-size.md"}]
    return []


def _function_nesting(node, path, name):
    d = _max_nesting(node.body)
    if d > NESTED_MAX:
        return [{"rule": "nesting_depth", "file": str(path), "line": node.lineno, "name": name, "message": f"函数 '{name}' 嵌套深度 {d} (> {NESTED_MAX})", "principle": "file-and-function-size.md"}]
    return []


def _check_function_shape(node, path):
    name = node.name
    return (
        _function_lines(node, path, name) +
        _function_params(node, path, name) +
        _function_complexity(node, path, name) +
        _function_nesting(node, path, name)
    )


def _check_commented_code(lines, path):
    errors = []
    patterns = [
        (r"^#\s*(def |class |import |from |return |if |for |while |print|raise |yield )", "py"),
        (r"^//\s*(function |const |let |var |class |import |export |if |for |while |return)", "ts/js"),
    ]
    for i, line in enumerate(lines, 1):
        stripped = line.strip()
        for pattern, lang in patterns:
            if re.match(pattern, stripped):
                errors.append({"rule": "dead_code", "file": str(path), "line": i, "message": f"疑似注释掉的代码 ({lang}): {stripped[:60]}", "principle": "dead-code-deletion.md"})
                break
    return errors


def _import_names(import_node):
    """yield single import node 的所有名字。"""
    for alias in import_node.names:
        if isinstance(import_node, ast.Import):
            yield alias.asname or alias.name.split(".")[0]
        else:
            yield alias.asname or alias.name


def _collect_imports(tree):
    """收集所有 import 名（扁平化嵌套）。"""
    imports = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.extend(_import_names(node))
    return imports


def _check_unused_imports(imports, lines, path):
    errors = []
    for imp in imports:
        count = sum(1 for line in lines if re.search(rf"\b{re.escape(imp)}\b", line))
        if count <= 1:
            errors.append({"rule": "unused_import", "file": str(path), "line": 0, "message": f"unused import: {imp}", "principle": "dead-code-deletion.md"})
    return errors


def _check_decorator_chain(tree, path):
    errors = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            n = len(node.decorator_list)
            if n >= 3:
                errors.append({"rule": "decorator_chain", "file": str(path), "line": node.lineno, "name": node.name, "message": f"{node.name} 有 {n} 个装饰器 (>= 3, 可能过度)", "principle": "naming-is-documentation.md"})
    return errors


def check_python_ast(path):
    try:
        text = path.read_text(encoding="utf-8")
        tree = ast.parse(text, filename=str(path))
    except (SyntaxError, UnicodeDecodeError, FileNotFoundError):
        return []
    lines = text.splitlines()

    errors = []
    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            errors.extend(_check_function_shape(node, path))
    errors.extend(_check_commented_code(lines, path))
    imports = _collect_imports(tree)
    errors.extend(_check_unused_imports(imports, lines, path))
    if len(imports) > IMPORTS_MAX:
        errors.append({"rule": "too_many_imports", "file": str(path), "message": f"文件有 {len(imports)} 个 import (> {IMPORTS_MAX})", "principle": "dependency-minimalism.md"})
    errors.extend(_check_decorator_chain(tree, path))
    return errors


BAD_NAMES = {"a", "b", "c", "tmp", "foo", "bar", "baz", "test", "data", "info", "stuff", "obj", "o", "x"}


def check_naming(path):
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, FileNotFoundError):
        return []
    errors = []
    for i, line in enumerate(text.splitlines(), 1):
        for match in re.finditer(r"\b(?:def|class)\s+([a-zA-Z_][a-zA-Z0-9_]*)", line):
            name = match.group(1)
            if name.lower() in BAD_NAMES:
                errors.append({"rule": "bad_name", "file": str(path), "line": i, "name": name, "message": f"无意义命名: {name}", "principle": "naming-is-documentation.md"})
    return errors


def check_file(path):
    if not path.exists():
        return [{"rule": "not_found", "file": str(path), "message": "文件不存在"}]
    errors = []
    errors.extend(check_file_size(path))
    errors.extend(check_todo_fixme(path))
    suffix = path.suffix
    if suffix == ".py":
        errors.extend(check_python_ast(path))
        errors.extend(check_naming(path))
    return errors


def _yield_files(target, recursive):
    pattern = "**/*" if recursive else "*"
    for f in sorted(Path(target).glob(pattern)):
        if f.is_file():
            yield f


def walk_paths(targets, recursive):
    for target in targets:
        p = Path(target)
        if p.is_file():
            yield p
        elif p.is_dir():
            yield from _yield_files(target, recursive)


def main():
    parser = argparse.ArgumentParser(description="代码简洁性自动校验 (simplification/ 10 条)")
    parser.add_argument("targets", nargs="+", help="文件或目录")
    parser.add_argument("--recursive", "-r", action="store_true", help="递归目录")
    parser.add_argument("--verbose", "-v", action="store_true", help="显示所有检查项")
    args = parser.parse_args()

    all_errors = []
    file_count = 0
    for path in walk_paths(args.targets, args.recursive):
        if path.suffix not in (".py", ".md", ".markdown", ".ts", ".tsx", ".js", ".jsx", ".vue"):
            continue
        file_count += 1
        errs = check_file(path)
        if args.verbose and not errs:
            print(f"  OK: {path}")
        all_errors.extend(errs)

    print(f"\n=== 校验 {file_count} 个文件 ===")
    print(f"阈值: 文件 <= {FILE_MAX_LINES} / 函数 <= {FUNC_MAX_LINES} / 圈复杂度 <= {CYCLOMATIC_MAX} / 嵌套 <= {NESTED_MAX} / 参数 <= {PARAMS_MAX}")
    print("---")

    if not all_errors:
        print("OK 全部通过 (simplification/ 10 条原则)")
        sys.exit(0)

    by_file = {}
    for e in all_errors:
        by_file.setdefault(e["file"], []).append(e)

    for f, errs in by_file.items():
        print(f"\n  {f}:")
        for e in errs:
            line = e.get("line", "")
            line_str = f":{line}" if line else ""
            print(f"    [{e['rule']}]{line_str} {e['message']}")

    print(f"\n共 {len(all_errors)} 个问题 ({len(by_file)} 个文件)")
    sys.exit(1)


if __name__ == "__main__":
    main()
