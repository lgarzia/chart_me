"""A collection of custom errors used in Chart Me
#https://www.programiz.com/python-programming/user-defined-exception
#https://www.programiz.com/python-programming/user-defined-exception

Default behavior excepts a message
"""
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

class InsufficientValidColumnsError(Exception):
    pass