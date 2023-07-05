import pytest
from strict import strict, StrictTypeError

class StrictClass:
    
    @strict()
    def self_multiply_first(self, a: int, b: int) -> int:
        return a * b
    @classmethod
    @strict()
    def class_multiply_first(cls, a: int, b: int) -> int:
        return a * b
    @staticmethod
    @strict()
    def static_multiply_first(a: int, b: int) -> int:
        return a * b

    @strict(skip_arguments=["b"])
    def self_multiply_second(self, a: int, b: int) -> float:
        return a * b
    
    @classmethod
    @strict(skip_arguments=["b"])
    def class_multiply_second(cls, a: int, b: int) -> float:
        return a * b
    
    @staticmethod
    @strict(skip_arguments=["b"])
    def static_multiply_second(a: int, b: int) -> float:
        return a * b

    @strict(skip_return=True)
    def self_multiply_third(self, a: int, b: int) -> int:
        return a * b
    
    @classmethod
    @strict(skip_return=True)
    def class_multiply_third(cls, a: int, b: int) -> int:
        return a * b
    
    @staticmethod
    @strict(skip_return=True)
    def static_multiply_third(a: int, b: int) -> int:
        return a * b
    @strict()
    def self_multiply_fourth(self, a: int, b: int) -> int:
        return f'{a * b}';
    @classmethod
    @strict()
    def class_multiply_fourth(cls, a: int, b: int) -> int:
        return f'{a * b}';

    @staticmethod
    @strict()
    def static_multiply_fourth(a: int, b: int) -> int:
        return f'{a * b}';

class TestStrictClassMethods:

    def test_self_normal_result(self):
        assert StrictClass().self_multiply_first(2, 3) == 6

    def test_class_normal_result(self):
        assert StrictClass.class_multiply_first(2, 3) == 6

    def test_static_normal_result(self):
        assert StrictClass.static_multiply_first(2, 3) == 6
    
    def test_self_fail_result(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass().self_multiply_first(2, 3.0) == 6
    
    def test_class_fail_result(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass.class_multiply_first(2, 3.0) == 6

    def test_static_fail_result(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass.static_multiply_first(2, 3.0) == 6

    def test_self_skipped_normal(self):
        assert StrictClass().self_multiply_second(2, 3.0) == 6.0

    def test_class_skipped_normal(self):
        assert StrictClass.class_multiply_second(2, 3.0) == 6.0

    def test_static_skipped_normal(self):
        assert StrictClass.static_multiply_second(2, 3.0) == 6.0
    def test_self_skipped_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass().self_multiply_second(2.0, 3) == 6.0
    def test_class_skipped_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass.class_multiply_second(2.0, 3) == 6.0
    def test_static_skipped_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass.static_multiply_second(2.0, 3) == 6.0
    def test_self_skip_return(self):
        assert StrictClass().self_multiply_third(4, 2) == 8.0

    def test_class_skip_return(self):
        assert StrictClass.class_multiply_third(4, 2) == 8.0

    def test_static_skip_return(self):
        assert StrictClass.static_multiply_third(4, 2) == 8.0
    def test_self_return_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass().self_multiply_fourth(4, 2) == '8'

    def test_class_return_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass.class_multiply_fourth(4, 2) == '8'

    def test_static_return_fail(self):
        with pytest.raises(StrictTypeError):
            assert StrictClass.static_multiply_fourth(4, 2) == '8'
    