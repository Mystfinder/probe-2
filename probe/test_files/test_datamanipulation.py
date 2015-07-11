from probe import datamanipulation
import unittest


class DatamanipulationErrorsTest(unittest.TestCase):
    def test_print(self):
        manipulation_error = datamanipulation.DatamanipulationError()
        page_error = datamanipulation.PageNotFoundError()
        list_error = datamanipulation.NotAListError()
        dict_error = datamanipulation.NotADictError()

        print(manipulation_error)
        print(page_error)
        print(list_error)
        print(dict_error)


class WriteXLSTest(unittest.TestCase):
    def test_performance(self):
        data_1 = [1, 2, 3, 4, 5, 6]
        data_2 = [-1, -2, -3]

        datamanipulation.write_xls(data_1, "aaaa.xls")
        datamanipulation.write_xls(data_1, "aaaa.xls", 2)
        datamanipulation.write_xls([data_1, data_2], "aaaa.xls")
        datamanipulation.write_xls([data_1, data_2], "aaaa.xls", 2)


class OpenXLSTest(unittest.TestCase):
    def test_performance(self):
        data_1 = [1, 2, 3, 4, 5, 6]
        data_2 = [-1, -2, -3]
        datamanipulation.write_xls([data_1, data_2], "aaaa2.xls")

        result_1 = datamanipulation.open_xls("aaaa2.xls", 0, 3)
        result_2 = datamanipulation.open_xls("aaaa2.xls", [0, 1], 4)
        result_3 = datamanipulation.open_xls("aaaa2.xls", [0, 1], [4, 2])
        result_4 = datamanipulation.open_xls("aaaa2.xls", [0], [4])

        self.assertTrue([[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]], result_1)
        self.assertTrue([[1.0, 2.0, 3.0, 4.0], [-1.0, -2.0, -3.0, ""]],
                        result_2)
        self.assertTrue([[1.0, 2.0, 3.0, 4.0], [-1.0, -2.0]], result_3)
        self.assertTrue([1.0, 2.0, 3.0, 4.0], result_4)


