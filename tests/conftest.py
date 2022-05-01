import pytest
import pandas as pd
import numpy as np
from datetime import datetime

@pytest.fixture
def conftest_basic_dataframe():
    data = {
        "inty_integers": [1, 2, 3] * 7,
        "floaty_floats": [1.234_523_45, 2.456_234, None] * 7,
        "stringy_strings": ["rabbit", "leopard", None] * 7,
        "datie_dates":[datetime(2020,1,1), datetime(2021,2,3), None]*7,
        "all_nulls":[None, None, None] *7,
        "mostly_nulls": [None, None, None]*6 + [None, None, 'Not Null']

    }
    df = pd.DataFrame(data)
    return df