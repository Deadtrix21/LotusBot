from dotenv import dotenv_values, load_dotenv
from src.Core.base import NightMareAutoSharded
from src.PreRun import run


load_dotenv()
NightMareAutoSharded().BootProcess()