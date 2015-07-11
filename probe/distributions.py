import math
from probe import functions
from probe import statchar
import pygal
import os


"""
1. empirical_cdf
2. empirical_cdf-graph
3. compare
4. compare_cdf_with_theoretical

1. Kolmogorov distribution
2. Normal distribution
3. Fisher distribution
4. t-distribution
5. chi-squared distribution
6. Poisson distribution
7. Zipf distribution

1. find_pecentile
"""


class DistributionsError(Exception):
    def __str__(self):
        return repr("An error for distributions.py")


class IncorrectDistributionInicializationError(DistributionsError):
    def __str__(self):
        return repr("Please check distribution requirements.")


class IncorrectInputError(DistributionsError):
    def __str__(self):
        return repr("Input violates requirements- check context.")


class NotAListError(DistributionsError):
    def __str__(self):
        return repr("Given variable not a list.")


class PercentileError(DistributionsError):
    def __str__(self):
        return repr("Percentile must be within (0, 1)")


def empirical_cdf(t, data_list):
    """
       Computes the empirical cdf of the given data_list for the
       given value t.
       For more information:
       http://en.wikipedia.org/wiki/Empirical_distribution_function
    """
    if type(data_list) is not list:
        raise NotAListError()

    n = len(data_list)
    number_of_elements = 0
    for element in data_list:
        if element <= t:
            number_of_elements += 1
    return number_of_elements/n


just_names = ["empiric cdf graph.svg", "Empiric cdf graph for data", "data"]


def empiric_cdf_graph(data_list, names=just_names):
    """
       Prints the graph of the empirical cdf of the data in data_list.
    """
    if type(data_list) is not list:
        raise NotAListError()

    for_print = []
    for element in data_list:
        for_print.append(empirical_cdf(element, data_list))
    functions.print_graph_discrete(for_print, True, True, True, names)


def compare(data_list, distribution):
    """
       Compares the difference between the empirical cdf of the
       data in data_list and the theoretical cdf of the specified
       distribution- returns the sum of squares between the cdfs in
       the points in data_list.
    """
    if type(data_list) is not list:
        raise NotAListError()

    cdf = distribution.cdf
    sum_of_squares = 0
    for element in data_list:
        A = empirical_cdf(element, data_list)
        B = cdf(element)
        sum_of_squares += math.pow(A-B, 2)
    return sum_of_squares


def compare_cdf_with_theoretical(data_list, distributions):
    """
       Prints the graphs of the empirical cdf of the data in
       data_list and the cdf of distribution for the points in
       data_list.
    """
    if type(data_list) is not list:
        raise NotAListError()

    data_list = sorted(data_list)
    line_chart = pygal.Line(dots_size=1)
    coordinates = []

    length = len(data_list)
    if length > 50:
        minimum = min(data_list)
        maximum = max(data_list)
        interval = maximum - minimum
        step = interval/10
        current = min(data_list)
        while current <= max(data_list):
            coordinates.append(current)
            current += step
        line_chart.x_labels = map(str, coordinates)
    else:
        i = 0
        current = data_list[i]
        while current <= max(data_list):
            coordinates.append(current)
            i += 1
            try:
                current = data_list[i]
            except IndexError:
                line_chart.x_labels = map(str, coordinates)
                break

    empirical_cdf_list = []
    for element in data_list:
        empirical_cdf_list.append(empirical_cdf(element, data_list))
    line_chart.add("empirical cdf", empirical_cdf_list)

    if type(distributions) is list:
        for dist in distributions:
            theoretical_cdf_list = []
            for element in data_list:
                theoretical_cdf_list.append(dist.cdf(element))
            if type(dist) is NormalDistribution:
                line_chart.add("Normal cdf", theoretical_cdf_list)
            if type(dist) is FisherDistribution:
                line_chart.add("Fisher cdf", theoretical_cdf_list)
            if type(dist) is t_Distribution:
                line_chart.add("t cdf", theoretical_cdf_list)
            if type(dist) is ChiSquaredDistribution:
                line_chart.add("chi-squared cdf", theoretical_cdf_list)
    else:
        dist = distributions
        theoretical_cdf_list = []
        for element in data_list:
            theoretical_cdf_list.append(distributions.cdf(element))
        if type(dist) is NormalDistribution:
            line_chart.add("Normal cdf", theoretical_cdf_list)
        if type(dist) is FisherDistribution:
            line_chart.add("Fisher cdf", theoretical_cdf_list)
        if type(dist) is t_Distribution:
            line_chart.add("t cdf", theoretical_cdf_list)
        if type(dist) is ChiSquaredDistribution:
            line_chart.add("chi-squared cdf", theoretical_cdf_list)

    current_dir = os.getcwd()
    if not os.path.exists(current_dir+"\probe svg container"):
        os.makedirs(current_dir+"\probe svg container")
    os.chdir(current_dir+"\probe svg container")
    line_chart.render_to_file("cdf comparison.svg")
    os.chdir(os.getcwd().split("\probe svg container")[0])


