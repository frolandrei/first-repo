def my_abs(value: int | float):
    if value < 0:
        return -value
    return value


if __name__ == "__main__":
    bad_tests = 0
    if my_abs(-1) != 1: bad_tests += 1
    if my_abs(0)  != 0: bad_tests += 1
    if my_abs(1)  != 1: bad_tests += 1
    if my_abs(-1.0) != 1.0: bad_tests += 1
    if my_abs(0.0)  != 0.0: bad_tests += 1
    if str(my_abs(-0.0))  != str(0.0): bad_tests += 1
    print(f"Количество непройденных тестов: {bad_tests}")

