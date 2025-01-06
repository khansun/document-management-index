from pathlib import Path
from functools import lru_cache
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    papermerge__search__url: str
    papermerge__redis__url: str | None = None
    papermerge__main__logging_cfg: Path | None = Path("/app/i3worker/logging.yaml")
    papermerge__database__url: str = 'sqlite:////db/db.sqlite3'


@lru_cache()
def get_settings():
    return Settings()

