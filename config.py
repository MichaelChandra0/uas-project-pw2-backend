import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = "projectUASPW2Kelompok"
    SECRET_API_KEY = "jesselyncantik123"

    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(BASEDIR, "inventory.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    cloud_name = os.getenv("CLOUD_NAME")
    api_key = os.getenv("API_KEY")
    api_secret = os.getenv("API_SECRET")
    secure = True
