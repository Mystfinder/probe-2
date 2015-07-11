from probe import hypotheses
import unittest


class ConfidenceIntervalTest(unittest.TestCase):
    def test_results(self):
        data = [6, 12, 9, 2, 4, 9, 15, 3, 9, 3, 4, 2, 8, 4]

        result_1 = hypotheses.confidence_interval(data, 0.95, 2)
        result_2 = hypotheses.confidence_interval(data, 0.95, 1)

        self.assertTrue(4.33 < result_1[0] and result_1[0] < 4.34)
        self.assertTrue(8.52 < result_1[1] and result_1[1] < 8.53)

        self.assertTrue(6.897 < result_2 and result_2 < 6.898)


class ConfidenceIntervalTheoreticalTest(unittest.TestCase):
    def test_results(self):
        n = 130
        mean = 98.249
        std_dev = 0.733
        result_1 = hypotheses.confidence_interval_theoretical(n,
                                                              mean, std_dev,
                                                              0.95, 2)
        result_2 = hypotheses.confidence_interval_theoretical(n,
                                                              mean, std_dev,
                                                              0.95, 1, 5)

        self.assertTrue(98.12 < result_1[0] and result_1[0] < 98.13)
        self.assertTrue(98.37 < result_1[1] and result_1[1] < 98.38)
        self.assertTrue(98.96 < result_2 and result_2 < 98.98)


if __name__ == '__main__':
    unittest.main()
