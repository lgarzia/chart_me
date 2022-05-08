"""Module host logic to infer data types

    Decent amount of inspiration from lux

"""

from asyncio import create_subprocess_shell
from typing import Protocol, Tuple, List, Optional, Type, Dict
import pandas as pd

from enum import Enum

from zmq import PROTOCOL_ERROR_ZMTP_MALFORMED_COMMAND_UNSPECIFIED
# https://altair-viz.github.io/user_guide/encoding.html [Q, O, N, T, G]
# https://pandas.pydata.org/docs/reference/api/pandas.api.types.infer_dtype.html 

class ChartMeDataType(Enum):
    FLOATS = 'F' #-> Metrics Avg/Media, etc... 
    INTEGER = 'I' #-> Hybrid Datatypes Numerical or seen As Categorical 
    TEMPORAL = 'T', #-> this lead to 'O' otherwise use
    NOMINAL = 'N',
    NOT_SUPPORTED_TYPE = 'NA'

#Idea 2 steps -> DataType + DataTypeMetaType -> rules for visualizations
class ChartMeDataTypeMetaType(Enum):
    KEY = 'K', #-> map to CountD
    BOOLEAN = 'B', #-> Context Aware
    QUANTITATIVE = 'Q', #-> Floats
    CATEGORICAL_HIGH_CARDINALITY = 'C-HC', #top-k
    CATEGORICAL_LOW_CARDINALITY = 'C-LC',
    TEMPORAL = 'T',
    NOT_SUPPORTED_TYPE = 'NA'

# TODO Need to return a dataclass
class InferDataTypeStrategy(Protocol):
    def infer_datatype(self, df:pd.DataFrame, col: str) -> str:
        raise NotImplementedError

class InferDataTypeStrategyDefault():

    def __init__(self, df:pd.DataFrame, cols:List[str], **kwargs):
        self.df = df
        self.cols = cols
        self.preaggregated: Optional[bool] = None
        self.__dict__.update(kwargs)
        self.col_to_cm_dtypes: Dict[str, ChartMeDataType] = {}
        self.col_to_cm_dtypes_meta: Dict[str, ChartMeDataTypeMetaType] = {}

    def _check_if_preaggregated_data(self, threshold: int=100):
        """First check determines aggregation - influences data type"""
        if self.df.shape[0] <= threshold:
            #check if at least l column is completely unique
            self.preaggregated = True if any(self.df.nunique() == self.df.shape[0]) else False
        else:
            self.preaggregated = False
        return self.preaggregated     

    def _get_raw_data_infer_type(self):
        """Apply *some* burden on user to setup DF accordingly"""
        from pandas.api.types import infer_dtype
        map_from_pd_cm = \
        {'string':ChartMeDataType.NOMINAL,
        'bytes': ChartMeDataType.NOT_SUPPORTED_TYPE,
        'floating': ChartMeDataType.FLOATS,
        'integer': ChartMeDataType.INTEGER,
        'mixed-integer':ChartMeDataType.NOT_SUPPORTED_TYPE, #Need to learn more here
        'mixed-integer-float': ChartMeDataType.FLOATS,
        'decimal':ChartMeDataType.FLOATS,
        'complex':ChartMeDataType.NOT_SUPPORTED_TYPE,
        'categorical':ChartMeDataType.NOMINAL,
        'boolean':ChartMeDataType.INTEGER,
        'datetime64':ChartMeDataType.TEMPORAL,
        'datetime':ChartMeDataType.TEMPORAL,
        'date':ChartMeDataType.TEMPORAL,
        'timedelta64':ChartMeDataType.NOMINAL,
        'timedelta':ChartMeDataType.NOMINAL,
        'time':ChartMeDataType.NOT_SUPPORTED_TYPE,
        'period':ChartMeDataType.NOMINAL,
        'mixed':ChartMeDataType.NOT_SUPPORTED_TYPE, #place burden back on user
        'unknown-array':ChartMeDataType.NOT_SUPPORTED_TYPE
        }

        map_from_pd = self.df[self.cols].apply(infer_dtype).to_dict()
        self.col_to_cm_dtypes = {k:map_from_pd_cm[v] for k,v in map_from_pd.items()}
        return self.col_to_cm_dtypes

    # TODO add 'sampling' not processing over huge series
    def _calculate_override_data_infer_type(self):
        """Part to is evaluate """
        for col, data_type in self.col_to_cm_dtypes.items():
            if data_type == ChartMeDataType.FLOATS:
                data_sans_nulls = self.df[col].dropna()
                if all(data_sans_nulls.apply(lambda x: x.is_integer())):
                    self.col_to_cm_dtypes[col] = ChartMeDataType.INTEGER # * Not casting becasause of pd.nan issue
            if data_type == ChartMeDataType.NOMINAL:
                from dateutil.parser import ParserError
                try: 
                    self.df[col] = pd.to_datetime(self.df[col])
                    self.col_to_cm_dtypes[col] = ChartMeDataType.TEMPORAL
                except (ParserError, TypeError, ValueError) as error:
                    pass
        return self.col_to_cm_dtypes

    def _get_data_infer_meta_type_col(self, col:str):
        """series of evaluations"""
        if self.col_to_cm_dtypes[col] == ChartMeDataType.NOT_SUPPORTED_TYPE:
            self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.NOT_SUPPORTED_TYPE 
        if self.col_to_cm_dtypes[col] == ChartMeDataType.FLOATS:
            self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.QUANTITATIVE
        if self.col_to_cm_dtypes[col] == ChartMeDataType.TEMPORAL:
            self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.TEMPORAL
        if self.col_to_cm_dtypes[col] == ChartMeDataType.INTEGER:
            #Check if a Key - All Unique and No Nulls
            if self.df[col].nunique() == self.df[col].shape[0]:
                self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.KEY
            #Check if a Boolean Value
            elif (int(self.df[col].min())==0 and int(self.df[col].max())==1 and self.df[col].nunique() == 2):
                self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.BOOLEAN
            else:
                self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.QUANTITATIVE
        if self.col_to_cm_dtypes[col] == ChartMeDataType.NOMINAL:
            hc_threshold = self.__dict__.get('cardinality_threshold_ratio', .10) 
            #if 100; 10 or less low cardinality
            if self.df[col].nunique() == self.df[col].shape[0]:
                self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.KEY
            elif self.df[col].nunique()/self.df.shape[0] <= hc_threshold:
                self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.CATEGORICAL_LOW_CARDINALITY
            else:
                self.col_to_cm_dtypes_meta[col] = ChartMeDataTypeMetaType.CATEGORICAL_HIGH_CARDINALITY
    
    def _calculate_data_type_meta(self):
        for col, val in self.col_to_cm_dtypes.items():
            self._get_data_infer_meta_type_col(col)
        return self.col_to_cm_dtypes_meta

    @classmethod
    def _override_str_check_if_date(cls, str_vals:Tuple[str]):
        from datetime import datetime
        try:
            check_ = [datetime.fromisoformat(d) for d in str_vals]
            return True
        except ValueError as e: 
            return False


