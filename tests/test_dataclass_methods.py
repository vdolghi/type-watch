import pytest
from src.strict import *
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Tuple, Set, FrozenSet, Deque, Counter, ChainMap, OrderedDict, Deque, Counter, ChainMap, Self, Type

@dataclass
class StrictClassData:
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
    _property_a: int = 0
    _property_b: int = 0

    @strict()
    def self_multiply_first(self: Self, a: int, b: int) -> int:
        return a * b
    @classmethod
    @strict()
    def class_multiply_first(cls: Type['StrictClassData'], a: int, b: int) -> int:
        return a * b
    @staticmethod
    @strict()
    def static_multiply_first(a: int, b: int) -> int:
        return a * b

    @strict(skip_arguments=["b"])
    def self_multiply_second(self: Self, a: int, b: int) -> float:
        return a * b
    
    @classmethod
    @strict(skip_arguments=["b"])
    def class_multiply_second(cls: Type['StrictClassData'], a: int, b: int) -> float:
        return a * b
    
    @staticmethod
    @strict(skip_arguments=["b"])
    def static_multiply_second(a: int, b: int) -> float:
        return a * b

    @strict(skip_return=True)
    def self_multiply_third(self: Self, a: int, b: int) -> int:
        return a * b
    
    @classmethod
    @strict(skip_return=True)
    def class_multiply_third(cls: Type['StrictClassData'], a: int, b: int) -> int:
        return a * b
    
    @staticmethod
    @strict(skip_return=True)
    def static_multiply_third(a: int, b: int) -> int:
        return a * b
    @strict()
    def self_multiply_fourth(self: Self, a: int, b: int) -> int:
        return f'{a * b}';
    @classmethod
    @strict()
    def class_multiply_fourth(cls: Type['StrictClassData'], a: int, b: int) -> int:
        return f'{a * b}';

    @staticmethod
    @strict()
    def static_multiply_fourth(a: int, b: int) -> int:
        return f'{a * b}';

    @property
    @strict()
    def property_a(self: Self) -> int:
        return self._property_a
    
    @property_a.setter
    @strict()
    def property_a(self: Self, value: int):
        self._property_a = value
        return None

    @property
    @strict()
    def property_b(self: Self) -> Optional[str]:
            return self._property_b
        
    @property_b.setter
    @strict()
    def property_b(self: Self, value: str):
        self._property_b = value
        return None

class TestStrictDataclassMethods:

    def test_self_normal_result(self):
        assert StrictClassData().self_multiply_first(2, 3) == 6

    def test_class_normal_result(self):
        assert StrictClassData.class_multiply_first(2, 3) == 6

    def test_static_normal_result(self):
        assert StrictClassData.static_multiply_first(2, 3) == 6
    
    def test_self_fail_result(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData().self_multiply_first(2, 3.0) == 6
    
    def test_class_fail_result(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData.class_multiply_first(2, 3.0) == 6

    def test_static_fail_result(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData.static_multiply_first(2, 3.0) == 6

    def test_self_skipped_normal(self):
        assert StrictClassData().self_multiply_second(2, 3.0) == 6.0

    def test_class_skipped_normal(self):
        assert StrictClassData.class_multiply_second(2, 3.0) == 6.0

    def test_static_skipped_normal(self):
        assert StrictClassData.static_multiply_second(2, 3.0) == 6.0
    def test_self_skipped_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData().self_multiply_second(2.0, 3) == 6.0
    def test_class_skipped_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData.class_multiply_second(2.0, 3) == 6.0
    def test_static_skipped_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData.static_multiply_second(2.0, 3) == 6.0
    def test_self_skip_return(self):
        assert StrictClassData().self_multiply_third(4, 2) == 8.0

    def test_class_skip_return(self):
        assert StrictClassData.class_multiply_third(4, 2) == 8.0

    def test_static_skip_return(self):
        assert StrictClassData.static_multiply_third(4, 2) == 8.0
    def test_self_return_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData().self_multiply_fourth(4, 2) == '8'

    def test_class_return_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData.class_multiply_fourth(4, 2) == '8'

    def test_static_return_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData.static_multiply_fourth(4, 2) == '8'

    def test_self_property_good(self):
        assert StrictClassData().property_a == 0

    def test_self_property_bad(self):
        with pytest.raises(StrictTypeError):
            assert StrictClassData().property_b == 'hello'

    def test_self_property_good_setter(self):
        sc: StrictClassData = StrictClassData()
        sc.property_a = 1
        assert sc.property_a == 1

    def test_self_property_bad_setter(self):
        sc: StrictClassData = StrictClassData()
        with pytest.raises(StrictTypeError):
            sc.property_b = 'hello'
            assert sc.property_b == 'hello'