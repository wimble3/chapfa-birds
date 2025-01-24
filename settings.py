import os


def load_env_file(dotenv_path: str, override: bool = False) -> None:
    with open(dotenv_path) as file_obj:
        lines = file_obj.read().splitlines()

    dotenv_vars = {}
    for line in lines:
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", maxsplit=1)
        dotenv_vars.setdefault(key, value)

    if override:
        os.environ.update(dotenv_vars)
    else:
        for key, value in dotenv_vars.items():
            os.environ.setdefault(key, value)


CURRENT_FILE_PATH = os.path.abspath(__file__)
BASE_DIR = os.path.dirname(CURRENT_FILE_PATH)
load_env_file(os.path.join(BASE_DIR, ".env"))


class Settings:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI")
    HOST = os.getenv("HOST")
    PORT = int(os.getenv("PORT"))
    DEBUG = bool(os.getenv("DEBUG"))
    TEMPLATE_PREFIX = os.getenv("TEMPLATE_PREFIX")

    BIRDS_ITEMS_PER_PAGE = int(os.getenv("BIRDS_ITEMS_PER_PAGE"))