class KolmogorovDistribution():
    """
       Provides kolmogorov_cdf method for the Kolmogorov distribution.
       for more information:
       http://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test#Kolmogorov_distribution
       http://www.jstatsoft.org/v08/i18/paper
    """
    def kolmogorov_cdf(x):
        if x == 0:
            return 0
        A = math.pow(2*math.pi, 0.5)/x
        summation = 0
        for i in range(1, 10):
            B = -math.pow(2*i-1, 2)*math.pow(math.pi, 2)
            C = 8*math.pow(x, 2)
            summation += math.exp(B/C)
        return A*summation


class NormalDistribution():
    """
       Implements the Normal distribution with its basic features.
       For more information:
       http://en.wikipedia.org/wiki/Normal_distribution
    """

    def normal_pdf(x, m, v):
        """
           Gives the value of the normal probability density function
           for the given x and the specified parameters of the normal
           distribution- m specifies the mean, v specifies the
           variance.
        """
        if v < 0:
            raise IncorrectInputError()

        A = 1/(math.pow(v*2*math.pi, 0.5))
        B = -math.pow(x-m, 2)/(2*v)
        C = math.exp(B)
        return A*C

    def normal_cdf(x, m, v):
        """
           Gives the value of the normal cumulative density function
           for the given x and the specified parameters of the normal
           distribution- m specifies the mean, v specifies the
           variance.
        """
        if v < 0:
            raise IncorrectInputError()

        A = (x-m)/(math.pow(v*2, 0.5))
        return 1/2*(1+functions.error_function(A))

    def normal_percentile(x, m, v):
        """
           Returns the quantile required. m specifies the mean of the
           distribution, v specifies the variance of the distribution.
           x must be in the interval
           (0, 1).
        """
        if v < 0:
            raise IncorrectInputError()
        if x <= 0 or x >= 1:
            raise PercentileError()

        f = functions.inverse_error_function
        return m + math.pow(2*v, 0.5)*f(2*x-1)

    def __init__(self, mean, variance):
        """
           Sets the parameters for the Normal distribution.
           variance >= 0
        """
        if variance < 0:
            raise IncorrectDistributionInicializationError()

        self.mean = mean
        self.variance = variance
        self.median = mean
        self.mode = mean
        self.skewness = 0
        self.ex_kurtosis = 0

    def pdf(self, x):
        """
           Gives the value of the normal probability density function
           for the given x.
        """
        m = self.mean
        v = self.variance
        return NormalDistribution.normal_pdf(x, m, v)

    def cdf(self, x):
        """
           Gives the value of the normal cumulative density function
           for the given x.
        """
        m = self.mean
        v = self.variance
        return NormalDistribution.normal_cdf(x, m, v)

    def percentile(self, x):
        """
           Returns the quantile required. x must be in the interval
           (0, 1).
        """
        if x <= 0 or x >= 1:
            raise PercentileError()

        m = self.mean
        v = self.variance
        return NormalDistribution.normal_percentile(x, m, v)


