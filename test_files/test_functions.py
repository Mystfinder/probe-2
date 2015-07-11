from probe import functions
from probe import matrices
import unittest
import math


class FunctionsErrorsTest(unittest.TestCase):
    def test_print(self):
        functions_error = functions.FucntionsError()
        naming_error = functions.NamingError()
        length_error = functions.ListsNotWithSameLengtgError()
        incorrect_error = functions.IncorrectInputError()

        print(functions_error)
        print(naming_error)
        print(length_error)
        print(incorrect_error)


class PrintGraphTest(unittest.TestCase):
    def test_for_all_cases(self):
        interval_1 = [2, 3]
        interval_2 = [-4, 5]
        interval_3 = [-6, -3]
        big_interval = [1, 100]
        bad_interval = [4, 1]

        def a_function(x):
            return math.pow(x, 2)

        functions.print_graph(a_function, interval_1, 1)
        functions.print_graph(a_function, interval_2, 1)
        functions.print_graph(a_function, interval_3, 1)
        functions.print_graph(a_function, interval_3, 1)
        functions.print_graph(a_function, big_interval, 1)

        with self.assertRaises(functions.IncorrectInputError):
            functions.print_graph(a_function, bad_interval, 1)

        functions.print_graph(a_function, interval_1, 1, False)

        with self.assertRaises(functions.NamingError):
            functions.print_graph(a_function, bad_interval, 1, True, 3)


class PrintGraphDiscreteTest(unittest.TestCase):
    def test_for_all_cases(self):
        list_1 = [2, 6, -3, 7, 3]
        list_2 = [-6, 3, 3, 6, -1]
        list_3 = []
        for i in range(60):
            list_3.append(i)

        functions.print_graph_discrete(list_1)
        functions.print_graph_discrete(list_1, False, False)

        names = ["test_name.svg", "test_title", ["test_name_1", "test_name_2"]]
        functions.print_graph_discrete([list_1, list_2], True, True,
                                       True, names)

        functions.print_graph_discrete(list_3)

        bad_names = [[34], 32]
        with self.assertRaises(functions.NamingError):
            functions.print_graph_discrete(list_1, True, True, True, bad_names)
        with self.assertRaises(functions.NamingError):
            functions.print_graph_discrete(list_1, True, True, True, [4])


class PrintHistogramTest(unittest.TestCase):
    def test_all_cases(self):
        list_1 = [2, 6, -3, 7, 5, 2, 6, 8, -2, 0, -11, 32]

        functions.print_histogram(list_1, 5)
        functions.print_histogram(list_1, [[-3, 4], [4, 50]], True)
        functions.print_histogram(list_1, 5, False, True)
        functions.print_histogram(list_1, [[5, 5]], True, True)

        bad_names = [[34], 32]
        with self.assertRaises(functions.NamingError):
            functions.print_histogram(list_1, 4,  False, False, bad_names)
        with self.assertRaises(functions.NamingError):
            functions.print_histogram(list_1, 4, False, False, [4])


class PrintComparisonTest(unittest.TestCase):
    def test_all_cases(self):
        list_1 = [2, 6, -3, 7, 3, 2, 6, 8, -2, 0, -11, 32]
        big_list = []
        for i in range(60):
            big_list.append(i)

        def a_function_1(x):
            return 2*x

        def a_function_2(x):
            return math.pow(x, 2)

        names = ["unnamed comparison.svg", "Title", ["Data", "F1"]]
        functions.print_comparison([list_1, 3], [a_function_1], names)
        names = ["unnamed comparison.svg", "Title", ["Data", "F1", "F2"]]
        functions.print_comparison([list_1, 1], [a_function_1, a_function_2],
                                   names)
        functions.print_comparison([list_1, 3], [a_function_1])

        bad_names = [[34], 32]
        with self.assertRaises(functions.NamingError):
            functions.print_comparison([list_1, 4], [a_function_1], bad_names)
        with self.assertRaises(functions.NamingError):
            functions.print_comparison([list_1, 4], [a_function_1], [4])

        functions.print_comparison([big_list, 40], [a_function_1])


class CorrelateTest(unittest.TestCase):
    def test_it(self):
        list_1 = [2, 6, -3, 7, 3, 2, 6, 8, -2, 0, -11, 32]
        list_2 = [2, 6, -3, 7, 2, 2, 7, 8, -2, 0, -11, 32]
        bad_list = [1, 2, 3]

        functions.correlate(list_1, list_2)
        with self.assertRaises(functions.ListsNotWithSameLengtgError):
            functions.correlate(list_1, bad_list)

        bad_names_1 = [[34], 32]
        bad_names_2 = [[23, 32, 42], 23]
        with self.assertRaises(functions.NamingError):
            functions.correlate(list_1, list_2, bad_names_1)
        with self.assertRaises(functions.NamingError):
            functions.correlate(list_1, list_2, bad_names_2)
        with self.assertRaises(functions.NamingError):
            functions.correlate(list_1, list_2, [4])


