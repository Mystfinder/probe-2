import math

"""
class Matrix:
1.transposed
1.5. transpose
2. truncated_matrix
2.5. truncate_matrix
3. simple_determinant
4. expnad_row
5. find_determinant
6. find_inverse

1. transpose_row
2. multiplication
"""


class MatricesError(Exception):
    def __str__(self):
        return repr("An error for matrices.py")


class NotARowError(MatricesError):
    def __str__(self):
        return repr("The given row is empty.")


class EmptyRowError(MatricesError):
    def __str__(self):
        return repr("The given element is not considered a column.")


class NotAMatrixError(MatricesError):
    def __str__(self):
        return repr("The given element is not considered a matrix.")


class IncorrectInputError(MatricesError):
    def __str__(self):
        return repr("Input does not match function requirements.")


class NoInverseError(MatricesError):
    def __str__(self):
        return repr("The determinant of the matrix is 0- it has no inverse.")


class NonValidMatricesForMultiplicationError(MatricesError):
    def __str__(self):
        return repr("Requirements for multiplication not men.")


class Matrix():
    """
       A matrix is a list of lists- every inner list represents a
       single matrix row. Every element in a row can be either a float
       or int object.
       ---
       Example: [[1, -2, 3], [5, 6.6, -7.0]]
    """
    def __init__(self, list_of_rows):
        if type(list_of_rows) is not list:
            raise NotAMatrixError()
        if list_of_rows != []:
            length = len(list_of_rows[0])
            for row in list_of_rows:
                if type(row) is not list:
                    raise NotAMatrixError()
                if len(row) != length:
                    raise NotAMatrixError()
                for element in row:
                    if type(element) is not float:
                        if type(element) is not int:
                            raise NotAMatrixError()
        else:
            raise NotAMatrixError()

        self.matrix = list_of_rows
        self.determinant = None
        self.inverse = None

    def transposed(self):
        """
            Takes a matrix in the form [[row_1], [row_2],..., [row_n]]
            and returns its transpose. The original matrix is not changed.
            For more information: http://en.wikipedia.org/wiki/Transpose
        """
        n1 = len(self.matrix)

        n2 = len(self.matrix[0])

        transpose = []
        for i in range(n2):
            transpose.append([])

        for i in range(n1):
            p = transpose_row([self.matrix[i]])
            for j in range(n2):
                transpose[j].append(p[j][0])

        return Matrix(transpose)

    def transpose(self):
        """ Takes a matrix in the form [[row_1], [row_2],..., [row_n]]
    and returns its transpose. The original matrix is changed.
    For more information: http://en.wikipedia.org/wiki/Transpose
    """
        n1 = len(self.matrix)
        n2 = len(self.matrix[0])

        transpose = []
        for i in range(n2):
            transpose.append([])

        for i in range(n1):
            p = transpose_row([self.matrix[i]])
            for j in range(n2):
                transpose[j].append(p[j][0])

        self.matrix = transpose
        return self

    def truncated_matrix(self, row, column, multiplier=False):
        """
            Takes a matrix A and returns the matrix that results
            when deleting the specified row and column form A. The original
            matrix is not changed.
            If multiplier is True also returns the element which results
            when intersecting the specified row and column (used in
            Laplace formuma:
            http://en.wikipedia.org/wiki/
            Determinant#Laplace.27s_formula_and_the_adjugate_matrix )
        """
        n = len(self.matrix) - 1
        new_matrix_list = []
        the_multiplier = self.matrix[row-1][column-1]
        for i in range(n):
            new_row = []
            if i < row-1:
                for j in range(n):
                    if j < column-1:
                        new_row.append(self.matrix[i][j])
                    else:
                        new_row.append(self.matrix[i][j+1])
                new_matrix_list.append(new_row)
            else:
                for j in range(n):
                    if j < column-1:
                        new_row.append(self.matrix[i+1][j])
                    else:
                        new_row.append(self.matrix[i+1][j+1])
                new_matrix_list.append(new_row)

        if multiplier is False:
            return Matrix(new_matrix_list)
        elif multiplier is True:
            return Matrix(new_matrix_list), the_multiplier

    def truncate_matrix(self, row, column, multiplier=False):
        """
            Takes a matrix A and returns the matrix that results
            when deleting the specified row and column form A. The original
            matrix is changed.
            If multiplier is True also returns the element which results
            when intersecting the specified row and column (used in
            Laplace formuma:
            http://en.wikipedia.org/wiki/
            Determinant#Laplace.27s_formula_and_the_adjugate_matrix )
        """
        n = len(self.matrix) - 1
        new_matrix_list = []
        the_multiplier = self.matrix[row-1][column-1]
        for i in range(n):
            new_row = []
            if i < row-1:
                for j in range(n):
                    if j < column-1:
                        new_row.append(self.matrix[i][j])
                    else:
                        new_row.append(self.matrix[i][j+1])
                new_matrix_list.append(new_row)
            else:
                for j in range(n):
                    if j < column-1:
                        new_row.append(self.matrix[i+1][j])
                    else:
                        new_row.append(self.matrix[i+1][j+1])
                new_matrix_list.append(new_row)

        self.matrix = new_matrix_list

        if multiplier is False:
            return self
        elif multiplier is True:
            return self, the_multiplier

    def simple_determinant(the_matrix):
        """
           Given a matrix with one row and one column retrurns its determinant.
           Given a matrix with 2 rows and 2 columns returns its determinant.
        """
        if len(the_matrix.matrix) == 1 and len(the_matrix.matrix[0]) == 1:
            return the_matrix.matrix[0][0]
        a = the_matrix.matrix[0][0]*the_matrix.matrix[1][1]
        b = the_matrix.matrix[0][1]*the_matrix.matrix[1][0]
        return a-b

    def expand_row(self):
        """
            Given a square matrix returns its coeficents and expansion
            according to the Laplace's formula. The expansion is performed
            on the first row of the matrix.
            -
            For more information: http://en.wikipedia.org/wiki/
            Determinant#Laplace.27s_formula_and_the_adjugate_matrix)
            -
        """
        row_length = len(self.matrix)
        column_length = len(self.matrix[0])
        if row_length != column_length:
            raise IncorrectInputError()

        expansion_list = [(1, self)]
        n = len(self.matrix)
        while len(expansion_list[0][1].matrix[0]) > 2:
            new_list = []
            for element in expansion_list:
                for i in range(len(element[1].matrix)):
                    result = element[1].truncated_matrix(1, i+1,
                                                         multiplier=True)
                    mini_matrix = result[0]
                    multiplier = result[1]
                    new_list.append((math.pow(-1, i+1+1)*element[0]*multiplier,
                                     mini_matrix))
            expansion_list = new_list
        return expansion_list

    def find_determinant(self, give_expansion=False):
        """
            Calculates the determinant of a square matrix.
            If the given matrix is not
            square returns an IncorrectInputError.
            -
            For more information: http://en.wikipedia.org/wiki/
            Determinant#Laplace.27s_formula_and_the_adjugate_matrix
            -
        """
        expansion_list = self.expand_row()
        summation = 0
        for element in expansion_list:
            summation += element[0]*Matrix.simple_determinant(element[1])

        self.determinant = summation

        if give_expansion is False:
            return summation
        elif give_expansion is True:
            return summation, expansion_list

    def find_inverse(self):
        """
            Calculates the inverse matrix of a given square matrix.
            If the given matrix is not square returns an IncorrectInputError.
            If there is no inverse matrix returns a NoInverseError and
            sets the inverse attribute of the given matrix to
            "No inverse exists!"
            -
            For more information: http://en.wikipedia.org/wiki/
            Invertible_matrix#Analytic_solution, zaradi cofactorite ima (i+j)%2
            -
        """
        n = len(self.matrix)

        det = None
        if self.determinant is not None:
            det = self.determinant
        else:
            det = self.find_determinant()

        if n == 1:
            inverse_list = []
            inverse_list.append([1/self.matrix[0][0]])
            return Matrix(inverse_list)

        if det == 0:
            self.inverse = "No inverse exists!"
            raise NoInverseError()

        coef = 1/det

        if n == 2:
            inverse_list = [[], []]
            inverse_list[0].append(coef*self.matrix[1][1])
            inverse_list[0].append(-coef*self.matrix[0][1])
            inverse_list[1].append(-coef*self.matrix[1][0])
            inverse_list[1].append(coef*self.matrix[0][0])
            return Matrix(inverse_list)
        else:
            inverse_list = []
            for i in range(n):
                row = []
                for j in range(n):
                    component_matrix = self.truncated_matrix(j+1, i+1)

                    c = component_matrix.find_determinant()*coef
                    if (i+j) % 2 != 0:
                        c = -c
                    row.append(c)
                inverse_list.append(row)
        self.inverse = Matrix(inverse_list)
        return self.inverse


