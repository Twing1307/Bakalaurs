from pathlib import Path
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parent
ART = ROOT / "artifacts"


def parse_junit(path: Path):
    """
    Support both structure options:
    - <testsuite tests="..." failures="..." errors="..." time="...">...</testsuite>
    - <testsuites> <testsuite .../> <testsuite .../> ... </testsuites>
    """
    tree = ET.parse(path)
    root = tree.getroot()

    def get_attrs(node):
        tests = int(node.attrib.get("tests", 0))
        failures = int(node.attrib.get("failures", 0))
        errors = int(node.attrib.get("errors", 0))
        time = float(node.attrib.get("time", 0.0))
        return tests, failures, errors, time

    if root.tag == "testsuite":
        tests, failures, errors, time = get_attrs(root)
        return tests, failures + errors, time

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

    # fallback: if the format is unexpected
    return 0, 0, 0.0


def parse_coverage(path: Path):
    tree = ET.parse(path)
    root = tree.getroot()
    # coverage.py xml: line-rate attribute in [0..1]
    line_rate = float(root.attrib.get("line-rate", 0.0))
    return line_rate * 100.0


def main():
    full_junit = ART / "full_junit.xml"
    full_cov = ART / "full_coverage.xml"
    part_junit = ART / "partial_junit.xml"
    part_cov = ART / "partial_coverage.xml"

    if not all(p.exists() for p in [full_junit, full_cov, part_junit, part_cov]):
        print("Not all artifacts found in artifacts/ folder.")
        return

    f_tests, f_failed, f_time = parse_junit(full_junit)
    f_cov = parse_coverage(full_cov)

    p_tests, p_failed, p_time = parse_junit(part_junit)
    p_cov = parse_coverage(part_cov)

    print("=== Full run ===")
    print(f"Tests: {f_tests}, failed: {f_failed}, time: {f_time:.3f}s, coverage: {f_cov:.1f}%")
    print("=== Partial (ATI) run ===")
    print(f"Tests: {p_tests}, failed: {p_failed}, time: {p_time:.3f}s, coverage: {p_cov:.1f}%")

    if f_time > 0 and p_time > 0:
        speedup = f_time / p_time
        print(f"\nSpeedup (full / partial): x{speedup:.2f}")

    if f_cov > 0:
        cov_ratio = p_cov / f_cov
        print(f"Coverage retained: {cov_ratio*100:.1f}% of full coverage")


if __name__ == "__main__":
    main()