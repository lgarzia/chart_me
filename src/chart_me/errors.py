"""A collection of custom errors used in Chart Me
#https://www.programiz.com/python-programming/user-defined-exception

Default behavior excepts a message
"""

class InsufficientValidColumnsError(Exception):
    """Raised after validation and inferred data types

        Scenario: Only columns chosen are NOT_SUPPORTED_TYPE 
    
    """  
    pass
