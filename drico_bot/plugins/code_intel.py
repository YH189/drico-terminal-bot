"""Code intelligence: explain-file, complexity, secrets, deps, todos, loc, largefiles."""

import ast
import json
import os
import re
from pathlib import Path

from drico_bot.core.paths import safe_path_under
from drico_bot.core.registry import Command
from drico_bot.knowledge.folder_index import INDEX_SKIP_DIR_NAMES
from drico_bot.knowledge.project import find_project_root_for_cwd

MAX_READ_BYTES = 1024 * 1024
DEFAULT_LARGE_BYTES = 100 * 1024
TEXT_SUFFIXES = frozenset(
    {
        ".py",
        ".md",
        ".txt",
        ".json",
        ".jsonl",
        ".yaml",
        ".yml",
        ".toml",
        ".js",
        ".ts",
        ".jsx",
        ".tsx",
        ".css",
        ".html",
        ".sh",
        ".sql",
        ".rs",
        ".go",
        ".java",
        ".c",
        ".cpp",
        ".h",
    }
)

SECRET_PATTERNS = [
    (
        "assignment",
        re.compile(
            r"(?i)(api[_-]?key|secret|password|token|auth[_-]?token)"
            r"\s*[=:]\s*['\"]([^'\"]{4,})['\"]"
        ),
    ),
    ("aws_access_key", re.compile(r"(AKIA[0-9A-Z]{16})")),
    (
        "private_key",
        re.compile(r"-----BEGIN ([A-Z ]+)?PRIVATE KEY-----"),
    ),
]

TODO_PATTERN = re.compile(
    r"(?i)\b(TODO|FIXME|HACK|XXX)\b\s*:?\s*(.*)$"
)


class CodeIntelError(Exception):
    """User-facing code intelligence error."""


def _path_stays_under_root(root, candidate):
    root = Path(root).resolve()
    try:
        candidate = candidate.resolve()
    except OSError:
        return False
    try:
        candidate.relative_to(root)
    except ValueError:
        return False
    return True


def _should_skip_dir(name):
    if name.startswith("."):
        return True
    return name in INDEX_SKIP_DIR_NAMES


def _should_skip_file(name):
    return name.startswith(".")


def _require_project_root(cwd=None):
    root = find_project_root_for_cwd(cwd)
    if root is None:
        raise CodeIntelError(
            "No indexed project for this directory. Run 'index <folder>' first."
        )
    return root


def resolve_code_path(user_path, cwd=None):
    """
    Resolve user_path under the indexed project root that contains cwd.
    """
    if cwd is None:
        cwd = Path.cwd()
    cwd = Path(cwd).resolve()
    root = _require_project_root(cwd)
    if user_path is None or not str(user_path).strip():
        return root
    try:
        target = safe_path_under(root, user_path)
    except ValueError:
        raise CodeIntelError("Path escapes the indexed project.")
    if not _path_stays_under_root(root, target):
        raise CodeIntelError("Path escapes the indexed project.")
    if target.is_symlink() and not _path_stays_under_root(root, target):
        raise CodeIntelError("Path escapes the indexed project.")
    return target


def _read_text_limited(path):
    path = Path(path)
    try:
        size = path.stat().st_size
    except OSError as exc:
        raise CodeIntelError("Cannot read file: {0}".format(path)) from exc
    if size > MAX_READ_BYTES:
        raise CodeIntelError(
            "File too large to read ({0} bytes). Maximum is {1}.".format(
                size, MAX_READ_BYTES
            )
        )
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        raise CodeIntelError("Not a UTF-8 text file: {0}".format(path))
    except OSError as exc:
        raise CodeIntelError("Cannot read file: {0}".format(path)) from exc


def _mask_secret(value):
    text = str(value)
    if len(text) <= 4:
        return text
    return text[:4] + "***"


