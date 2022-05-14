"""Collection of panda manipulations - leverage prior to charts 

    This big idea is to keep pandas operations isolated from visuals
    keep Altair logic very simple if possible

"""
from typing import Union, List, Dict, Optional
import pandas as pd
#https://jamesrledoux.com/code/group-by-aggregate-pandas
#{'Age': ['mean', 'min', 'max']} # TODO document function signature
def pd_group_me(df:pd.DataFrame, cols:Union[List[str], str], agg_dict:Dict, is_temporal:bool=False)->pd.DataFrame:
    df = df.groupby(cols).agg(agg_dict).reset_index()
    key_cols = [f"{k}_{i}" for k in agg_dict.keys() for i in agg_dict[k]]
    sort_key = [key_cols][0]
    df.columns = list([cols]) + list(key_cols)
    if is_temporal:
        return df.sort_values(list([cols]), ascending=True)
    else:
        return df.sort_values(sort_key, ascending=False)

#https://predictivehacks.com/?all-tips=how-to-truncate-dates-to-month-in-pandas
#https://pandas.pydata.org/docs/reference/api/pandas.Series.dt.to_period.html
def pd_truncate_date(df: pd.DataFrame, col:str) -> pd.Series:
    return df[col].dt.to_period('M').astype(str)