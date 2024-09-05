from dataclasses import dataclass

from wth.utils.dataclass import deserialize


@dataclass
class B:
    name: str


@dataclass
class A:
    name: str = ""
    b: list[B] = None


t1 = deserialize([{"name": "wttch", "b": [{"name": "wb"}]}], list[A])
print(t1)
t1 = deserialize({"name": "wttch"}, A)
print(t1)
