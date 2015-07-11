import math
import pygal
import os

"""
1. print_graph
2. print_graph_discrete
3. print_histogram
4. print_compare
5. correlate
6. log_log_correlate

1. numerical_integration (proper integral)

1. factorial
2. semi_factorial
3. hypergeometric_function(+)
4. beta_function
5. incomplete beta_function
6. regularized_beta_function
7. gamma_function
8. lower_incomplete gamma_function
9. error_function
10. inverse_error_function
11. floor_function
12. ceiling_function
13. harmonic_number_function
14. generalized_harmonic_number_function
"""


class FucntionsError(Exception):
    def __str__(self):
        return repr("An error for functions.py")


class NamingError(FucntionsError):
    def __str__(self):
        return repr("Naming requirements not matched. Please check function.")


class ListsNotWithSameLengtgError(FucntionsError):
    def __str__(self):
        return repr("Given lists are not with same length as required.")


class IncorrectInputError(FucntionsError):
    def __str__(self):
        return repr("Incorrecr input for function, check description.")


def print_graph(function, interval, step, coords=True,
                name="Function graph.svg"):
    """
       Draws the graph of a univariate, continuous(quite) function.
    """
    if type(name) is not str:
        raise NamingError()

    if interval[0] > interval[1]:
        raise IncorrectInputError

    coordinate = interval[0]
    coordinates = []
    points = []
    while coordinate <= interval[1]:
        coordinates.append(coordinate)
        points.append(function(coordinate))
        coordinate += step

    line_chart = pygal.Line(dots_size=1, x_label_rotation=90)
    line_chart.title = 'Graph'
    if coords is True:
        if interval[0] >= 0 and interval[1] >= 0:
            length = interval[1] - interval[0]
        elif interval[0] < 0 and interval[1] >= 0:
            length = abs(interval[1]) + abs(interval[0])
        elif interval[0] < 0 and interval[1] < 0:
            length = abs(interval[0]) - abs(interval[1])
        if length/step > 50:
            new_step = length/50
            coordinates = []
            coordinate = interval[0]
            while coordinate <= interval[1]:
                coordinates.append(coordinate)
                coordinate += new_step
        line_chart.x_labels = map(str, coordinates)

    line_chart.add('Values', points)

    current_dir = os.getcwd()
    if not os.path.exists(current_dir+"\probe svg container"):
        os.makedirs(current_dir+"\probe svg container")
    os.chdir(os.getcwd()+"\probe svg container")
    line_chart.render_to_file(name)
    os.chdir(os.getcwd().split("\probe svg container")[0])


just_names = ["unnamed discrete graph.svg", "Title", "Something"]


