from PythonSrc.Core.Base import NightmareLotus
from dotenv import dotenv_values, load_dotenv

load_dotenv()

# from PythonSrc.PostConfigureations import Extentions


NightmareLotus = NightmareLotus()
NightmareLotus.boot()