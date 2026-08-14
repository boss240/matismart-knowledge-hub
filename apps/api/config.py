from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="", env_file=".env", extra="ignore")

    matismart_env: str = "local"
    database_url: str = "postgresql+psycopg://matismart:matismart_local_only@localhost:5432/matismart_knowledge"
    api_key: str | None = None


settings = Settings()
