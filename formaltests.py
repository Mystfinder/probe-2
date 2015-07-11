import math
from probe import statchar
from probe import distributions


class FormaltestsError(Exception):
    def __str__(self):
        return repr("An error for formaltests.py")


class PercentileError(FormaltestsError):
    def __str__(self):
        return repr("Percentile must be within (0, 1)")


def shapiro_wilk_test(data, percentile):
    """
       Calculates the Shapiro-Wilks test for normal distribution of the
       given data. Variable percentile specifies the percentile given
       to the test. The null hypothesis is that the data is normally
       distributed.
    """
    if percentile >= 1 or percentile <= 0:
        raise PercentileError()

    n = len(data)
    sorted_data = sorted(data)
    m_list = []
    f = distributions.NormalDistribution.normal_quantile
    for i in range(n):
        var = (i+1-0.375)/(n+0.25)
        m_list.append(f(var, 0, 1))

    summation = 0
    for i in range(n):
        summation += math.pow(m_list[i], 2)

    coeficients = []
    u = 1/(math.pow(n, 0.5))

    A = -2.706056*math.pow(u, 5)
    B = 4.434685*math.pow(u, 4)
    C = -2.07119*math.pow(u, 3)
    D = -0.147981*math.pow(u, 2)
    E = 0.221157*u
    a_last = A+B+C+D+E+m_list[-1]*math.pow(summation, -0.5)

    A = -3.582633*math.pow(u, 5)
    B = 5.682633*math.pow(u, 4)
    C = -1.752461*math.pow(u, 3)
    D = -0.293762*math.pow(u, 2)
    E = 0.042981*u
    a_semi_last = A+B+C+D+E+m_list[-2]*math.pow(summation, -0.5)

    A = summation-2*math.pow(m_list[-1], 2)-2*math.pow(m_list[-2], 2)
    B = 1-2*math.pow(a_last, 2)-2*math.pow(a_semi_last, 2)
    e = A/B

    a_list = [-a_last, -a_semi_last]
    for i in range(2, n-2):
        a_list.append(m_list[i]/math.pow(e, 0.5))
    a_list += [a_semi_last, a_last]

    summation = 0
    for i in range(n):
        summation += a_list[i]*sorted_data[i]
    else:
        A = math.pow(summation, 2)
    B = statchar.SS(sorted_data)

    W = A/B

    A = 0.0038915*math.pow(math.log(n), 3)
    B = -0.083751*math.pow(math.log(n), 2)
    C = -0.31082*math.log(n)
    mean = A+B+C-1.5861

    A = 0.0030302*math.pow(math.log(n), 2)
    B = -0.082676*math.log(n)
    var_squared = math.exp(A+B-0.4803)

    z = (math.log(1-W)-mean)/var_squared
    critical = distributions.NormalDistribution.normal_quantile(percentile,
                                                                0, 1)
    if z > critical:
        print("Reject null hyphotesis. Data is not normally distributed.")
    else:
        print("Accept null hyphotesis. Data is normally distributed.")
    return W


def kolmogorov_smirnov_test(data, distribution, percentile):
    """
       Computes the Kolmogorov-Smirnov test. This test evaluates
       whether the data presented comes from the distribution
       given. percentile specifies the desired porbability. The
       null hypothesis is that the data is from the given distribution.
       -
       For more information:
       http://en.wikipedia.org/wiki/Kolmogorov%E2%80%93Smirnov_test#
       Kolmogorov.E2.80.93Smirnov_statistic
       -
    """
    if percentile >= 1 or percentile <= 0:
        raise PercentileError()

    data = sorted(data)
    F = distribution.cdf
    E = distributions.empirical_cdf
    K = distributions.KolmogorovDistribution.kolmogorov_cdf

    potential_statistic_list = []
    for element in data:
        potential_statistic_list.append(abs(E(element, data)-F(element)))
    Kolmogorov_Smirnov_statistic = max(potential_statistic_list)
    q = math.pow(len(data), 0.5)

    critical = distributions.find_percentile(percentile, K)

    if math.pow(len(data), 0.5)*Kolmogorov_Smirnov_statistic > critical:
        return False
    else:
        return True