def print_graph_discrete(data, sort_data=True, stroke=True,
                         coords=True, names=just_names):
    """
        Plots discrete data.
        * data can be a list, or list of lists. Values of names[2] correspond
          to these cases. If data is list of lists, the length of the lists
          should be the same, otherwise the values will not be printed
          correctly.
        * sort_data sorts the data in ascending order. If data is a list
          of lists all lists are sorted.
        * stroke specifies whether lines between the dots will be present in
          the graph. If stroke = True (default) there will be lines. If
          stroke = False there will be no lines
        * coords assigns numbers to the x-axis indicating the number of the
          observation. If len(data) > 75 the x-axis will be overcrowded, so
          len(data) is partitioned into 75 steps and these steps are assign
          as x-axis coordinates. Caution - if data is list of lists it is
          wise that the lists inside are of the same length!
        * names assigns names to various commponents of the graph. names[0]
          specifies the name of the file where the graph is stored (must
          end with ".svg"), names[1] gives the title of the graph (visible)
          from within the file, and names[2] contains the names to be
          given to the components of data.
    """
    for element in names:
        if type(element) is not list:
            if type(element) is not str:
                raise NamingError()
        else:
            for inner_element in element:
                if type(inner_element) is not str:
                    raise NamingError()

    the_data = []
    if sort_data is True:
        if type(data[0]) is list:
            for a_list in data:
                new = sorted(a_list)
                the_data.append(new)
        else:
            the_data = sorted(data)
    else:
        the_data = data

    if stroke is False:
        line_chart = pygal.Line(dots_size=1, x_label_rotation=90, stroke=False)
    else:
        line_chart = pygal.Line(dots_size=1, x_label_rotation=90)

    coordinates = []
    if coords is True:
        if type(the_data[0]) is not list:
            length = len(the_data)
        else:
            length = len(the_data[0])
        if length > 50:
            new_step = length/50
            coordinate = 1
            while coordinate <= length:
                coordinates.append(coordinate)
                coordinate += new_step
        else:
            coordinate = 1
            while coordinate <= length:
                coordinates.append(coordinate)
                coordinate += 1
        line_chart.x_labels = map(str, coordinates)

    points = []
    if type(the_data[0]) is list:
        i = 0
        for a_list in the_data:
            points.append([])
            for element in a_list:
                points[i].append(element)
            i += 1
    else:
        for element in the_data:
            points.append(element)

    line_chart.title = names[1]
    if type(names[2]) is list:
        i = 0
        for element in names[2]:
            line_chart.add(element, points[i])
            i += 1
    else:
        line_chart.add(names[2], points)

    current_dir = os.getcwd()
    if not os.path.exists(current_dir+"\probe svg container"):
        os.makedirs(current_dir+"\probe svg container")
    os.chdir(os.getcwd()+"\probe svg container")
    line_chart.render_to_file(names[0])
    os.chdir(os.getcwd().split("\probe svg container")[0])


just_names = ["unnamed histogram.svg", "Title", "thing"]


def print_histogram(data_list, number_of_bars, exact=False,
                    normalize=False, table_names=just_names,):
    """
       Prints a histogram of the data presented in data_list.
       * data_list can be a list with int or float object.
       * number_of_bars specifies the number of bars of interest. If
         exact is False number_of_bars MUST be an int or float object,
         the bars are created artificially and the data is split
         automatically. If exact is True then number_of_bars MUST
         be a list of lists with two elements containing the boundaries
         of the bars to be shown. Note: if [3,7] are two boundary
         values all elements with values >= 3 and < 7 will be taken
         into account in the bar; if [3,3] all elements with value
         = 3 will be taken into account.
       * exact - see above
       * names assigns names to various commponents of the histogram. names[0]
         specifies the name of the file where the histogram is stored (must
         end with ".svg"), names[1] gives the title of the histogram (visible)
         from within the file, and names[2] contains the name to be
         given to the data.
    """
    for element in table_names:
        if type(element) is not list:
            if type(element) is not str:
                raise NamingError()
        else:
            for inner_element in element:
                if type(inner_element) is not str:
                    raise NamingError()

    counts = []
    names = []

    if exact is True:
        for element in number_of_bars:
            count = 0
            left = element[0]
            right = element[1]
            for data_element in data_list:
                if left == right:
                    if data_element == left:
                        count += 1
                elif data_element >= left and data_element < right:
                    count += 1
            counts.append(count)
            if left == right:
                names.append(str(left))
            else:
                names.append(str(left)+"-"+str(right))
    else:
        data_count = len(data_list)
        reasonable_number_of_bars = int(data_count/3)
        if number_of_bars > reasonable_number_of_bars:
            a_string = "Unreasonably many bars selected. Number of bars set to {0}"
            print(a_string.format(reasonable_number_of_bars))
            number_of_bars = reasonable_number_of_bars

        maximum = max(data_list)
        minimum = min(data_list)
        length = maximum - minimum
        step = length/number_of_bars
        current = minimum
        while current != maximum:
            count = 0
            for element in data_list:
                if element >= current and element <= (current+step):
                    count += 1
            counts.append(count)
            names.append(str(current)+"-"+str(current+step))
            current += step

    if exact is False and normalize is True:
        maximum = max(data_list)
        minimum = min(data_list)
        length = maximum - minimum
        step = length/number_of_bars

        area = 0
        for element in counts:
            area += step*element
        normalized_counts = []
        for element in counts:
            normalized_element = element/area
            normalized_counts.append(normalized_element)
        counts = normalized_counts

    bar_chart = pygal.Bar(x_label_rotation=90)
    bar_chart.x_labels = names

    bar_chart.title = table_names[1]
    bar_chart.add(table_names[2], counts)

    current_dir = os.getcwd()
    if not os.path.exists(current_dir+"\probe svg container"):
        os.makedirs(current_dir+"\probe svg container")
    os.chdir(os.getcwd()+"\probe svg container")
    bar_chart.render_to_file(table_names[0])
    os.chdir(os.getcwd().split("\probe svg container")[0])


