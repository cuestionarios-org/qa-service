# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:admin1234@localhost:5432/db_qa")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL","postgresql://admin:admin1234@localhost:5432/db_aq")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.getenv("SECRET_KEY", "mi_clave_secreta")


class DevelopmentConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = True

class TestingConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    TESTING = True

class ProductionConfig(Config):
    # SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL')
    DEBUG = False

config_dict = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig
}
