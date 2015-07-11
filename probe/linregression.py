from probe import matrices


def add_to_matrix_for_intercept(a_matrix):
    """
       Adds a column of 1-s to the regressor matrix for better
       performance of the linear regression model.
    """
    n1 = len(a_matrix.matrix)
    n2 = len(a_matrix.matrix[0])
    new_matrix_list = []
    for i in range(n1):
        new_matrix_list.append([1])
    for i in range(n1):
        for j in range(n2):
            new_matrix_list[i].append(a_matrix.matrix[i][j])
    return matrices.Matrix(new_matrix_list)


def coeficents_estimation(regressand_vector_matrix_raw, regressor_matrix):
    """
       Estimates the optimal coeficents in the linear regression model
       using the method of least squares.
       -
       For more information:
       http://en.wikipedia.org/wiki/
       Linear_least_squares_%28mathematics%29#Computation
       -
    """
    regressand_matrix = regressand_vector_matrix_raw.transposed()
    regressor_matrix = add_to_matrix_for_intercept(regressor_matrix)

    transposed = regressor_matrix.transposed()
    D = matrices.multiplication(transposed, regressor_matrix)
    C = D.find_inverse()
    F = matrices.multiplication(C, transposed)
    K = matrices.multiplication(F, regressand_matrix)

    return K.transpose().matrix
