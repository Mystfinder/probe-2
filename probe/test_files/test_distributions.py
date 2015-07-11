from probe import distributions
import unittest


class DistributionsErrorsTest(unittest.TestCase):
    def test_print(self):
        distribution_error = distributions.DistributionsError()
        big_error = distributions.IncorrectDistributionInicializationError()
        input_error = distributions.IncorrectInputError()
        list_error = distributions.NotAListError()
        percentile_error = distributions.PercentileError()

        print(distribution_error)
        print(big_error)
        print(input_error)
        print(list_error)
        print(percentile_error)


class EmpiricalCdfTest(unittest.TestCase):
    def test_results(self):
        data_list = [2, 5, 2, 7, 4, 0, 2, 3, 9, 3, 2, 4, 2]
        bad_data = "asd"
        point = 4

        result = distributions.empirical_cdf(4, data_list)

        self.assertTrue(0.769 < result and result < 0.77)
        with self.assertRaises(distributions.NotAListError):
            distributions.empirical_cdf(4, bad_data)


class EmpiricCdfGraphTest(unittest.TestCase):
    def test_preformance(self):
        data_list = [2, 5, 2, 7, 4, 0, 2, 3, 9, 3, 2, 4, 2]
        bad_data = "asd"

        distributions.empiric_cdf_graph(data_list)

        with self.assertRaises(distributions.NotAListError):
            distributions.empiric_cdf_graph(bad_data)


class CompareTest(unittest.TestCase):
    def test_results(self):
        data_list = [2, 5, 2, 7, 4, 0, 2, 3, 9, 3, 2, 4, 2]
        bad_data = "as"
        big_data = []

        normal_dist = distributions.NormalDistribution(3, 4)
        fisher_dist = distributions.FisherDistribution(2, 3)

        result_norm = distributions.compare(data_list, normal_dist)
        result_fisher = distributions.compare(data_list, fisher_dist)

        self.assertTrue(0.157 < result_norm and result_norm < 0.159)
        self.assertTrue(0.432 < result_fisher and result_fisher < 0.433)

        with self.assertRaises(distributions.NotAListError):
            distributions.compare(bad_data, normal_dist)


class CompareCdfWithTheoreticalTest(unittest.TestCase):
    def test_performance(self):
        data_list = [2, 5, 2, 7, 4, 5, 2, 3, 9, 3, 2, 4, 2]
        bad_data = "as"
        big_data = []
        for i in range(60):
            big_data.append(i)

        dist_1 = distributions.NormalDistribution(2, 3)
        dist_2 = distributions.FisherDistribution(2, 3)
        dist_3 = distributions.t_Distribution(7)
        dist_4 = distributions.ChiSquaredDistribution(8)

        distributions.compare_cdf_with_theoretical(data_list,
                                                   [dist_1, dist_2, dist_3,
                                                    dist_4])

        distributions.compare_cdf_with_theoretical(data_list, dist_1)
        distributions.compare_cdf_with_theoretical(data_list, dist_2)
        distributions.compare_cdf_with_theoretical(data_list, dist_3)
        distributions.compare_cdf_with_theoretical(data_list, dist_4)
        with self.assertRaises(distributions.NotAListError):
            distributions.compare_cdf_with_theoretical(bad_data, dist_1)

        distributions.compare_cdf_with_theoretical(big_data, dist_1)


class kolmogorovDistributionTest(unittest.TestCase):
    def test_results(self):
        result_1 = distributions.KolmogorovDistribution.kolmogorov_cdf(3)
        result_2 = distributions.KolmogorovDistribution.kolmogorov_cdf(0)

        self.assertTrue(0.99 < result_1 and result_1 < 1)
        self.assertEqual(0, result_2)


