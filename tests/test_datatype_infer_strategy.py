import chart_me.datatype_infer_strategy_configs as dti
import pytest


#preagg_inputs = "cols,output"
#preagg_checks = 

@pytest.mark.parametrize("pa_cols, pa_output", [("unique_vals", True), 
('unique_with_nulls', False),
('duplicates', False), 
("unique_vals,duplicates", True)])

def test_preagg_checks(conftest_check_agg_dataframe, pa_cols, pa_output):
    cols = list(pa_cols.split(','))
    df = conftest_check_agg_dataframe[cols]
    infer = dti.InferDataTypeStrategyDefault(df, cols)
    assert infer._check_if_preaggregated_data() is pa_output

def test_preagg_checks_too_big(conftest_check_agg_dataframe_too_big):
    df = conftest_check_agg_dataframe_too_big
    cols = ['unique_vals']
    infer = dti.InferDataTypeStrategyDefault(df, cols)
    assert infer._check_if_preaggregated_data() is False