import os
from dotenv import load_dotenv
from pathlib import Path 

print(os.getcwd())

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
    DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRESS_DB}?sslmode=verify-full&sslrootcert=/certs/global-bundle.pem"
    # DATABASE_URL = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}:{POSTGRES_PORT}/{POSTGRESS_DB}"

settings = Settings_database()


print(ENV_FILE)