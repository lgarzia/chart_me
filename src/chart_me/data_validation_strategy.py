from typing import Protocol
import pandas as pd
#https://www.programiz.com/python-programming/user-defined-exception

class ValidateColumnStrategy(Protocol):
    def validate_column(self, df:pd.DataFrame, col: str) -> bool:
        raise NotImplementedError

class ColumnDoesNotExistsError(Exception):
    pass

class ColumnAllNullError(Exception):
    pass

class ColumnTooManyNullsError(Exception):

    def __init__(self, null_rate, message="Null Rate below Threshold"):
        self.null_rate = null_rate
        self.message = message
        super().__init__(self.message)

    def __str__(self):
        return f'{self.null_rate} calculated --> {self.message}'

class ValidateColumnStrategyDefault:

    null_rate:float = .95 #default check
    def __init__(self, df: pd.DataFrame, col:str):
        self.df = df 
        self.col =col

    def validate_column(self)-> bool:
        #check is exists
        try:
            s_col = self.df[self.col]
        except KeyError:
            raise ColumnDoesNotExistsError()
        
        if s_col.isnull().all():
            raise ColumnAllNullError()

        if s_col.isnull().sum()/len(s_col) > ValidateColumnStrategyDefault.null_rate:
            raise ColumnTooManyNullsError(null_rate=ValidateColumnStrategyDefault.null_rate)
        
        return True