class log_log_correlate(unittest.TestCase):
    def test_it(self):
        list_1 = [2, 36, 3, 7, 3, 2, 6, 8, 2, 3, 11, 32]
        list_2 = [2, 6, 3, 7, 2, 2, 7, 8, 2, 4, 11, 32]
        bad_list_1 = [-2, 6, 3, 7, 2, 2, 7, 8, 2, 0, 11, 32]
        bad_list_2 = [0, 6, 3, 7, 2, 2, 7, 8, 2, 0, 11, 32]
        bad_list_3 = [1]

        functions.log_log_correlate(list_1, list_2)
        with self.assertRaises(functions.IncorrectInputError):
            functions.log_log_correlate(list_1, bad_list_1)
        with self.assertRaises(functions.IncorrectInputError):
            functions.log_log_correlate(list_1, bad_list_2)
        with self.assertRaises(functions.ListsNotWithSameLengtgError):
            functions.log_log_correlate(list_1, bad_list_3)

        bad_names_1 = [34, 32]
        bad_names_2 = [[23, 32, 42], 23]
        with self.assertRaises(functions.NamingError):
            functions.log_log_correlate(list_1, list_2, bad_names_1)
        with self.assertRaises(functions.NamingError):
            functions.log_log_correlate(list_1, list_2, bad_names_2)
        with self.assertRaises(functions.NamingError):
            functions.log_log_correlate(list_1, list_2, [4])


class FactorialTest(unittest.TestCase):
    def test_input(self):
        string = "asd"
        invalid_float = 7.15
        invalid_int = -5

        with self.assertRaises(functions.IncorrectInputError):
            functions.factorial(string)
        with self.assertRaises(functions.IncorrectInputError):
            functions.factorial(invalid_float)
        with self.assertRaises(functions.IncorrectInputError):
            functions.factorial(invalid_int)

    def test_zero(self):
        zero = 0

        self.assertEqual(1, functions.factorial(zero))

    def test_results(self):
        valid_float = 7.0
        valid_int = 4

        self.assertEqual(5040, functions.factorial(valid_float))
        self.assertEqual(24, functions.factorial(valid_int))


class SemiFactorialTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])
        invalid_n_1 = 3.2
        invalid_n_2 = -2

        f = functions.semi_factorial

        with self.assertRaises(functions.IncorrectInputError):
            f(string, 1)
        with self.assertRaises(functions.IncorrectInputError):
            f(-3, matrix)
        with self.assertRaises(functions.IncorrectInputError):
            f(2, invalid_n_1)
        with self.assertRaises(functions.IncorrectInputError):
            f(-2, invalid_n_2)

    def test_zero(self):
        start = 666
        n = 0

        f = functions.semi_factorial

        self.assertEqual(1, f(start, n))

    def test_results(self):
        start_1 = 4
        n_1 = 5
        start_2 = -0.4
        n_2 = 12
        start_3 = 7.0
        n_3 = 3

        f = functions.semi_factorial

        result_1 = f(start_1, n_1)
        result_2 = f(start_2, n_2)
        result_3 = f(start_3, n_3)

        self.assertEqual(6720, result_1)
        self.assertTrue(-4064302.358 < result_2 and result_2 < -4064302.357)
        self.assertEqual(504, result_3)


class HypergeometricFunctionTest(unittest.TestCase):
    def test_input(self):
        parameter_list_1 = [1/3, 2/3]
        parameter_list_2 = [5/6]

        f = functions.hypergeometric_function

        result = f(parameter_list_1, parameter_list_2, 27/32)

        self.assertTrue(1.59 < result and result < 1.6)


class BetaFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])
        invalid_a = -2
        invalid_b = -3.0

        f = functions.beta_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string, 1.55)
        with self.assertRaises(functions.IncorrectInputError):
            f(4, matrix)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_a, 2)
        with self.assertRaises(functions.IncorrectInputError):
            f(2.3, invalid_b)

    def test_results(self):
        a_1 = 2
        b_1 = 3
        a_2 = 122
        b_2 = 2.12
        a_3 = 7.0
        b_3 = 3.4

        f = functions.beta_function
        result_1 = f(a_1, b_1)
        result_2 = f(a_2, b_2)
        result_3 = f(a_3, b_3)

        self.assertTrue(0.083 < result_1 and result_1 < 0.084)
        power = math.pow(10, -5)
        self.assertTrue(3.951*power < result_2 and result_2 < 3.9511*power)
        self.assertTrue(0.0023 < result_3 and result_3 < 0.0024)


class IncomleteBetaFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])
        a_list = [2, 5, 6]
        invalid_a = -2
        invalid_b = -3.0
        invalid_x = -1

        f = functions.incomplete_beta_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string, 1.55, 2)
        with self.assertRaises(functions.IncorrectInputError):
            f(0.3, matrix, 4.2)
        with self.assertRaises(functions.IncorrectInputError):
            f(0.5, 20, a_list)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_x, 2, 33)
        with self.assertRaises(functions.IncorrectInputError):
            f(0.3, invalid_a, 66.6)
        with self.assertRaises(functions.IncorrectInputError):
            f(0.1, 3.2, invalid_b)

        with self.assertRaises(functions.IncorrectInputError):
            f(0.2, "as", 2)
        with self.assertRaises(functions.IncorrectInputError):
            f(0.2, -2, 2)
        with self.assertRaises(functions.IncorrectInputError):
            f(0.2, 3, "as")
        with self.assertRaises(functions.IncorrectInputError):
            f(0.2, 3, -4)

    def test_results(self):
        x_1 = 0.2
        a_1 = 2
        b_1 = 3
        x_2 = 0.5
        a_2 = 122
        b_2 = 2.12
        x_3 = 0
        a_3 = 7.0
        b_3 = 3.4

        f = functions.incomplete_beta_function
        result_1 = f(x_1, a_1, b_1)
        result_2 = f(x_2, a_2, b_2)
        result_3 = f(x_3, a_3, b_3)

        self.assertTrue(0.015 < result_1 and result_1 < 0.0151)
        power = math.pow(10, -40)
        self.assertTrue(7.157*power < result_2 and result_2 < 7.158*power)
        self.assertEqual(0, result_3)


class RegularizedBetaFunctionTest(unittest.TestCase):
    def test_input(self):
        result = functions.regularized_beta_function(0.5, 4, 6)

        self.assertTrue(0.7 < result and result < 0.8)


class GammaFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])
        invalid_t_1 = -2
        invalid_t_2 = 0

        f = functions.gamma_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string)
        with self.assertRaises(functions.IncorrectInputError):
            f(matrix)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_t_1)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_t_2)

    def test_results(self):
        t_1 = 0.5
        t_2 = 1
        t_3 = 20.2

        f = functions.gamma_function
        result_1 = f(t_1)
        result_2 = f(t_2)
        result_3 = f(t_3)

        self.assertTrue(1.772 < result_1 and result_1 < 1.773)
        self.assertTrue(0.9999 < result_2 and result_2 < 1)
        power = math.pow(10, 17)
        self.assertTrue(2.2*power < result_3 and result_3 < 2.3*power)


class LowerIncompleteGammaFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])
        invalid_s = -2
        invalid_x = -3.0

        f = functions.lower_incomplete_gamma_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string, 2)
        with self.assertRaises(functions.IncorrectInputError):
            f(3.42, matrix)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_s, 1)
        with self.assertRaises(functions.IncorrectInputError):
            f(2.3, invalid_x)

    def test_results(self):
        s_1 = 1
        x_1 = 2
        s_2 = 1.44
        x_2 = 0.66
        s_3 = 5.0
        x_3 = 2.4
        s_4 = 223
        x_4 = 2.1

        f = functions.lower_incomplete_gamma_function
        result_1 = f(s_1, x_1)
        result_2 = f(s_2, x_2)
        result_3 = f(s_3, x_3)
        result_4 = f(s_4, x_4)

        self.assertTrue(0.864 < result_1 and result_1 < 0.865)
        self.assertTrue(0.262 < result_2 and result_2 < 0.263)
        self.assertTrue(2.3 < result_3 and result_3 < 2.3009)
        power = math.pow(10, 68)
        self.assertTrue(3.969*power < result_4 and result_4 < 3.970*power)


class ErrorFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])

        f = functions.error_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string)
        with self.assertRaises(functions.IncorrectInputError):
            f(matrix)

    def test_results(self):
        x_1 = 0
        x_2 = 0.66
        x_3 = 1.4
        x_4 = -2.1

        f = functions.error_function
        result_1 = f(x_2)
        result_2 = f(x_3)
        result_3 = f(x_4)

        self.assertEqual(0, f(x_1))
        self.assertTrue(0.649 < result_1 and result_1 < 0.650)
        self.assertTrue(0.952 < result_2 and result_2 < 0.953)
        self.assertTrue(-0.9971 < result_3 and result_3 < -0.0997)


class InverseErrorFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])
        invalid_x_1 = -2
        invalid_x_2 = 3

        f = functions.inverse_error_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string)
        with self.assertRaises(functions.IncorrectInputError):
            f(matrix)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_x_1)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_x_2)

    def test_results(self):
        x_1 = 0
        x_2 = 0.5
        x_3 = 0.14
        x_4 = -0.44

        f = functions.inverse_error_function
        result_1 = f(x_2)
        result_2 = f(x_3)
        result_3 = f(x_4)

        self.assertEqual(0, f(x_1))
        self.assertTrue(0.476 < result_1 and result_1 < 0.477)
        self.assertTrue(0.124 < result_2 and result_2 < 0.125)
        self.assertTrue(-0.413 < result_3 and result_3 < -0.412)


class FloorFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])

        f = functions.floor_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string)
        with self.assertRaises(functions.IncorrectInputError):
            f(matrix)

    def test_results(self):
        test_int_1 = 3
        test_int_2 = -2
        test_int_3 = 0

        test_float_1 = 6.66
        test_float_2 = -3.0
        test_float_3 = -3.34
        test_float_4 = 0.0

        f = functions.floor_function

        self.assertEqual(3, f(test_int_1))
        self.assertEqual(-2, f(test_int_2))
        self.assertEqual(0, f(test_int_3))

        self.assertEqual(6, f(test_float_1))
        self.assertEqual(-3, f(test_float_2))
        self.assertEqual(-4, f(test_float_3))
        self.assertEqual(0, f(test_float_4))


class CeilingFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "vrv"
        matrix = matrices.Matrix([[1, 2, 4], [5, 33, 2]])

        f = functions.ceiling_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string)
        with self.assertRaises(functions.IncorrectInputError):
            f(matrix)

    def test_results(self):
        test_int_1 = 3
        test_int_2 = -2
        test_int_3 = 0

        test_float_1 = 6.66
        test_float_2 = -3
        test_float_3 = -3.34
        test_float_4 = 0.0

        f = functions.ceiling_function

        self.assertEqual(3, f(test_int_1))
        self.assertEqual(-2, f(test_int_2))
        self.assertEqual(0, f(test_int_3))

        self.assertEqual(7, f(test_float_1))
        self.assertEqual(-3, f(test_float_2))
        self.assertEqual(-3, f(test_float_3))
        self.assertEqual(0, f(test_float_4))


class HarmonicNumberFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "asd"
        invalid_float = 7.15
        invalid_int = -5
        zero = 0

        f = functions.harmonic_number_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_float)
        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_int)
        with self.assertRaises(functions.IncorrectInputError):
            f(zero)

    def test_results(self):
        valid_float = 7.0
        valid_int = 4

        f = functions.harmonic_number_function

        result_1 = f(valid_float)
        result_2 = f(valid_int)

        self.assertTrue(2.59 <= result_1 and result_1 <= 2.6)
        self.assertTrue(2.08 <= result_2 and result_2 <= 2.09)


class GeneralizedHarmonicNumberFunctionTest(unittest.TestCase):
    def test_input(self):
        string = "asd"

        valid_int_n = 3
        int_r = 5
        valid_float_n = 3.0
        valid_float_r = 5.0

        invalid_int_n = -5
        invalid_float_n = 7.15
        invalid_float_r = 3.54

        zero = 0

        f = functions.generalized_harmonic_number_function

        with self.assertRaises(functions.IncorrectInputError):
            f(string, int_r)
        with self.assertRaises(functions.IncorrectInputError):
            f(valid_int_n, string)

        with self.assertRaises(functions.IncorrectInputError):
            f(string, valid_float_r)
        with self.assertRaises(functions.IncorrectInputError):
            f(valid_float_n, string)

        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_int_n, int_r)

        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_int_n, valid_float_r)

        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_float_n, int_r)

        with self.assertRaises(functions.IncorrectInputError):
            f(invalid_float_n, valid_float_r)

        with self.assertRaises(functions.IncorrectInputError):
            f(zero, int_r)
        with self.assertRaises(functions.IncorrectInputError):
            f(zero, valid_float_r)

        with self.assertRaises(functions.IncorrectInputError):
            f(3, 3.5)

    def test_results(self):
        valid_float = 7.0
        valid_int = 4

        f = functions.generalized_harmonic_number_function
        result_1 = f(valid_float, valid_int)
        result_2 = f(valid_int, valid_float)
        result_3 = f(5000, 10000)

        self.assertTrue(1.08 <= result_1 and result_1 <= 1.082)
        self.assertTrue(1.0083 <= result_2 and result_2 <= 1.0084)
        self.assertEqual(1, result_3)


if __name__ == '__main__':
    unittest.main()
