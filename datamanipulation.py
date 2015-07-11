import requests
from bs4 import BeautifulSoup
from probe import matrices
import os

import xlrd
import xlwt


"""
1. open_xls
2. write_xls

1. partition_into_list
2. recombinate_list
3.! filter_interval
4.! find_index
5.! extract_interval

1. get_data
2. extract_data

1. atomize_to_dicts
2. expanded_dict_list
3. associate
4. organize
5. separate

class Data:
1. get_data
2. extract_data
3. organize
4. organize_for_linear_regression
5. organize_for_ANOVA
"""


class DatamanipulationError(Exception):
    def __str__(self):
        return repr("An error for datamanipulation.py.")


class PageNotFoundError(DatamanipulationError):
    def __str__(self):
        return repr("Page did not respond.")


class NotAListError(DatamanipulationError):
    def __str__(self):
        return repr("Given variable not a list.")


class NotADictError(DatamanipulationError):
    def __str__(self):
        return repr("Given variable not a dict.")


def open_xls(filename, column_index_list, extraction_length_list):
    """
       Reads columns from given xls document (in the xls container folder).
       * filename specifies the name of the document: "name.xls"
       * column_index_list specifies the indices (in accordance with xlrd)
         of the wanted columns. If column_index_list is an integer, open_xls
         retrurns a list, if column_index_list is a list with integers,
         open_xls returns a list of lists.
       * extraction_length_list specifies how many rows will be affected by
         open_xls. If extraction_length_list is an integer n then from every
         column n entries will be extracted. If extraction_length_list is a
         list with integers then each value in the list gives the number of
         elements to be extracted from the column with corresponding
         index from column_index_list.
    """
    os.chdir(os.getcwd()+"\probe Excel container")
    book = xlrd.open_workbook(filename)
    os.chdir(os.getcwd().split("\probe Excel container")[0])
    first_sheet = book.sheet_by_index(0)
    data_list = []

    if type(column_index_list) is int:
        for i in range(extraction_length_list):
            value = first_sheet.cell(i, column_index_list).value
            data_list.append(value)
        return data_list

    for i in range(len(column_index_list)):
        data_list.append([])
    if type(extraction_length_list) is int:
        data_list_index = 0
        for column_index in column_index_list:
            for i in range(extraction_length_list):
                value = first_sheet.cell(i, column_index).value
                data_list[data_list_index].append(value)
            data_list_index += 1
    else:
        data_list_index = 0
        for column_index in column_index_list:
            for i in range(extraction_length_list[data_list_index]):
                value = first_sheet.cell(i, column_index).value
                data_list[data_list_index].append(value)
            data_list_index += 1

    if len(data_list) == 1:
        return data_list[0]
    else:
        return data_list


def write_xls(data_lists, filename, from_column_index=False):
    """
       Writes data to a xls file (in the xls container folder).
       * data_lists is the data to be writen to the xls file. It
         can be either a list, or a list of lists.
       * filename specifies the name of the new xls file. If a file with
         the same name already exists then a new file is created with the
         same name modified by the number added at its end. Example:
         "bananas.xls" is taken so "bananas1.xls" will be created, if
         "bananas1.xls" is taken then "bananas2.xls" will be created and
         so on...
       * from_column_index specifies the column from which onward the
         data will be written (the first column has index 0). If
         from_column_index is False (or 0) the first list in data_lists will be
         written to the first column, the second list will be written to
         the second_column.... If from_column_index = n then the first list
         in data_lists will be written to the n+1-th column the second list
         if data_lists will be written to the n+2-th column...
    """
    book = xlwt.Workbook(encoding="utf-8")
    sheet1 = book.add_sheet("Sheet1")

    first_time = True

    j = 0
    if from_column_index is not False:
        j = from_column_index

    if type(data_lists[0]) is not list:
        i = 0
        for element in data_lists:
            sheet1.write(i, j, element)
            i += 1

        current_dir = os.getcwd()
        if not os.path.exists(current_dir+"\probe Excel container"):
            os.makedirs(current_dir+"\probe Excel container")
        os.chdir(os.getcwd()+"\probe Excel container")
        book.save(filename)
        os.chdir(os.getcwd().split("\probe Excel container")[0])
    else:
        for a_list in data_lists:
            i = 0
            for element in a_list:
                sheet1.write(i, j, element)
                i += 1
            j += 1

        current_dir = os.getcwd()
        if not os.path.exists(current_dir+"\probe Excel container"):
            os.makedirs(current_dir+"\probe Excel container")
        os.chdir(os.getcwd()+"\probe Excel container")
        book.save(filename)
        os.chdir(os.getcwd().split("\probe Excel container")[0])


