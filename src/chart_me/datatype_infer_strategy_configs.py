"""Module host logic to infer data types

    Decent amount of inspiration from lux

"""
from typing import Protocol, Tuple, List, Optional
import pandas as pd

from enum import Enum
class DataType(Enum):
    QUANTITATIVE = 'Q'
    TEMPORAL = 'T',
    CATEGORICAL_HIGH_CARDINALITY = 'C-HC',
    CATEGORICAL_LOW_CARDINALITY = 'C-LC',
    KEY = 'K'

# TODO Need to return a dataclass
class InferDataTypeStrategy(Protocol):
    def infer_datatype(self, df:pd.DataFrame, col: str) -> str:
        raise NotImplementedError

class InferDataTypeStrategyDefault():

    def __init__(self, df:pd.DataFrame, cols:List[str]):
        self.df = df
        self.cols = cols
        self.preaggregated: Optional[bool] = None
    
    def _check_if_preaggregated_data(self, threshold: int=100):
        """First check determines aggregation - influences data type"""
        if self.df.shape[0] <= threshold:
            #check if at least l column is completely unique
            self.preaggregated = True if any(self.df.nunique() == self.df.shape[0]) else False
        else:
            self.preaggregated = False
        return self.preaggregated     


    @classmethod
    def _override_str_check_if_date(cls, str_vals:Tuple[str]):
        from datetime import datetime
        try:
            check_ = [datetime.fromisoformat(d) for d in str_vals]
            return True
        except ValueError as e: 
            return False

    def get_data_type(self)->DataType:
        from pandas.api.types import is_datetime
        return DataType.QUANTITATIVE

