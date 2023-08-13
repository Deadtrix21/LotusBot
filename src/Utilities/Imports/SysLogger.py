from loguru import logger
from ..Imports.SysImports import *

def SetLogger(name: str):
    logger.remove(0)
    logger.add(sys.stderr, level="TRACE")
    logger.add(f"src/Logs/{name}.log", rotation="7 days")
    return logger
def GetLogger(name: str):
    logger.add(f"src/Logs/{name}.log", rotation="7 days")
    return logger
