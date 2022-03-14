# datalist

Extracts element simply with conditions.

```python
person_list(name="John")
```
is equivalent to 
```python
[person.age for person in person_list if person.name == "John"][0]
```

## Example

If you have the following data:

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

persons = [Person("John", 35), 
           Person("Smith", 22)]
```
If you want person instance whose name is John:

with traditional ways:

```python
# comprehension
John = [person for person in persons if person.name == "John"][0]  
# can raise index error if list is empty
```
```python
# for statement
John = None
for person in persons:
    if person.name == "John":
        John = person
```

If datalist:
```python
persons = DataList([Person("John", 35), 
                    Person("Smith", 22)])

John = persons(name="John")  # Simple!
```
Or use get() for more explicitly.
```python
John = persons.get(name="John")
```

In Complicated conditions:

```python
@dataclass
class Person:
    name: str
    age: int
    country: str

persons = DataList([Person("Abigail", 17, "America"),
                    Person("Ai", 17, "Japan"),
                    Person("Aaron", 35, "British"),
                    Person("Smith", 22, "South Africa")])

Ai = persons.get(
    lambda person: person.name.startswith("A"),
    age=17,
    country="Japan")
```

All positional arguments must be callable which accepts element and return bool.



### get_all
get_all() returns list of all elements satisfying the conditions.

```python
persons = DataList([Person("Abigail", 35),
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

If datalist:

```python
names = persons.names
# persons.line_up("name") also works
```

DataList DOESN'T have "names" attribute, but all elements have "name" attribute.
To get all values of an attribute, access datalist with the attribute of elements + "s".

