import math
from probe import distributions
from probe import statchar


def confidence_interval(data, percentile, number_of_tails):
    """
       Computes confidence interval for the
       mean of the given data covering the probability given by the
       variable percentile.
       * data specifies the given data.
       * precentile gives the probability that the mean of the data is in
         the confidence interval.
       * number_of_tails gives the number of tails of the normal distribution
         to be considered.
    """
    square = math.pow(len(data), 0.5)
    mean = statchar.aritmetic_mean(data)
    std_dev = statchar.std_dev_corrected(data)
    dist = distributions.NormalDistribution(0, 1)
    if number_of_tails == 2:
        alfa = (1-percentile)/2
        c = distributions.find_percentile(1-alfa, dist.cdf)
        left = mean - c*std_dev/square
        right = mean + c*std_dev/square
        return left, right
    elif number_of_tails == 1:
        alfa = percentile
        c = distributions.find_percentile(alfa, dist.cdf)
        SEM = statchar.std_error_of_mean(data)
        left = mean
        right = mean + c*SEM/square
        return right

data = [6, 12, 9, 2, 4, 9, 15, 3, 9, 3, 4, 2, 8, 4]


def confidence_interval_theoretical(n, mean, std_dev, percentile,
                                    number_of_tails, SEM=0):
    """
       Computes confidence interval for the mean of the implicite data
       covering the probability given by the variable percentile.
       * n specifies the number of observations in the implicit data.
       * mean specifies the mean of the implicit data.
       * std_dev specifies the standard deviation of the implicit data.
       * precentile gives the probability that the mean of the implicit
         data is in the confidence interval
       * number_of_tails gives the number of tails of the normal distribution
         to be considered.
       * SEM gives the estimated standard error of means, it should be used
         only if tails == 1.
    """
    square = math.pow(n, 0.5)
    dist = distributions.NormalDistribution(0, 1)
    if number_of_tails == 2:
        alfa = (1-percentile)/2
        c = distributions.find_percentile(1-alfa, dist.cdf)
        left = mean - c*std_dev/square
        right = mean + c*std_dev/square
        return left, right
    elif number_of_tails == 1:
        alfa = percentile
        c = distributions.find_percentile(alfa, dist.cdf)
        right = mean + c*SEM/square

        return right