class FisherDistribution:
    """
       Implements the Fisher distribution with its basic features.
       For more information:
       https://en.wikipedia.org/wiki/F-distribution
    """

    def f_pdf(x, df1, df2):
        """
           Gives the value of the Fisher probability density function
           for the given x (x must be in (0, inf))and the specified
           parameters of the Fisher distribution- df1 and df2 specify
           the degrees of freedom (d1 and d2 > 0).
           TODO: implement for x = 0!
        """
        if df1 <= 0 or df2 <= 0:
            raise IncorrectInputError()

        A = math.pow(df1*x, df1)
        B = math.pow(df2, df2)
        C = math.pow(df1*x+df2, df1+df2)
        D = math.pow(A*B/C, 0.5)
        beta = functions.beta_function(df1/2, df2/2)
        return D/(x*beta)

    def f_cdf(x, df1, df2):
        """
           Gives the value of the Fisher cumulative density function
           for the given x (x must be in [0, inf))and the specified
           parameters of the Fisher distribution- df1 and df2 specify
           the degrees of freedom (d1 and d2 > 0).
        """
        if df1 <= 0 or df2 <= 0:
            raise IncorrectInputError()

        index = df1*x/(df1*x+df2)
        A = functions.incomplete_beta_function(index, df1/2, df2/2)
        B = functions.beta_function(df1/2, df2/2)
        return A/B

    def __init__(self, df1, df2):
        """
           Sets the parameters for the Fisher distribution.
           The degrees of freedon d1 and d2 must be > 0.
        """
        if df1 <= 0 or df2 <= 0:
            raise IncorrectDistributionInicializationError()

        self.df1 = df1
        self.df2 = df2
        if df2 > 2:
            self.mean = df2/(df2-2)
        else:
            self.mean = "not defined"
        if df2 > 4:
            A = 2*math.pow(df2, 2)*(df1*df2-2)
            B = df1*math.pow(df2-2, 2)*(df2-4)
            self.variance = A/B
        else:
            self.variance = "not defined"
        # maybe not so
        self.median = "not defined"
        if df1 > 2:
            self.mode = ((df1-2)/df1)*(df2/(df2+2))
        else:
            self.mode = "not defined"
        # self.skewness = 0
        # self.ex_kurtosis = 0

    def pdf(self, x):
        """
           Gives the value of the Fisher probability density function
           for the given x.
        """
        df1 = self.df1
        df2 = self.df2
        return FisherDistribution.f_pdf(x, df1, df2)

    def cdf(self, x):
        """
           Gives the value of the Fisher cumulative density function
           for the given x.
        """
        df1 = self.df1
        df2 = self.df2
        return FisherDistribution.f_cdf(x, df1, df2)


class t_Distribution():
    """
       Implements the t-distribution with its basic features.
       For more information:
       http://mathworld.wolfram.com/Studentst-Distribution.html
    """
    def t_pdf(x, df):
        """
           Gives the value of the t probability density function
           for the given x (x can be any real number)and the specified
           parameter of the t-distribution- df specifies
           the degrees of freedom (df > 0).
        """
        if df <= 0:
            raise IncorrectInputError()

        f = functions.gamma_function
        A = f((df+1)/2)
        B = math.pow(df*math.pi, 0.5)*f(df/2)
        C = -(df+1)/2
        D = 1+math.pow(x, 2)/df
        return A/B*math.pow(D, C)

    def t_cdf(x, df):
        """
           Gives the value of the t cumulative distribution function
           for the given x (x can be any real number)and the specified
           parameter of the t-distribution- df specifies
           the degrees of freedom (df > 0).
        """
        if df <= 0:
            raise IncorrectInputError()

        b = functions.regularized_beta_function
        A = b(df/(df+math.pow(x, 2)), df/2, 1/2)
        main_element = 1-A
        if x < 0:
            main_element = - main_element
        the_sum = 1/2 + 1/2*main_element
        return the_sum

    def __init__(self, df):
        """
           Sets the parameters for the t distribution.
           The degrees of freedon df must be > 0.
        """
        if df <= 0:
            raise IncorrectDistributionInicializationError()

        self.df = df
        if df > 1:
            self.mean = 0
        else:
            self.mean = "not defined"

        if df > 2:
            self.variance = df/(df-2)
        elif 1 < df <= 2:
            self.variance = "infinite"
        else:
            self.variance = "not defined"

        self.median = 0
        self.mode = 0

        if df > 3:
            self.skewness = 0
        else:
            self.skewness = "not defined"

        if df > 4:
            self.ex_kurtosis = 6/(df-4)
        elif 2 < df <= 4:
            self.ex_kurtosis = "infinite"
        else:
            self.ex_kurtosis = "not defined"

    def pdf(self, x):
        """
           Gives the value of the t probability density function
           for the given x.
        """
        df = self.df
        return t_Distribution.t_pdf(x, df)

    def cdf(self, x):
        """
           Gives the value of the t cumulative density function
           for the given x.
        """
        df = self.df
        return t_Distribution.t_cdf(x, df)


