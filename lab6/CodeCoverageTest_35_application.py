
import pytest

from customs_duty import duty_rate, total_duty, clearance_channel


def test_books_are_duty_free():
    assert duty_rate("books", "FTA") == 0


def test_low_value_personal_import():
    assert total_duty("books", 500, "US", False) == 0


def test_prohibited_categories():
    for category in ("weapons", "narcotics"):
        with pytest.raises(ValueError, match="prohibited item"):
            duty_rate(category, "US")


def test_duty_rates():
    assert duty_rate("electronics", "FTA") == 0.10
    assert duty_rate("electronics", "US") == 0.20
    assert duty_rate("clothing", "FTA") == 0.05
    assert duty_rate("clothing", "US") == 0.12
    assert duty_rate("furniture", "US") == 0.15


def test_negative_value():
    with pytest.raises(ValueError, match="negative value"):
        total_duty("books", -1, "US", False)


def test_gift_exemption():
    assert total_duty("electronics", 5000, "US", True) == 0
    assert total_duty("electronics", 6000, "US", True) == 200


def test_low_value_non_gift_exemption():
    assert total_duty("electronics", 1000, "US", False) == 0


def test_minimum_duty():
    assert total_duty("electronics", 1100, "FTA", False) == 110
    assert total_duty("clothing", 1100, "FTA", False) == 55


def test_clearance_prohibited():
    assert clearance_channel(100, "weapons", True) == "refuse"


def test_clearance_high_value():
    assert clearance_channel(100001, "books", True) == "inspect"


def test_clearance_missing_documents():
    assert clearance_channel(20001, "books", False) == "inspect"


def test_clearance_green():
    assert clearance_channel(20000, "books", True) == "green"

def test_minimum_duty_applies():
    assert total_duty("electronics", 5100, "FTA", True) == 50