just_names = ["unnamed comparison.svg", "Title",
              ["meta histogram for the data", "some function"]]


def print_comparison(meta_histogram_parameters, functions_list,
                     names=just_names):
    """
       Due to not being implementet in pygal, this functions tries
       to combine the graph of a histogram and the graphs of some
       other probability density functions. The histogram itself is
       printed as a pygal Line object, the resemblence to the actual
       histogram should be sufficient.
       * meta_histogram_parametes is a list with specifications for
         the histogram. meta_histogram_parametes[0] is the data list
         for the histogram, meta_histogram_parametes[1] is the number
         of wanted bars
       * functions_list is a list with the probability density
         functions wanted
       * names assigns names to various commponents of the meta histogram.
         names[0] specifies the name of the file where the meta histogram
         is stored (must end with ".svg"), names[1] gives the title of the meta
         histogram (visible) from within the file, and names[2] contains the
         names to be given to the printed data- names[2][0] is the name of the
         data for which the meta histogram is for, names[2][i] is the name
         for the i-th function for which the comparison is being made.

    """
    for element in names:
        if type(element) is not list:
            if type(element) is not str:
                raise NamingError()
        else:
            for inner_element in element:
                if type(inner_element) is not str:
                    raise NamingError()

    data_list = meta_histogram_parameters[0]
    number_of_bars = meta_histogram_parameters[1]
    data_count = len(data_list)
    reasonable_number_of_bars = int(data_count/3)
    if number_of_bars > reasonable_number_of_bars:
        a_string = "Unreasonably many bars selected. Number of bars set to {0}"
        print(a_string.format(reasonable_number_of_bars))
        number_of_bars = reasonable_number_of_bars

    counts = []
    middle_points = []
    inner_names = []

    maximum = max(data_list)
    minimum = min(data_list)
    length = maximum - minimum
    step = length/number_of_bars

    # compose meta histogram
    hist_step = length/number_of_bars
    current = minimum
    while current <= maximum:
        count = 0
        for element in data_list:
            if element >= current and element < (current+step):
                count += 1
        counts.append(count)
        middle_points.append(int((current + (current + step))/2))
        inner_names.append(str(current)+"-"+str(current+step))
        current += hist_step

    # normalize the meta hsitogram
    area = 0
    for element in counts:
        area += step*element
    normalized_counts = []
    for element in counts:
        normalized_element = element/area
        normalized_counts.append(normalized_element)

    line_chart = pygal.Line(x_label_rotation=90)
    line_chart.title = names[1]
    line_chart.x_labels = inner_names
    line_chart.add(names[2][0], normalized_counts)

    # print the functions
    i = 1
    for function in functions_list:
        j = 0
        current_point = middle_points[0]
        points = []
        while current_point <= middle_points[-1]:
            points.append(function(current_point))
            try:
                j += 1
                current_point = middle_points[j]
            except IndexError:
                current_point += 1
        line_chart.add(names[2][i], points)
        i += 1

    current_dir = os.getcwd()
    if not os.path.exists(current_dir+"\probe svg container"):
        os.makedirs(current_dir+"\probe svg container")
    os.chdir(os.getcwd()+"\probe svg container")
    line_chart.render_to_file(names[0])
    os.chdir(os.getcwd().split("\probe svg container")[0])


