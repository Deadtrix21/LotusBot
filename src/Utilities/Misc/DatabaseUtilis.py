from ..Imports.SysImports import os, json

def rEnv(name:str):
    return os.getenv(name)



loc = os.getcwd() + "/src/Configs/"


def read_json(name:str):
    try:
        with open(loc + name, "r") as file:
            return json.load(file)
    except Exception:
        return {}

def write_json(name:str, WritableData:dict):
    try:
        with open(loc + name, "w") as file:
            json.dump(WritableData, file)
            return True
    except Exception:
        return False