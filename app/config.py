# app/config.py

import os
from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.getenv("QA_POSTGRES_USER","admin")
POSTGRES_PASSWORD = os.getenv("QA_POSTGRES_PASSWORD","admin1234")
POSTGRES_DB = os.getenv("QA_POSTGRES_DB","db_qa")
POSTGRES_HOST = os.getenv("QA_POSTGRES_HOST","localhost")
POSTGRES_PORT = os.getenv("POSTGRES_PORT","5432")
POSTGRES_DB = os.getenv("QA_POSTGRES_DB","db_qa")


class Config:
    # SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "postgresql://admin:admin1234@localhost:5432/db_qa")
    # SQLALCHEMY_DATABASE_URI = os.getenv("QA_DATABASE_URL","postgresql+psycopg2://admin:admin1234@postgres:5432/db_aq")
    SQLALCHEMY_DATABASE_URI = f"postgresql+psycopg2://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SEED_DB = os.getenv("QA_SEED_DB", "no")


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