class NormalDistributionsTest(unittest.TestCase):
    def test_results(self):
        norm = distributions.NormalDistribution(2, 3)
        the_error = distributions.IncorrectDistributionInicializationError
        with self.assertRaises(the_error):
            norm = distributions.NormalDistribution(2, -3)

        result_1 = norm.pdf(1)
        result_2 = norm.cdf(3)
        result_3 = norm.percentile(0.95)

        result_4 = distributions.NormalDistribution.normal_pdf(0, 2, 3)
        result_5 = distributions.NormalDistribution.normal_cdf(1, 2, 3)
        result_6 = distributions.NormalDistribution.normal_percentile(0.95, 2,
                                                                      3)

        self.assertTrue(0.19 < result_1 and result_1 < 0.2)
        self.assertTrue(0.71 < result_2 and result_2 < 0.72)
        self.assertTrue(4.84 < result_3 and result_3 < 4.85)
        self.assertTrue(0.11 < result_4 and result_4 < 0.12)
        self.assertTrue(0.28 < result_5 and result_5 < 0.29)
        self.assertTrue(4.84 < result_6 and result_6 < 4.85)

        with self.assertRaises(distributions.IncorrectInputError):
            distributions.NormalDistribution.normal_pdf(0, 2, -3)
        with self.assertRaises(distributions.IncorrectInputError):
            distributions.NormalDistribution.normal_cdf(1, 2, -3)
        with self.assertRaises(distributions.IncorrectInputError):
            distributions.NormalDistribution.normal_percentile(0.4, 5, -6)
        with self.assertRaises(distributions.PercentileError):
            distributions.NormalDistribution.normal_percentile(2, -5, 6)
        with self.assertRaises(distributions.PercentileError):
            norm.percentile(1.2)

        with self.assertRaises(distributions.IncorrectInputError):
            distributions.NormalDistribution.normal_pdf(0.95, 2, -3)
        with self.assertRaises(distributions.IncorrectInputError):
            distributions.NormalDistribution.normal_cdf(0.95, 2, -3)
        with self.assertRaises(distributions.IncorrectInputError):
            distributions.NormalDistribution.normal_percentile(0.95, 2, -3)
        with self.assertRaises(distributions.PercentileError):
            distributions.NormalDistribution.normal_percentile(1.2, 2, 3)
        with self.assertRaises(distributions.PercentileError):
            norm.percentile(-2)


class FisherDistributionTest(unittest.TestCase):
    def test_results(self):
        the_error = distributions.IncorrectDistributionInicializationError
        with self.assertRaises(the_error):
            distributions.FisherDistribution(-1, 3)

        fish = distributions.FisherDistribution(2, 1)
        fish = distributions.FisherDistribution(2, 5)
        fish = distributions.FisherDistribution(4, 5)
        fish = distributions.FisherDistribution(2, 3)

        result_1 = fish.pdf(1)
        result_2 = fish.cdf(3)

        result_3 = distributions.FisherDistribution.f_pdf(0.5, 2, 3)
        result_4 = distributions.FisherDistribution.f_cdf(1, 2, 3)

        self.assertTrue(0.27 < result_1 and result_1 < 0.28)
        self.assertTrue(0.8 < result_2 and result_2 < 0.81)
        self.assertTrue(0.48 < result_3 and result_3 < 0.49)
        self.assertTrue(0.53 < result_4 and result_4 < 0.54)

        with self.assertRaises(distributions.IncorrectInputError):
            result_3 = distributions.FisherDistribution.f_pdf(0.5, 2, -3)
        with self.assertRaises(distributions.IncorrectInputError):
            result_3 = distributions.FisherDistribution.f_cdf(0.5, -2, 3)


class tDistributionTest(unittest.TestCase):
    def test_results(self):
        the_error = distributions.IncorrectDistributionInicializationError
        with self.assertRaises(the_error):
            distributions.t_Distribution(-1)

        t = distributions.t_Distribution(1)
        t = distributions.t_Distribution(2)
        t = distributions.t_Distribution(3)
        t = distributions.t_Distribution(4)
        t = distributions.t_Distribution(5)

        result_1 = t.pdf(1)
        result_2 = t.pdf(-2)

        result_3 = t.cdf(1)
        result_4 = t.cdf(-2)

        self.assertTrue(0.21 < result_1 and result_1 < 0.22)
        self.assertTrue(0.06 < result_2 and result_2 < 0.07)
        self.assertTrue(0.81 < result_3 and result_3 < 0.82)
        self.assertTrue(0.05 < result_4 and result_4 < 0.06)

        with self.assertRaises(distributions.IncorrectInputError):
            distributions.t_Distribution.t_cdf(3, 0)
        with self.assertRaises(distributions.IncorrectInputError):
            distributions.t_Distribution.t_pdf(3, 0)


