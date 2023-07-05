import pytest
from strict import strict, StrictTypeError

@strict()
def multiply_first(a: int, b: int) -> int:
    return a * b

@strict(skip_arguments=["b"])
def multiply_second(a: int, b: int) -> float:
    return a * b

@strict(skip_return=True)
def multiply_third(a: int, b: int) -> int:
    return a * b
@strict()
def multiply_fourth(a: int, b: int) -> int:
    return f'{a * b}';

def test_normal_result():
    assert multiply_first(2, 3) == 6
def test_fail_result():
    with pytest.raises(StrictTypeError):
        assert multiply_first(2, 3.0) == 6
def test_skipped_normal():
    assert multiply_second(2, 3.0) == 6.0
def test_skipped_fail():
    with pytest.raises(StrictTypeError):
        assert multiply_second(2.0, 3) == 6.0

def test_skip_return():
    assert multiply_third(4, 2) == 8.0
def test_return_fail():
    with pytest.raises(StrictTypeError):
        assert multiply_fourth(4, 2) == '8'


