import pytest
from strict import StrictTypeChecking, StrictTypeError
import inspect

class StrictClass(metaclass=StrictTypeChecking):
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