def partition_into_lists(given_list, length):
    """
       Divides the list into a new list of lists in the following manner.
       Example:
       a_list = [1,2,3,4,1,2,3,4,1,2,3,4]
       partition_into_lists(data, 4)
       the result is: [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]]
    """
    if type(given_list) is not list:
        raise NotAListError()

    big_list = []
    for i in range(length):
        big_list.append([])
    i = 0
    for element in given_list:
        big_list[i].append(element)
        i += 1
        if i == length:
            i = 0
    return big_list


def recombinate_list(list_of_lists):
    """
       Takes a list of lists and creates a new list win the following manner.
       Example:
       big_list = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]]
       recombinate_list(big_list)
       the result is: [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
       This functions reverses the result of the partition_into_lists
       function.
    """
    if type(list_of_lists) is not list:
        raise NotAListError()
    for element in list_of_lists:
        if type(element) is not list:
            raise NotAListError()

    recombination_list = []
    length = len(list_of_lists[0])

    i = 0
    for i in range(length):
        for element in list_of_lists:
            recombination_list.append(element[i])
    return recombination_list


def filter_interval(given_list, interesting_possition, length):
    """
       Filters the given_list list and returns a resulting list
       * interesting_possition specifies the first element of interest
         (in list enumeration)
       * length specifies the interval in which an elemenet of interest
         is appearing
       Example:
       a_list = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
       filter_interaval(a_list, 0, 4)
       the result is: [1, 1, 1]

    """
    if type(given_list) is not list:
        raise NotAListError()

    filtered_list = []
    i = 0
    for element in given_list:
        if i == interesting_possition:
            filtered_list.append(element)
        i += 1
        if i == length:
            i = 0

    return filtered_list


def find_index(a_list, sufficient_information, check=False):
    """
    sufficient_informations caries information sufficient for identification
    of an element. The elements of a_list MUST  of type str.
    Example:
    The element of interest is "/n/n/n/dasfaefafeafaf". Suppose "/n/n"
    is sufficient for the identification- then sufficient_information = "/n/n".
    find_index function returns the index of the first element identified
    in this way. If check is True then the identified element is displayed.
    """
    if type(a_list) is not list:
        raise NotAListError()

    index = None
    for element in a_list:
        if sufficient_information in element:
            index = a_list.index(element)
            if check is True:
                print(element)
            break

    return index


def extract_interval(a_list, interval, multiple=False):
    """
       Extracts the elements in a_list with inices in the specified interval.
       If multiple is True then a_list must be a list of lists and the
       result will be a list of lists with extracted elements as above.
    """
    if type(a_list) is not list:
        raise NotAListError()

    start = interval[0]
    end = interval[1]
    index = 0

    if multiple is True:
        big_list = []
        i = 0
        for small_list in a_list:
            big_list.append([])
            for element in small_list:
                if index >= start and index <= end:
                    big_list[i].append(element)
                index += 1
            i += 1
            index = 0
        return big_list
    else:
        new_list = []
        for element in a_list:
            if index >= start and index <= end:
                new_list.append(element)
            index += 1
        return new_list


