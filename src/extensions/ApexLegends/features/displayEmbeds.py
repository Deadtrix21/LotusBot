from src.utils.base_imports import *


def build_embed(value: dict):
    returnData: list = []
    if ("br" in value):
        dictBR = value["br"]
        embedBR = DiscordEmbed(
            title="Apex Legends Battle Royale",
            description=f"Servers Checked At: {arrow.utcnow().format('YYYY-MM-DD HH:mm ZZ')}",
            color=0x000c30
        )
        returnData.append(embedBR)
        data = dictBR["current"]
        embedBR.add_field(name="Current Map", value=f"{data['map']}", inline=False)
        embedBR.add_field(name="Remaining Time", value=f"{data['remainingTimer']}", inline=False)
        data = dictBR["next"]
        embedBR.add_field(name="Next Map", value=f"{data['map']}", inline=False)
        embedBR.add_field(name="Rotating At",
                          value=f"{arrow.get(data['readableDate_start']).format('YYYY-MM-DD HH:mm ZZ')}", inline=False)
        embedBR.add_field(name="Next Rotation",
                          value=f"{arrow.get(data['readableDate_end']).format('YYYY-MM-DD HH:mm ZZ')}", inline=False)
    if ("r" in value):
        dictR = value["r"]
        embedR = DiscordEmbed(
            title="Apex Legends Ranked",
            description=f"Servers Checked At: {arrow.utcnow().format('YYYY-MM-DD HH:mm ZZ')}",
            color=0x000c30)
        returnData.append(embedR)
        data = dictR["current"]
        embedR.add_field(name="Current Map", value=f"{data['map']}", inline=False)
        embedR.add_field(name="Remaining Time", value=f"{data['remainingTimer']}", inline=False)
        data = dictR["next"]
        embedR.add_field(name="Next Map", value=f"{data['map']}", inline=False)
        embedR.add_field(name="Rotating At",
                         value=f"{arrow.get(data['readableDate_start']).format('YYYY-MM-DD HH:mm ZZ')}",
                         inline=False)
        embedR.add_field(name="Next Rotation",
                         value=f"{arrow.get(data['readableDate_end']).format('YYYY-MM-DD HH:mm ZZ')}",
                         inline=False)
    if ("ltm" in value):
        dictLtm = value["ltm"]
        embedLtm = DiscordEmbed(
            title="Apex Legends Limited Time Events",
            description=f"Servers Checked At: {arrow.utcnow().format('YYYY-MM-DD HH:mm ZZ')}",
            color=0x000c30)
        returnData.append(embedLtm)
        data = dictLtm["current"]
        embedLtm.add_field(name="Current Map", value=f"{data['map']}", inline=False)
        embedLtm.add_field(name="Game Mode", value=f"{data['eventName']}", inline=False)
        embedLtm.add_field(name="Remaining Time", value=f"{data['remainingTimer']}", inline=False)
        data = dictLtm["next"]
        embedLtm.add_field(name="Next Map", value=f"{data['map']}", inline=False)
        embedLtm.add_field(name="Game Mode", value=f"{data['eventName']}", inline=False)
        embedLtm.add_field(name="Rotating At",
                           value=f"{arrow.get(data['readableDate_start']).format('YYYY-MM-DD HH:mm ZZ')}", inline=False)
        embedLtm.add_field(name="Next Rotation",
                           value=f"{arrow.get(data['readableDate_end']).format('YYYY-MM-DD HH:mm ZZ')}", inline=False)
    return returnData
