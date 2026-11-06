import pytest
from application.logik import finns_stad


@pytest.mark.parametrize(
    "namn, forvantat",
    [
        ("Stockholm", True),
        ("Kiruna", True),
        ("Göteborg", True),
        ("Uppsala", False),
        ("stockholm", False),
        ("", False),
        (None, False),
    ],
)
def test_finns_stad(namn, forvantat):
    assert finns_stad(namn) == forvantat