def get_data(url, specify1, specify2, text=True,
             symbol="not specified", concrete=False, pattern=False):
    """
   !* Priority of arguments: url -> specify1 -> specify2 -> concrete ->
      pattern -> symbol-> text
    * url specifies target page
    * specify1 represents the first argument to be given to BeatifulSoup's
      find_all function. specify1 can be single a single string or
      a list with two strings- each string corresponds to an iteration of
      find_all, specifically with the second string find_all is applied
      to the subpage returned when performing find_all with the first ftring.
    * specify2 represents the second argument to be given to
      BeautifulSoup's find_all function.
      specify2 can be a single dictionary or a list of two dictionaries. The
      dictionaries have a single string key and a single string value.
      Each dictionary is unpacked into find_all. Each dictionary corresponds to
      a string in specify1 and is interpret as a filter for the data returned
      by find_all(specify1[i]). If a filter
      is required for specify1[1] but not for specify1[0] the specify2
      is of the form [None,{dictionary}].
    * text deals with the final type of the data that is being extracted.
      1. text = False
         means that the final type of the data will be float (if possible).
         In effect if data of the form "13424" is being extracted the
         resulting data will be 13424.0. Extracting data of the form
         "Nasty string!" with text = False will result in an error.
      2. text = True (by default)
         means that we do not want to midify the data that we extract.
         If the extracted data is of type str, the result will be data of
         type str, if the extracted data is of type float,
         the result will be data of type float.
      3. text = given_string
         means the same as 1. with addition that before the conversion
         to float if performed the given_string is being removed
         from the extracted string.
         Example:
         text = "," means "312,222"->"312222"->312222.0
      4. If the type of the extracted data is int or float the value of
         text will have no effect. The resulting data will be of type float.
    * symbol deals with unwanted symbols that can be encountered
      during extraction. symbol works only if text is not False.
      symbol can be a single character string or a list with two elements-
      the first one is a single character string and the second one
      is an int object > 0. If symbol is a single character string
      then the data will be splitted whenever the character is found,
      Example_1:
      symbol = ",", "asd,dsa"-> ["asd", "dsa"].
      If symbol is a list the interger points to the
      element in the partition that is of interest to us
      (0 points to the first element).
      Example_2:
      symbol = [",", 1], "asd,dsa"->["dsa"]
    * concrete deals with unnecessary data.
      concrete can be a list with two string values. The first value
      identifies the index of the first element of interest, the second value
      identifies theindex of the last element of interest
      (the find_index function is being used). If the first value is None
      the first index i 0, if the second value is None then the second index is
      lend(data)-1. Only data between those indeices proceeds to
      further evaluation.
    * pattern deals with the extraction of desired data form the resulting
      list knowing that the desired data is located on indices which differ
      by the integer n. Pattern can be a list with the integer values.
      The first integer specifies the index of the first element of
      interest, the second integer specifies the number n
      (the filter_interval function is being used)


    """
    page = requests.get(url)
    if page.status_code == 404:
        raise PageNotFoundError()
    soup = BeautifulSoup(page.content)

    if type(specify1) is list and type(specify2) is list:
        soup = soup.find_all(specify1[0], specify2[0])[0]
        specify1 = specify1[1]
        specify2 = specify2[1]
    elif type(specify1) is list:
        soup = soup.find_all(specify1[0])[0]
        specify1 = specify1[1]

    data = soup.find_all(specify1, specify2)

    the_list = []

    index_of_interest = None
    if type(symbol) is list:
        index_of_interest = symbol[1]
        symbol = symbol[0]

    text_list = []
    for element in data:
        text_list.append(element.text)

    if concrete is not False:
        if concrete[0] is not None:
            start = find_index(text_list, concrete[0])
        else:
            start = 0
        if concrete[1] is not None:
            end = find_index(text_list, concrete[1])
        else:
            end = len(text_list)-1
        text_list = extract_interval(text_list, [start, end])

    if pattern is not False:
        text_list = filter_interval(text_list, pattern[0], pattern[1])

    for element in text_list:
        if symbol is False:
            symbol = "not specified"
        elements = element.split(symbol)
        if type(element) is int or type(element) is float:
            the_list.append(float(element))
        elif text is True:
            if index_of_interest is None:
                for an_element in elements:
                    stripped_element = an_element.strip()
                    the_list.append(stripped_element)
            else:
                stripped_element = elements[index_of_interest].strip()
                the_list.append(stripped_element)
        elif text is False:
            if index_of_interest is None:
                for an_element in elements:
                    stripped_element = an_element.strip()
                    the_list.append(float(stripped_element))
            else:
                stripped_element = elements[index_of_interest].strip()
                the_list.append(float(stripped_element))
        elif type(text) is str:
            if index_of_interest is None:
                parts = []
                for an_element in elements:
                    stripped_element = an_element.strip()
                    more_parts = stripped_element.split(text)
                    stripped_element = "".join(more_parts)
                    the_list.append(float(stripped_element))
            else:
                stripped_element = elements[index_of_interest].strip()
                more_parts = stripped_element.split(text)
                stripped_element = "".join(more_parts)
                the_list.append(float(stripped_element))

    return the_list


def extract_data(parameters_lists):
    """
       Extracts the data specified by parameters_lists. Every list in
       parameters_list specifies data to be extracted, the extracted data
       is stored in a list, extrac_data returns a list of lists.
    """
    if type(parameters_lists) is not list:
        raise NotAListError()

    macro_list = []
    for parameters_list in parameters_lists:
        if type(parameters_list) is not list:
            raise NotAListError()
        macro_list.append(get_data(*parameters_list))
    return macro_list


