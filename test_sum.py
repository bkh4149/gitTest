import unittest
from sum import sum_range


class TestSumRange(unittest.TestCase):
    def test_1_to_10(self):
        self.assertEqual(sum_range(1, 10), 55)

    def test_1_to_1(self):
        self.assertEqual(sum_range(1, 1), 1)

    def test_1_to_100(self):
        self.assertEqual(sum_range(1, 100), 5050)

    def test_same_number(self):
        self.assertEqual(sum_range(5, 5), 5)

    def test_negative_range(self):
        self.assertEqual(sum_range(-3, 3), 0)


if __name__ == "__main__":
    unittest.main()
