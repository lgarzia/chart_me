"""Module to manage Chart Configurations to support customization down the road"""
from dataclasses import dataclass
from chart_me.data_validation_strategy import ValidateColumnStrategy, ValidateColumnStrategyDefault
from typing import Type

validate_column_strategy: Type[ValidateColumnStrategy]

@dataclass
class ChartConfig:
    validate_column_strategy = ValidateColumnStrategyDefault