class ChiSquaredDistribution():
    """
       Implements the chi-squared distribution with its basic features.
       For more information:
       http://en.wikipedia.org/wiki/Chi-squared_distribution#Characteristics
    """
    def chi_squared_pdf(x, df):
        """
           Gives the value of the chi-squared probability density function
           for the given x (x can be any real number, >= 0)and the specified
           parameter of the chi-squareddistribution- df specifies
           the degrees of freedom (df > 0).
        """
        if df <= 0:
            raise IncorrectInputError()

        if x < 0:
            return 0
        A = math.pow(x, df/2-1)*math.exp(-x/2)
        B = math.pow(2, df/2)*functions.gamma_function(df/2)
        return A/B

    def chi_squared_cdf(x, df):
        """
           Gives the value of the chi-squared probability density function
           for the given x (x can be any real number, >= 0)and the specified
           parameter of the chi-squareddistribution- df specifies
           the degrees of freedom (df > 0).
        """
        if df <= 0:
            raise IncorrectInputError()

        if x < 0:
            return 0
        A = functions.lower_incomplete_gamma_function(df/2, x/2)
        B = functions.gamma_function(df/2)
        return A/B

    def __init__(self, df):
        """
           Sets the parameters for the chi-squared distribution.
           df must be > 0.
        """
        if df <= 0:
            raise IncorrectDistributionInicializationError()

        self.df = df
        self.mean = df
        self.variance = 2*df
        self.median = df*math.pow(1-2/(9*df), 3)
        if 0 >= df-2:
            self.mode = 0
        else:
            self.mode = df-2
        self.skewness = math.pow(8/df, 0.5)
        self.ex_kurtosis = 12/df

    def pdf(self, x):
        """
           Gives the value of the chi-squared probability density function
           for the given x.
        """
        df = self.df
        return ChiSquaredDistribution.chi_squared_pdf(x, df)

    def cdf(self, x):
        """
           Gives the value of the chi-squared cumulative distribution function
           for the given x.
        """
        df = self.df
        return ChiSquaredDistribution.chi_squared_cdf(x, df)


class PoissonDistribution():
    """
       Implements the Poisson distribution with its basic features.
       For more information:
       http://en.wikipedia.org/wiki/Poisson_distribution
    """
    def poisson_pmf(k, the_lambda):
        """
           Gives the value of the Poisson probability mass function
           for the given k (k can be a whole, nonnrgative nuber)
           and the specified parameter of the Poisson distribution-
           the_lambda must be > 0.
        """
        if the_lambda <= 0:
            raise IncorrectInputError()

        A = math.pow(the_lambda, k)
        B = math.exp(-the_lambda)
        C = functions.factorial(k)
        return A*B/C

    def poisson_cdf(k, the_lambda):
        """
           Gives the value of the Poisson cumulative density function
           for the given k (k can be a whole, nonnrgative nuber)
           and the specified parameter of the Poisson distribution-
           the_lambda must be > 0.
        """
        if the_lambda <= 0:
            raise IncorrectInputError()

        A = math.exp(-the_lambda)
        index = functions.floor_function(k)
        summation = 0
        for i in range(index+1):
            summation += math.pow(the_lambda, i)/functions.factorial(i)
        return A*summation

    def __init__(self, the_lambda):
        """
           Sets the parameters for the Poisson distribution.
           the_lambda must be > 0
        """
        if the_lambda <= 0:
            raise IncorrectDistributionInicializationError()

        self.the_lambda = the_lambda
        self.mean = the_lambda
        self.variance = the_lambda
        self.median = functions.floor_function(the_lambda+1/3-0.02/the_lambda)
        self.mode = functions.floor_function(the_lambda)
        self.skewness = math.pow(the_lambda, -0.5)
        self.ex_kurtosis = math.pow(the_lambda, -1)

    def pmf(self, k):
        """
           Gives the value of the Poisson probability mass function
           for the given k (k >= 0, whole number).
        """
        the_lambda = self.the_lambda
        return PoissonDistribution.poisson_pmf(k, the_lambda)

    def cdf(self, k):
        """
           Gives the value of the Poisson cumulative density function
           for the given k (k >= 0, whole number).
        """
        the_lambda = self.the_lambda
        return PoissonDistribution.poisson_cdf(k, the_lambda)

    def exact(self, k):
        """
           Gives the exact probability for occurence of the given k
           (k >= 0, whole number)
        """
        the_lambda = self.the_lambda
        A = PoissonDistribution.poisson_cdf(k, the_lambda)
        if k == 0:
            return A
        B = PoissonDistribution.poisson_cdf(k-1, the_lambda)
        return A - B


