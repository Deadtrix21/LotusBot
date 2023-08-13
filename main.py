import time

from dotenv import dotenv_values, load_dotenv
from src.Core.base import NightMareAutoSharded

load_dotenv()
from src.PreRun import run
from src.PreRun import BuildYaml

time.sleep(5)
# NightMareAutoSharded().BootProcess()