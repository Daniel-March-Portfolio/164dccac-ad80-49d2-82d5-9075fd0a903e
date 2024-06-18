from fastapi import FastAPI

from app import AppInterface


class API(FastAPI):
    def __init__(self, app: AppInterface):
        super().__init__()
        self.__app = app

    @property
    def app(self):
        return self.__app
