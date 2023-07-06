import pytest
from src.strict import *
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Set, FrozenSet, Deque, Counter, ChainMap, OrderedDict, Deque, Counter, ChainMap

@dataclass
class StrictClass(metaclass=StrictTypeChecking):
    #generate some random data
    a: int = 1
    b: Optional[str] = None 
    c: List[int] = field(default_factory=lambda: [1,2,3])
    d: Dict[str, int] = field(default_factory=lambda: {'a': 1, 'b': 2, 'c': 3})
    e: Tuple[int, int, int] = field(default_factory=lambda: (1,2,3))
    f: Set[int] = field(default_factory=lambda: {1,2,3})
    g: FrozenSet[int] = field(default_factory=lambda: frozenset({1,2,3}))
    h: Deque[int] = field(default_factory=lambda: Deque([1,2,3]))
    i: Counter[int] = field(default_factory=lambda: Counter({1: 1, 2: 2, 3: 3}))
    j: ChainMap[int, int] = field(default_factory=lambda: ChainMap({1: 1, 2: 2, 3: 3}))
    k: OrderedDict[int, int] = field(default_factory=lambda: OrderedDict({1: 1, 2: 2, 3: 3}))
    @staticmethod
    def my_static_method(x: int, y: str) -> bool:
        return True

    @classmethod
    def my_class_method(cls, x: int, y: str) -> bool:
        return True

    def my_instance_method(self, x: int, y: str) -> bool:
        return True
def test_instance_method():
    obj = StrictClass()
    assert obj.my_instance_method(1, "hello") == True
    with pytest.raises(StrictTypeError):
        obj.my_instance_method("1", "hello")
    with pytest.raises(StrictTypeError):
        obj.my_instance_method(1, 2)
def test_static_method():
    assert StrictClass.my_static_method(1, "hello") == True
    with pytest.raises(StrictTypeError):
        StrictClass.my_static_method("1", "hello")
    with pytest.raises(StrictTypeError):
        StrictClass.my_static_method(1, 2)

def test_class_method():
    assert StrictClass.my_class_method(1, "hello") == True
    with pytest.raises(StrictTypeError):
        StrictClass.my_class_method("1", "hello")
    with pytest.raises(StrictTypeError):
        StrictClass.my_class_method(1, 2)