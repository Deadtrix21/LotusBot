from PythonSrc.Utilities.Imports import System

def rEnv(name:str):
    return System.os.getenv(name)



loc = System.os.getcwd() + "/PythonSrc/Configs/"


def read_json(name:str):
    try:
        with open(loc + name, "r") as file:
            return System.json.load(file)
    except Exception:
        return {}

def write_json(name:str, WritableData:dict):
    try:
        with open(loc + name, "w") as file:
            System.json.dump(WritableData, file)
            return True
    except Exception:
        return False