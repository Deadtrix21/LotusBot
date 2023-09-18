import discord
import os, json

def discord_intents():
    return discord.Intents.default().all()




loc = os.getcwd() + "/src/config/"


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