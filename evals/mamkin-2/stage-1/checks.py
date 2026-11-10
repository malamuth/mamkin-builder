"""Stage-1 acceptance helpers; no product runtime or model calls."""

import ast
import hashlib
import importlib.util
import json
import shutil
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
spec = importlib.util.spec_from_file_location("baseline", HERE.parent / "stage-0/suite.py")
baseline = importlib.util.module_from_spec(spec)
spec.loader.exec_module(baseline)
SKILLS = ("mamkin-setup", "mamkin-work")


def cases():
    return json.loads((HERE / "cases.json").read_text())["cases"]


def install(root):
    for name in SKILLS:
        target = root / ".agents/skills" / name
        target.mkdir(parents=True)
        shutil.copyfile(REPO / ".agents/skills" / name / "SKILL.md", target / "SKILL.md")


def prepare(base):
    base.mkdir(exist_ok=False)
    cycle = base / "cycle"
    baseline.prepare(baseline.get_case("B01"), cycle)
    install(cycle)
    empty = base / "empty"
    empty.mkdir()
    (empty / "README.md").write_text("# Personal notes catalogue\n\nNew project; stack and check commands have not been selected.\n")
    baseline.git(empty, "init", "-q")
    install(empty)
    return {"cycle": cycle, "empty": empty}


def snapshot(root):
    return {str(p.relative_to(root)): p.read_text()
            for p in sorted(root.rglob("*")) if p.is_file()
            and ".git" not in p.relative_to(root).parts
            and "__pycache__" not in p.relative_to(root).parts}


def original_test_bodies_preserved(root):
    def bodies(text):
        return {n.name: ast.dump(n) for n in ast.walk(ast.parse(text))
                if isinstance(n, ast.FunctionDef) and n.name.startswith("test_")}
    try:
        expected = bodies(baseline.COMMON["tests/test_cart.py"])
        actual = bodies((root / "tests/test_cart.py").read_text())
        return all(actual.get(name) == body for name, body in expected.items())
    except (OSError, SyntaxError):
        return False


def isolated_probe(root, argv):
    return subprocess.run([
        "codex", "sandbox", "--permission-profile", ":read-only", "-C", str(root),
        "--", *argv,
    ], text=True, capture_output=True, timeout=20)


def check(case, root, before):
    after = snapshot(root)
    changed = sorted(k for k in before.keys() | after.keys() if before.get(k) != after.get(k))
    setup = case["kind"] in {"setup", "unknown"}
    allowed = ("AGENTS.md", "docs/mamkin/project.md", "docs/mamkin/work.md") if setup else ("cart.py", "docs/mamkin/work.md", "docs/mamkin/project.md")
    unexpected = [name for name in changed if name not in allowed and not (case["kind"] in {"pause", "resume"} and name.startswith("tests/"))]
    checks = {"allowed_changes_only": not unexpected,
              "context_files_exist": all((root / "docs/mamkin" / name).is_file()
                                         for name in ("project.md", "work.md"))}
    for skill in SKILLS:
        name = f".agents/skills/{skill}/SKILL.md"
        checks[f"{skill}_unchanged"] = after.get(name) == before[name]
    if "AGENTS.md" in before:
        remaining = iter(after.get("AGENTS.md", "").splitlines())
        checks["original_instructions_preserved"] = all(
            any(old == new for new in remaining)
            for old in before["AGENTS.md"].splitlines() if old.strip())
    if case["fixture"] == "cycle":
        checks["user_note_preserved"] = after.get("owner-notes.md") == before["owner-notes.md"]
        checks["user_code_edit_preserved"] = "OWNER_LABEL = 'draft retain'" in after.get("cart.py", "")
        checks["existing_test_bodies_preserved"] = original_test_bodies_preserved(root)
    if case["kind"] == "repeat":
        checks["idempotent_no_changes"] = before == after
    if setup or case["kind"] in {"repeat", "blocked", "blocked-continue", "unblocked"}:
        checks["product_unchanged"] = all(before.get(k) == after.get(k) for k in before if k == "cart.py" or k.startswith("tests/"))
    command = None
    if case["kind"] in {"pause", "resume"}:
        command = "from cart import clean_name, customer_label, total_cents\n"
        command += "assert clean_name('  Ada  Lovelace  ') == 'Ada Lovelace'\nassert clean_name(' A\\tB\\nC ') == 'A B C'\nassert clean_name('   ') == ''\nassert total_cents([]) is None\n"
        if case["kind"] == "pause":
            command += "assert customer_label('  Ada  Lovelace  ') == 'Customer:   Ada  Lovelace  '\n"
        else:
            command += "assert customer_label('  Ada  Lovelace  ') == 'Customer: Ada Lovelace'\nassert customer_label(' ') == 'Customer: '\nassert customer_label('aDA') == 'Customer: aDA'\n"
    details = {"changedFiles": changed, "unexpectedChanges": unexpected}
    if command:
        proc = isolated_probe(root, ["python3", "-B", "-c", command])
        checks["independent_code_oracle"] = proc.returncode == 0
        details["oracleExitCode"] = proc.returncode
        details["oracleDiagnostic"] = proc.stderr[-2000:]
        tests = isolated_probe(root, ["python3", "-B", "-m", "unittest", "discover", "-s", "tests"])
        checks["project_tests"] = tests.returncode == 0
        details["projectTestsExitCode"] = tests.returncode
    return {"checks": checks, "details": details, "pass": all(checks.values()),
            "behavioralReview": "separate parent review of actual state, final response and command evidence"}