def iter_project_files(root, target):
    root = Path(root).resolve()
    target = Path(target).resolve()
    if target.is_file():
        yield target
        return
    if not target.is_dir():
        raise CodeIntelError("Not a file or directory: {0}".format(target))
    for dirpath, dirnames, filenames in os.walk(target, topdown=True, followlinks=False):
        current = Path(dirpath)
        if not _path_stays_under_root(root, current):
            dirnames[:] = []
            continue
        pruned = []
        for name in dirnames:
            if _should_skip_dir(name):
                continue
            child = current / name
            if child.is_symlink() and not _path_stays_under_root(root, child):
                continue
            pruned.append(name)
        dirnames[:] = pruned
        for name in filenames:
            if _should_skip_file(name):
                continue
            src = current / name
            if src.is_symlink() and not _path_stays_under_root(root, src):
                continue
            if not _path_stays_under_root(root, src):
                continue
            yield src


def explain_file(path, cwd=None):
    target = resolve_code_path(path, cwd=cwd)
    if not target.is_file():
        raise CodeIntelError("explain-file requires a file path.")
    rel = str(target.relative_to(_require_project_root(cwd)))
    suffix = target.suffix.lower()
    lines = []
    lines.append("File: {0}".format(rel))
    lines.append("Size: {0} bytes".format(target.stat().st_size))
    if suffix == ".py":
        source = _read_text_limited(target)
        try:
            tree = ast.parse(source, filename=str(target))
        except SyntaxError as exc:
            lines.append("Python: syntax error ({0})".format(exc.msg))
            return "\n".join(lines)
        doc = ast.get_docstring(tree)
        if doc:
            first = doc.strip().splitlines()[0]
            lines.append("Module doc: {0}".format(first[:120]))
        imports = []
        for node in tree.body:
            if isinstance(node, ast.Import):
                for alias in node.names:
                    imports.append(alias.name)
            elif isinstance(node, ast.ImportFrom):
                mod = node.module or ""
                for alias in node.names:
                    imports.append("{0}.{1}".format(mod, alias.name) if mod else alias.name)
        if imports:
            lines.append("Imports: {0}".format(", ".join(imports[:20])))
        funcs = []
        classes = []
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                funcs.append("{0} (line {1})".format(node.name, node.lineno))
            elif isinstance(node, ast.ClassDef):
                methods = [
                    n.name
                    for n in node.body
                    if isinstance(n, ast.FunctionDef)
                ]
                classes.append(
                    "{0} (line {1}, methods: {2})".format(
                        node.name, node.lineno, ", ".join(methods[:8]) or "-"
                    )
                )
        if classes:
            lines.append("Classes: {0}".format("; ".join(classes)))
        if funcs:
            lines.append("Functions: {0}".format("; ".join(funcs)))
    elif suffix in (".md", ".txt"):
        source = _read_text_limited(target)
        line_count = len(source.splitlines())
        preview = source.strip().splitlines()[:3]
        lines.append("Lines: {0}".format(line_count))
        for row in preview:
            lines.append("  {0}".format(row[:100]))
    elif suffix == ".json":
        data = json.loads(_read_text_limited(target))
        if isinstance(data, dict):
            keys = list(data.keys())[:15]
            lines.append("JSON object keys: {0}".format(", ".join(keys)))
        else:
            lines.append("JSON top-level: {0}".format(type(data).__name__))
    else:
        lines.append("Type: {0}".format(suffix or "unknown"))
    return "\n".join(lines)


def _cyclomatic_complexity(node):
    score = 1
    for child in ast.walk(node):
        if isinstance(
            child,
            (ast.If, ast.For, ast.While, ast.ExceptHandler, ast.With, ast.Assert),
        ):
            score += 1
        elif isinstance(child, ast.BoolOp):
            score += max(0, len(child.values) - 1)
        elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
            score += 1
    return score