just_names = ["unnamed correlation.svg", "Title", ["thing1", "thing2"]]


def correlate(data_list1, data_list2, names=just_names):
    """
       Gives a correlation graph of the data in data_list1 and data_list2.
       names specifies the names given to the various elements in the
       graph- names[0] specifies the name of the file where the graph
       is stored (must end with ".svg"), names[1] gives the title of
       the graph, the list names[2] specifies the names of the data in
       data_list1 and data_list2.
    """
    for element in names:
        if type(element) is not list:
            if type(element) is not str:
                raise NamingError()
        else:
            if len(element) != 2:
                raise NamingError()
            for inner_element in element:
                if type(inner_element) is not str:
                    raise NamingError()

    if len(data_list1) != len(data_list2):
        raise ListsNotWithSameLengtgError()

    xy_chart = pygal.XY(stroke=False)
    xy_chart.title = names[1]

    tuple_list = []
    for i in range(len(data_list1)):
        element = (data_list1[i], data_list2[i])
        tuple_list.append(element)

    the_name = "Correlation between {0} and {1}".format(names[2][0],
                                                        names[2][1])
    xy_chart.add(the_name, tuple_list)

    current_dir = os.getcwd()
    if not os.path.exists(current_dir+"\probe svg container"):
        os.makedirs(current_dir+"\probe svg container")
    os.chdir(os.getcwd()+"\probe svg container")
    xy_chart.render_to_file(names[0])
    os.chdir(os.getcwd().split("\probe svg container")[0])


just_names = ["log-log correlation.svg", "Title", ["thing1", "thing2"]]


def log_log_correlate(data_list1, data_list2, names=just_names):
    """
       Transforms the data in data_list1 and data_list2 into natural
       logarithms and gives a correlation graph of the data.
       data_list1 and data_list2 MUST NOT contain data <=0.
       names specifies the names given to the various elements in the
       graph- names[0] specifies the name of the file where the graph
       is stored (must end with ".svg"), names[1] gives the title of
       the graph, the list names[2] specifies the names of the data in
       data_list1 and data_list2.
    """
    for element in names:
        if type(element) is not list:
            if type(element) is not str:
                raise NamingError()
        else:
            if len(element) != 2:
                raise NamingError()
            for inner_element in element:
                if type(inner_element) is not str:
                    raise NamingError()

    if len(data_list1) != len(data_list2):
        raise ListsNotWithSameLengtgError()

    log_list1 = []
    log_list2 = []
    try:
        for i in range(len(data_list1)):
            log_list1.append(math.log(data_list1[i]))
            log_list2.append(math.log(data_list2[i]))
    except ValueError:
        raise IncorrectInputError()

    xy_chart = pygal.XY(stroke=False)
    xy_chart.title = names[1]

    tuple_list = []
    for i in range(len(data_list1)):
        element = (log_list1[i], log_list2[i])
        tuple_list.append(element)

    the_name = "Correlation between {0} and {1}".format(names[2][0],
                                                        names[2][1])
    xy_chart.add(the_name, tuple_list)

    current_dir = os.getcwd()
    if not os.path.exists(current_dir+"\probe svg container"):
        os.makedirs(current_dir+"\probe svg container")
    os.chdir(os.getcwd()+"\probe svg container")
    xy_chart.render_to_file(names[0])
    os.chdir(os.getcwd().split("\probe svg container")[0])


