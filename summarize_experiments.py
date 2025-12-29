from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
ART = ROOT / "artifacts"

FRACTIONS = [20, 40, 60, 80]

SCENARIO_INFO = {
    1: "Vienas moduļa izmaiņas (mod_5)",
    2: "Trīs moduļu izmaiņas (mod_1, mod_3, mod_7)",
}


def parse_junit(path: Path):
    if not path.exists():
        return 0, 0, 0.0
    tree = ET.parse(path)
    root = tree.getroot()

    def get_attrs(node):
        tests = int(node.attrib.get("tests", 0))
        failures = int(node.attrib.get("failures", 0))
        errors = int(node.attrib.get("errors", 0))
        time = float(node.attrib.get("time", 0.0))
        return tests, failures, errors, time

    if root.tag == "testsuite":
        t, f, e, tm = get_attrs(root)
        return t, f + e, tm

    if root.tag == "testsuites":
        total_tests = total_failures = total_errors = 0
        total_time = 0.0
        for ts in root.findall("testsuite"):
            t, f, e, tm = get_attrs(ts)
            total_tests += t
            total_failures += f
            total_errors += e
            total_time += tm
        return total_tests, total_failures + total_errors, total_time

    return 0, 0, 0.0


def parse_coverage(path: Path):
    if not path.exists():
        return 0.0
    tree = ET.parse(path)
    root = tree.getroot()
    line_rate = float(root.attrib.get("line-rate", 0.0))
    return line_rate * 100.0


def main():
    full_junit = ART / "full_junit.xml"
    full_cov = ART / "full_coverage.xml"

    f_tests, f_failed, f_time = parse_junit(full_junit)
    f_cov = parse_coverage(full_cov)

    print("=== Pilnais tests ===")
    print(f"Tests: {f_tests}, failed: {f_failed}, time: {f_time:.3f}s, coverage: {f_cov:.1f}%\n")

    print("=== Eksperimentu kopsavilkums ===")
    print("Scenario;Fraction%;Tests;Time_s;Coverage%;Speedup;Coverage_retention%")

    for sid, desc in SCENARIO_INFO.items():
        for frac in FRACTIONS:
            junit_path = ART / f"partial_s{sid}_f{frac}_junit.xml"
            cov_path = ART / f"partial_s{sid}_f{frac}_coverage.xml"

            p_tests, p_failed, p_time = parse_junit(junit_path)
            p_cov = parse_coverage(cov_path)

            if p_tests == 0 and p_time == 0 and p_cov == 0:
                continue

            speedup = (f_time / p_time) if (f_time > 0 and p_time > 0) else 0.0
            cov_ret = (p_cov / f_cov * 100.0) if f_cov > 0 else 0.0

            print(
                f"{sid}-{desc};{frac};{p_tests};{p_time:.3f};{p_cov:.1f};"
                f"{speedup:.2f};{cov_ret:.1f}"
            )


if __name__ == "__main__":
    main()