def complexity_report(path=None, cwd=None, limit=15):
    root = _require_project_root(cwd)
    target = resolve_code_path(path, cwd=cwd)
    entries = []
    for file_path in iter_project_files(root, target):
        if file_path.suffix.lower() != ".py":
            continue
        try:
            source = _read_text_limited(file_path)
            tree = ast.parse(source, filename=str(file_path))
        except (SyntaxError, CodeIntelError):
            continue
        rel = str(file_path.relative_to(root))
        for node in tree.body:
            if isinstance(node, ast.FunctionDef):
                entries.append(
                    (
                        _cyclomatic_complexity(node),
                        "{0}:{1}".format(rel, node.name),
                        node.lineno,
                    )
                )
    entries.sort(key=lambda item: (-item[0], item[1]))
    lines = ["Cyclomatic complexity (top {0}):".format(limit)]
    if not entries:
        lines.append("No Python functions found.")
        return "\n".join(lines)
    for score, label, lineno in entries[:limit]:
        lines.append("  {0}  {1} (line {2})".format(score, label, lineno))
    return "\n".join(lines)


def scan_secrets(path=None, cwd=None):
    root = _require_project_root(cwd)
    target = resolve_code_path(path, cwd=cwd)
    findings = []
    for file_path in iter_project_files(root, target):
        if file_path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = _read_text_limited(file_path)
        except CodeIntelError:
            continue
        rel = str(file_path.relative_to(root))
        for line_no, line in enumerate(text.splitlines(), start=1):
            for kind, pattern in SECRET_PATTERNS:
                for match in pattern.finditer(line):
                    if kind == "assignment":
                        raw = match.group(2)
                    elif kind == "private_key":
                        raw = "PRIVATE_KEY"
                    else:
                        raw = match.group(1)
                    findings.append(
                        (rel, line_no, kind, _mask_secret(raw))
                    )
    lines = ["Secrets scan (masked):"]
    if not findings:
        lines.append("No likely secrets found.")
        return "\n".join(lines)
    for rel, line_no, kind, masked in findings[:50]:
        lines.append("  {0}:{1} [{2}] {3}".format(rel, line_no, kind, masked))
    if len(findings) > 50:
        lines.append("  ... and {0} more".format(len(findings) - 50))
    return "\n".join(lines)


def _parse_requirements(text):
    deps = []
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("-"):
            continue
        name = re.split(r"[<>=!~\[]", line, 1)[0].strip()
        if name:
            deps.append(name)
    return deps


def _parse_pyproject_deps(text):
    deps = []
    in_project = False
    in_deps = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped == "[project]":
            in_project = True
            in_deps = False
            continue
        if stripped.startswith("[") and stripped.endswith("]"):
            in_project = False
            in_deps = False
            continue
        if in_project and stripped.startswith("dependencies"):
            in_deps = True
            if "[" in stripped and "]" in stripped:
                inner = stripped.split("[", 1)[1].rsplit("]", 1)[0]
                for part in inner.split(","):
                    part = part.strip().strip('"').strip("'")
                    if part:
                        deps.append(part)
                in_deps = False
            continue
        if in_deps:
            if stripped.startswith("]"):
                in_deps = False
                continue
            part = stripped.strip(",").strip('"').strip("'")
            if part:
                deps.append(part)
    return deps


def deps_report(path=None, cwd=None):
    root = _require_project_root(cwd)
    target = resolve_code_path(path, cwd=cwd)
    search_root = target if target.is_dir() else target.parent
    lines = ["Dependencies:"]
    found = False
    req = search_root / "requirements.txt"
    if req.is_file():
        found = True
        for name in _parse_requirements(_read_text_limited(req)):
            lines.append("  requirements.txt: {0}".format(name))
    pyproject = search_root / "pyproject.toml"
    if pyproject.is_file():
        found = True
        for name in _parse_pyproject_deps(_read_text_limited(pyproject)):
            lines.append("  pyproject.toml: {0}".format(name))
    pkg = search_root / "package.json"
    if pkg.is_file():
        found = True
        try:
            data = json.loads(_read_text_limited(pkg))
        except json.JSONDecodeError:
            data = {}
        for section in ("dependencies", "devDependencies"):
            block = data.get(section)
            if isinstance(block, dict):
                for name in sorted(block.keys()):
                    lines.append("  package.json {0}: {1}".format(section, name))
    if not found:
        lines.append("No requirements.txt, pyproject.toml, or package.json in scope.")
    return "\n".join(lines)


