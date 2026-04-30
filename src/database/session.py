from src.config import settings
from src.database.models import Base
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine

async_engine: AsyncEngine = create_async_engine(settings.DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    async with async_engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

