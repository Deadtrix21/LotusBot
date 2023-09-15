from loguru import logger
import sys

logger.remove(0)
logger.add(sys.stderr, level="TRACE")

def SpecificLog(log_name: str):
    logger.add(
        f"./Logs/{log_name}.log",
        filter=lambda record: record["extra"].get("name") == f"{log_name}",
        level="TRACE", retention="1 week"
    )
    loggerName = logger.bind(name=f"{log_name}")
    return loggerName

