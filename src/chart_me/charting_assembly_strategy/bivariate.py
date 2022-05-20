from typing import List, Optional
from xml.etree.ElementTree import QName
import pandas as pd
import altair as alt
from functools import singledispatch
from chart_me.datatype_infer_strategy import InferedDataTypes, ChartMeDataType, ChartMeDataTypeMetaType

def assemble_bivariate_charts(df:pd.DataFrame, cols:List[str], infered_data_types:InferedDataTypes, **kwargs)-> Optional[List[alt.Chart]]:
    """Delegated Function to Manage Univariate Use Cases

    Args:
        df (pd.DataFrame): 
        cols (List[str]): 
        infered_data_types (InferedDataTypes):
    """
    if len(cols) == 1:
        raise ValueError("This module only supports two valid columns")
    col_name1 = cols[0]
    col_name2 = cols[1] 
    merged_meta_types = {ChartMeDataTypeMetaType.CATEGORICAL_HIGH_CARDINALITY: ChartMeDataTypeMetaType.KEY, 
                        ChartMeDataTypeMetaType.BOOLEAN: ChartMeDataTypeMetaType.CATEGORICAL_LOW_CARDINALITY} 
    col_MT1 = merged_meta_types.get(infered_data_types.chart_me_data_types_meta[col_name1], infered_data_types.chart_me_data_types_meta[col_name1]) 
    col_MT2 = merged_meta_types.get(infered_data_types.chart_me_data_types_meta[col_name2], infered_data_types.chart_me_data_types_meta[col_name2])    
    preagg_fl = infered_data_types.preaggregated #doesn't impact behavior for univariate/bivariate
    return_charts = []

    if set([col_MT1, col_MT2])  == set([ChartMeDataTypeMetaType.QUANTITATIVE, ChartMeDataTypeMetaType.QUANTITATIVE]):
        return_charts.append(build_scatter_plot(df, col_name1, col_name2))
   
    elif set([col_MT1, col_MT2]) == set([ChartMeDataTypeMetaType.QUANTITATIVE, ChartMeDataTypeMetaType.KEY]):
        col_name_x, col_name_y = [col_name2, col_name1] if col_MT1 == ChartMeDataTypeMetaType.KEY else [col_name1, col_name2]
        return_charts.append(build_hbar_value(df.head(), col_name_x, col_name_y))

    elif set([col_MT1, col_MT2]) == set([ChartMeDataTypeMetaType.QUANTITATIVE, ChartMeDataTypeMetaType.CATEGORICAL_LOW_CARDINALITY]):
        col_name_n, col_name_q = [col_name1, col_name2] if col_MT1 == ChartMeDataTypeMetaType.CATEGORICAL_LOW_CARDINALITY else [col_name2, col_name1]
        if not preagg_fl:
            return_charts.append(build_facet_histogram(df, col_name_n, col_name_q))
        from chart_me.pandas_util import pd_group_me
        agg_dict = {f"{col_name_q}": ['count', 'min', 'max', 'mean', 'median']}
        df = pd_group_me(df, col_name_n, agg_dict, make_long_form=True)
        print(df.head(n=2))
        #return_charts.insert(0, df)
        #TODO how to store manipulated dataframes to pass back to user
        return_charts.append(build_facet_hbars(df, col_name_facet="measures", 
            col_name_y=col_name_n, col_name_x=col_name_q))

    
    else: 
        raise NotImplementedError(f"unknown handling of metatype-{str(col_MT1)}-{str(col_MT2)}")
    return return_charts

def build_scatter_plot(df: pd.DataFrame, col_name1: str, col_name2:str):

    chart = alt.Chart(df).mark_point().encode(
        x=f'{col_name1}:Q', 
        y=f'{col_name2}:Q'
    )
    return chart

def build_hbar_value(df: pd.DataFrame, col_name_x:str, col_name_y:str):
    """Idea is to track keys"""
    chart = alt.Chart(df).mark_bar().encode(
        x=f'{col_name_x}:Q',
        y=f'{col_name_y}:O'        
    )
    return chart

def build_facet_histogram(df: pd.DataFrame, col_name_facet: str, col_name_hist_q:str):
    chart = alt.Chart(df).mark_bar().encode(
        alt.X(f"{col_name_hist_q}:Q", bin=True), 
        y='count()', 
        facet=alt.Facet(f"{col_name_facet}:O", columns=4)
    )
    return chart

def build_facet_hbars(df: pd.DataFrame, col_name_facet:str, col_name_y:str, col_name_x:str):
    chart = alt.Chart(df).mark_bar().encode(
        x=f'{col_name_x}:Q',
        y=f'{col_name_y}:O', 
        facet=alt.Facet(f"{col_name_facet}:O", columns=2)
    ).resolve_scale(x='independent')
    return chart