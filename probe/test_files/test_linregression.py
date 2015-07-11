from probe import linregression
from probe import matrices
import unittest


class AddToMatrixForInterceptTest(unittest.TestCase):
    def test_results(self):
        matrix = matrices.Matrix([[1], [2], [3], [4], [5]])

        result = linregression.add_to_matrix_for_intercept(matrix)

        self.assertTrue([[1, 1], [1, 2], [1, 3], [1, 4], [1, 5]], result)


class CoeficentsEstimationTest(unittest.TestCase):
    def test_results(self):
        matrix_1 = matrices.Matrix([[1], [2], [3], [4], [5]])
        matrix_2 = matrices.Matrix([[1, 2, 1.3, 3.75, 2.25]])

        result = linregression.coeficents_estimation(matrix_2, matrix_1)

        self.assertTrue(0.78 < result[0][0] and result[0][0] < 0.79)
        self.assertTrue(0.42 < result[0][1] and result[0][1] < 0.43)


if __name__ == '__main__':
    unittest.main()