def todos_report(path=None, cwd=None, limit=50):
    root = _require_project_root(cwd)
    target = resolve_code_path(path, cwd=cwd)
    hits = []
    for file_path in iter_project_files(root, target):
        if file_path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = _read_text_limited(file_path)
        except CodeIntelError:
            continue
        rel = str(file_path.relative_to(root))
        for line_no, line in enumerate(text.splitlines(), start=1):
            match = TODO_PATTERN.search(line)
            if match:
                tag = match.group(1).upper()
                note = match.group(2).strip()[:80]
                hits.append((rel, line_no, tag, note))
    lines = ["TODO / FIXME markers:"]
    if not hits:
        lines.append("None found.")
        return "\n".join(lines)
    for rel, line_no, tag, note in hits[:limit]:
        if note:
            lines.append("  {0}:{1} {2} — {3}".format(rel, line_no, tag, note))
        else:
            lines.append("  {0}:{1} {2}".format(rel, line_no, tag))
    if len(hits) > limit:
        lines.append("  ... and {0} more".format(len(hits) - limit))
    return "\n".join(lines)


def loc_report(path=None, cwd=None):
    root = _require_project_root(cwd)
    target = resolve_code_path(path, cwd=cwd)
    totals = {}
    total_lines = 0
    total_files = 0
    for file_path in iter_project_files(root, target):
        if file_path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = _read_text_limited(file_path)
        except CodeIntelError:
            continue
        ext = file_path.suffix.lower() or "(no ext)"
        count = len(text.splitlines())
        totals[ext] = totals.get(ext, 0) + count
        total_lines += count
        total_files += 1
    lines = [
        "Lines of code: {0} lines in {1} text files".format(total_lines, total_files)
    ]
    for ext in sorted(totals.keys()):
        lines.append("  {0}: {1}".format(ext, totals[ext]))
    return "\n".join(lines)


def largefiles_report(path=None, cwd=None, min_bytes=None, limit=20):
    if min_bytes is None:
        min_bytes = DEFAULT_LARGE_BYTES
    root = _require_project_root(cwd)
    target = resolve_code_path(path, cwd=cwd)
    large = []
    for file_path in iter_project_files(root, target):
        try:
            size = file_path.stat().st_size
        except OSError:
            continue
        if size >= min_bytes:
            rel = str(file_path.relative_to(root))
            large.append((size, rel))
    large.sort(key=lambda item: (-item[0], item[1]))
    lines = ["Files >= {0} bytes:".format(min_bytes)]
    if not large:
        lines.append("None found.")
        return "\n".join(lines)
    for size, rel in large[:limit]:
        lines.append("  {0}  {1}".format(size, rel))
    if len(large) > limit:
        lines.append("  ... and {0} more".format(len(large) - limit))
    return "\n".join(lines)


def _path_from_context(context):
    normalized = context.normalized
    parts = normalized.split()
    if len(parts) <= 1:
        return None
    return " ".join(context.raw.split()[1:])


def _run_command(context, fn):
    try:
        user_path = _path_from_context(context)
        print(fn(path=user_path, cwd=Path.cwd()))
        print()
    except CodeIntelError as exc:
        print("Drico > {0}\n".format(exc))


def register(registry):
    category = "code"
    commands = [
        ("explain-file", lambda c: _run_command(c, explain_file), "Summarize a source file."),
        ("complexity", lambda c: _run_command(c, complexity_report), "Cyclomatic complexity for Python."),
        ("secrets", lambda c: _run_command(c, scan_secrets), "Scan for secrets (masked)."),
        ("deps", lambda c: _run_command(c, deps_report), "List dependency manifests."),
        ("todos", lambda c: _run_command(c, todos_report), "Find TODO/FIXME markers."),
        ("loc", lambda c: _run_command(c, loc_report), "Count lines by extension."),
        ("largefiles", lambda c: _run_command(c, largefiles_report), "List large files."),
    ]
    for name, handler, help_text in commands:
        registry.register(
            Command(
                name=name,
                handler=handler,
                help_text=help_text,
                category=category,
            )
        )
