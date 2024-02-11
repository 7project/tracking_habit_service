from pathlib import Path
from envparse import Env

env = Env()
env.read_envfile()

DB_HOST = env("DB_HOST")
DB_PORT = env("DB_PORT")
DB_NAME = env("DB_NAME")
DB_USER = env("DB_USER")
DB_PASS = env("DB_PASS")

DATABASE_URL = env("DATABASE_URL")

path_private_key: Path = Path(__file__).parent / "cert" / "jwt-private.pem"
path_public_key: Path = Path(__file__).parent / "cert" / "jwt-public.pem"
algorithm = "RS256"
expire_minutes = 35
# expire_timedelta = 5
