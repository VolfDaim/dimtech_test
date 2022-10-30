from sanic_envconfig import EnvConfig


class Settings(EnvConfig):
    DEBUG: bool = True
    HOST: str = '0.0.0.0'
    PORT: int = 5432
    DB_URL: str = 'postgresql://postgres:123@localhost:5432/postgres'
