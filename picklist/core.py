from typing import Callable


_unique_default_value = object()

class PickList(list):
    """
    Friendly list to pick data with conditions.

    Examples
    --------
    @dataclass
    class Person:
        name: str
        age: int

    persons = PickList(Person("John", 26),
                       Person("Smith", 22))

    persons.pick(name="John").age == 26  # True
    persons.pop(age=22)  # Smith
    """

    def pick(self, *checks: Callable, **conditions):
        """Returns an element which satisfies all conditions by checks and attrs.

        Parameters
        ----------
        *checks: Callable
            if Callable(element):
                extracts the element.
        **conditions: {key : val}
            if element.key == val:
                extracts the element.

        Examples
        --------
        @dataclass
        class Person:
            name: str
            age: int

        persons = DataList([Person("John", 26),
                            Person("Smith", 22)])

        John = persons(lambda person: person.age > 20, \
                       name = "John")
        """
        try:
            return self._extract(*checks, **conditions).__next__()
        except StopIteration:
            return None

    def remove(self, __value=_unique_default_value, **kwargs):
        if __value is _unique_default_value:
            __value = self.pick(**kwargs)
        super().remove(__value)

    def pop(self, __value=_unique_default_value, **kwargs):
        if __value is _unique_default_value:
            __value = self.pick(**kwargs)
        super().pop(__value)

    def get_all(self, *checks: Callable, **attrs) -> "PickList":
        """Returns ALL elements which satisfy all conditions by checks and attrs.

        Parameters
        ----------
        *checks: Callable
            if Callable(element):
                the element can be returned.
        **attrs:
            if element.key == val:
                the element can be returned."""

        return PickList([ele for ele in self._extract(*checks, **attrs)])

    def _extract(self, *checks, **attrs):
        access = self._access
        items = attrs.items()

        for element in self:
            for attr, value in items:
                if access(element, attr) != value:
                    break
            else:
                for check in checks:
                    if not check(element):
                        break
                else:
                    yield element

    def _access(self, element, attr):
        try:
            result = element[attr]
        except TypeError:
            try:
                result = getattr(element, attr)
            except AttributeError:
                raise AttributeError(f"Failed to find attribute or mapped key. {attr} for {element}.")
            else:
                self._access = lambda element, attr: getattr(element, attr)
                return result
        else:
            self._access = lambda element, attr: element[attr]
            return result

    def __getattr__(self, attrs: str) -> "PickList":
        """
        persons.ages = [22, 26]
        Alias of [person.age for person in persons]

        """
        if not attrs.endswith("s"):
            raise AttributeError
        attr = attrs[:-1]
        if not self:
            return PickList([])
        return self.get_values(attr)

    def get_values(self, name: str):
        """
        persons_pick_list.get_values(age)
        is almost alias of
        [person.age for person in persons_pick_list]

        This can be replaced by
        persons_pick_list.ages.
        """
        is_accessible_list = map(lambda element: self._is_accessible_with(element, name), self)
        if all(is_accessible_list):
            return PickList([self._access(ele, name) for ele in self])
        else:
            AttributeError(f"Elements without attribution: {name} exist.")

    def _is_accessible_with(self, element, destination_name):
        try:
            self._access(element, destination_name)
        except (KeyError, AttributeError):
            return False
        return True
