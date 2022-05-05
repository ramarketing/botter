import os

from dotenv import dotenv_values


class Config:
    variables = {}

    def __init__(self, **kwargs):
        config = dotenv_values(dotenv_path=f'{os.getcwd()}/.env')

        for key in kwargs.keys():
            setattr(self, key.upper(), kwargs[key])

        for key in config.keys():
            setattr(self, key.upper(), config[key])

    def __getattribute__(self, __name):
        try:
            value = self.variables[__name]
        except KeyError:
            value = os.getenv(__name, None)

        return value

    def __setattr__(self, __name, __value):
        if __name in self.variables:
            return
        self.variables[__name] = __value


config = Config(**{
    'base_dir': os.getcwd(),
})
