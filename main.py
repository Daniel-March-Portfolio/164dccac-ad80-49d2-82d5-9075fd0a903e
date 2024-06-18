from api import API
from app import App
from database import Database

import os

DATABASE_URL = os.getenv("DATABASE_URL")

database = Database(DATABASE_URL)
app = App(database)
api = API(app)
