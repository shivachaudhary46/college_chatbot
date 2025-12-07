from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str 
    SECRET_KEY: str
    ALGO: str = "HS256"
    ACCESS_TOKEN_EXPIRE: int = 30 # minutes
    ENVIRONMENT: str = "developement"
    DEBUG: bool = False
    FRONTEND_URL: str

    google_api_key: str | None = None 
    pinecone_api_key: str | None = None 

    model_config = {
        "extra": "allow",
        "env_file": ".env"
    }

settings = Settings() 
