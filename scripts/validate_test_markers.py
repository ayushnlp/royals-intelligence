#!/usr/bin/env python3
"""
Royals Intelligence - Test Marker Classification Validator
Verifies that all tests in backend/tests/ belong to exactly one primary execution group:
  - Group A: 'unit' or 'environment' (Target: 83 tests)
  - Group B: 'data_dependent' (Target: 103 tests)
  - Group C: 'data_integrity' (Target: 10 tests)
Total: 196 tests.
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = ROOT_DIR / "backend"


def main():
    print("=" * 70)
    print("ROYALS INTELLIGENCE — TEST SUITE CLASSIFICATION AUDIT")
    print("=" * 70)

    # 1. Total collection
    cmd_all = ["pytest", "--collect-only", "-q"]
    res_all = subprocess.run(cmd_all, cwd=str(BACKEND_DIR), capture_output=True, text=True)
    if res_all.returncode != 0:
        print(f"ERROR: pytest collection failed:\n{res_all.stderr}")
        return 1

    lines_all = [l.strip() for l in res_all.stdout.splitlines() if l.strip().startswith("tests/") and "::" in l]
    total_tests = len(lines_all)
    print(f"Total pytest items collected: {total_tests}")

    # 2. Group A collection (unit or environment)
    cmd_a = ["pytest", "-m", "unit or environment", "--collect-only", "-q"]
    res_a = subprocess.run(cmd_a, cwd=str(BACKEND_DIR), capture_output=True, text=True)
    lines_a = [l.strip() for l in res_a.stdout.splitlines() if l.strip().startswith("tests/") and "::" in l]
    count_a = len(lines_a)

    # 3. Group B collection (data_dependent)
    cmd_b = ["pytest", "-m", "data_dependent", "--collect-only", "-q"]
    res_b = subprocess.run(cmd_b, cwd=str(BACKEND_DIR), capture_output=True, text=True)
    lines_b = [l.strip() for l in res_b.stdout.splitlines() if l.strip().startswith("tests/") and "::" in l]
    count_b = len(lines_b)

    # 4. Group C collection (data_integrity)
    cmd_c = ["pytest", "-m", "data_integrity", "--collect-only", "-q"]
    res_c = subprocess.run(cmd_c, cwd=str(BACKEND_DIR), capture_output=True, text=True)
    lines_c = [l.strip() for l in res_c.stdout.splitlines() if l.strip().startswith("tests/") and "::" in l]
    count_c = len(lines_c)

    print(f"  Group A (Unit & Environment):  {count_a:3d} tests (Expected: 83)")
    print(f"  Group B (Data-Dependent):     {count_b:3d} tests (Expected: 103)")
    print(f"  Group C (Data Integrity):     {count_c:3d} tests (Expected: 10)")
    print("-" * 70)
    print(f"  Sum of Groups (A + B + C):    {count_a + count_b + count_c:3d} tests (Expected: 196)")

    # 5. Overlap and omission checks
    set_a = set(lines_a)
    set_b = set(lines_b)
    set_c = set(lines_c)
    set_all = set(lines_all)

    overlap_ab = set_a & set_b
    overlap_ac = set_a & set_c
    overlap_bc = set_b & set_c
    unclassified = set_all - (set_a | set_b | set_c)

    errors = []
    if total_tests != 196:
        errors.append(f"Expected 196 total tests, got {total_tests}")
    if count_a != 83:
        errors.append(f"Expected 83 Group A tests, got {count_a}")
    if count_b != 103:
        errors.append(f"Expected 103 Group B tests, got {count_b}")
    if count_c != 10:
        errors.append(f"Expected 10 Group C tests, got {count_c}")
    if overlap_ab:
        errors.append(f"Overlap between Group A and Group B ({len(overlap_ab)} tests)")
    if overlap_ac:
        errors.append(f"Overlap between Group A and Group C ({len(overlap_ac)} tests)")
    if overlap_bc:
        errors.append(f"Overlap between Group B and Group C ({len(overlap_bc)} tests)")
    if unclassified:
        errors.append(f"Unclassified tests detected ({len(unclassified)} tests): {list(unclassified)[:5]}")

    if errors:
        print("\nAUDIT FAILED:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("\nAUDIT PASSED: All 196 tests strictly and uniquely classified!")
    print("=" * 70)
    return 0


if __name__ == "__main__":
    sys.exit(main())
