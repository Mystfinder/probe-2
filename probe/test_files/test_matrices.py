from probe import matrices
import unittest
import math


class MatricesErrorsTest(unittest.TestCase):
    def test_print(self):
        matrices_error = matrices.MatricesError()
        not_a_row_error = matrices.NotARowError()
        empty_row_error = matrices.EmptyRowError()
        not_a_matrix_error = matrices.NotAMatrixError()
        incorrect_error = matrices.IncorrectInputError()
        no_inverse_error = matrices.NoInverseError()
        not_valid_error = matrices.NonValidMatricesForMultiplicationError()

        print(matrices_error)
        print(not_a_row_error)
        print(empty_row_error)
        print(not_a_matrix_error)
        print(incorrect_error)
        print(no_inverse_error)
        print(not_valid_error)


class InitTest(unittest.TestCase):
    def test_input(self):
        input_bad_list = []
        input_string = "not a list"
        input_different_length = [[1, 2, 3], [3, 4, 5], [1]]
        input_incorrect_1 = [[1, 2, 3], "string"]
        input_incorrect_2 = [[1, 2, "fail"], [4, 5, 6]]

        with self.assertRaises(matrices.NotAMatrixError):
                matrices.Matrix(input_bad_list)
        with self.assertRaises(matrices.NotAMatrixError):
                matrices.Matrix(input_string)
        with self.assertRaises(matrices.NotAMatrixError):
                matrices.Matrix(input_different_length)
        with self.assertRaises(matrices.NotAMatrixError):
                matrices.Matrix(input_incorrect_1)
        with self.assertRaises(matrices.NotAMatrixError):
                matrices.Matrix(input_incorrect_2)


class TransposedTest(unittest.TestCase):
    def test_result(self):
        a_matrix_1 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        a_matrix_2 = matrices.Matrix([[]])
        a_matrix_3 = matrices.Matrix([[666]])

        self.assertTrue(a_matrix_1 != a_matrix_1.transposed())
        self.assertEqual([[1, 4, 7], [2, 5, 8], [3, 6, 9]],
                         a_matrix_1.transposed().matrix)

        with self.assertRaises(matrices.EmptyRowError):
            a_matrix_2.transposed()

        self.assertTrue(a_matrix_3 != a_matrix_3.transposed())
        self.assertEqual([[666]], a_matrix_3.transposed().matrix)


class TransposeTest(unittest.TestCase):
    def test_result(self):
        a_matrix_1 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
        a_matrix_2 = matrices.Matrix([[]])
        a_matrix_3 = matrices.Matrix([[666]])

        self.assertTrue(a_matrix_1 == a_matrix_1.transpose())
        a_matrix_1.transpose()
        self.assertEqual([[1, 4, 7], [2, 5, 8], [3, 6, 9]],
                         a_matrix_1.transpose().matrix)

        with self.assertRaises(matrices.EmptyRowError):
            a_matrix_2.transpose()

        self.assertTrue(a_matrix_3 == a_matrix_3.transpose())
        self.assertEqual([[666]], a_matrix_3.transpose().matrix)


class TruncatedMatrixTest(unittest.TestCase):
        def test_result(self):
            a_matrix_1 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

            self.assertTrue(a_matrix_1 != a_matrix_1.truncated_matrix(3, 2))
            self.assertEqual([[1, 3], [4, 6]],
                             a_matrix_1.truncated_matrix(3, 2).matrix)

            self.assertTrue((a_matrix_1, 8) != a_matrix_1.truncated_matrix(3, 2,
                                                                           True))

            the_tuple = a_matrix_1.truncated_matrix(3, 2, True)
            self.assertEqual(([[1, 3], [4, 6]], 8),
                             (the_tuple[0].matrix, the_tuple[1]))


class TruncateMatrixTest(unittest.TestCase):
        def test_result(self):
            a_matrix_1 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            a_matrix_2 = matrices.Matrix([[1, 2, 3, 33],
                                          [4, 5, 6, 66], [7, 8, 9, 99]])
            reserve_1 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            reserve_2 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            reserve_3 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])

            self.assertTrue(a_matrix_1 == a_matrix_1.truncate_matrix(3, 2))
            a_matrix_1 = reserve_1
            self.assertEqual([[1, 3], [4, 6]],
                             a_matrix_1.truncate_matrix(3, 2).matrix)
            a_matrix_1 = reserve_2

            self.assertEqual([[4, 5], [7, 8]],
                             a_matrix_2.truncate_matrix(1, 3).matrix)

            self.assertTrue((a_matrix_1, 8) == a_matrix_1.truncate_matrix(3, 2,
                                                                          True))
            a_matrix_1 = reserve_3

            the_tuple = a_matrix_1.truncate_matrix(3, 2, True)
            self.assertEqual(([[1, 3], [4, 6]], 8),
                             (the_tuple[0].matrix, the_tuple[1]))


class SimpleDeterminantTest(unittest.TestCase):
        def test_result(self):
            a_matrix_1 = matrices.Matrix([[0, 0], [1, 2]])
            a_matrix_2 = matrices.Matrix([[3, -6], [-5, 6]])
            a_matrix_3 = matrices.Matrix([[3]])

            self.assertEqual(0, matrices.Matrix.simple_determinant(a_matrix_1))
            self.assertEqual(-12, matrices.Matrix.simple_determinant(a_matrix_2))
            self.assertEqual(3, matrices.Matrix.simple_determinant(a_matrix_3))


