# picklist

Extracts element easily.

```python
# normal way
[person for person in person_list if person.name == "John"][0]

# equivalent with picklist
person_list(name="John")
```

## Example

If you have the following data:

```python
from dataclasses import dataclass
from picklist import PickList

@dataclass
class Person:
    name: str
    age: int

John = Person("John", 35)
Smith = Person("Smith", 22)

persons = PickList([John, Smith])
```

Let's pick an element with "John" value in "name" attribute.

```python
persons(name="John")  # == John
# persons.get(name="John") also works same
```
This is equivalent to following ways.
```python
# comprehension
try:
    John = [person for person in persons if person.name == "John"][0]
except IndexError:  # if list is empty:
    John = None
```

```python
# for loop
John = None
for person in persons:
    if person.name == "John":
        John = person
        break
```
Not only objects holding value with attr, but also dict is available.
Let's see the example of dict.





### get_all
get_all() returns list of all elements satisfying the conditions.

```python
persons = PickList([Person("Abigail", 35),
                    Person("John", 35),
                    Person("Smith", 22)])

persons_aged_35 = persons.get_all(age=35)  # [John, Abigail] has 2 Person instances
```

### Values of an attribute
If you want names of all persons:

if traditional way:

```python
names = [person.name for person in persons]
```

If picklist:

```python
names = persons.names
# persons.make_list_of("name") also works
```

PickList DOESN'T have "names" attribute, but all elements have "name" attribute.
To get all values of an attribute, access picklist with the attribute of elements + "s".



In Complicated conditions:

```python
@dataclass
class Person:
    name: str
    age: int
    country: str


persons = PickList([Person("Abigail", 17, "America"),
                    Person("Ai", 17, "Japan"),
                    Person("Aaron", 35, "British"),
                    Person("Smith", 22, "South Africa")])

Ai = persons.pick(
    lambda person: person.name.startswith("A"),
    age=17,
    country="Japan")
```

All positional arguments must be callable which accepts element and return bool.


