# Bakalaura darba demonstrācijas projekts

Šis repozitorijs satur bakalaura darba praktiskās daļas demonstrācijas projektu, kas izmantots adaptīvās testēšanas indeksa (ATI) pieejas novērtēšanai nepārtrauktās integrācijas (CI) kontekstā.

Projekts kalpo kā kontrolēta eksperimentālā vide, lai salīdzinātu pilnu regresijas testēšanu ar daļēju testēšanu, izmantojot ATI balstītu testu atlasi.

---

## Projekta struktūra

- `src/` – demonstrācijas moduļi (10 Python moduļi)
- `tests/` – PyTest testu komplekts (50 testi)
- `ati_rank.py` – ATI aprēķina un testu atlases skripts
- `run_experiments.py` – eksperimentu automatizēta izpilde dažādos izmaiņu scenārijos
- `summarize_experiments.py` – rezultātu apkopošana un tabulu ģenerēšana
- `artifacts/` – JUnit un koda pārklājuma (coverage) XML artefakti

---

## Prasības

- Python **3.10 vai jaunāka versija**
- PyTest
- pytest-cov (koda pārklājuma mērīšanai)

---

## Uzstādīšana

1. Klonējiet repozitoriju:
```bash
git clone https://github.com/Twing1307/Bakalaurs.git
cd Bakalaurs/ati-demo
```

---

## Izveidojiet un aktivizējiet virtuālo vidi:
```bash
python -m venv .venv
```
## Windows
```bash
.venv\Scripts\activate
```
## Linux / macOS:
```bash
source .venv/bin/activate
```
## Instalējiet nepieciešamās bibliotēkas:
```bash
pip install -r requirements.txt
```

---

## Pilna testu komplekta palaišana
```bash
pytest
```
## Eksperimentu palaišana (ATI balstīta testu atlase)
```bash
python run_experiments.py
```

---

## Eksperimentu rezultātu apkopošana
```bash
python summarize_experiments.py
```
