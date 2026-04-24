"""
Beckn v2.1 Generalised Schema Test Suite
==========================================
Validates any Beckn v2.1 generalised schema pack against four quality layers.

Usage (from within a schema project root, where v2.1/ is a subfolder):
    python tests/run_tests.py

Usage (explicit paths):
    python tests/run_tests.py --schema-root /path/to/v2.1 --core /path/to/core

Layers:
    L1 — OpenAPI 3.1.1 structural validation (attributes.yaml); validates v2.1 containers
    L2 — JSON-LD prefix resolution (context.jsonld + examples); validates #generalised import
    L3 — Cross-file consistency (attributes.yaml ↔ context.jsonld ↔ vocab.jsonld)
    L4 — Example payload validation against extension + core schemas; uses v2.1 payload paths

Schema folder discovery:
    Any subdirectory of schema-root that contains an attributes.yaml file is treated as a
    schema folder and tested. {domain}-common/ subfolders are automatically excluded.

Exit code: 0 if all checks pass, 1 if any fail.
"""

import sys
import argparse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import l1_openapi
import l2_jsonld
import l3_consistency
import l4_examples


PASS = "\033[32m✓\033[0m"
FAIL = "\033[31m✗\033[0m"
WARN = "\033[33m!\033[0m"
BOLD = "\033[1m"
RESET = "\033[0m"


def find_v21_root(path: Path) -> Path:
    """
    If path contains a v2.1/ subdirectory, return it.
    Otherwise return path as-is.
    """
    v21 = path / "v2.1"
    if v21.is_dir():
        return v21
    return path


def discover_schema_folders(schema_root: Path):
    """
    Auto-discover schema folders containing attributes.yaml.
    Supports two layouts:
      1. Flat:    schema_root/SchemaName/attributes.yaml
      2. Versioned: schema_root/SchemaName/v2.1/attributes.yaml
    Excludes {domain}-common/ folders (by checking if the name ends with '-common').
    Returns folders sorted alphabetically by schema name.
    """
    folders = []
    for candidate in sorted(schema_root.iterdir()):
        if not candidate.is_dir():
            continue
        if candidate.name.endswith("-common"):
            continue  # Shared type containers — excluded by convention
        # Flat layout: attributes.yaml directly inside
        if (candidate / "attributes.yaml").exists():
            folders.append(candidate)
        else:
            # Versioned layout: look for v2.1/attributes.yaml
            v21_sub = candidate / "v2.1"
            if v21_sub.is_dir() and (v21_sub / "attributes.yaml").exists():
                folders.append(v21_sub)
    return folders


def print_results(layer_name, schema_name, results):
    passed = sum(1 for r in results if r["passed"])
    total  = len(results)
    status = PASS if passed == total else FAIL

    print(f"  {status} {layer_name}  ({passed}/{total} checks passed)")
    for r in results:
        icon = PASS if r["passed"] else FAIL
        detail = r["detail"]
        if r["passed"]:
            print(f"      {icon} {r['check']}: {detail}")
        else:
            print(f"      {icon} {r['check']}:")
            if isinstance(detail, list):
                for d in detail:
                    print(f"           → {d}")
            else:
                print(f"           → {detail}")

    return passed, total


def run_all(schema_root: Path, core_dir: Path):
    grand_pass = 0
    grand_total = 0
    any_failure = False

    # Auto-detect v2.1 subfolder
    schema_root = find_v21_root(schema_root)
    schema_folders = discover_schema_folders(schema_root)

    print(f"\n{BOLD}Beckn v2.1 Generalised Schema Test Suite{RESET}")
    print(f"Schema root : {schema_root}")
    core_note = "" if core_dir.exists() else "  (not found — L4 will be skipped)"
    print(f"Core dir    : {core_dir}{core_note}")
    print(f"Schemas     : {len(schema_folders)} discovered")
    print()

    if not schema_folders:
        print(f"{WARN} No schema folders found (looking for subdirectories with attributes.yaml under {schema_root})")
        return 1

    for schema_dir in schema_folders:
        # For versioned layout (Schema/v2.1/), display the parent name
        display_name = schema_dir.parent.name if schema_dir.name.startswith("v") else schema_dir.name
        print(f"{BOLD}{'─'*60}{RESET}")
        print(f"{BOLD}{display_name}{RESET}")

        r1 = l1_openapi.run(schema_dir)
        p, t = print_results("L1 OpenAPI", display_name, r1)
        grand_pass += p; grand_total += t
        if p < t: any_failure = True

        r2 = l2_jsonld.run(schema_dir)
        p, t = print_results("L2 JSON-LD", display_name, r2)
        grand_pass += p; grand_total += t
        if p < t: any_failure = True

        r3 = l3_consistency.run(schema_dir)
        p, t = print_results("L3 Consistency", display_name, r3)
        grand_pass += p; grand_total += t
        if p < t: any_failure = True

        if core_dir.exists():
            r4 = l4_examples.run(schema_dir, core_dir)
            p, t = print_results("L4 Examples", display_name, r4)
            grand_pass += p; grand_total += t
            if p < t: any_failure = True
        else:
            print(f"  {WARN} L4 Examples: core/ not found — skipping")

        print()

    print(f"{BOLD}{'═'*60}{RESET}")
    overall = PASS if not any_failure else FAIL
    print(f"{BOLD}{overall} Total: {grand_pass}/{grand_total} checks passed{RESET}")
    if any_failure:
        print("   Failures require attention before schema publication.")
    else:
        print("   All checks passed. v2.1 schema pack is consistent and valid.")
    print()

    return 1 if any_failure else 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Beckn v2.1 generalised schema test suite")
    parser.add_argument(
        "--schema-root",
        type=Path,
        default=None,
        help="Root directory containing v2.1 schema folders (default: parent of this script)"
    )
    parser.add_argument(
        "--core",
        type=Path,
        default=None,
        help="Core beckn directory with beckn.yaml and attributes.yaml (default: ../core relative to schema-root)"
    )
    args = parser.parse_args()

    schema_root = args.schema_root or Path(__file__).parent.parent
    core_dir    = args.core or (schema_root.parent / "core")

    sys.exit(run_all(schema_root, core_dir))
