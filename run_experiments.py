import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).parent
ART = ROOT / "artifacts"
ART.mkdir(exist_ok=True)

# 2 scenāriji: viens modulis un trīs moduļi
SCENARIOS = [
    {
        "id": 1,
        "name": "single_mod5",
        "changed_files": ["src/mod_5.py"],
    },
    {
        "id": 2,
        "name": "multi_mod1_3_7",
        "changed_files": ["src/mod_1.py", "src/mod_3.py", "src/mod_7.py"],
    },
]

FRACTIONS = [0.2, 0.4, 0.6, 0.8]


def run():
    print("Running ATI experiments...")
    for scenario in SCENARIOS:
        sid = scenario["id"]
        changed = scenario["changed_files"]
        print(f"\n=== Scenario {sid}: changed_files={changed} ===")

        for frac in FRACTIONS:
            frac_pct = int(frac * 100)
            print(f"\n  -> top_fraction = {frac} ({frac_pct}%)")

            selected_path = ROOT / f"selected_s{sid}_f{frac_pct}.txt"

            # 1) ATI aprēķins un testu atlase
            cmd_ati = [
                sys.executable,
                "ati_rank.py",
                "--changed-files",
                *changed,
                "--top-fraction",
                str(frac),
                "--output",
                str(selected_path),
            ]
            print("  Running:", " ".join(cmd_ati))
            subprocess.run(cmd_ati, check=True)

            if not selected_path.exists():
                print(f"  [WARN] {selected_path} not created, skipping pytest")
                continue

            tests = [
                line.strip()
                for line in selected_path.read_text(encoding="utf-8").splitlines()
                if line.strip()
            ]
            if not tests:
                print(f"  [WARN] No tests in {selected_path}, skipping pytest")
                continue

            junit_path = ART / f"partial_s{sid}_f{frac_pct}_junit.xml"
            cov_path = ART / f"partial_s{sid}_f{frac_pct}_coverage.xml"

            # 2) pytest tikai izvēlētajiem testiem
            cmd_pytest = [
                "pytest",
                "-q",
                *tests,
                "--durations=0",
                f"--junitxml={junit_path}",
                "--cov=src",
                f"--cov-report=xml:{cov_path}",
            ]
            print("  Running:", " ".join(cmd_pytest))
            subprocess.run(cmd_pytest, check=True)

    print("\nAll experiments finished.")


if __name__ == "__main__":
    run()