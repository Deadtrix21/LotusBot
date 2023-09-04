from PythonSrc.Utilities.Imports.System import *
from PythonSrc.Utilities.Imports.Discord import *
from PythonSrc.Utilities import Logger
from PythonSrc.Utilities.Misc.Database import read_json, write_json
from .... import Database as Entity





async def InternShip():
    json_data = read_json("EconomyConfig.json")
    jobs = []
    des_jobs = "Please select one of the following jobs:\n"
    json_data['datetime-last'] = str(datetime.datetime.now())
    array = await Entity.Work.all().to_list()
    for i in array:
        jobs.append(i.name)
        des_jobs += i.name + "\n"
    json_data['intern-jobs'] = jobs
    json_data['intern-jobs-des'] = des_jobs
    write_json("EconomyConfig.json", json_data)
