"""Collection of panda manipulations - leverage prior to charts 

    This big idea is to keep pandas operations isolated from visuals
    keep Altair logic very simple if possible

"""
from typing import Union, List, Dict, Optional
import pandas as pd
#https://jamesrledoux.com/code/group-by-aggregate-pandas
#{'Age': ['mean', 'min', 'max']} # TODO document function signature
def pd_group_me(df:pd.DataFrame, cols:Union[List[str], str], agg_dict:Dict, is_temporal:bool=False, make_long_form=False)->pd.DataFrame:
    df = df.groupby(cols).agg(agg_dict).reset_index()
    key_cols = [f"{k}-{i}" for k in agg_dict.keys() for i in agg_dict[k]]
    sort_key = [key_cols][0]
    df.columns = list([cols]) + list(key_cols)
    if is_temporal:
        df = df.sort_values(list([cols]), ascending=True)
    else:
        df =  df.sort_values(sort_key, ascending=False)
    if make_long_form:
        df = pd.melt(df, id_vars=cols, var_name='measures', value_name=next(iter(agg_dict.keys())))
        df['measures'] = df['measures'].str.split('-').str[-1]
    return df
#https://predictivehacks.com/?all-tips=how-to-truncate-dates-to-month-in-pandas
#https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.to_period.html
def pd_truncate_date(df: pd.DataFrame, col:str) -> pd.Series:
    return df[col].dt.to_period('M').astype(str)