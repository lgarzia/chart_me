"""Module for managing univariate use cases!"""
from typing import List, Optional
import pandas as pd
import altair as alt
from functools import singledispatch
from chart_me.datatype_infer_strategy import InferedDataTypes, ChartMeDataType, ChartMeDataTypeMetaType

def assemble_univariate_charts(df:pd.DataFrame, cols:List[str], infered_data_types:InferedDataTypes, **kwargs)-> Optional[List[alt.Chart]]:
    """Delegated Function to Manage Univariate Use Cases

    Args:
        df (pd.DataFrame): 
        cols (List[str]): 
        infered_data_types (InferedDataTypes):
    """
    if len(cols) != 1:
        raise ValueError("Only suport single column")
    
    col_DT = infered_data_types.chart_me_data_types[cols[0]]
    col_MT = infered_data_types.chart_me_data_types_meta[cols[0]]
    preagg_fl = infered_data_types.preaggregated
    return_charts = []
    if (col_DT == ChartMeDataType.FLOATS and col_MT == ChartMeDataTypeMetaType.QUANTITATIVE):
        return_charts.append(build_histogram(df, cols[0]))
    else: 
        return None

    return return_charts

def build_histogram(df:pd.DataFrame, col_name:str)->alt.Chart:
    """_summary_

    Args:
        df (pd.DataFrame): _description_
        col_name (str): _description_

    Returns:
        alt.Chart: _description_
    """
    chart = alt.Chart(df).mark_bar().encode(
        alt.X(f"{col_name}:Q", bin=True),
        y='count()'
    )
    return chart
