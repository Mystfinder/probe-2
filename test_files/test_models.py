from probe import models
from probe import matrices
import unittest


class LinearRegressionTest(unittest.TestCase):
    def test_results(self):
        X = matrices.Matrix([[1], [2], [3], [4], [5]])
        Y = matrices.Matrix([[1, 2, 1.3, 3.75, 2.25]])
        z = matrices.Matrix([[2]])

        L = models.LinearRegression(Y, X)

        result = L.predict(z)

        self.assertTrue(1.63 < result and result < 1.64)


class ANOVATest(unittest.TestCase):
    def test_results(self):
        factors = ["X", "Y", "Z"]
        all_data = [[1, 2, 2], [5, 6, 5], [2, 1]]

        anova = models.ANOVA(factors, all_data)

        self.assertTrue(35.68 < anova.F and anova.F < 35.69)
        result_1 = anova.decision(0.95)

        self.assertEqual("Reject null hypothesis.", result_1)


if __name__ == '__main__':
    unittest.main()
