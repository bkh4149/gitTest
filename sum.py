def sum_range(start, end):
    return sum(range(start, end + 1))


def factorial(n):
    if n < 0:
        raise ValueError("n must be a non-negative integer")
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result


if __name__ == "__main__":
    print(sum_range(1, 10))
