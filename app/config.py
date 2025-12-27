import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from datetime import timedelta

load_dotenv()

def mysql_uri() -> str:
    user = os.getenv("DB_USER", "rizqi")
    password = os.getenv("DB_PASSWORD", "123")
    host = os.getenv("DB_HOST", "mysql.railway.internal")
    db_name = os.getenv("DB_NAME", "railway")
    db_port = os.getenv("DB_PORT", "3306")

    if not password:
        print("--- DEBUG: PASSWORD TIDAK TERDETEKSI (KOSONG) ---")
    
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