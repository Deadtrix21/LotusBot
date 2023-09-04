from PythonSrc.Utilities.Imports.System import *
from PythonSrc.Utilities.Imports.Discord import *
from PythonSrc.Utilities import Logger


class UserNotRegistered(commands.CommandError):
    def __init__(self, member: Member = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.member = member


class UserNotRegisteredForTax(commands.CommandError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class UserRegisteredForTax(commands.CommandError):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
