import os
from dotenv import load_dotenv
from pathlib import Path 



BASE_DIR = Path(os.getcwd())
ENV_FILE = os.path.join(BASE_DIR,'.env')

load_dotenv(dotenv_path=ENV_FILE)

class Settings_database: 
    PROJECT_NAME:str = "IA-MEDICINE"
    PROJECT_VERSION:str = "1.0"
    POSTGRESS_DB:str =  os.getenv('POSTGRES_DB')
    POSTGRES_USER:str = os.getenv('POSTGRES_USER')
    POSTGRES_PASSWORD:str = os.getenv("POSTGRES_PASSWORD")
    POSTGRES_SERVER:str = os.getenv("POSTGRES_SERVER")
    POSTGRES_PORT:str = os.getenv("POSTGRES_PORT")
    POSTGRES_SSLMODE:str = os.getenv("POSTGRES_SSLMODE")
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRESS_DB}?{POSTGRES_SSLMODE}"
    # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRESS_DB}"

settings = Settings_database()


