from src.mod_7 import add_7, mul_7


def test_mod_7_1():
    assert add_7(2, 2) == 4
    assert mul_7(3, 2) == 6


def test_mod_7_2():
    assert add_7(-1, 1) == 0
    assert mul_7(0, 5) == 0


def test_mod_7_3():
    assert add_7(10, 5) == 15
    assert mul_7(3, 3) == 9


def test_mod_7_4():
    assert add_7(100, -50) == 50
    assert mul_7(2, -3) == -6


def test_mod_7_5():
    assert add_7(0, 0) == 0
    assert mul_7(1, 1) == 1
