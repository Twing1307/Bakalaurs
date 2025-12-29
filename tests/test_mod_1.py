from src.mod_1 import add_1, mul_1


def test_mod_1_1():
    assert add_1(2, 2) == 4
    assert mul_1(3, 2) == 6


def test_mod_1_2():
    assert add_1(-1, 1) == 0
    assert mul_1(0, 5) == 0


def test_mod_1_3():
    assert add_1(10, 5) == 15
    assert mul_1(3, 3) == 9


def test_mod_1_4():
    assert add_1(100, -50) == 50
    assert mul_1(2, -3) == -6


def test_mod_1_5():
    assert add_1(0, 0) == 0
    assert mul_1(1, 1) == 1
