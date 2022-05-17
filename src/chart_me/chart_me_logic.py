"""module for main function """
import pandas as pd
import altair as alt
from altair import Chart
from typing import List, Type
from chart_me.chart_configs import ChartConfig
from chart_me.datatype_infer_strategy import InferDataTypeStrategyDefault
from chart_me.charting_assembly_strategy import AssembleChartsStrategyDefault

def chart_me(df:pd.DataFrame, cols: List[str], chart_confs: Type[ChartConfig] = ChartConfig)-> Chart:
    """core function that'll return an Altair Chart to visualize

    Args:
        df (pd.DataFrame): Base Dataset
        cols (List[str]): Represent column names in pandas dataframe of interest
        chart_confs (_type_, optional): Manages all settings for Chart creations. Defaults to ChartConfig:ChartConfig.

    Returns:
        alt.Chart: Altair Chart
    """
    
    if cols:
        # TODO check inputs - validation strategy

        # get inferred datatypes
        infer = InferDataTypeStrategyDefault(df, cols)
        infer_dtypes = infer.infer_datatypes()

        # get charting strategy
        assembler = AssembleChartsStrategyDefault(df, cols, infer_dtypes)
        return assembler.assemble_charts()

    else:
        return ValueError('need to send a least one column')
