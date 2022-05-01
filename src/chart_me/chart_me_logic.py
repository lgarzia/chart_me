"""module for main function """
import pandas as pd
import altair as alt
from altair import Chart
from typing import List, Type
from chart_me.chart_configs import ChartConfig

from vega_datasets import data
cars = data.cars()

def chart_me(df:pd.DataFrame, cols: List[str], chart_confs: Type[ChartConfig] = ChartConfig)-> Chart:
    """core function that'll return an Altair Chart to visualize

    Args:
        df (pd.DataFrame): Base Dataset
        cols (List[str]): Represent column names in pandas dataframe of interest
        chart_confs (_type_, optional): Manages all settings for Chart creations. Defaults to ChartConfig:ChartConfig.

    Returns:
        alt.Chart: Altair Chart
    """
    # TODO expand pass univariate
    if cols:
        if len(cols)> 1:
            raise NotImplementedError('only support univariate cases')
        else:
            # *I know Python is Jump without looking; trying to add a bit of user experience upfront
            for c in cols:
                v = chart_confs.validate_column_strategy(df, c)
                v.validate_column()
            return alt.Chart(cars).mark_point().encode(
        x='Horsepower',
        y='Miles_per_Gallon',
        color='Origin',
        ).interactive()
    else:
        raise TypeError('Require at least 1 column')    

