from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy import URL

# 프로젝트 루트. .env 경로를 절대경로로 잡아야
# 어느 디렉터리에서 실행하든 설정을 찾을 수 있다.
BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    """애플리케이션 설정.

    .env 파일 또는 OS 환경변수에서 값을 읽어 검증한다.
    Spring의 application.yml + @ConfigurationProperties 에 해당한다.
    필드명 db_host 는 환경변수 DB_HOST 와 대응된다(대소문자 무시).
    """

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",  # .env에 모르는 키가 있어도 무시
    )

    # --- Database ---
    db_host: str = "localhost"
    db_port: int = 3306
    db_user: str
    db_password: str
    db_name: str

    # --- Connection Pool ---
    db_pool_size: int = Field(10, ge=1)
    db_max_overflow: int = Field(0, ge=0)
    db_pool_recycle: int = Field(300, ge=-1)
    db_echo: bool = False

    @property
    def database_url(self) -> URL:
        """SQLAlchemy 접속 URL.

        URL.create() 는 비밀번호에 들어간 특수문자(@ : / 등)를
        자동으로 이스케이프한다. f-string 으로 직접 조립하면
        비밀번호에 @ 하나만 있어도 접속이 깨진다.
        """
        return URL.create(
            drivername="mysql+pymysql",
            username=self.db_user,
            password=self.db_password,
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
        )


@lru_cache
def get_settings() -> Settings:
    """설정 싱글턴. 라우터에서는 Depends(get_settings) 로 주입받을 수 있다."""
    return Settings()


settings = get_settings()
