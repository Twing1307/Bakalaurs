from src.mod_0 import add_0, mul_0


def test_mod_0_1():
    assert add_0(2, 2) == 4
    assert mul_0(3, 2) == 6


def test_mod_0_2():
    assert add_0(-1, 1) == 0
    assert mul_0(0, 5) == 0


def test_mod_0_3():
    assert add_0(10, 5) == 15
    assert mul_0(3, 3) == 9


def test_mod_0_4():
    assert add_0(100, -50) == 50
    assert mul_0(2, -3) == -6


def test_mod_0_5():
    assert add_0(0, 0) == 0
    assert mul_0(1, 1) == 1
