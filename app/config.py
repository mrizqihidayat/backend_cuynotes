import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from datetime import timedelta

load_dotenv()

def mysql_uri() -> str:
    # If Railway provides full URLs, prefer them and normalize scheme
    full_url = os.getenv("MYSQL_URL") or os.getenv("MYSQL_PUBLIC_URL") or os.getenv("DATABASE_URL")
    if full_url:
        if full_url.startswith("mysql://"):
            full_url = "mysql+pymysql://" + full_url[len("mysql://") :]
        return full_url

    # Prefer explicit DB_* vars, but support Railway's MYSQL*/RAILWAY_* too
    user = os.getenv("DB_USER") or os.getenv("MYSQLUSER") or "root"
    password = (
        os.getenv("DB_PASSWORD")
        or os.getenv("MYSQLPASSWORD")
        or os.getenv("MYSQL_ROOT_PASSWORD")
        or ""
    )
    host = (
        os.getenv("DB_HOST")
        or os.getenv("MYSQLHOST")
        or os.getenv("RAILWAY_PRIVATE_DOMAIN")
        or os.getenv("RAILWAY_TCP_PROXY_DOMAIN")
        or "mysql.railway.internal"
    )
    db_name = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE") or os.getenv("MYSQL_DATABASE") or "railway"
    db_port = os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or os.getenv("RAILWAY_TCP_PROXY_PORT") or "3306"

    if not password:
        print("--- DEBUG: PASSWORD TIDAK TERDETEKSI (KOSONG) ---")
    
    return f"mysql+pymysql://{user}:{password}@{host}:{db_port}/{db_name}"

class Config:
    SQLALCHEMY_DATABASE_URI = mysql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    
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
        # Enforce normal behavior: fail fast when DB is unreachable.
        raise RuntimeError(f"Database not connected: {e}")