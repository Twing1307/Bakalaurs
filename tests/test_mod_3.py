from src.mod_3 import add_3, mul_3


def test_mod_3_1():
    assert add_3(2, 2) == 4
    assert mul_3(3, 2) == 6


def test_mod_3_2():
    assert add_3(-1, 1) == 0
    assert mul_3(0, 5) == 0


def test_mod_3_3():
    assert add_3(10, 5) == 15
    assert mul_3(3, 3) == 9


def test_mod_3_4():
    assert add_3(100, -50) == 50
    assert mul_3(2, -3) == -6


def test_mod_3_5():
    assert add_3(0, 0) == 0
    assert mul_3(1, 1) == 1
