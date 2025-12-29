from src.mod_5 import add_5, mul_5


def test_mod_5_1():
    assert add_5(2, 2) == 4
    assert mul_5(3, 2) == 6


def test_mod_5_2():
    assert add_5(-1, 1) == 0
    assert mul_5(0, 5) == 0


def test_mod_5_3():
    assert add_5(10, 5) == 15
    assert mul_5(3, 3) == 9


def test_mod_5_4():
    assert add_5(100, -50) == 50
    assert mul_5(2, -3) == -6


def test_mod_5_5():
    assert add_5(0, 0) == 0
    assert mul_5(1, 1) == 1