def numerical_integration_finite(interval, function, iterations=10000):
    """ Numerically calculates a proper integral using
        the composite trapezoid rule.
        -
        For more information: http://en.wikipedia.org/wiki/
        Numerical_integration
        -
    """
    if interval[0] == interval[1]:
        return 0
    summation = 0
    summation += 1/2*function(interval[0])
    summation += 1/2*function(interval[1])
    n = iterations
    for k in range(1, n):
        element = k*(interval[1]-interval[0])/n
        summation += function(interval[0]+element)
    return (interval[1]-interval[0])/n*summation


def factorial(p, power_reduction=False):
    """ Calculates the factorial function. Argument must be an
        int object or a float object of the type integer.0.
        Argument must be >= 0.
        Returns int object.
        For more information: http://en.wikipedia.org/wiki/Factorial
    """
    if type(p) is not int:
        if type(p) is not float:
            raise IncorrectInputError()
        elif int(p) != p:
            raise IncorrectInputError()
        else:
            p = int(p)
    if p < 0:
        raise IncorrectInputError()
    if p == 0:
        return 1
    multiplication = 1
    if power_reduction is False:
        for i in range(2, p):
            multiplication *= i
        else:
            multiplication *= p
        return multiplication
    elif power_reduction is True:
        power_reduction = 0
        for i in range(2, p):
            multiplication *= i
            if multiplication > math.pow(10, 100):
                multiplication /= math.pow(10, 100)
                power_reduction += 1
        else:
            multiplication *= p
            if multiplication > math.pow(10, 100):
                multiplication /= math.pow(10, 100)
                power_reduction += 1
        return [multiplication, power_reduction]


def semi_factorial(start, n, power_reduction=False):
    """ Calculates a somewhat reversed factorial. Argument start is in
        (-inf, inf), argument n is an int object or float object of the
        type number.0. n >= 0
        -
        For more information: http://mathworld.wolfram.com/
        PochhammerSymbol.html
        -
    """
    if type(start) is not int:
        if type(start) is not float:
            raise IncorrectInputError()
    if type(n) is not int:
        if type(n) is not float:
            raise IncorrectInputError()
        elif int(n) != n:
            raise IncorrectInputError()

    if n < 0:
        raise IncorrectInputError()

    if n == 0:
        return 1
    multiplication = start
    if power_reduction is False:
        for i in range(1, n):
            multiplication *= start + i
        return multiplication
    elif power_reduction is True:
        power_reduction = 0
        for i in range(1, n):
            multiplication *= start + i
            if multiplication > math.pow(10, 100):
                multiplication /= math.pow(10, 100)
                power_reduction += 1
        return [multiplication, power_reduction]


def hypergeometric_function(list_a, list_b, x):
    """ Calculates the hypergeometric functions in its most general form.
        -
        For more information:
        1. http://en.wikipedia.org/wiki/
        Generalized_hypergeometric_function#Notation
        *
        2. http://mathworld.wolfram.com/HypergeometricFunction.html
        !! Bugs detected, avoid if possible !!
        -
    """
    n = 200
    summation = 0
    for i in range(n):
        A = 1
        B = 1
        power_reduction_1 = 0
        power_reduction_2 = 0
        for element in list_a:
            result_1 = []
            if i >= 1:
                result_1 = semi_factorial(element, i, True)
            else:
                result_1.append(1)
                result_1.append(0)

            A *= result_1[0]
            power_reduction_1 = result_1[1]
        for element in list_b:
            result_2 = []
            if i >= 1:
                result_2 = semi_factorial(element, i, True)
            else:
                result_2.append(1)
                result_2.append(0)

            B *= result_2[0]
            power_reduction_2 = result_2[1]

        C = []
        if i >= 1:
            C = factorial(i, True)
        else:
            C.append(1)
            C.append(0)

        D = 1
        power_reduction_3 = 0
        for p in range(i):
            D *= x
            if D > math.pow(10, 100):
                D /= math.pow(10, 100)
                power_reduction_3 += 1

        difference = power_reduction_1 + power_reduction_3 - C[1]
        difference -= power_reduction_2
        asd = ((A/B)*(D/C[0]))
        summation += ((A/B)*(D/C[0]))*math.pow(math.pow(10, 100), difference)

    return summation


