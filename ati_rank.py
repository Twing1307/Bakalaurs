import argparse
import os
import re
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple

ROOT = Path(__file__).parent
TESTS_DIR = ROOT / "tests"

W1 = 0.6  # delta_loc weight
W2 = 0.2  # defect_rate weight 
W3 = 0.2  # (1 - coverage) weight 

def parse_args():
    parser = argparse.ArgumentParser(
        description="Calculate Adaptive Testing Index (ATI) and select top tests."
    )
    parser.add_argument(
        "--changed-files",
        nargs="+",
        required=True,
        help="List of changed source files (e.g. src/mod_5.py)",
    )
    parser.add_argument(
        "--top-fraction",
        type=float,
        default=0.4,
        help="Fraction of tests to select (0..1). Ignored if --top-n is provided.",
    )
    parser.add_argument(
        "--top-n",
        type=int,
        default=None,
        help="Absolute number of tests to select.",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="selected_tests.txt",
        help="Output file with test paths, one per line.",
    )
    return parser.parse_args()


def git_delta_loc(path: Path) -> int:
    """
    Try to get the number of changed lines using git diff (HEAD~1..HEAD).
    If git is unavailable or the file isn't in the repo, return 0.
    """
    try:
        cmd = ["git", "diff", "--numstat", "HEAD~1..HEAD", str(path)]
        out = subprocess.check_output(cmd, text=True, cwd=str(ROOT))
        total = 0
        for line in out.splitlines():
            parts = line.split("\t")
            if len(parts) >= 3:
                added, deleted, _ = parts
                if added != "-" and deleted != "-":
                    total += int(added) + int(deleted)
        return total
    except Exception:
        return 0


IMPORT_RE = re.compile(r"from\s+src\.([a-zA-Z0-9_]+)\s+import|import\s+src\.([a-zA-Z0-9_\.]+)")


def map_tests_to_modules() -> Dict[Path, Set[str]]:
    """
    A parser: we search tests for lines like
    from src.mod_5 import ...
    and match test file -> set of module names (mod_5, etc.).
    """
    mapping: Dict[Path, Set[str]] = {}
    for test_file in TESTS_DIR.glob("test_*.py"):
        modules: Set[str] = set()
        text = test_file.read_text(encoding="utf-8")
        for m in IMPORT_RE.finditer(text):
            mod1, mod2 = m.groups()
            if mod1:
                modules.add(mod1)
            elif mod2:
                # mod2 can be 'mod_5' or 'mod_5.something'
                modules.add(mod2.split(".")[0])
        if modules:
            mapping[test_file] = modules
    return mapping


def get_defect_rate(_test_file: Path) -> float:
    return 0.0


def get_coverage(_test_file: Path) -> float:
    return 1.0


def compute_ati(
    changed_files: List[Path],
    test_to_modules: Dict[Path, Set[str]],
) -> Dict[Path, float]:
    # normalize the paths: src/mod_5.py -> mod_5
    changed_mod_names: Set[str] = set()
    for p in changed_files:
        if p.suffix == ".py" and p.parent.name == "src":
            changed_mod_names.add(p.stem)

    # Calculate delta_loc for modified modules.
    module_delta: Dict[str, int] = {}
    for mod in changed_mod_names:
        path = ROOT / "src" / f"{mod}.py"
        module_delta[mod] = git_delta_loc(path)

    # If all are 0, to avoid division by 0, we substitute 1
    max_delta = max(module_delta.values()) if module_delta else 0
    if max_delta == 0:
        max_delta = 1

    ati_scores: Dict[Path, float] = {}
    for test_file, modules in test_to_modules.items():
        # Tthe maximum delta_loc among the modules that the test checks.
        raw_delta = max((module_delta.get(m, 0) for m in modules), default=0)
        delta_norm = raw_delta / max_delta

        defect_rate = get_defect_rate(test_file)
        coverage = get_coverage(test_file)

        ati = W1 * delta_norm + W2 * defect_rate + W3 * (1.0 - coverage)
        ati_scores[test_file] = ati

    return ati_scores


def main():
    args = parse_args()

    changed_paths = [Path(p) for p in args.changed_files]
    test_to_modules = map_tests_to_modules()
    if not test_to_modules:
        print("No test -> module mappings found. Did you run gen_demo.py?")
        return

    ati_scores = compute_ati(changed_paths, test_to_modules)

    # sort by ATI in descending order
    ranked: List[Tuple[Path, float]] = sorted(
        ati_scores.items(), key=lambda kv: kv[1], reverse=True
    )

    total_tests = len(ranked)
    if args.top_n is not None:
        k = max(1, min(args.top_n, total_tests))
    else:
        frac = max(0.0, min(1.0, args.top_fraction))
        k = max(1, int(total_tests * frac))

    selected = ranked[:k]

    out_path = ROOT / args.output
    with out_path.open("w", encoding="utf-8") as f:
        for test_file, score in selected:
            # pytest will be able to run by file name
            f.write(f"{test_file.as_posix()}\n")

    print(f"Selected {k}/{total_tests} tests -> {out_path}")
    for test_file, score in selected:
        print(f"{test_file}: ATI={score:.4f}")


if __name__ == "__main__":
    main()