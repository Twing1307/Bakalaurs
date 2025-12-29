from src.mod_2 import add_2, mul_2


def test_mod_2_1():
    assert add_2(2, 2) == 4
    assert mul_2(3, 2) == 6


def test_mod_2_2():
    assert add_2(-1, 1) == 0
    assert mul_2(0, 5) == 0


def test_mod_2_3():
    assert add_2(10, 5) == 15
    assert mul_2(3, 3) == 9


def test_mod_2_4():
    assert add_2(100, -50) == 50
    assert mul_2(2, -3) == -6


def test_mod_2_5():
    assert add_2(0, 0) == 0
    assert mul_2(1, 1) == 1