class ChiSquaredDistributionTest(unittest.TestCase):
    def test_results(self):
        the_error = distributions.IncorrectDistributionInicializationError
        with self.assertRaises(the_error):
            distributions.ChiSquaredDistribution(-1)

        c = distributions.ChiSquaredDistribution(1)
        c = distributions.ChiSquaredDistribution(3)

        result_1 = c.pdf(1)
        result_2 = c.cdf(3)

        result_3 = distributions.ChiSquaredDistribution.chi_squared_pdf(0.5, 2)
        result_4 = distributions.ChiSquaredDistribution.chi_squared_cdf(0.5, 4)

        result_5 = distributions.ChiSquaredDistribution.chi_squared_pdf(-0.3,
                                                                        2)
        result_6 = distributions.ChiSquaredDistribution.chi_squared_cdf(-0.2,
                                                                        7)

        self.assertTrue(0.24 < result_1 and result_1 < 0.25)
        self.assertTrue(0.6 < result_2 and result_2 < 0.61)
        self.assertTrue(0.38 < result_3 and result_3 < 0.39)
        self.assertTrue(0.02 < result_4 and result_4 < 0.03)
        self.assertEqual(0, result_5)
        self.assertEqual(0, result_6)

        with self.assertRaises(distributions.IncorrectInputError):
            distributions.ChiSquaredDistribution.chi_squared_cdf(3, 0)
        with self.assertRaises(distributions.IncorrectInputError):
            distributions.ChiSquaredDistribution.chi_squared_pdf(3, 0)


class PoissonDistributionTest(unittest.TestCase):
    def test_results(self):
        the_error = distributions.IncorrectDistributionInicializationError
        with self.assertRaises(the_error):
            distributions.PoissonDistribution(-1)

        p = distributions.PoissonDistribution(1)

        result_1 = p.pmf(1)
        result_2 = p.cdf(2)

        result_3 = distributions.PoissonDistribution.poisson_pmf(3, 2)
        result_4 = distributions.PoissonDistribution.poisson_cdf(3, 2)

        result_5 = p.exact(2)
        result_6 = p.exact(0)
        print(result_6)

        self.assertTrue(0.36 < result_1 and result_1 < 0.37)
        self.assertTrue(0.91 < result_2 and result_2 < 0.92)
        self.assertTrue(0.18 < result_3 and result_3 < 0.19)
        self.assertTrue(0.85 < result_4 and result_4 < 0.86)
        self.assertTrue(0.18 < result_5 and result_5 < 0.19)

        with self.assertRaises(distributions.IncorrectInputError):
            distributions.PoissonDistribution.poisson_pmf(3, 0)
        with self.assertRaises(distributions.IncorrectInputError):
            distributions.PoissonDistribution.poisson_cdf(3, 0)


class ZipfDistributionTest(unittest.TestCase):
    def test_results(self):
        the_error = distributions.IncorrectDistributionInicializationError
        with self.assertRaises(the_error):
            distributions.ZipfDistribution(-1, 5)

        z = distributions.ZipfDistribution(1, 7)

        result_1 = z.pmf(1)
        result_2 = z.cdf(2)

        result_3 = distributions.ZipfDistribution.zipf_pmf(3, 6, 8)
        result_4 = distributions.ZipfDistribution.zipf_cdf(3, 6, 8)

        self.assertTrue(0.38 < result_1 and result_1 < 0.39)
        self.assertTrue(0.57 < result_2 and result_2 < 0.58)
        self.assertTrue(0.001 < result_3 and result_3 < 0.002)
        self.assertTrue(0.99 < result_4 and result_4 < 1)


class FindPercentileTest(unittest.TestCase):
    def test_results(self):
        normal_dist = distributions.NormalDistribution(0, 1)
        t_dist = distributions.t_Distribution(7)

        result_norm = distributions.find_percentile(0.95, normal_dist.cdf)
        with self.assertRaises(distributions.PercentileError):
            distributions.find_percentile(1.2, normal_dist.cdf)
        cdf = distributions.NormalDistribution.normal_cdf
        result_with_args = distributions.find_percentile(0.8, cdf, (2, 5))

        self.assertTrue(1.644 < result_norm and result_norm < 1.645)


if __name__ == '__main__':
    unittest.main()
