from yaml import safe_load


class PrimaryService:
    def __init__(self):
        self.__service = None
        self.__service_env = None
        self.setup_hook()

    def setup_hook(self):
        try:
            with open('../environment/.env.yml', 'r') as file:
                self.__service = safe_load(file)['discord']
        except Exception as e:
            try:
                with open('.env.yml', 'r') as file:
                    self.__service = safe_load(file)['discord']
            except Exception as error:
                print("Cannot find config")
        self.__service_env = self.__service[self.check_env()]

    def check_env(self) -> str:
        return self.__service["app-env"]

    def get_config(self):
        return self.__service

    def get_env_config(self):
        return self.__service_env

