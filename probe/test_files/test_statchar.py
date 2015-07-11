from probe import statchar
import unittest

class StatcharErrorsTest(unittest.TestCase):
    def test_print(self):
        statchar_error = statchar.StatcharError()
        not_list_error = statchar.NotAListError()
        length_error = statchar.ListsNotWithSameLengthError()

        print(statchar_error)
        print(not_list_error)
        print(length_error)


class AritmeticMeanTest(unittest.TestCase):
    def test_results(self):
        data_1 = [8, 4, 12, 11, 8]
        data_2 = [5, -3, -23, 4, 2]
        bad_data = "as"

        f = statchar.aritmetic_mean

        self.assertEqual(8.6, f(data_1))
        self.assertEqual(-3, f(data_2))

        with self.assertRaises(statchar.NotAListError):
            f(bad_data)


class SSTest(unittest.TestCase):
    def test_results(self):
        data_1 = [8, 4, 12, 11, 8]
        data_2 = [5, -3, -23, 4, 2]
        bad_data = "as"

        f = statchar.SS

        self.assertEqual(39.2, f(data_1))
        self.assertEqual(538, f(data_2))

        with self.assertRaises(statchar.NotAListError):
            f(bad_data)


class SSAbstractTest(unittest.TestCase):
    def test_results(self):
        data_1 = [8, 4, 12, 11, 8]
        data_2 = [5, -3, -23, 4, 2]
        data_3 = [4, -28]
        bad_data_1 = "as"
        bad_data_2 = "ti"

        f = statchar.SS_abstract

        self.assertEqual(1368, f(data_1, data_2))
        self.assertEqual(1368, f(data_2, data_1))

        the_error = statchar.ListsNotWithSameLengthError
        with self.assertRaises(the_error):
            f(data_1, data_3)

        with self.assertRaises(statchar.NotAListError):
            f(data_1, bad_data_1)
        with self.assertRaises(statchar.NotAListError):
            f(bad_data_2, data_1)


class SSWithMeanTest(unittest.TestCase):
    def test_results(self):
        data_1 = [8, 4, 12, 11, 8]
        data_2 = [5, -3, -23, 4, 2]
        bad_data = "as"

        f = statchar.SS_with_mean

        self.assertEqual(145, f(data_1, 4))
        self.assertEqual(543, f(data_2, -2))

        with self.assertRaises(statchar.NotAListError):
            f(bad_data, 4)


class SSTrearTest(unittest.TestCase):
    def test_results(self):
        data_1 = [8, 4, 12, 11, 8]
        data_2 = [5, -3, -23, 4, 2]
        data_3 = [1, 1, -4, 5]
        data_4 = [-1]
        data_5 = [6, -3, 9, 12, 0, 32, 2-1]
        p = [data_1, data_2, data_3, data_4, data_5]
        bad_data_1 = "as"
        bad_data_2 = "ti"

        f = statchar.SStreat

        self.assertEqual(1545, f(p, data_1))

        the_error = statchar.ListsNotWithSameLengthError
        with self.assertRaises(the_error):
            f(p, data_3)

        with self.assertRaises(statchar.NotAListError):
            f(data_1, bad_data_1)
        with self.assertRaises(statchar.NotAListError):
            f(bad_data_2, data_1)


class SSresTest(unittest.TestCase):
    def test_results(self):
        data_1 = [8, 4, 12, 11, 8]
        data_2 = [5, -3, -23, 4, 2]
        bad_data_1 = "as"
        bad_data_2 = "ti"

        f = statchar.SSres

        self.assertEqual(1040, f([data_1, data_2], [2, 4]))

        with self.assertRaises(statchar.NotAListError):
            f(data_1, bad_data_1)
        with self.assertRaises(statchar.NotAListError):
            f(bad_data_2, data_1)


