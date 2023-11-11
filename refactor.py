def myBestFunctionToFindModule(test):
    if test[a] < 0:
        return -test[a]
    else:
        return test[a]


if __name__ == "__main__":
    test = [-15, -1, 0, 1, 15]
    for a in range(len(test)):
        assert myBestFunctionToFindModule(test) == abs(test[a])
