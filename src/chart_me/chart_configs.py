"""Defines default Chart Config

Build out ChartConfig used as default - specifies:
* validate_column_strategy: Type[ValidateColumnStrategy]
* datatype_infer_strategy: Type[InferDataTypeStrategy]
* assemble_charts_strategy: Type[AssembleChartsStrategy]

"""
from dataclasses import dataclass
from chart_me.data_validation_strategy import ValidateColumnStrategy, ValidateColumnStrategyDefault
from typing import Type
from chart_me.datatype_infer_strategy import InferDataTypeStrategy, InferDataTypeStrategyDefault
from chart_me.charting_assembly_strategy import AssembleChartsStrategy, AssembleChartsStrategyDefault
from chart_me.data_validation_strategy import ValidateColumnStrategyDefault

validate_column_strategy: Type[ValidateColumnStrategy]
datatype_infer_strategy: Type[InferDataTypeStrategy]
assemble_charts_strategy: Type[AssembleChartsStrategy]

@dataclass
class ChartConfig:
    """Default Instance of Chart Config"""
    validate_column_strategy = ValidateColumnStrategyDefault
    datatype_infer_strategy = InferDataTypeStrategyDefault
    assemble_charts_strategy = AssembleChartsStrategyDefault