def atomize_to_dicts(the_list, name):
    """
       Creates a list of dicts with single key and value where
       key = name, and the values correspond to the elements of the_list.
    """
    if type(the_list) is not list:
            raise NotAListError()

    dict_list = []
    for element in the_list:
        dict_list.append({name: element})
    return dict_list


def expanded_dict_list(dict_list_1, dict_list_2):
    """
       Takes two lists with dictionaries and returns a new list with
       dictionaries where the elements dict_list1[i] and dict_list2[i]
       are merged into a single dictionary which is an element of the
       new dictionary. If dict_list_1 and dict_list_2 have different
       lengths then expanded_dict_list will perform the merging for
       the number of elements of the smaller list.
    """
    if type(dict_list_1) is not list:
            raise NotAListError()
    if type(dict_list_2) is not list:
            raise NotAListError()

    expanded_dict_list = []
    for i in range(len(dict_list_1)):
        element_1 = dict_list_1[i]
        element_2 = dict_list_2[i]
        Y = element_1.copy()
        Y.update(element_2)
        expanded_dict_list.append(Y)

    return expanded_dict_list


def associate(the_lists, identifier=0):
    """
       Transforms the_lists into a single dict with keys the elements of
       the list with index = identifier, and values- a list of elements
       comprised of corresponding elements from the rest of the lists in
       the_lists.
    """
    if type(the_lists) is not list:
            raise NotAListError()
    else:
        for element in the_lists:
            if type(element) is not list:
                raise NotAListError()

    united_dict = {}
    keys = []
    values = []
    identifier_searcher = 0

    # Locates the indentifying data list- its elements will be keys for
    # the new dictionary. Also separates the remaining data in the values
    # list of lists.
    for element in the_lists:
        if identifier_searcher == identifier:
            keys = element
        else:
            values.append(element)
        identifier_searcher += 1
    # Assigns to every identifier element the corresponding data.
    for i in range(len(keys)):
        append_me = []
        for element in values:
            append_me.append(element[i])
        united_dict[keys[i]] = append_me
    return united_dict


def organize(all_data, names_list, identifier=0):
    """
       Organizes the data in all_data into a dict with elements of the form
       "identifying data element[i]": [list with one dictionary].
       -
       Example:
       We observe person1, person2 and person3 and we registrate that for
       time t the have ran m meters.
       Say we have
       list_1 = ["person1", "person2", "person3"],
       list_2 = [5,6,2] (the time measured),
       list_3 = [10,12,11] (the meters ran)
       and all_data = [list_1, list_2, list_3].
       Say we want to identify our observations by the person- we set
       identifier = 0 since all_data[0] == list_1.
       names_list provides the names we want to give to our osevations,
       say we give ["time", "length"] (corresponding to list2 and list3)
       The final result will be:
       {"person1":[{"time":5, "length":10}], "person2":[{"time":6,"length":12}]
       ,"person3":[{"time":2, "length":11}]}

    """
    if type(all_data) is not list:
            raise NotAListError()
    else:
        for element in all_data:
            if type(element) is not list:
                raise NotAListError()
    if type(names_list) is not list:
            raise NotAListError()

    data_list = []
    identifier_data = None
    for element in all_data:
        if element == all_data[identifier]:
            identifier_data = element
        else:
            data_list.append(element)

    # Assigns name to every element in every list in data_list
    atomized_list = []

    for i in range(len(data_list)):
        element = atomize_to_dicts(data_list[i], names_list[i])
        atomized_list.append(element)

    # Merges the two lists of dictionaries in the atomized_list list
    # and gives a new list of dictionaries.
    expansion = atomized_list[0]
    for element in atomized_list:
        if element == expansion:
            continue
        expansion = expanded_dict_list(expansion, element)

    all_lists = []
    all_lists.append(identifier_data)
    all_lists.append(expansion)
    organized = associate(all_lists)
    return organized


def separate(data_list, interval_of_separation):
    """
       Separates data_list into a list of lists with length equal
       to interval_of_separation. The rlements in each sublist are
       assigned in accordance with interval_of_separation in the
       following manner.
       Example:
       a_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
       separate(data_list, 3)
       the result is: [[1, 4, 7], [2, 5, 8], [3, 6, 9]]

    """
    if type(data_list) is not list:
            raise NotAListError()

    new_data_lists = []
    for i in range(interval_of_separation):
        new_data_lists.append([])

    i = 0
    for element in data_list:
        new_data_lists[i].append(element)
        i += 1
        if i == interval_of_separation:
            i = 0
    return new_data_lists


