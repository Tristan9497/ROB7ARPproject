import unittest
import FAST

n = 11
test_detector = FAST.Detector(n)


class MyTestCase(unittest.TestCase):
    def test_does_it_work_at_all(self):
        test = test_detector.test_preliminary([100, 50, 50, 50, 50])
        self.assertEqual(True, test)  # add assertion here

    def test_different_parity(self):
        test = test_detector.test_preliminary([100, 50, 150, 50, 150])
        self.assertEqual(False, test)  # add assertion here

    def test_continous(self):
        test = test_detector.check_continous(100, [150, 150, 150, 150,
                                                 150, 150, 150, 150,
                                                 150, 150, 150, 100,
                                                 100, 100, 100, 100, ])
        self.assertTrue(test, "there was one, did not find it")
        test2 = test_detector.check_continous(100, [150, 150, 150, 150,
                                                 150, 100, 150, 150,
                                                 150, 100, 100, 100,
                                                 100, 100, 100, 100, ])
        self.assertFalse(test2, "There wasn't one, but I found one??")

    def test_continous_tricky(self):
        test = test_detector.check_continous(100, [150, 150, 150, 150,
                                                   150, 150, 150, 100,
                                                   100, 100, 150, 100,
                                                   150, 150, 150, 150, ])
        self.assertTrue(test, "there was one, did not find it")


if __name__ == '__main__':
    unittest.main()
