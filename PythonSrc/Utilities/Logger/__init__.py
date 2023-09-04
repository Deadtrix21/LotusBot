from loguru import logger
from PythonSrc.Utilities.Imports.System import sys


def SetLogger(name: str):
    logger.remove(0)
    logger.add(sys.stderr, level="TRACE")
    logger.add(f"./Logs/{name}.log", rotation="7 days")
    return logger

def GetLogger(name: str):
    logger.add(f"./Logs/{name}.log", rotation="7 days")
    return logger