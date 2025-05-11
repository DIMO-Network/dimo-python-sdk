import pytest
from dimo.errors import DimoTypeError, check_type, check_optional_type


def test_check_type_passes_for_correct_type():
    # call check_type with valid args which should not raise anything
    check_type("count", 5, int)


def test_check_type_raises_for_incorrect_type():
    with pytest.raises(DimoTypeError) as exc:
        check_type("name", 123, str)
    err = exc.value
    assert err.param_name == "name"
    assert err.expected_type is str
    assert isinstance(err.actual_value, int)

    assert "name must be a str" in str(err)
    assert "but was entered as type int" in str(err)


def test_check_optional_type_allows_none():
    # None is allowed
    check_optional_type("maybe", None, dict)


def test_check_optional_type_raises_for_wrong_non_none():
    with pytest.raises(DimoTypeError) as exc:
        check_optional_type("maybe", 3.14, str)
    err = exc.value
    assert err.param_name == "maybe"
    assert err.expected_type is str
    assert isinstance(err.actual_value, float)
