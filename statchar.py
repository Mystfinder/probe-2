import math


"""
1. aritmetic_mean
2. SS
3. SS_abstract
4. SS_with_mean
5. SStreat
6. SSres
7. SStot
8. power_sum
9. median
10. mode
11. std_dev_uncorrected
12. std_dev_corrected
13. std_error_of_mean
14. skewness
15. remove_heavy_ouliers
"""


class StatcharError(Exception):
    def __str__(self):
        return repr("An error for statchar.py")


class NotAListError(StatcharError):
    def __str__(self):
        return repr("Given variable not a list.")


class ListsNotWithSameLengthError(StatcharError):
    def __str__(self):
        return repr("Given lists are not with same length as required.")


def aritmetic_mean(data):
    """
       Computes the aritmetic mean of the given data.
    """
    if type(data) is not list:
        raise NotAListError()

    mean = 0
    for element in data:
        mean += element
    else:
        mean /= len(data)
    return mean


def SS(data):
    """
        Computes the standard sum of squares of a sample.
        -
        For more information (concretization needed):
        https://stat.ethz.ch/education/semesters/as2010/anova/
        ANOVA_how_to_do.pdf
        -
    """
    if type(data) is not list:
        raise NotAListError()

    mean = aritmetic_mean(data)
    sum_of_squares = 0
    for element in data:
        sum_of_squares += math.pow(element-mean, 2)
    return sum_of_squares


def SS_abstract(list_1, list_2):
    """
        Computes the difference of two elements with same index ind the
        given data lists, then takes a square. Sums all squares.
        Lists must be with same length!
    """
    if type(list_1) is not list:
        raise NotAListError()
    if type(list_2) is not list:
        raise NotAListError()

    n = len(list_1)
    p = len(list_2)
    if n != p:
        raise ListsNotWithSameLengthError()

    summation = 0
    for i in range(n):
        summation += math.pow(list_1[i]-list_2[i], 2)
    return summation


def SS_with_mean(data, mean):
    """
        Computes sum of squares whereas form every element from the data
        one substracts the mean argument.
    """
    if type(data) is not list:
        raise NotAListError()

    SS = 0
    for i in range(len(data)):
        SS += math.pow(data[i]-mean, 2)
    return SS


def SStreat(data_for_length, data):
    """
       Computes sum of squares in ANOVA context-
       sum of squares between treatment groups: multiplies treatments and
       number of observation. The two arguments must be with same length!
    """
    if type(data_for_length) is not list:
        raise NotAListError()
    if type(data) is not list:
        raise NotAListError()
    if len(data_for_length) != len(data):
        raise ListsNotWithSameLengthError()

    SST = 0
    for i in range(len(data)):
        SST += math.pow(data[i], 2) * len(data_for_length[i])
    return SST


def SSres(data_lists, means_list):
    """
        A generalizations SS_with_mean with many data lists and respective
        maeans list, interpretated in ANOVA context-
        sum of squares within treatment groups.
    """
    if type(data_lists) is not list:
        raise NotAListError()
    if type(means_list) is not list:
        raise NotAListError()

    SSR = 0
    for i in range(len(data_lists)):
        for j in range(len(data_lists[i])):
            SSR += math.pow(data_lists[i][j]-means_list[i], 2)
    return SSR


# perhaps to add the possibility to return the grand mean
def SStot(data_lists, grand_mean=False):
    """
        Computes the sum of squares for all the data lists, the grand
        mean for the data is used for substraction. If the grand mean
        is not specified it is calculated.
    """
    if type(data_lists) is not list:
        raise NotAListError()

    sum_of_all = 0
    count_of_all_data = 0
    if grand_mean is False:
        for list_element in data_lists:
            count_of_all_data += len(list_element)
            for data_element in list_element:
                sum_of_all += data_element
        grand_mean = sum_of_all/count_of_all_data

    SStot = 0
    for i in range(len(data_lists)):
        for j in range(len(data_lists[i])):
            SStot += math.pow(data_lists[i][j]-grand_mean, 2)
    return SStot


