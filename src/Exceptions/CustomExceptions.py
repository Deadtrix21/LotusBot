from ..Utilities.Imports.SysImports import *
from ..Utilities.Imports.DiscordImports import *



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



