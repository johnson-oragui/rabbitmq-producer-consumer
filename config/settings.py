from decouple import config

class Settings:
    DB_URL = str(config('DB_URL'))


settings = Settings()
