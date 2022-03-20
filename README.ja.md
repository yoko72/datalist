# picklist

つまむように簡単に要素を抽出できるリストです。

## Quick example
こういうコードを、
```python
[person for person in person_list if person.name == "John"][0]
```

スッキリさせます。
```python
person_list.pick(name="John")
```

## Install
```
python -m pip install git+https://github.com/yoko72/picklist
```

## Example

下記のようなデータがあるとして
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

nameが"John"の要素を抽出してみます。
```python
example = persons.pick(name="John")  # example is John
# .pickすら省略してもOK
```
簡単に欲しい要素が抽出できました。
pickメソッドは任意のキーワード引数(key=value)を受け取り、要素.key==valueの全ての条件を満たす要素を1つ返します。

これは以下のfor文や内包表記のものと(ほぼ)同価です。

```python
# for文
example = None
for person in persons:
    if person.name == "John":
        example = person
        break
```

```python
# 内包表記
try:
    example = [person for person in persons if person.name == "John"][0]
except IndexError:  # もしリストが空なら
    example = None
```

内包表記は目的の1件のデータを見つけても処理が終わらない点が異なります。

### 扱えるデータ

例にあげたdataclass以外も要素として扱えます。
辞書のようにelement["key"]でアクセスできるか、element.keyとして属性にアクセスできるものであればOKです。
辞書の例を見てみましょう。

```python
John_dict = {"name": "John", "age": 35}
Smith_dict = {"name": "Smith", "age": 22}

plist = PickList([John_dict, Smith_dict])
plist.pick(name="Smith")  # is Smith_dict  # 返り値もdict
```

### 全て抽出
get_allメソッドは、条件に合う**全ての**要素を抽出し結果をPickListで返します。

```python
persons = PickList([Person("Abigail", 35),
                    Person("John", 35),
                    Person("Smith", 22)])

persons_aged_35 = persons.get_all(age=35)  
# == PickList([person for person in persons if person.age==35])
```

### 値一覧

各要素の"name"の値の一覧は以下のように取得できます。
```python
names = persons.names
# ["Abigail", "John", "Smith"]
# persons.get_values("name")でも同じ
```
同価な例：

```python
names = [person.name for person in persons]
```
"name**s**"という属性は元々はどこにもなく、"name"属性をリスト内の各要素が有しているだけでした。
PickListは"s"で終わる不明な属性にアクセスされた際、各要素にその属性(s抜き)があるか調べます。
もしあれば、その値一覧をPickListで返します。なければAttributeErrorがraiseされます。

"s"は複数形に由来していますが、英語の文法などは無視され、単純に"s"で終わるかどうかだけを見ています。
不可算名詞や不規則変化などは考慮しないので、picklist.informationsや、plist.womansなどもありえます。

この使い方を避けたい場合、get_valuesメソッドでも同じことができます。
```python
#これらは同価
PickList.get_values("example")
PickList.examples
```

### 複雑な条件
位置引数に条件式を渡せば複雑な条件で抽出することもできます。
条件式は要素を１つ受け取るcallableです。
bool(Callable(各要素)) is Trueになる場合のみ抽出されます。

```python
example = persons.pick(
    lambda person: 
        person.name.startswith("A")
        and person.weight > 45.0,
    age=27, height=160)
```

### listのサブクラス
PickListは標準のlistを継承しています。各メソッドや演算子など、同様に使えます。