class SSTotTest(unittest.TestCase):
    def test_results(self):
        data_1 = [8, 4, 12, 11, 8]
        data_2 = [5, -3, -23, 4, 2]
        data_3 = [1, 1, -4, 5]
        data_4 = [-1]
        data_5 = [6, -3, 9, 12, 0, 32, 2-1]
        p = [data_1, data_2, data_3, data_4, data_5]
        bad_data = "as"

        f = statchar.SStot
        result_1 = f(p)
        result_2 = f(p, 120)

        self.assertTrue(1986.9 < result_1 and result_1 < 1987)
        self.assertEqual(298251, f(p, 120))

        with self.assertRaises(statchar.NotAListError):
            f(bad_data)


class PowerSumTest(unittest.TestCase):
    def test_results(self):
        list_1 = [5, -3, -23, 4, 2]
        bad_data = "as"

        f = statchar.power_sum

        result = f(list_1, 2)
        self.assertTrue(result, 538)

        with self.assertRaises(statchar.NotAListError):
            f(bad_data, 2)


class MedianTest(unittest.TestCase):
    def test_results(self):
        list_1 = [5, -3, -23, 4, 2]
        list_2 = [5, -3, -23, 4, 2, 4]
        bad_data = "as"

        f = statchar.median

        result_1 = f(list_1)
        result_2 = f(list_2)

        self.assertTrue(result_1, 2)
        self.assertTrue(result_2, 3)

        with self.assertRaises(statchar.NotAListError):
            f(bad_data)


class ModeTest(unittest.TestCase):
    def test_results(self):
        list_1 = [5, -3, -23, 4, 2, 5, 2, 6, 7, 8, 9]
        bad_data = "as"

        f = statchar.mode

        result_1 = f(list_1)
        result_2 = f(list_1, True)

        self.assertTrue(result_1, [2, 5])
        self.assertTrue(result_2, ([2, 5], 2))

        with self.assertRaises(statchar.NotAListError):
            f(bad_data)


class StdDevUncorrectedTest(unittest.TestCase):
    def test_results(self):
        list_1 = [1, 2, 3, 4, 5]

        result = statchar.std_dev_uncorrected(list_1)
        self.assertTrue(1.41 < result and result < 1.42)


class StdDevCorrectedTest(unittest.TestCase):
    def test_results(self):
        list_1 = [1, 2, 3, 4, 5]

        result = statchar.std_dev_corrected(list_1)
        self.assertTrue(1.581 < result and result < 1.582)


class StdErrorOfMeanTest(unittest.TestCase):
    def test_results(self):
        list_1 = [1, 2, 3, 4, 5]

        result = statchar.std_error_of_mean(list_1)
        self.assertTrue(0.707 < result and result < 0.708)


class SkewnessTest(unittest.TestCase):
    def test_results(self):
        list_1 = [5, -3, -23, 4, 2, 156]
        bad_data = "as"

        f = statchar.skewness

        result = f(list_1)
        self.assertTrue(378.91 < result and result < 378.92)

        with self.assertRaises(statchar.NotAListError):
            f(bad_data)


class CorrelationCoeficentTest(unittest.TestCase):
    def test_results(self):
        data_list_1 = [1, 2, 3, 4, 5]
        data_list_2 = [4, 3, 5, 2, 8]
        bad_list = [1, 2, 4]
        bad_data = "as"

        f = statchar.correlation_coeficient
        result = f(data_list_1, data_list_2)

        self.assertTrue(0.48 < result and result < 0.49)
        with self.assertRaises(statchar.ListsNotWithSameLengthError):
            f(data_list_1, bad_list)

        with self.assertRaises(statchar.NotAListError):
            f(bad_data, data_list_1)
        with self.assertRaises(statchar.NotAListError):
            f(data_list_1, bad_data)


class RemoveHeavyOutliersTest(unittest.TestCase):
    def test_results(self):
        a_list = [5, -3, -23, 4, 2, 156]
        bad_data = "as"

        f = statchar.remove_heavy_outliers

        result = f(a_list, 2, 5)

        self.assertTrue([5, -3, 4, 2], result)

        with self.assertRaises(statchar.NotAListError):
            f(bad_data, 4, 5)


if __name__ == '__main__':
    unittest.main()

