def myBestFunctionToFindModule:
    if a < 0:
        return -a
    return a



if __name__ = "__main__":
    test = [-15 -1 0 1 15]
    for test in test:
        assert mybestfunctiontofindmodule(test) == abs(test)
