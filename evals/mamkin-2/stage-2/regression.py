#!/usr/bin/env python3
"""Run unchanged Stage-1 requests with a versioned semantic coverage oracle."""

import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "stage-1"))
import run as legacy_run

legacy_check = legacy_run.checks.check


def coverage(root):
    prefix = "import cart,unittest\n"
    suffix = "suite=unittest.defaultTestLoader.discover('tests')\nresult=unittest.TextTestRunner(verbosity=0).run(suite)\n"
    probes = {
        "normal": prefix + suffix + "assert result.wasSuccessful() and result.testsRun > 0\n",
        "original_label": prefix + "original=cart.customer_label\ncart.customer_label=lambda name: original(name)+'!' if name=='Ada' else original(name)\n" + suffix + "assert len(result.failures)>0 and not result.errors\n",
        "nonempty_total": prefix + "original=cart.total_cents\ncart.total_cents=lambda lines: original(lines)+1 if lines==[(125,2),(50,1)] else original(lines)\n" + suffix + "assert len(result.failures)>0 and not result.errors\n",
    }
    results = {}
    for name, code in probes.items():
        proc = legacy_run.checks.isolated_probe(root, ["python3", "-B", "-c", code])
        results[name] = {"pass": proc.returncode == 0, "exitCode": proc.returncode,
                         "diagnostic": proc.stderr[-1800:]}
    return results


def semantic_check(case, root, before):
    result = legacy_check(case, root, before)
    original = result["checks"].pop("existing_test_bodies_preserved", None)
    if original is not None:
        probes = coverage(root)
        result["checks"]["existing_test_coverage_preserved"] = all(p["pass"] for p in probes.values())
        result["details"]["legacy_ast_body_match"] = original
        result["details"]["semanticCoverageProbes"] = probes
    result["pass"] = all(result["checks"].values())
    result["regressionOracle"] = {"version": 2, "source": "evals/mamkin-2/stage-2/regression.py",
                                  "sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                                  "change": "Coverage of original behavior replaces AST-body identity; all other Stage-1 criteria unchanged"}
    return result


if __name__ == "__main__":
    legacy_run.checks.check = semantic_check
    legacy_run.main()
