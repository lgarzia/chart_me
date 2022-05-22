"""module for main function """
import pandas as pd
import altair as alt
from altair import Chart
from typing import List, Type, Union
from chart_me.chart_configs import ChartConfig
from chart_me.datatype_infer_strategy import InferDataTypeStrategyDefault
from chart_me.charting_assembly_strategy import AssembleChartsStrategyDefault

def chart_me(df:pd.DataFrame, *col_args:str, chart_confs: Type[ChartConfig] = ChartConfig)-> Chart:
    """core function that'll return an Altair Chart to visualize

    Args:
        df (pd.DataFrame): Base Dataset
        *cols (List[str]): Represent column names in pandas dataframe of interest
        chart_confs (_type_, optional): Manages all settings for Chart creations. Defaults to ChartConfig:ChartConfig.

    Returns:
        alt.Chart: Altair Chart
    """
    cols:List[str] = list(col_args) #appears arguments for position only is Tuple -> logic expects to pass list of columns
    if cols:
        # TODO check inputs - validation strategy

        # get inferred datatypes
        infer = InferDataTypeStrategyDefault(df, cols)
        infer_dtypes = infer.infer_datatypes()

        # get charting strategy
        assembler = AssembleChartsStrategyDefault(df, cols, infer_dtypes)
        charts_ = assembler.assemble_charts()
        for c in charts_:
            c.display() 

    else:
        return ValueError('need to send a least one column')
