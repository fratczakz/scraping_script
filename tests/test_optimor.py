import time
import pytest

import optimor.core as core


@pytest.mark.parametrize(
    ("country", "expected"),
    [
        ("Germany", 2)
    ]
)
def test_get_land_line_value(selenium, country, expected):
    o2b = core.O2Browser()
    time.sleep(3)

    o2b.query_country('Germany')
    val = o2b.get_land_line_value()
    o2b.close()

    assert val == expected
