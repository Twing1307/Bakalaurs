from src.mod_8 import add_8, mul_8


def test_mod_8_1():
    assert add_8(2, 2) == 4
    assert mul_8(3, 2) == 6


def test_mod_8_2():
    assert add_8(-1, 1) == 0
    assert mul_8(0, 5) == 0


def test_mod_8_3():
    assert add_8(10, 5) == 15
    assert mul_8(3, 3) == 9


def test_mod_8_4():
    assert add_8(100, -50) == 50
    assert mul_8(2, -3) == -6


def test_mod_8_5():
    assert add_8(0, 0) == 0
    assert mul_8(1, 1) == 1