class Data():
    """
       Implements a container for data. The data is presented as a list
       of lists.
       The data given can be tranformed for use by the implemented models.
    """
    def __init__(self):
        self.unorganized_data = []
        self.organized_data = None
        self.organized_for_linear_regression = None

        self.organized_for_ANOVA_readable = None
        self.organized_for_ANOVA_use = None

    def get_data(self, parameters_list, return_it=False):
        """
           Extracts data from the internet with the get_data function.
        """
        data = get_data(*parameters_list)
        self.unorganized_data.append(data)
        if return_it is True:
            return data

    def extract_data(self, parameters_lists, return_it=False):
        """
           Extracts data from the internet with the extract_data function.
        """
        data = extract_data(parameters_lists)
        self.unorganized_data.append(data)
        if return_it is True:
            return data

    def organize(self, names_list,
                 identifier=0, return_it=False):
        """
           Organizes self.unorganized_data into a dict with one of
           the data lists in self.unorganized_data as the identifying key using
           the organize function.
        """
        organized = organize(self.unorganized_data, names_list, identifier)
        self.organized_data = organized
        if return_it is True:
            return organized

    def organize_for_linear_regression(self, regressand_name,
                                       observation_number=0):
        """
           Rearanges the data in self.organized_data into for suitable
           for linear regression.
           * regressand_name specifies which type of observation
             will be the regressand, the rest form the regressor matrix.
           * observation_number specifies which of the observations made
             (for all the identifiers) will be taken into account.
        """
        regressand_vector = []
        regressor_matrix_list = []

        names = []
        # Extracts the names of the observations. TODO: optimize.
        a_value = list(self.organized_data.values())[0][0]
        for key in a_value.keys():
            names.append(key)

        # Assigns the observations with regressand_name to the
        # regressand_vector and the others to the regressor_matrix_list.
        for value in self.organized_data.values():
            data = value[observation_number]
            regressor_matrix_row = []
            for name in names:
                if name == regressand_name:
                    regressand_vector.append(data[name])
                else:
                    regressor_matrix_row.append(data[name])
            regressor_matrix_list.append(regressor_matrix_row)

        regressand_vector_matrix = matrices.Matrix([regressand_vector])
        regressor_matrix = matrices.Matrix(regressor_matrix_list)
        self.organized_for_linear_regression = [regressand_vector_matrix,
                                                regressor_matrix]

    def organize_for_ANOVA(self, factor_values_list, transform_into_factor,
                           observation_number=0):
        """
           Rearanges the data into form compatible with the ANOVA model.
           * factor_value_list specifies the levels of the desired factor. If
             factor_value_list is a list without lists within, for every
             element a list will be created with data in self.organized_data
             corresponding to that element. If factor_value_list contains
             lists, the lists must be of the form [left_end, right_end],
             left_end specifies the left end of the elements in
             self.organized_data considered in the factor, right_end
             specifies the right end of the elements in self.organized_data
             considered in the factor (if left_end = 2 and right_end = 5,
             then the factor consists of elements >= 2, < 5).
           * transform_into_factor specifies which key in the subdicts in
             self.organized_data will be transformed to a factor (applying
             the procedure skeched above).
           * observation_number specifies which obseravation in
             self.organized_data will be used for the ANOVA.
        """
        if type(factor_values_list) is not list:
            raise NotAListError()

        factor_dict = {}
        for factor in factor_values_list:
            element_list = []
            if type(factor) is list:
                left_end = factor[0]
                right_end = factor[1]
                for value_list in self.organized_data.values():
                    element = value_list[observation_number]
                    for key, value in element.items():
                        if key == transform_into_factor:
                            if left_end <= value and value <= right_end:
                                element_list.append(value)
                name = str(left_end) + "-" + str(right_end)
                factor_dict[name] = element_list
            else:
                for value_list in self.organized_data.values():
                    element = value_list[observation_number]
                    for key, value in element.items():
                        if key == transform_into_factor:
                            if factor == value:
                                element_list.append(value)

                name = str(factor)
                factor_dict[name] = element_list

        self.organized_for_ANOVA_readable = factor_dict

        factor_list = []
        list_of_data_sets = []
        for key, value in factor_dict.items():
            factor_list.append(key)
            list_of_data_sets.append(value)

        self.organized_for_ANOVA_use = [factor_list, list_of_data_sets]
