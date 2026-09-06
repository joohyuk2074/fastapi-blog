from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool

from core.config import settings

# 접속 정보는 .env 에서 읽는다 (core/config.py 참고)
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    poolclass=QueuePool,
    pool_size=settings.db_pool_size,
    max_overflow=settings.db_max_overflow,
    pool_recycle=settings.db_pool_recycle,
)


def direct_get_conn():
    conn = None
    try:
        conn = engine.connect()
        return conn
    except SQLAlchemyError as e:
        print(e)
        raise e
