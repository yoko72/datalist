from typing import Callable


class DataList(list):
    """
    List that returns an element which satisfies all conditions on call.

    Examples
    --------
    @dataclass
    class Person:
        name: str
        age: int

    persons = DataList([Person("John", 26),
                        Person("Smith", 22)])

    persons(name="John").age == 26  # True
    """

    def __init__(self, iterable, *, default=None):
        """
        Parameters
        ----------
        iterable:
            Iterable like list.
        default:
            Default value. The is returned if none of elements match your conditions.
        """
        super().__init__(iterable)
        self.default = default

    def __call__(self, *checks: Callable, **attrs):
        """Returns an element which satisfies all conditions by checks and attrs.

        Parameters
        ----------
        *checks: Callable
            if Callable(element):
                the element can be returned.
        **attrs:
            if element.key == val:
                the element can be returned.

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
            return self._extract(*checks, **attrs).__next__()
        except StopIteration:
            return self.default

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
                if getattr(element, attr) != value:
                    break
            else:
                for check in checks:
                    if not check(element):
                        break
                else:
                    yield element

    def set_default(self, val):
        """
        Parameters
        ----------
        val:
            Default value. The is returned if none of elements match your conditions.
        """
        self.default = val

    def __getattr__(self, attrs: str) -> "DataList":
        if not attrs.endswith("s"):
            raise AttributeError
        attr = attrs[:-1]
        if not self:
            return DataList([])
        return self.line_up(attr)

    def line_up(self, attr: str):
        has_attr = map(lambda element: hasattr(element, attr), self)
        if all(has_attr):
            return DataList([getattr(ele, attr) for ele in self])
        else:
            AttributeError(f"Elements without attribution: {attr} exist.")