def beta_function(a, b):
    """ Calculates the beta function. n principle arguments a, b >0
        but implemented for a, b >= 1.
        For more information: http://en.wikipedia.org/wiki/Beta_function
    """
    if type(a) is not int:
        if type(a) is not float:
            raise IncorrectInputError()
    if a <= 0:
        raise IncorrectInputError()
    if type(b) is not int:
        if type(b) is not float:
            raise IncorrectInputError()
    if b <= 0:
        raise IncorrectInputError()

    def integrand(t):
        if t == 0 or t == 1:
            return 0
        A = math.pow(t, a-1)
        B = math.pow(1-t, b-1)
        return A*B
    return numerical_integration_finite([0, 1], integrand)


def incomplete_beta_function(x, a, b):
    """ Calculates the incomplete beta function. In principle arguments a, b >0
        but implemented for a, b >= 1.
        -
        For more information: http://en.wikipedia.org/wiki/
        Beta_function#Incomplete_beta_function
        -
        !! It is not specified whether x => 0, x <= 1.
        It is assumed that x => 0, x <= 1 !!
    """
    if type(x) is not int:
        if type(x) is not float:
            raise IncorrectInputError()
    if x < 0 or x > 1:
        raise IncorrectInputError()
    if type(a) is not int:
        if type(a) is not float:
            raise IncorrectInputError()
    if a <= 0:
        raise IncorrectInputError()
    if type(b) is not int:
        if type(b) is not float:
            raise IncorrectInputError()
    if b <= 0:
        raise IncorrectInputError()

    def integrand(t):
        if t == 0 or t == 1:
            return 0
        A = math.pow(t, a-1)
        B = math.pow(1-t, b-1)
        return A*B
    return numerical_integration_finite([0, x], integrand)


def regularized_beta_function(x, a, b):
    """
       Calculates the regularized beta function.
       For more information:
       http://mathworld.wolfram.com/RegularizedBetaFunction.html
    """
    return incomplete_beta_function(x, a, b)/beta_function(a, b)


def gamma_function(t):
    """ Calculates the gamma function. Argument t > 0.
        -
        For more information: http://en.wikipedia.org/wiki/
        Gamma_function#Alternative_definitions
        -
    """
    if type(t) is not int:
        if type(t) is not float:
            raise IncorrectInputError()
    if t <= 0:
        raise IncorrectInputError()

    Euler_Mascheroni_constant = 0.577216
    A = math.exp(-Euler_Mascheroni_constant*t)/t
    B = 1
    for i in range(100000):
        C = math.pow(1+t/(i+1), - 1)
        D = math.exp(t/(i+1))
        B *= C*D
    return A*B


def lower_incomplete_gamma_function(s, x):
    """ Calculates the lower incomplete gamma function.
        Argumensts s, x > 0.
        -
        For more information:
        http://en.wikipedia.org/wiki/
        Incomplete_gamma_function#Definition;
        *
        http://en.wikipedia.org/wiki/
        Incomplete_gamma_function#Continuation_to_complex_values
        -
    """
    if type(s) is not int:
        if type(s) is not float:
            raise IncorrectInputError()
    if s <= 0:
        raise IncorrectInputError()
    if type(x) is not int:
        if type(x) is not float:
            raise IncorrectInputError()
    if x < 0:
        raise IncorrectInputError()

    def integrand(t):
        if t == 0:
            return 0
        A = math.pow(t, s-1)
        B = math.exp(-t)
        return A*B
    return numerical_integration_finite([0, x], integrand)


