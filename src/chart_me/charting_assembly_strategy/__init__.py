"""At this time - assume columns validated and inferred data types collected"""
import imp
from typing import Protocol, List, Optional
import altair as alt
import pandas as pd
import warnings

from chart_me.datatype_infer_strategy import InferedDataTypes, ChartMeDataType
from chart_me.errors import InsufficientValidColumnsError

from .univariate import assemble_univariate_charts

class AssembleChartsStrategy(Protocol):
    def assemble_charts(self)->List[alt.Chart]:
        """Core engine to turn data and metadata into visualizations

        Args:
            df (pd.DataFrame): 
            cols (List[str]): at least 1 and no more then 4 at this time
            infered_data_types (InferedDataTypes): metadata required to guide Altair rules

        Returns:
            List[alt.Chart]: return a list of Altair visuals to be rendered
        """

class AssembleChartsStrategyDefault():

    def __init__(self, df:pd.DataFrame, cols:List[str], infered_data_types:InferedDataTypes, **kwargs) -> None:
        """_summary_

        Args:
            df (pd.DataFrame): 
            cols (List[str]): at least 1 and no more then 4 at this time
            infered_data_types (InferedDataTypes): metadata required to guide Altair rules
        """
        self.df = df
        self.user_provided_cols = cols
        self.preaggreted_fl = infered_data_types.preaggregated
        self.infered_data_types = infered_data_types
        self.__dict__.update(kwargs)

    def assemble_charts(self)-> Optional[List[alt.Chart]]:
        """assembles charts based on columns count

        Returns:
            List[alt.Chart]: return list of charts to display
        """
        # TODO preprocess ---> remove 'NOT_SUPPORTED_TYPE -> if zeros out columns return Error
        self.supported_cols = []
        #logic is predicated on number of columns & preaggregated status
        for c in self.user_provided_cols:
            if self.infered_data_types.chart_me_data_types[c] == ChartMeDataType.NOT_SUPPORTED_TYPE:
                warnings.warn(f"{c}-is not a supported datatype - ignoring")
            else:
                self.supported_cols.append(c)
        if not len(self.supported_cols):
            raise InsufficientValidColumnsError(f"There's no columns with supported DataType")
        else:
            charts = assemble_univariate_charts(self.df, self.supported_cols, self.infered_data_types)

        return charts