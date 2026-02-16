from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    postgres_db: str = "threat_modeling"
    postgres_user: str = "tm_user"
    postgres_password: str = "tm_pass"
    postgres_port: int = 5432

    asset_service_port: int = 8001
    threat_engine_port: int = 8002
    ml_service_port: int = 8003

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()
