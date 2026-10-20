"""Automated Integration Testing Array Runner.

Decentralized Air-Gapped Bio-Sieve Protocol.

Executes each test module in the `tests/` directory, captures real-time
compiler execution telemetry, and prints the formatted telemetry table.

Usage:
    python run_test_array.py
"""

from __future__ import annotations

import io
import os
import sys
import time
import unittest


def run_single_suite(test_module_name: str) -> tuple[int, int, float, bool]:
    """Run a single test module and return (total_run, passed, elapsed_s, is_success)."""
    loader = unittest.TestLoader()
    suite = loader.loadTestsFromName(test_module_name)
    stream = io.StringIO()
    runner = unittest.TextTestRunner(stream=stream, verbosity=0)

    t0 = time.perf_counter()
    result = runner.run(suite)
    elapsed_s = time.perf_counter() - t0

    total_run = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)
    passed = total_run - failures - errors
    is_success = result.wasSuccessful()

    return total_run, passed, elapsed_s, is_success


def main() -> None:
    if sys.platform == "win32":
        try:
            os.system("")  # Enable ANSI / VT100
        except Exception:
            pass
        if hasattr(sys.stdout, "reconfigure"):
            try:
                sys.stdout.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass

    test_modules = [
        ("tests/test_fragment_affinity.py", "tests.test_fragment_affinity", "UNIT TESTS VALIDATED"),
        ("tests/test_thermal_interlock.py", "tests.test_thermal_interlock", "UNIT TESTS VALIDATED"),
        ("tests/test_validation_engine.py", "tests.test_validation_engine", "UNIT TESTS VALIDATED"),
        ("tests/test_pipeline.py", "tests.test_pipeline", "PIPELINE RUNS CLEAR"),
    ]

    results = []
    total_suite_start = time.perf_counter()
    all_passed = True
    grand_total_tests = 0
    grand_total_passed = 0

    for file_path, module_name, desc in test_modules:
        total, passed, elapsed, ok = run_single_suite(module_name)
        if not ok:
            all_passed = False
        grand_total_tests += total
        grand_total_passed += passed
        results.append((file_path, total, passed, elapsed, ok, desc))

    total_elapsed = time.perf_counter() - total_suite_start

    # Exact 81-character wide box formatting:
    # 1 ('┌') + 38 ('─') + 1 ('┬') + 40 ('─') + 1 ('┐') = 81 chars
    top_border = "┌" + "─" * 38 + "┬" + "─" * 40 + "┐"
    mid_border = "├" + "─" * 38 + "┼" + "─" * 40 + "┤"
    bot_border = "└" + "─" * 38 + "┴" + "─" * 40 + "┘"

    def fmt_row(left: str, right: str, tag: str = "") -> str:
        # Col 1: width 38
        c1 = f" {left}"[:37].ljust(38)
        # Col 2: width 40
        if tag:
            avail = 40 - len(tag)
            c2 = f" {right}"[:avail].ljust(avail) + tag
        else:
            c2 = f" {right}"[:39].ljust(40)
        return f"│{c1}│{c2}│"

    lines = [
        "",
        top_border,
        fmt_row("AUTOMATED INTEGRATION TESTING ARRAY", "SUITE EXECUTION TELEMETRY STATUS"),
        mid_border,
    ]

    for file_path, total, passed, elapsed, ok, desc in results:
        status_tag = "[OK]" if ok else "[FAIL]"
        detail_str = f"{elapsed:.3f}s // {passed}/{total} {desc}"
        lines.append(fmt_row(file_path, detail_str, status_tag))
        lines.append(mid_border)

    runtime_c2 = f"TOTAL COMPILER RUNTIME: {total_elapsed:.3f}s"
    status_str = f"STATUS: {grand_total_passed} / {grand_total_tests} TESTS EVALUATED"
    status_tag = "[PASS]" if all_passed else "[FAIL]"

    lines.append(fmt_row("OVERALL SUITE RUNTIME VERIFICATION", runtime_c2))
    lines.append(fmt_row("python -m unittest discover tests", status_str, status_tag))
    lines.append(bot_border)
    lines.append("")

    output_text = "\n".join(lines)

    try:
        sys.stdout.buffer.write(output_text.encode("utf-8") + b"\n")
    except Exception:
        print(output_text)

    if not all_passed:
        sys.exit(1)


if __name__ == "__main__":
    main()
