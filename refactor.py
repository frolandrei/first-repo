def my_abs(a: int | float):
    if a < 0:
        return -a
    return a


if __name__ == "__main__":
    test = [-15, -1, 0, 1, 15]
    for a in test:
        assert my_abs(a) == abs(a)