def error_function(x):
    """ Calculates the error function (Gauss error function). Takes
        arguments in (-inf, inf).
        For more information: http://en.wikipedia.org/wiki/Error_function
        """
    if type(x) is not int:
        if type(x) is not float:
            raise IncorrectInputError()

    def integrand(t):
        return math.exp(-math.pow(t, 2))
    A = numerical_integration_finite([0, x], integrand)
    B = 2/math.pow(math.pi, 0.5)
    return A*B


def inverse_error_function(x):
    """ Calculates the inverse of the error function. Takes arguments in
        [-1, 1].
        -
        For more information: http://en.wikipedia.org/wiki/
        Error_function#Inverse_functions
        -
    """
    if type(x) is not int:
        if type(x) is not float:
            raise IncorrectInputError()
    if x < -1 or x > 1:
        raise IncorrectInputError()

    coeficients = [1, 1]
    series = 0

    def next_coeficient(index):
        m = 0
        summation = 0
        while m <= index-1:
            A = (m+1)*(2*m+1)
            summation += coeficients[m]*coeficients[index-1-m]/A
            m += 1
        coeficients.append(summation)
    for index in range(2, 650):
        next_coeficient(index)
    for index in range(0, 650):
        A = coeficients[index]/(2*index+1)
        B = math.pow(math.pi, 0.5)/2*x
        C = math.pow(B, 2*index+1)
        series += A*C
    return series


def floor_function(x):
    """ Calculates the floor function. Argument can be int or float object.
        Returns int object.
        -
        For more information: http://en.wikipedia.org/wiki/
        Floor_and_ceiling_functions
        -
        """
    if type(x) is not int:
        if type(x) is not float:
            raise IncorrectInputError()

    integer = 0
    if x > 0:
        while integer < x:
            integer += 1
            if integer == x:
                return integer
        return integer - 1
    elif x < 0:
        while integer > x:
            integer -= 1
            if integer == x:
                return integer
        return integer
    else:
        return 0


def ceiling_function(x):
    """ Calculates the ceiling function. Argument can be int or float object.
        Returns int object.
        -
        For more information: http://en.wikipedia.org/wiki/
        Floor_and_ceiling_functions
        -
        """
    if type(x) is not int:
        if type(x) is not float:
            raise IncorrectInputError()

    integer = 0
    if x > 0:
        while integer < x:
            integer += 1
            if integer == x:
                return integer
        return integer
    elif x < 0:
        while integer > x:
            integer -= 1
            if integer == x:
                return integer
        return integer + 1
    else:
        return 0


def harmonic_number_function(n):
    """ Calculates harmonic numbers. Argumnet must be an int object or
        float object of the type integer.0. Argument must be >= 1.
        For more information: http://en.wikipedia.org/wiki/Harmonic_number
        """
    if type(n) is not int:
        if type(n) is not float:
            raise IncorrectInputError()
        elif int(n) != n:
            raise IncorrectInputError()
        else:
            n = int(n)
    if n < 1:
        raise IncorrectInputError()
    summation = 0
    for i in range(1, n+1):
        summation += 1/i
    return summation


def generalized_harmonic_number_function(n, r):
    """ Calculates generalized harmonic numbers. Argumnets n and r must
        be an int object or float object of the type integer.0.
        Argument n must be >= 1.
        For more information: http://mathworld.wolfram.com/HarmonicNumber.html
        (formula (31))
        !! It is not specified whether r >= 0. It is assumed that  r is in
        (-inf, inf) !!
        """
    if type(n) is not int:
        if type(n) is not float:
            raise IncorrectInputError()
        elif int(n) != n:
            raise IncorrectInputError()
        else:
            n = int(n)
    if type(r) is not int:
        if type(r) is not float:
            raise IncorrectInputError()
        elif int(r) != r:
            raise IncorrectInputError()
        else:
            r = int(r)
    if n < 1:
        raise IncorrectInputError()

    summation = 0
    for i in range(1, n+1):
        try:
            summation += 1/math.pow(i, r)
        except OverflowError:
            summation += 0
    return summation
