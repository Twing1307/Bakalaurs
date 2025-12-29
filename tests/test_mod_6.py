from src.mod_6 import add_6, mul_6


def test_mod_6_1():
    assert add_6(2, 2) == 4
    assert mul_6(3, 2) == 6


def test_mod_6_2():
    assert add_6(-1, 1) == 0
    assert mul_6(0, 5) == 0


def test_mod_6_3():
    assert add_6(10, 5) == 15
    assert mul_6(3, 3) == 9


def test_mod_6_4():
    assert add_6(100, -50) == 50
    assert mul_6(2, -3) == -6


def test_mod_6_5():
    assert add_6(0, 0) == 0
    assert mul_6(1, 1) == 1
