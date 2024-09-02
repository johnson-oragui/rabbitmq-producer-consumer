from decouple import config

class Settings:
    DB_URL = str(config('DB_URL'))
    MAIL_USERNAME = str(config('MAIL_USERNAME'))
    MAIL_PASSWORD = str(config('MAIL_PASSWORD'))
    MAIL_SERVER = str(config('MAIL_SERVER'))
    MAIL_PORT = str(config('MAIL_PORT'))


settings = Settings()
