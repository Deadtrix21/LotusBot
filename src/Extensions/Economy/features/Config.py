from ....Utilities.Imports.SysImports import *
from ....Utilities.Misc.DatabaseUtilis import *
from .... import DatabaseModels as Entity

loc = os.getcwd() + "src/Configs/"


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
