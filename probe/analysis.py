import math
from probe import statchar
from probe import distributions
from probe import functions


"""
1. preliminary_analysis
2. compare_data_sets
"""


def preliminary_analysis(data_list, additional_parameters):
    """
       Performs a preliminary analysis.
       More specificaly compares the data in data_list with
       the implemented distributions and gives the sum of
       squares of the differences between the the empirical
       cdf and the cdfs of the implemented distributions.
       Prints a "cdf comparison.svg" graph with the cdfs.
       * additional_parameters specifies the parameters with
         which the distributions will be initialized:
         ** additional_parameters[0] == True -> a Normal distribution
            with parameters estimated from data_list will be
            initialized.
         ** additional_parameters[1] == [a, b] -> a Fisher distribution
            with pratameters [a, b] will be initialized.
         ** additional_parameters[2] == [a] -> a t-distribution with
            parameter [a] will be initialized.
         ** additional_parameters[3] == [a] -> a chi-squared distribution
            with parameter [a] will be initialized
         ** if additional_parameters[i] == False the corresponding
            distribution will not be initialized.
       ! For Fisher distribution check- the values id data_list must
         be >= 0.
    """
    # Data characteristics
    mean = statchar.aritmetic_mean(data_list)
    std_dev_corrected = statchar.std_dev_corrected(data_list)
    skewness = statchar.skewness(data_list)

    median = statchar.median(data_list)
    mode = statchar.mode(data_list)

    info_dict = {}
    info_dict["mean"] = mean
    info_dict["std_dev_corrected"] = std_dev_corrected
    info_dict["skewness"] = skewness
    info_dict["median"] = median
    info_dict["mode"] = mode

    active_distributions_list = []
    i = 0
    for element in additional_parameters:
        if i == 0 and element is not False:
            estimated_variance = math.pow(std_dev_corrected, 2)
            dist = distributions.NormalDistribution
            active_distributions_list.append(dist(mean, estimated_variance))
        if i == 1 and element is not False:
            dist = distributions.FisherDistribution
            active_distributions_list.append(dist(*additional_parameters[1]))
        if i == 2 and element is not False:
            dist = distributions.t_Distribution
            active_distributions_list.append(dist(*additional_parameters[2]))
        if i == 3 and element is not False:
            dist = distributions.ChiSquaredDistribution
            active_distributions_list.append(dist(*additional_parameters[3]))
        elif element is False:
            active_distributions_list.append(False)
        i += 1

    only_active_distributions_list = []
    for element in active_distributions_list:
        if element is not False:
            only_active_distributions_list.append(element)

    compare_cdf = distributions.compare
    compare_cdf_dict = {}

    print("Data characteristics:")
    for key, value in info_dict.items():
        print("{0}: {1}".format(key, value))
    print("-----------------------")

    # Normal distribution
    normal_dist = None
    normal_info_dict = {}
    if active_distributions_list[0] is not False:
        normal_dist = active_distributions_list[0]
        normal_info_dict["mean"] = normal_dist.mean
        normal_info_dict["std_dev"] = math.pow(normal_dist.variance, 0.5)
        normal_info_dict["variance"] = normal_dist.variance
        normal_info_dict["skewness"] = normal_dist.skewness
        normal_info_dict["median"] = normal_dist.median
        normal_info_dict["mode"] = normal_dist.mode

        print("Normal distribution:")
        for key, value in normal_info_dict.items():
            print("{0}: {1}".format(key, value))
        print("-----------------------")

        compare_cdf_dict["Normal distribution"] = compare_cdf(data_list,
                                                              normal_dist)
    # Fisher distribution
    fisher_dist = None
    fisher_info_dict = {}
    if active_distributions_list[1] is not False:
        fisher_dist = active_distributions_list[1]
        fisher_info_dict["mean"] = fisher_dist.mean
        if fisher_dist.variance == "not defined":
            fisher_info_dict["std_dev"] = "not defined"
            fisher_info_dict["variance"] = "not defined"
        else:
            fisher_info_dict["std_dev"] = math.pow(fisher_dist.variance, 0.5)
            fisher_info_dict["variance"] = fisher_dist.variance
        # fisher_info_dict["skewness"] = fisher_dist.skewness
        fisher_info_dict["median"] = fisher_dist.median
        fisher_info_dict["mode"] = fisher_dist.mode

        print("Fisher distribution:")
        for key, value in fisher_info_dict.items():
            print("{0}: {1}".format(key, value))
        print("-----------------------")

        compare_cdf_dict["Fisher distribution"] = compare_cdf(data_list,
                                                              fisher_dist)

    # t-distribution
    t_dist = None
    t_info_dict = {}
    if active_distributions_list[2] is not False:
        t_dist = active_distributions_list[2]
        t_info_dict["mean"] = t_dist.mean
        if t_dist.variance == "not defined":
            t_info_dict["std_dev"] = "not defined"
            t_info_dict["variance"] = "not defined"
        elif t_dist.variance == "infinite":
            t_info_dict["std_dev"] = "infinite"
            t_info_dict["variance"] = "infinite"
        else:
            t_info_dict["std_dev"] = math.pow(t_dist.variance, 0.5)
            t_info_dict["variance"] = t_dist.variance
        t_info_dict["skewness"] = t_dist.skewness
        t_info_dict["median"] = t_dist.median
        t_info_dict["mode"] = t_dist.mode

        print("t-distribution:")
        for key, value in t_info_dict.items():
            print("{0}: {1}".format(key, value))
        print("-----------------------")

        compare_cdf_dict["t-distribution"] = compare_cdf(data_list,
                                                         t_dist)

    # chi-squared distribution
    chi_dist = None
    chi_info_dict = {}
    if active_distributions_list[3] is not False:
        chi_dist = active_distributions_list[3]
        chi_info_dict["mean"] = chi_dist.mean
        chi_info_dict["std_dev"] = math.pow(chi_dist.variance,
                                            0.5)
        chi_info_dict["variance"] = chi_dist.variance
        chi_info_dict["skewness"] = chi_dist.skewness
        chi_info_dict["median"] = chi_dist.median
        chi_info_dict["mode"] = chi_dist.mode

        print("chi-squared distribution:")
        for key, value in chi_info_dict.items():
            print("{0}: {1}".format(key, value))
        print("-----------------------")

        result = compare_cdf(data_list, chi_dist)
        compare_cdf_dict["chi-squared distribution"] = result

    comparison_cdf_graph = distributions.compare_cdf_with_theoretical
    comparison_cdf_graph(data_list, only_active_distributions_list)

    print("Sum of squares between the cdfs of the empirical and that of the")
    for key, value in compare_cdf_dict.items():
        print("{0}: {1}".format(key, value))


def compare_data_sets(data_list_1, data_list_2, names_list):
    """
       Compares two data sets.
       Prints a graph "Comparison between two data sets.svg" comparing
       the elements of the data sets directrly.
       Prints a graph "Correlation between two data sets.svg" showing
       the correlation between the two data sets.
       Retruns the Pearson correlation coeficient.
    """
    result = statchar.correlation_coeficient(data_list_1, data_list_2)

    names_list_discrete = ["Comparison between two data sets.svg",
                           "Comparison between two data sets",
                           names_list]
    names_list_correlate = ["Correlation between two data sets.svg",
                            "Correlation between two data sets",
                            names_list]
    functions.print_graph_discrete([data_list_1, data_list_2], False,
                                   False, True, names_list_discrete)
    functions.correlate(data_list_1, data_list_2, names_list_correlate)

    return result