def transpose_row(row):
    """
       Takes a row in the form [[number_1, number_2,..., number_n]]
       and returns a column in the form [[number_1], [number_2],...,
       [munber_n]].
    """

    if type(row) is not list or len(row) > 1 or len(row) == 0:
        raise NotARowError()
    if row == [[]]:
        raise EmptyRowError()
    length = len(row[0])
    transposed_row = []
    for i in range(length):
        element = [row[0][i]]
        if type(element[0]) is not float:
            if type(element[0]) is not int:
                raise NotARowError()
        transposed_row.append(element)
    return transposed_row


def multiplication(A, B):
    """
       Given two matrices A with n rows and m columns, and B with m rows
       and p columns, returns their product- matrix C wirh n rows and p columns.
       -
       For more information: http://mathworld.wolfram.com/
       MatrixMultiplication.html
       -
    """
    n = len(A.matrix)
    m = len(A.matrix[0])
    p = len(B.matrix[0])

    if m != len(B.matrix):
        raise NonValidMatricesForMultiplicationError()

    new_matrix_list = []
    row = []
    for i in range(n):
        row = []
        for j in range(p):
            c = 0
            for k in range(m):
                c += A.matrix[i][k]*B.matrix[k][j]
            row.append(c)
        new_matrix_list.append(row)

    return Matrix(new_matrix_list)
