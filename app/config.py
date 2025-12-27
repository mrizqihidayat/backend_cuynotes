import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from datetime import timedelta

load_dotenv()

def mysql_uri() -> str:
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASSWORD")
    host = os.getenv("DB_HOST")
    db_name = os.getenv("DB_NAME")
    db_port = os.getenv("DB_PORT")

    # Debugging sederhana (akan muncul di log Railway saat startup)
    if not password:
        print("WARNING: DB_PASSWORD is empty!")

    return f"mysql+pymysql://{user}:{password}@{host}:{db_port}/{db_name}"

class Config:
    SQLALCHEMY_DATABASE_URI = mysql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    #secret key jwt
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "123")

    #token expires JWT
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

def db_connection():
    uri = Config.SQLALCHEMY_DATABASE_URI
    try:
        engine = create_engine(uri)
        connection = engine.connect()
        print("Database connected")
        connection.close()
        return True
    except OperationalError as e:
        raise RuntimeError(f"Database not connected: {e}")