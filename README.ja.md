# datalist

条件にあうデータを簡単に抽出できるリストです。

こういったコードが、
```python
[person.age for person in person_list if person.name == "John"][0]
```

スッキリします。
```python
person_list.get(name="John")
# .getすら省略してもOK.
```

## Example

以下のようなデータがあるとして

```python
from dataclasses import dataclass

@dataclass
class Person:
    name: str
    age: int

John = Person("John", 35)
Smith = Person("Smith", 22)
```

nameが"John"のデータが欲しい場合は以下のように。
```python
from datalist import DataList

persons = DataList([John, Smith])
```

```python
# datalist
John = persons.get(name="John")
```
簡単に欲しいデータが抽出できます。
以下の内包表記やfor文のものと同価です。

```python
# 内包表記
try:
    John = [person for person in persons if person.name == "John"][0]
except IndexError:  # もしリストが空なら
    John = None
```

```python
# for文
John = None
for person in persons:
    if person.name == "John":
        John = person
        break
```

データクラス以外も扱えます。
辞書のようにobj["key"]でアクセスするもの、もしくは通常のclassのように属性(obj.attr)としてアクセスできるものであればOKです。

```python
# 辞書
John_dict = {"name":"John", "age": 35}
Smith_dict = {"name":"Smith", "age":22}

dlist = DataList([John_dict, Smith_dict])
dlist.get(name="Smith")  # Smith_dict
```

位置引数に条件式を渡せば複雑な条件で抽出することもできます。
条件式は１つの要素を受け取るcallableで、boolを返さなければいけません。

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

### get_all
get_allメソッドは、条件に合う全てのデータを抽出しリストを返します。

```python
persons = DataList([Person("Abigail", 35),
                    Person("John", 35),
                    Person("Smith", 22)])

persons_aged_35 = persons.get_all(age=35)  
# == [person for person in persons if person.age=35]
```

### Values of an attribute

各データの"name"の値のリストは以下のように取得できます。
```python
names = persons.names
# ["Abigail", "John", "Smith"]
# persons.make_list_of("name") also ok
```
これは以下と同価です。

```python
names = [person.name for person in persons]
```
"name**s**"という属性は元はどこにもありません。"name"属性を各データが有していただけでした。
DataListは"s"で終わる不明な属性でアクセスされた際、各データにその名前(s抜き)の属性がないか調べます。
もしあれば、その属性の値をDataListで返します。 なければAttributeErrorがraiseされます。

この使い方を避けたい場合、make_list_ofメソッドでも同じことができます。

### 普通のList
DataListは標準のlistを継承しています。appendやpopなども全て使用可能です。
