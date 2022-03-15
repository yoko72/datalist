from typing import Callable, Optional


class DataList(list):
    """
    List that returns an element which satisfies all conditions.

    Examples
    --------
    @dataclass
    class Person:
        name: str
        age: int

    persons = DataList(Person("John", 26),
                       Person("Smith", 22))

    persons(name="John").age == 26  # True
    """
    def __init__(self, iterable):
        """
        Parameters
        ----------
        iterable:
            Data for extraction.
        """
        super().__init__(iterable)
        self._has_mapping_data: Optional[bool] = None
        # Indicates the access destination.
        # If True, (usually if dict)
        # NO: element.attr
        # YES!: element["attr"]
        # If None, the destination is not decided yet.

    def __call__(self, *checks: Callable, **conditions):
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

    def get(self, *args, **kwargs):
        """Alias of __call__"""
        return self(*args, **kwargs)

    get.__doc__ = get.__doc__ + "\n" + __call__.__doc__

    def get_all(self, *checks: Callable, **attrs) -> "DataList":
        """Returns ALL elements which satisfy all conditions by checks and attrs.

        Parameters
        ----------
        *checks: Callable
            if Callable(element):
                the element can be returned.
        **attrs:
            if element.key == val:
                the element can be returned."""

        return DataList([ele for ele in self._extract(*checks, **attrs)])

    def _extract(self, *checks, **attrs):
        for element in self:
            for attr, value in attrs.items():
                if self._access(element, attr) != value:
                    break
            else:
                for check in checks:
                    if not check(element):
                        break
                else:
                    yield element

    def _access(self, element, attr):
        if self._has_mapping_data is False:
            return getattr(element, attr)
        elif self._has_mapping_data:
            return element[attr]
        else:
            try:
                result = element[attr]
            except TypeError:
                try:
                    result = getattr(element, attr)
                except AttributeError:
                    raise AttributeError(f"Failed to find attribute or mapped key. {attr} for {element}.")
                else:
                    self._has_mapping_data = False
                    return result
            else:
                self._has_mapping_data = True
                return result

    def __getattr__(self, attrs: str) -> "DataList":
        if not attrs.endswith("s"):
            raise AttributeError
        attr = attrs[:-1]
        if not self:
            return DataList([])
        return self.line_up(attr)

    def line_up(self, name: str):
        is_accessible_list = map(lambda element: self._is_accessible_with(element, name), self)
        if all(is_accessible_list):
            return DataList([self._access(ele, name) for ele in self])
        else:
            AttributeError(f"Elements without attribution or key: {name} exist.")

    def _is_accessible_with(self, element, destination_name):
        try:
            self._access(element, destination_name)
        except (KeyError, AttributeError):
            return False
        return True

