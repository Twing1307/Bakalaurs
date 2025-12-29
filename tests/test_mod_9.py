from src.mod_9 import add_9, mul_9


def test_mod_9_1():
    assert add_9(2, 2) == 4
    assert mul_9(3, 2) == 6


def test_mod_9_2():
    assert add_9(-1, 1) == 0
    assert mul_9(0, 5) == 0


def test_mod_9_3():
    assert add_9(10, 5) == 15
    assert mul_9(3, 3) == 9


def test_mod_9_4():
    assert add_9(100, -50) == 50
    assert mul_9(2, -3) == -6


def test_mod_9_5():
    assert add_9(0, 0) == 0
    assert mul_9(1, 1) == 1
