import unittest
import FAST


class MyTestCase(unittest.TestCase):
    def test_does_it_work_at_all(self):
        test = FAST.fast_test_preliminary([100, 50, 50, 50, 50], 25)
        self.assertEqual(True, test)  # add assertion here

    def test_different_parity(self):
        test = FAST.fast_test_preliminary([100, 50, 150, 50, 150], 25)
        self.assertEqual(False, test)  # add assertion here


if __name__ == '__main__':
    unittest.main()
