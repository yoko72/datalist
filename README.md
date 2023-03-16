[日本語はこちら](https://github.com/yoko72/picklist/README.ja.md)
# picklist

Picklist is a user-friendly list to pick element with conditions.

## Quick example
```python
# normal way
[person for person in person_list if person.name == "John"][0]

# equivalent with picklist
person_list.pick(name="John")  # easy!
```

## Install
```
$ python -m pip install git+https://github.com/yoko72/picklist
```

## Example

With following data:

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

Let's pick an element whose value of "name" attribute is "John".

```python
persons.pick(name="John")  # == John
# Even .pick is omitted, it works same.
```
The pick method accepts any keyword arguments(key=value), and returns the element which satisfies all element.key == value conditions.

It's almost equivalent to following ways.

```python
# for loop
John = None
for person in persons:
    if person.name == "John":
        John = person
        break
```

```python
# comprehension
try:
    John = [person for person in persons if person.name == "John"][0]
except IndexError:  # if list is empty:
    John = None
```

Comprehension way differs a little from pick method and for loop. 
It doesn't stop the process even after it finds the object.

## Dict as element

Not only objects holding value as attr, but also dictlike object is available.
Let's see the example of dict.

```python
John_dict = {"name": "John", "age": 35}
Smith_dict = {"name": "Smith", "age": 22}

plist = PickList([John_dict, Smith_dict])
plist.pick(name="Smith")  # is Smith_dict
```



### get_all
get_all() returns list of **all** elements satisfying the conditions as picklist.

```python
persons = PickList([Person("Abigail", 35),
                    Person("John", 35),
                    Person("Smith", 22)])

persons_aged_35 = persons.get_all(age=35)  
# == PickList([person for person in persons if person.age==35])
```

### Values of an attribute
If you want names of all persons,
```python
names = persons.names
# ["Abigail", "John", "Smith"]
# persons.get_values("name") also works same.
```

It's equivalent with:
```python
names = [person.name for person in persons]
```

Nothing has "names" attribute, but all elements have "name" attribute.
If picklist is accessed with undefined attribute with "s" suffix, each element is checked if they have the attribute without "s" suffix.
If they have, picklist returns the values of each element as PickList.
If not, AttributeError is raised.

This usage comes from the usage of multiple form in English, but it purely checks if it ends with "s" or not.
Therefore, incorrect english words are possible like picklist.informations, plist.womans and so on.

You can use get_values method if you don't like such usage, it works same.

Followings are equivalent.
```python
plist.get_values("example")
plist.examples
```

### Complicated conditions:
You can extract with complicated conditions by giving callable as positional argument.
The callable must accept one argument, and the element is extracted only when bool(Callable(element)) is True.

```python
example = persons.pick(
    lambda person: 
        person.name.startswith("A")
        and person.weight > 45.0,
    age=27, height=160)
```

## Subclass of list
Picklist inherits from standard class. Each method or operator for the list is available.
