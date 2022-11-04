from sanic_envconfig import EnvConfig


default_settings = {
    'DEBUG': 'True',
    'HOST': '0.0.0.0',
    'PORT': '5432',
    'DB_URL': 'postgresql://postgres:123@localhost:5432/postgres',
}