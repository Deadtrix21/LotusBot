from core.subConfigs import SubConfigurations

configs = SubConfigurations()
from configs.py import EconomyConfig
configs.config_callback(EconomyConfig.InternShip)
