"""Taking inspiration from PyJanitor on testing Pandas Stuff"""
from cmath import exp
from ctypes.wintypes import FLOAT
from unittest import result
import chart_me.validate_strategy_configs as vsc
from chart_me.datatype_infer_strategy_configs import ChartMeDataType, ChartMeDataTypeMetaType
import pytest

def test_column_does_not_exist_error(conftest_basic_dataframe):
    df = conftest_basic_dataframe
    c_validator = vsc.ValidateColumnStrategyDefault(df, 'col_no_exist')
    with pytest.raises(vsc.ColumnDoesNotExistsError):
        c_validator.validate_column()

def test_column_is_all_null_error(conftest_basic_dataframe):
    df = conftest_basic_dataframe
    c_validator = vsc.ValidateColumnStrategyDefault(df, 'all_nulls')
    with pytest.raises(vsc.ColumnAllNullError):
        c_validator.validate_column()

def test_column_is_mostly_null_error(conftest_basic_dataframe):
    df = conftest_basic_dataframe
    c_validator = vsc.ValidateColumnStrategyDefault(df, 'mostly_nulls')
    with pytest.raises(vsc.ColumnTooManyNullsError):
        c_validator.validate_column()

@pytest.mark.parametrize("col_names", ['inty_integers', 'floaty_floats', 'stringy_strings', 'datie_dates'])
def test_columns_are_valid(conftest_basic_dataframe, col_names):
    df = conftest_basic_dataframe
    c_validator = vsc.ValidateColumnStrategyDefault(df, col_names)
    assert c_validator.validate_column()



def test_infer_data_types(ct_df_check_infer_dtypes):
    df = ct_df_check_infer_dtypes
    cols = ct_df_check_infer_dtypes.columns.tolist()
    from chart_me.datatype_infer_strategy_configs import InferDataTypeStrategyDefault
    infer = InferDataTypeStrategyDefault(df, cols)
    results = infer._get_raw_data_infer_type()
    print(results)
    expected = {'inty_integers': ChartMeDataType.INTEGER, 
    'inty_integers_w_nulls': ChartMeDataType.FLOATS, 
    'floaty_floats': ChartMeDataType.FLOATS, 
    'stringy_strings': ChartMeDataType.NOMINAL, 
    'stringy_strings_w_nulls': ChartMeDataType.NOMINAL, 
    'datie_dates': ChartMeDataType.TEMPORAL,
    'datie_dates_null': ChartMeDataType.TEMPORAL, 
    'boolie_bools': ChartMeDataType.INTEGER, 
    'boolie_bools_null': ChartMeDataType.INTEGER # * This is interesting result
    }
    assert results == expected


def test_calculate_override_data_infer_type(ct_df_override_dtypes):
    df = ct_df_override_dtypes
    cols = df.columns.tolist()
    from chart_me.datatype_infer_strategy_configs import InferDataTypeStrategyDefault
    infer = InferDataTypeStrategyDefault(df, cols)
    _ = infer._get_raw_data_infer_type()
    results = infer._calculate_override_data_infer_type()
    expected =  {'stringy_dates': ChartMeDataType.TEMPORAL, 
    'inty_integers_w_nulls': ChartMeDataType.INTEGER, 
    'floaty_integers': ChartMeDataType.INTEGER, 
    'string_not_dates': ChartMeDataType.NOMINAL}
    assert results == expected


def test_calculate_data_type_meta(ct_df_calculate_meta_dtypes):
    df = ct_df_calculate_meta_dtypes
    cols = df.columns.tolist()
    from chart_me.datatype_infer_strategy_configs import InferDataTypeStrategyDefault
    infer = InferDataTypeStrategyDefault(df, cols, cardinality_threshold_ratio=.4)
    _ = infer._get_raw_data_infer_type()
    _ = infer._calculate_override_data_infer_type()
    results = infer._calculate_data_type_meta()
    expected =  {'temporal_t': ChartMeDataTypeMetaType.TEMPORAL, 
    'floaties_q': ChartMeDataTypeMetaType.QUANTITATIVE, 
    'nominal_lc': ChartMeDataTypeMetaType.CATEGORICAL_LOW_CARDINALITY,
    'nominal_hc': ChartMeDataTypeMetaType.CATEGORICAL_HIGH_CARDINALITY, 
    'nominal_k': ChartMeDataTypeMetaType.KEY, 
    'integers_b': ChartMeDataTypeMetaType.BOOLEAN,
    'integers_k': ChartMeDataTypeMetaType.KEY,
    'integers_q': ChartMeDataTypeMetaType.QUANTITATIVE    
    }
    print(results)
    assert results == expected