def power_sum(data, power):
    """
       Substracts form each element of data the estimated mean
       and sums everything.
    """
    mean = aritmetic_mean(data)
    power_sum = 0
    for element in data:
        power_sum += math.pow(element-mean, power)
    return power_sum


def median(data):
    """
        Calculates an estimation of the median of the sample.
    """
    if type(data) is not list:
        raise NotAListError()

    sorted_data = sorted(data)
    length = len(sorted_data)
    if length % 2 != 0:
        return sorted_data[length//2]
    else:
        return (sorted_data[length//2 - 1] + sorted_data[length//2])/2


def mode(data, show_frequency=False):
    if type(data) is not list:
        raise NotAListError()
    """
        Calculates an estimation of the mode of the sample.
        For more information: ???
    """
    frequency = {}
    for element in data:
        if element not in frequency.keys():
            frequency[element] = 1
        else:
            frequency[element] += 1

    mode_element = None
    mode_frequency = 0
    multi_mode = []

    for element, times in frequency.items():
        if times > mode_frequency:
            mode_element = element
            mode_frequency = times

    for element, times in frequency.items():
        if times == mode_frequency:
            multi_mode.append(element)

    if show_frequency is False:
        return multi_mode
    else:
        return multi_mode, mode_frequency


def std_dev_uncorrected(data):
    """
        Calculates an uncorected estimation of the standard deviation of the
        given sample.
        -
        For more information: http://en.wikipedia.org/wiki/
        Standard_deviation#Estimation
        -
    """
    std_dev = SS(data)
    std_dev /= len(data)
    std_dev = math.pow(std_dev, 0.5)
    return std_dev


def std_dev_corrected(data):
    """
        Calculates the corected estimation of the standard deviation of the
        given sample.
        -
        For more information: http://en.wikipedia.org/wiki/
        Standard_deviation#Estimation
        -
    """
    std_dev = SS(data)
    std_dev /= len(data)-1
    std_dev = math.pow(std_dev, 0.5)
    return std_dev


def std_error_of_mean(data):
    """
       Calculates the standard error of the mean.
    """
    A = std_dev_corrected(data)
    B = math.pow(len(data), 0.5)
    return A/B


def skewness(data):
    """
       Calculates the skewness of the presented data.
    """
    if type(data) is not list:
        raise NotAListError()

    length = len(data)
    expr1 = power_sum(data, 3)
    expr2 = power_sum(data, 2)

    expr1 /= length
    expr2 = math.pow(expr2/length, 3/2)
    return (math.pow(length*(length-1), 2)*expr1)/((length-2)*expr2)


def correlation_coeficient(data_list_1, data_list_2):
    """
       Calculates Pearson correlation coefficient.
       data_list_1 and data_list_2 must be of same length.
    """
    if type(data_list_1) is not list:
        raise NotAListError()
    if type(data_list_2) is not list:
        raise NotAListError()
    if len(data_list_1) != len(data_list_2):
        raise ListsNotWithSameLengthError()

    n = len(data_list_1)

    A = 0
    B = 0
    C = 0
    D = 0
    E = 0
    F = 0
    G = 0
    for i in range(n):
        A += data_list_1[i]*data_list_2[i]
        B += data_list_1[i]
        C += data_list_2[i]

        D += math.pow(data_list_1[i], 2)
        E += data_list_1[i]

        F += math.pow(data_list_2[i], 2)
        G += data_list_2[i]

    nominator = n*A - B*C
    denominator_1 = math.pow(n*D - math.pow(E, 2), 0.5)
    denominator_2 = math.pow(n*F - math.pow(G, 2), 0.5)
    denominator = denominator_1*denominator_2

    return nominator/denominator


def remove_heavy_outliers(data, mean, std_dev):
    """
       Removes heavy outliers from the sample. An emement is considered
       an outlier if it is not in [mean - 1.5*std_dev, mean + 1.5*std_dev]
    """
    if type(data) is not list:
        raise NotAListError()

    criterion1 = mean - 1.5*std_dev
    criterion2 = mean + 1.5*std_dev
    modified_data = []
    for element in data:
        if element >= criterion1 and element <= criterion2:
            modified_data.append(element)
    return modified_data
