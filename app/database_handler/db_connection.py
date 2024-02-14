from sqlalchemy.ext.asyncio import (
    create_async_engine,
    async_sessionmaker,
    AsyncSession,
    AsyncEngine,
)

DB_NAME = "gonito-test"
DB_USER = "user-test"
DB_PASS = "secret-test"
DB_HOST = "db"
DB_PORT = "5432"
DB_CONNECTION_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME
)

def get_engine() -> AsyncEngine:
    engine = create_async_engine(
        DB_CONNECTION_URL,
        echo=True,
    )
    return engine

def get_session(engine: AsyncEngine) -> AsyncSession:
    async_session = async_sessionmaker(engine, expire_on_commit=True)
    return async_session