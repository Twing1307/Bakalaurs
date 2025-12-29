# gen_demo.py
import os
from pathlib import Path

ROOT = Path(__file__).parent
SRC = ROOT / "src"
TESTS = ROOT / "tests"


def ensure_dirs():
    SRC.mkdir(exist_ok=True)
    TESTS.mkdir(exist_ok=True)


MOD_TEMPLATE = """def add_{i}(a, b):
    return a + b


def mul_{i}(a, b):
    return a * b
"""


TEST_TEMPLATE = """from src.mod_{i} import add_{i}, mul_{i}


def test_mod_{i}_1():
    assert add_{i}(2, 2) == 4
    assert mul_{i}(3, 2) == 6


def test_mod_{i}_2():
    assert add_{i}(-1, 1) == 0
    assert mul_{i}(0, 5) == 0


def test_mod_{i}_3():
    assert add_{i}(10, 5) == 15
    assert mul_{i}(3, 3) == 9


def test_mod_{i}_4():
    assert add_{i}(100, -50) == 50
    assert mul_{i}(2, -3) == -6


def test_mod_{i}_5():
    assert add_{i}(0, 0) == 0
    assert mul_{i}(1, 1) == 1
"""


def create_modules_and_tests(num_modules: int = 10):
    for i in range(num_modules):
        mod_path = SRC / f"mod_{i}.py"
        test_path = TESTS / f"test_mod_{i}.py"

        if not mod_path.exists():
            mod_path.write_text(MOD_TEMPLATE.format(i=i), encoding="utf-8")

        if not test_path.exists():
            test_path.write_text(TEST_TEMPLATE.format(i=i), encoding="utf-8")


if __name__ == "__main__":
    ensure_dirs()
    create_modules_and_tests()
    print("Demo project generated: src/mod_*.py and tests/test_mod_*.py")