class ZipfDistribution():
    """
       Implements the Zipf distribution with its basic features.
       For more information:
       http://en.wikipedia.org/wiki/Zipf%27s_law
    """
    def zipf_pmf(k, s, N):
        """
           Gives the value of the Zipf probability mass function
           for the given k (k can be a whole, in [1, 2, ..., N])
           and the specified parameters of the Zipf distribution-
           s >= 0, N in [1, 2, ...]
        """
        A = 1/math.pow(k, s)
        B = functions.generalized_harmonic_number_function(N, s)
        return A/B

    def zipf_cdf(k, s, N):
        """
           Gives the value of the Zipf cumulative distribution function
           for the given k (k can be a whole, in [1, 2, ..., N])
           and the specified parameters of the Zipf distribution-
           s >= 0, N in [1, 2, ...]
        """
        A = functions.generalized_harmonic_number_function(k, s)
        B = functions.generalized_harmonic_number_function(N, s)
        return A/B

    def __init__(self, s, N):
        """
           Sets the parameters for the Zipf distribution.
           s must be > 0.
        """
        if s < 0:
            raise IncorrectDistributionInicializationError()

        self.s = s
        self.N = N

        A = functions.generalized_harmonic_number_function(N, s-1)
        B = functions.generalized_harmonic_number_function(N, s)
        self.mean = A/B

        # http://mathworld.wolfram.com/ZipfDistribution.html
        # http://mathworld.wolfram.com/RiemannZetaFunction.html
        # - bad integral
        # self.variance = "Implement me!"

        self.mode = 1

    def pmf(self, k):
        """
           Gives the value of the Zipf probability mass function
           for the given k (k in [1, 2, ..., N]).
        """
        s = self.s
        N = self.N
        return ZipfDistribution.zipf_pmf(k, s, N)

    def cdf(self, k):
        """
           Gives the value of the Zipf cumulative density function
           for the given k (k in [1, 2, ..., N]).
        """
        s = self.s
        N = self.N
        return ZipfDistribution.zipf_cdf(k, s, N)


def find_percentile(percentile, cdf, args=None):
    """
       Finds the percentile of the given cdf.
       (https://en.wikipedia.org/wiki/Percentile)
       * percentile specifies the wanted percentile (must be in (0, 1)).
       * cdf is the cdf of interest
       * args provides the additional arguments necessary for
         the cdf function.
    """
    if percentile >= 1 or percentile <= 0:
        raise PercentileError()

    start = 0.01
    end = 10

    if args is None:
        if cdf(start) > percentile:
            while cdf(start) >= percentile:
                start -= 50
        while cdf(end) < percentile:
            end += end

        middle = (start + end)/2
        while abs(cdf(middle)-(percentile)) > 0.0001:
            if cdf(middle) > percentile:
                end = middle
            else:
                start = middle
            middle = (start + end)/2
    else:
        if cdf(start, *args) > percentile:
            while cdf(start, *args) >= percentile:
                start -= 50
        while cdf(end, *args) < percentile:
            end += end

        middle = (start + end)/2
        while abs(cdf(middle, *args)-(percentile)) > 0.0001:
            if cdf(middle, *args) > percentile:
                end = middle
            else:
                start = middle
            middle = (start + end)/2

    return middle
