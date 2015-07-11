from probe import formaltests
import unittest


class FormaltestsErrorsTest(unittest.TestCase):
    def test_print(self):
        formal_error = formaltests.FormaltestsError()
        percentile_error = formaltests.PercentileError()

        print(formal_error)
        print(percentile_error)


class ShapiroWilkTest(unittest.TestCase):
    def test_results(self):
        data = [1, 4, 4, 4, 6, 7, 8, 2, 8]

        with self.assertRaises(formaltests.PercentileError):
            formaltests.shapiro_wilk_test(data, -2)

        formaltests.shapiro_wilk_test(data, 0.95)


class KolmogorovSmirnovTest(unittest.TestCase):
    def test_results(self):
        data = [1, 4, 4, 4, 6, 7, 8, 2, 8]
        dist = distributions.NormalDistribution(0, 1)

        with self.assertRaises(formaltests.PercentileError):
            formaltests.kolmogorov_smirnov_test(data, dist, -2)

        result = formaltests.kolmogorov_smirnov_test(data, dist, 0.95)
        self.assertTrue(False is result)


if __name__ == '__main__':
    unittest.main()
