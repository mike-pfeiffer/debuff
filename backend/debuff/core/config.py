from starlette.config import Config


API_PREFIX = "/api"
VERSION = "0.0.0"

config = Config(".env")

DEBUG: bool = config("DEBUG", cast=bool, default=False)

PROJECT_NAME: str = config("Debuff", default="Debuff")
