from fastapi import FastAPI

from api.v1.routes import router
from app import AppInterface


class API(FastAPI):
    def __init__(self, app: AppInterface):
        super().__init__()
        self.__app = app
        self.include_router(router)

    @property
    def app(self):
        return self.__app
