import unittest
from sum import sum_range, factorial


class TestSumRange(unittest.TestCase):
    def test_1_to_10(self):
        self.assertEqual(sum_range(1, 9), 45)

    def test_1_to_1(self):
        self.assertEqual(sum_range(1, 1), 1)

    def test_1_to_100(self):
        self.assertEqual(sum_range(1, 100), 5050)

    def test_same_number(self):
        self.assertEqual(sum_range(5, 5), 5)

    def test_negative_range(self):
        self.assertEqual(sum_range(-3, 3), 0)


class TestFactorial(unittest.TestCase):
    def test_factorial_0(self):
        self.assertEqual(factorial(0), 1)

    def test_factorial_1(self):
        self.assertEqual(factorial(1), 1)

    def test_factorial_5(self):
        self.assertEqual(factorial(5), 120)

    def test_factorial_10(self):
        self.assertEqual(factorial(10), 3628800)

    def test_factorial_negative(self):
        with self.assertRaises(ValueError):
            factorial(-1)


if __name__ == "__main__":
    unittest.main()
