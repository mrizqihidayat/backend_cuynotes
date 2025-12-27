import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from datetime import timedelta

load_dotenv()

def mysql_uri() -> str:
    user = os.getenv("DB_USER", "root")
    password = os.getenv("DB_PASSWORD", "")
    host = os.getenv("DB_HOST", "mysql.railway.internal")
    db_name = os.getenv("DB_NAME", "railway")

    db_port = os.getenv("DB_PORT", "3306")
    if not db_port:
        db_port = "3306"

    return f"mysql+pymysql://{user}:{password}@{host}:{db_port}/{db_name}"

class Config:
    @property
    def SQLALCHEMY_DATABASE_URI(self):
        return mysql_uri()
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "rahasia")

    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

def db_connection():
    uri = mysql_uri()
    try:
        # Menambahkan pool_pre_ping agar koneksi ke MySQL Railway lebih stabil
        engine = create_engine(uri, pool_pre_ping=True)
        connection = engine.connect()
        print(f"Database connected to {uri.split('@')[1]}") 
        connection.close()
        return True
    except Exception as e:
        # Memberikan pesan error yang lebih detail di log Railway
        print(f"Connection Failed: {str(e)}")
        raise RuntimeError(f"Database not connected: {e}")