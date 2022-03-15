import unittest
import datalist
from dataclasses import dataclass, asdict


class TestCase(unittest.TestCase):
    def setUp(self) -> None:
        @dataclass
        class Person:
            name: str
            age: int
            country: str

        self.sample_class = Person
        self.sample_data = datalist.DataList([Person("Abigail", 17, "America"),
                            Person("Ai", 17, "Japan"),
                            Person("Aaron", 35, "British"),
                            Person("Smith", 22, "South Africa")])
        self.sample_dict = datalist.DataList([asdict(person) for person in self.sample_data])

    def test_get(self):
        self.assertEqual("Ai", self.sample_data.get(name="Ai", country="Japan").name)
        self.assertEqual("Ai", self.sample_dict.get(name="Ai", country="Japan")["name"])

    def test_get_all(self):
        self.assertEqual(self.sample_data[0:2], self.sample_data.get_all(age=17))
        self.assertEqual(self.sample_dict[0:2], self.sample_dict.get_all(age=17))

    def test_get_not_found(self):
        self.assertEqual(self.sample_data.get(name="Bob"), None)
        self.assertEqual(self.sample_dict.get(name="Bob"), None)

    def test_get_all_not_found(self):
        self.assertEqual([], self.sample_data.get_all(age=100))
        self.assertEqual([], self.sample_dict.get_all(age=100))

    def test_get_with_invalid_attr(self):
        with self.assertRaises(AttributeError):
            self.sample_data.get(sex="male")
        with self.assertRaises(KeyError):
            self.sample_dict.get(sex="male")

    def test_lineup(self):
        expected = [17, 17, 35, 22]
        self.assertEqual(expected, self.sample_data.line_up("age"))
        self.assertEqual(expected, self.sample_data.ages)
        self.assertEqual(expected, self.sample_dict.line_up("age"))
        self.assertEqual(expected, self.sample_dict.ages)


if __name__ == "__main__":
    unittest.main()