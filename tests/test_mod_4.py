from src.mod_4 import add_4, mul_4


def test_mod_4_1():
    assert add_4(2, 2) == 4
    assert mul_4(3, 2) == 6


def test_mod_4_2():
    assert add_4(-1, 1) == 0
    assert mul_4(0, 5) == 0


def test_mod_4_3():
    assert add_4(10, 5) == 15
    assert mul_4(3, 3) == 9


def test_mod_4_4():
    assert add_4(100, -50) == 50
    assert mul_4(2, -3) == -6


def test_mod_4_5():
    assert add_4(0, 0) == 0
    assert mul_4(1, 1) == 1