class PartitionIntoListsTest(unittest.TestCase):
    def test_results(self):
        a_list = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
        bad_list = "as"

        result = datamanipulation.partition_into_lists(a_list, 4)

        self.assertTrue([1.0, 2.0, 3.0], result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.partition_into_lists(bad_list, 4)


class RecombinateListTest(unittest.TestCase):
    def test_results(self):
        big_list = [[1, 1, 1], [2, 2, 2], [3, 3, 3], [4, 4, 4]]
        bad_list = "as"
        nasty_list = ["as"]

        result = datamanipulation.recombinate_list(big_list)

        self.assertTrue([1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4], result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.recombinate_list(bad_list)
        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.recombinate_list(nasty_list)


class FilterIntervalTest(unittest.TestCase):
    def test_results(self):
        a_list = [1, 2, 3, 4, 1, 2, 3, 4, 1, 2, 3, 4]
        bad_list = "as"

        result = datamanipulation.filter_interval(a_list, 0, 4)

        self.assertTrue([1, 1, 1], result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.filter_interval(bad_list, 0, 4)


class FindIndexTest(unittest.TestCase):
    def test_results(self):
        a_list = ["3", "1", "4", "6", "!", "8", "3", "7"]
        bad_list = "as"

        result = datamanipulation.find_index(a_list, "!", True)

        self.assertTrue(4, result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.find_index(bad_list, "!", True)


class ExtractIntervalTest(unittest.TestCase):
    def test_results(self):
        a_list = [[1, 2, 3, 4], [5, 6, 7, 8]]
        bad_list = "as"

        result_1 = datamanipulation.extract_interval(a_list, [1, 3])
        result_2 = datamanipulation.extract_interval(a_list, [1, 3], True)

        self.assertTrue([2, 3, 4], result_1)
        self.assertTrue([[2, 3, 4], [6, 7, 8]], result_2)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.extract_interval(bad_list, [1, 2], True)


class GetDataTest(unittest.TestCase):
    def test_performance(self):
        try:
            url = "http://fmi.py-bg.net/tasks/1/solutions"
            parameters_1 = [url, "td", {"class": "results"}, True, " "]

            url = "http://www.cuetracker.net/Statistics/Matches-and-Frames/Won/All-time"
            parameters_2 = [url, ["tbody", "td"], False, True, False,
                            False, [1, 6]]
            parameters_3 = [url, ["tbody", "td"], False, ",", False,
                            False, [3, 6]]

            url = "https://en.wikipedia.org/wiki/List_of_cities_in_Germany_by_population"
            parameters_4 = [url, "td",
                            {"style": "background-color:#E0E0E0;"},
                            True, '♠', False, [1, 2]]
            parameters_5 = [url, "td",
                            {"style": "background-color:#E0E0E0;"},
                            True, '♠', ["70063", "70051"]]
            parameters_6 = [url, "td",
                            {"style": "background-color:#E0E0E0;"},
                            True, '♠', [None, "70051"]]
            parameters_7 = [url, "td",
                            {"style": "background-color:#E0E0E0;"},
                            True, '♠', ["70063", None]]
            parameters_8 = [url, "td", {"style": "background-color: #E0E0E0;"},
                            ",", ['♠', 1]]

            url = "http://fmi.py-bg.net/leaderboard"
            parameters_9 = [url, "td", {"class": "points"}, False]
            parameters_10 = [url, ["td", "sd"], [{"class": "points"},
                             {"class": "points"}], False]

            url = "http://fmi.py-bg.net/leader*^&$ard"
            parameters_11 = [url, "td", {"class": "points"}, False]

            datamanipulation.get_data(*parameters_1)
            datamanipulation.get_data(*parameters_2)
            datamanipulation.get_data(*parameters_3)
            datamanipulation.get_data(*parameters_4)
            datamanipulation.get_data(*parameters_5)
            datamanipulation.get_data(*parameters_6)
            datamanipulation.get_data(*parameters_7)
            datamanipulation.get_data(*parameters_8)
            datamanipulation.get_data(*parameters_9)
            datamanipulation.get_data(*parameters_10)

            with self.assertRaises(datamanipulation.PageNotFoundError):
                datamanipulation.get_data(*parameters_11)

        except datamanipulation.PageNotFoundError:
            pass


class ExtractDataTest(unittest.TestCase):
    def test_performance(self):
        url = "http://fmi.py-bg.net/tasks/1/solutions"
        parameters_1 = [url, "td", {"class": "results"}, True, " "]

        url = "http://www.cuetracker.net/Statistics/Matches-and-Frames/Won/All-time"
        parameters_2 = [url, ["tbody", "td"], False,
                        True, False, False, [1, 6]]

        parameters = [parameters_1, parameters_2]

        datamanipulation.extract_data(parameters)

        bad_list = "as"
        nasty_list = ["as"]
        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.extract_data(bad_list)
        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.extract_data(nasty_list)


class AtomizeToDictsTest(unittest.TestCase):
    def test_results(self):
        a_list = [1, 2, 3]
        bad_list = "as"

        result = datamanipulation.atomize_to_dicts(a_list, "name")

        self.assertTrue([{"name": 1}, {"name": 2}, {"name": 3}], result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.atomize_to_dicts(bad_list, "name")


class ExpandedDictListTest(unittest.TestCase):
    def test_results(self):
        dict_list_1 = [{"az": 2}, {"ti": 2}]
        dict_list_2 = [{"sa": 3}, {"fg": 6}]
        bad_list = "as"

        result = datamanipulation.expanded_dict_list(dict_list_1, dict_list_2)

        self.assertTrue([{'sa': 3, 'az': 2}, {'fg': 6, 'ti': 2}], result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.expanded_dict_list(bad_list, dict_list_1)
        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.expanded_dict_list(dict_list_1, bad_list)


class AssociateTest(unittest.TestCase):
    def test_results(self):
        list_1 = [1, 2, 3]
        list_2 = [11, 22, 33]
        list_3 = ["1", "2", "3"]
        bad_list = "as"

        result = datamanipulation.associate([list_1, list_2, list_3], 2)

        self.assertTrue({'3': [3, 33], '2': [2, 22], '1': [1, 11]}, result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.associate(bad_list, 2)
        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.associate([bad_list, list_2, list_3], 2)


class OrganizeTest(unittest.TestCase):
    def test_results(self):
        list_1 = [1, 2, 3]
        list_2 = [11, 22, 33]
        list_3 = ["1", "2", "3"]
        bad_list = "as"

        names = ["numbers", "animals"]

        result = datamanipulation.organize([list_1, list_2, list_3], names, 2)

        aim = {'2': [{'numbers': 2, 'animals': 22}],
               '1': [{'numbers': 1, 'animals': 11}],
               '3': [{'numbers': 3, 'animals': 33}]}

        self.assertTrue(aim, result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.organize([bad_list, list_2, list_3], names, 2)
        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.organize(bad_list, bad_list, 2)
        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.organize([list_1, list_2, list_3], bad_list, 2)


class SeparateTest(unittest.TestCase):
    def test_results(self):
        a_list = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        bad_list = "as"

        result = datamanipulation.separate(a_list, 3)

        self.assertTrue([[1, 4, 7], [2, 5, 8], [3, 6, 9]], result)

        with self.assertRaises(datamanipulation.NotAListError):
            datamanipulation.separate(bad_list, 2)


class DataTest(unittest.TestCase):
    def test_results(self):
        data_1 = ["person1", "person2", "person3"]
        data_2 = [5, 6, 2]
        data_3 = [10, 12, 11]
        all_data = [data_1, data_2, data_3]
        names = ["time", "length"]

        some_data = datamanipulation.Data()
        some_data.unorganized_data = all_data

        some_data.organize(names, 0, True)
        aim_1 = {'person3': [{'length': 11, 'time': 2}],
                 'person2': [{'length': 12, 'time': 6}],
                 'person1': [{'length': 10, 'time': 5}]}

        some_data.organize_for_linear_regression("time")

        self.assertTrue(aim_1, some_data.organized_data)
        self.assertTrue([[5, 2, 6]],
                        some_data.organized_for_linear_regression[0].matrix)
        self.assertTrue([[10, 11, 12]],
                        some_data.organized_for_linear_regression[1].matrix)

        some_data.organize_for_ANOVA([[10, 12]], "length")
        some_data.organize_for_ANOVA([11, 12, 10], "length")

        self.assertTrue({"12": [12], "10": [10], "11": [11]},
                        some_data.organized_for_ANOVA_readable)
        self.assertTrue([["12", "10", "11"], [[12], [10], [11]]],
                        some_data.organized_for_ANOVA_use)

        url = "http://fmi.py-bg.net/tasks/1/solutions"
        parameters_1 = [url, "td", {"class": "results"}, True, " "]
        url = "http://www.cuetracker.net/Statistics/Matches-and-Frames/Won/All-time"
        parameters_2 = [url, ["tbody", "td"], False, True,
                        False, False, [1, 6]]
        parameters = [parameters_1, parameters_2]

        some_data.get_data(parameters_1, True)
        some_data.extract_data(parameters, True)

        with self.assertRaises(datamanipulation.NotAListError):
            some_data.organize_for_ANOVA("as", 2)


if __name__ == '__main__':
    unittest.main()
