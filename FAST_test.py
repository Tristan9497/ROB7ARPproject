import unittest
import FAST


class MyTestCase(unittest.TestCase):
    def test_does_it_work_at_all(self):
        test = FAST.fast_test_preliminary([100, 50, 50, 50, 50], 25)
        self.assertEqual(True, test)  # add assertion here

    def test_different_parity(self):
        test = FAST.fast_test_preliminary([100, 50, 150, 50, 150], 25)
        self.assertEqual(False, test)  # add assertion here

    def test_continous_9(self):
        test = FAST.fast_check_continous_9(100, [150, 150, 150, 150,
                                                 150, 150, 150, 150,
                                                 150, 100, 100, 100,
                                                 100, 100, 100, 100, ], 25)
        self.assertTrue(test, "there was one, found it")
        test2 = FAST.fast_check_continous_9(100, [150, 150, 150, 150,
                                                 150, 100, 150, 150,
                                                 150, 100, 100, 100,
                                                 100, 100, 100, 100, ], 25)
        self.assertFalse(test2, "There wasn't one, didn't found one")


if __name__ == '__main__':
    unittest.main()
