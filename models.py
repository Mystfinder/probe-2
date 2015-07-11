from probe import distributions
from probe import linregression
from probe import matrices
from probe import statchar


class LinearRegression():
    """
       An inplementation of the linear regression model.
       For more information:
       http://en.wikipedia.org/wiki/Coefficient_of_determination
       http://www.r-tutor.com/elementary-statistics/multiple-linear-regression/multiple-coefficient-determination

    """
    def __init__(self, regressand_vector_matrix, regressor_matrix):
        self.regressand_vector_matrix = regressand_vector_matrix
        self.regressor_matrix = regressor_matrix

        f = linregression.add_to_matrix_for_intercept
        # Add intercept for improved performance of the model
        self.regressor_matrix_for_intecept = f(regressor_matrix)

        self.coeficents = linregression.coeficents_estimation(
            regressand_vector_matrix, regressor_matrix)
        self.mean = statchar.aritmetic_mean(regressand_vector_matrix.matrix[0])
        self.SStot = statchar.SS_with_mean(regressand_vector_matrix.matrix[0],
                                           self.mean)

        fi = []
        for element in regressor_matrix.matrix:
            fi.append(LinearRegression.predict(self,
                                               matrices.Matrix([element])))

        self.SSreg = statchar.SS_with_mean(fi, self.mean)
        self.SSres = statchar.SS_abstract(fi,
                                          regressand_vector_matrix.matrix[0])

        self.R_squared = self.SSreg/self.SStot

        n = len(regressand_vector_matrix.matrix[0])
        p = len(regressor_matrix.matrix[0])
        A = n - 1
        B = n - p - 1
        self.adjusted_R_squared = 1-(1-self.R_squared)*(A/B)

    def predict(self, regressor_row_matrix):
        f = linregression.add_to_matrix_for_intercept
        regressor_row_matrix = f(regressor_row_matrix)
        summation = 0
        for i in range(len(self.coeficents[0])):
            summation += self.coeficents[0][i]*regressor_row_matrix.matrix[0][i]
        return summation


class ANOVA():
    """
       An implementation of the ANOVA model. The zero hypothesis is
       that the means are equal.
       For more information:
       https://stat.ethz.ch/education/semesters/as2010/anova/ANOVA_how_to_do.pdf

    """
    def __init__(self, list_of_factors, list_of_data_sets):
        self.list_of_means = []
        for i in range(len(list_of_factors)):
            data = list_of_data_sets[i]
            self.list_of_means.append(statchar.aritmetic_mean(data))

        all_elements = []
        for i in range(len(list_of_factors)):
            all_elements += list_of_data_sets[i]
        self.grand_mean = statchar.aritmetic_mean(all_elements)

        self.estimated_effects = []
        for i in range(len(list_of_factors)):
            mean = self.list_of_means[i]
            self.estimated_effects.append(mean-self.grand_mean)

        # DF- degrees of freedom
        self.DFtreat = len(list_of_factors) - 1
        self.DFtot = len(all_elements) - 1
        self.DFres = (self.DFtot-self.DFtreat)

        # sum of squares
        self.SStreat = statchar.SStreat(list_of_data_sets,
                                        self.estimated_effects)
        self.SSres = statchar.SSres(list_of_data_sets, self.list_of_means)
        self.SStot = statchar.SStot(list_of_data_sets, self.grand_mean)

        # mean squares
        self.MStreat = self.SStreat/self.DFtreat
        self.MSres = self.SSres/self.DFres

        self.F = self.MStreat/self.MSres

    def decision(self, percentile):
        critical = distributions.find_percentile(
            percentile, distributions.FisherDistribution.f_cdf,
            [self.DFtreat, self.DFres])
        if self.F > critical:
            return "Reject null hypothesis."
        else:
            return "Accept null hyphothesis."
