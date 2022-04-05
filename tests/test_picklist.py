import unittest
from src import PickList
from dataclasses import dataclass, asdict
from myutils.myutils import measure_time


class TestCase(unittest.TestCase):
    def setUp(self):
        @dataclass
        class Person:
            name: str
            age: int
            country: str

        self.sample_class = Person
        self.sample_data = PickList([
            Person("Abigail", 17, "America"),
            Person("Ai", 17, "Japan"),
            Person("Aaron", 35, "British"),
            Person("Smith", 22, "South Africa")])
        self.sample_dict = PickList([asdict(person) for person in self.sample_data])

    def test_pick(self):
        self.assertEqual("Ai", self.sample_data.pick(name="Ai", country="Japan").name)
        self.assertEqual("Ai", self.sample_dict.pick(name="Ai", country="Japan")["name"])

    def test_get_all(self):
        self.assertEqual(self.sample_data[0:2], self.sample_data.get_all(age=17))
        self.assertEqual(self.sample_dict[0:2], self.sample_dict.get_all(age=17))

    def test_compare_performance(self):
        test_num = 1
        test_key = "key"
        test_dicts = [{test_key: num} for num in range(10)]

        def comprehension_try():
            try:
                result = [test_dict for test_dict in test_dicts if test_dict[test_key] == test_num][0]
            except IndexError:
                result = None
            return result

        def comprehension_if():
            result_list = [test_dict for test_dict in test_dicts if test_dict[test_key] == test_num]
            if result_list:
                result = result_list[0]
            else:
                result = None
            return result

        def for_loop():
            result = None
            for dict_ in test_dicts:
                if dict_[test_key] == test_num:
                    return dict_
            return result

        plist = PickList(test_dicts)

        def pick():
            return plist.pick(key=test_num)

        result = for_loop()
        for func in [comprehension_try, comprehension_if, pick, for_loop]:
            func = measure_time(func)
            new_result = func()
            assert result == new_result

    def test_pick_not_found(self):
        self.assertEqual(self.sample_data.pick(name="Bob"), None)
        self.assertEqual(self.sample_dict.pick(name="Bob"), None)

    def test_get_all_not_found(self):
        self.assertEqual([], self.sample_data.get_all(age=100))
        self.assertEqual([], self.sample_dict.get_all(age=100))

    def test_get_with_invalid_attr(self):
        with self.assertRaises(AttributeError):
            self.sample_data.pick(sex="male")
        with self.assertRaises(KeyError):
            self.sample_dict.pick(sex="male")

    def test_make_list_of(self):
        expected = [17, 17, 35, 22]
        self.assertEqual(expected, self.sample_data.get_values("age"))
        self.assertEqual(expected, self.sample_data.ages)
        self.assertEqual(expected, self.sample_dict.get_values("age"))
        self.assertEqual(expected, self.sample_dict.ages)


if __name__ == "__main__":
    unittest.main()