class ExpandRowTest(unittest.TestCase):
        def test_result(self):
            a_matrix_1 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            invalid_matrix_1 = matrices.Matrix([[2, 3, 4], [-5, 2, 0]])
            invalid_matrix_2 = matrices.Matrix([[2, 3], [-5, 2], [3, 3]])

            multiplier_list = []
            matrices_list = []

            for element in a_matrix_1.expand_row():
                multiplier_list.append(element[0])
                matrices_list.append(element[1].matrix)

            self.assertEqual((1, [[5, 6], [8, 9]]),
                             (multiplier_list[0], matrices_list[0]))
            self.assertEqual((-2, [[4, 6], [7, 9]]),
                             (multiplier_list[1], matrices_list[1]))
            self.assertEqual((3, [[4, 5], [7, 8]]),
                             (multiplier_list[2], matrices_list[2]))

            with self.assertRaises(matrices.IncorrectInputError):
                invalid_matrix_1.expand_row()
            with self.assertRaises(matrices.IncorrectInputError):
                invalid_matrix_2.expand_row()


class FindDeterminantTest(unittest.TestCase):
        def test_result(self):
            a_matrix_1 = matrices.Matrix([[32, 2, 3], [-12, 5, 6], [7, 8, -9]])
            a_matrix_2 = matrices.Matrix([[5, 2, 3], [4, 5, 6], [7, 8, 9]])
            a_matrix_3 = matrices.Matrix([[1, 2, 3], [4, 5, 6], [7, 8, 9]])
            invalid_matrix_1 = matrices.Matrix([[2, 32, 4], [-5, 2, -12]])
            invalid_matrix_2 = matrices.Matrix([[2, 32], [-5, 22], [0, -2]])
            simple_matrix = matrices.Matrix([[2]])

            a_matrix_1.find_determinant()
            a_matrix_2.find_determinant()
            a_matrix_3.find_determinant()
            result = simple_matrix.find_determinant(True)

            with self.assertRaises(matrices.IncorrectInputError):
                invalid_matrix_1.find_determinant()
            with self.assertRaises(matrices.IncorrectInputError):
                invalid_matrix_2.find_determinant()

            self.assertEqual(-3501, a_matrix_1.determinant)
            self.assertEqual(-12, a_matrix_2.determinant)
            self.assertEqual(0, a_matrix_3.determinant)

            self.assertEqual(2, result[0])
            self.assertEqual((1, [[2]]), (result[1][0][0],
                                          result[1][0][1].matrix))


class FindInverseTest(unittest.TestCase):
    def test_result(self):
        a_matrix_1x1 = matrices.Matrix([[-6]])
        a_matrix_2x2 = matrices.Matrix([[32, 2], [-12, 5]])
        a_matrix_3x3 = matrices.Matrix([[5, 2, 3], [4, 5, 6], [7, 8, 9]])
        a_matrix_zero_determinant = matrices.Matrix([[1, 2, 3],
                                                    [4, 5, 6], [7, 8, 9]])
        a_matrix_2x3 = matrices.Matrix([[1, 2, 3], [4, -5, 6]])
        matrix = matrices.Matrix([[1]])

        inverse_matrix_1 = a_matrix_1x1.find_inverse()
        inverse_matrix_2 = a_matrix_2x2.find_inverse()
        inverse_matrix_3 = a_matrix_3x3.find_inverse()
        inverse_matrix = matrix.find_inverse()

        with self.assertRaises(matrices.NoInverseError):
                a_matrix_zero_determinant.find_inverse()
        with self.assertRaises(matrices.IncorrectInputError):
                a_matrix_2x3.find_inverse()

        inverse_matrix = matrix.find_inverse()
        self.assertEqual([[1]], inverse_matrix.matrix)


class TransposeRrowTest(unittest.TestCase):
    def test_non_row(self):
        string = "sc ag"
        integer = 666
        invalid_row = [[4, 5, "chips"]]
        with self.assertRaises(matrices.NotARowError):
            matrices.transpose_row(string)
        with self.assertRaises(matrices.NotARowError):
            matrices.transpose_row(integer)
        with self.assertRaises(matrices.NotARowError):
            matrices.transpose_row(invalid_row)

    def test_empty_row(self):
        empty_row = [[]]
        with self.assertRaises(matrices.EmptyRowError):
            matrices.transpose_row(empty_row)

    def test_transpose_tow(self):
        a_row_1 = [[666]]
        a_row_2 = [[23, 44, 78]]
        self.assertEqual([[666]], matrices.transpose_row(a_row_1))
        self.assertEqual([[23], [44], [78]], matrices.transpose_row(a_row_2))


class MultiplicationTest(unittest.TestCase):
    def test_result(self):
        a_matrix_1 = matrices.Matrix([[1, 2, 3], [4, 5, 6]])
        a_matrix_2 = matrices.Matrix([[7, 8], [9, 10], [11, 12]])
        bad_matrix = matrices.Matrix([[1, 1, 7], [2, 3, 4]])

        result_list = [[58, 64], [139, 154]]
        result_matrix = matrices.multiplication(a_matrix_1, a_matrix_2)

        with self.assertRaises(matrices.NonValidMatricesForMultiplicationError):
            matrices.multiplication(a_matrix_1, bad_matrix)

        self.assertEqual(result_list, result_matrix.matrix)


if __name__ == '__main__':
    unittest.main()
