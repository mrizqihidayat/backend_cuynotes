import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError
from sqlalchemy.engine import make_url
from datetime import timedelta

load_dotenv()

def mysql_uri() -> str:
    """Mendeteksi dan membangun URI koneksi database dari environment variables."""
    full_url = os.getenv("MYSQL_URL") or os.getenv("MYSQL_PUBLIC_URL") or os.getenv("DATABASE_URL")
    
    if full_url:
        if full_url.startswith("mysql://"):
            full_url = full_url.replace("mysql://", "mysql+pymysql://", 1)
        return full_url

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
        or "mysql.railway.internal"
    )
    db_name = (
        os.getenv("DB_NAME") 
        or os.getenv("MYSQLDATABASE") 
        or os.getenv("MYSQL_DATABASE") 
        or "railway"
    )
    db_port = os.getenv("DB_PORT") or os.getenv("MYSQLPORT") or "3306"

    if not password:
        print("--- DEBUG WARNING: DATABASE PASSWORD IS EMPTY ---")
    
    return f"mysql+pymysql://{user}:{password}@{host}:{db_port}/{db_name}"

class Config:
    SQLALCHEMY_DATABASE_URI = mysql_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}
    
    JWT_SECRET_KEY = os.getenv("SECRET_KEY", "super-secret-key-123")
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=8)

def db_connection():
    """Fungsi untuk memverifikasi koneksi database saat aplikasi booting."""
    uri = Config.SQLALCHEMY_DATABASE_URI
    try:
        try:
            parsed = make_url(uri)
            print(f"--- ATTEMPTING CONNECTION: host={parsed.host}, port={parsed.port}, db={parsed.database}, user={parsed.username} ---")
        except:
            print("--- ATTEMPTING CONNECTION: (URL parse failed for logging) ---")

        engine = create_engine(uri)
        with engine.connect() as conn:
            print("--- STATUS: Database Connected Successfully! ---")
        return True
    except OperationalError as e:
        print(f"--- STATUS ERROR: Connection Failed! Details: {e} ---")
        raise RuntimeError(f"Database connection failed: {e}")