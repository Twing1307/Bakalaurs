# plot_results.py
# Builds a readable figure from artifacts/*_junit.xml and artifacts/*_coverage.xml
# Output: .\figures\att_4_2.png (two Y-axes: TET and CR)

from pathlib import Path
import re
import xml.etree.ElementTree as ET
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
ART = ROOT / "artifacts"
OUT_DIR = ROOT / "figures"
OUT_DIR.mkdir(exist_ok=True)

def junit_time_seconds(p: Path) -> float:
    root = ET.parse(p).getroot()

    # Prefer testsuite time
    suites = []
    if root.tag.endswith("testsuites"):
        suites = list(root.findall(".//testsuite"))
    elif root.tag.endswith("testsuite"):
        suites = [root]
    else:
        suites = list(root.findall(".//testsuite"))

    total = 0.0
    got = False
    for ts in suites:
        t = ts.attrib.get("time")
        if t is not None:
            try:
                total += float(t)
                got = True
            except ValueError:
                pass
    if got and total > 0:
        return total

    # Fallback: sum testcase times
    total = 0.0
    for tc in root.findall(".//testcase"):
        t = tc.attrib.get("time")
        if not t:
            continue
        try:
            total += float(t)
        except ValueError:
            pass
    return total

def coverage_percent(p: Path) -> float:
    root = ET.parse(p).getroot()
    lr = root.attrib.get("line-rate")
    if lr is None:
        m = root.find(".//metrics")
        lr = m.attrib.get("line-rate") if m is not None else None
    if lr is None:
        raise ValueError(f"Nav atrasts 'line-rate' coverage XML failā: {p}")
    return float(lr) * 100.0

def fraction_from_name(p: Path) -> int | None:
    # expected: ..._f20_... or ...f20... (yours: partial_s1_f20_junit.xml)
    m = re.search(r"(?:^|[_-])f(20|40|60|80)(?:[_-]|\.|$)", p.name.lower())
    return int(m.group(1)) if m else None

if not ART.exists():
    raise FileNotFoundError(f"Nav mapes: {ART}")

junits = sorted(ART.glob("*junit.xml"))
covs = sorted(ART.glob("*coverage.xml"))

if not junits or not covs:
    raise FileNotFoundError(
        "Nav atrasti *junit.xml vai *coverage.xml mapē artifacts.\n"
        "Pārliecinieties, ka pytest tika palaists ar --junitxml=... un --cov-report=xml:..."
    )

by_frac = {}  # frac -> {"tet": ..., "cr": ...}

for p in junits:
    f = fraction_from_name(p)
    if f is None:
        continue
    by_frac.setdefault(f, {})["tet"] = junit_time_seconds(p)

for p in covs:
    f = fraction_from_name(p)
    if f is None:
        continue
    by_frac.setdefault(f, {})["cr"] = coverage_percent(p)

points = [(f, d["tet"], d["cr"]) for f, d in by_frac.items() if "tet" in d and "cr" in d]
points.sort(key=lambda x: x[0])

if not points:
    found = "\n".join([f" - {p.name}" for p in (junits[:10] + covs[:10])])
    raise ValueError(
        "Neizdevās savākt punktus 20/40/60/80. Pārbaudiet failu nosaukumus artifacts mapē.\n"
        "Failu piemēri:\n" + found
    )

x = [p[0] for p in points]
tet = [p[1] for p in points]
cr = [p[2] for p in points]

# --- Plot 1: TET only ---
fig1, ax = plt.subplots()
ax.plot(x, tet, marker="o", linestyle="-")
ax.set_xlabel("Atlasīto testu daļa (%)")
ax.set_ylabel("TET (s)")
ax.set_title("TET atkarībā no atlasīto testu daļas")
ax.grid(True, alpha=0.3)
fig1.tight_layout()

out1 = OUT_DIR / "att_4_2a_TET.png"
plt.savefig(out1, dpi=200)
plt.close(fig1)

# --- Plot 2: CR only ---
fig2, ax = plt.subplots()
ax.plot(x, cr, marker="s", linestyle="--")
ax.set_xlabel("Atlasīto testu daļa (%)")
ax.set_ylabel("CR (%)")
ax.set_title("CR atkarībā no atlasīto testu daļas")
ax.grid(True, alpha=0.3)
fig2.tight_layout()

out2 = OUT_DIR / "att_4_2b_CR.png"
plt.savefig(out2, dpi=200)
plt.close(fig2)

print(f"Saglabāti grafiki:\n - {out1}\n - {out2}")

