import asyncio

from src.core.config import settings
from src.database.base_model import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker, AsyncEngine
from loguru import logger

async_engine: AsyncEngine = create_async_engine(settings.DB_URL, echo=True)
AsyncSessionLocal = async_sessionmaker(async_engine, expire_on_commit=False, class_=AsyncSession)

async def init_db():
    from src.database.models import Product
    async with async_engine.begin() as connection:
        await connection.run_sync(BaseModel.metadata.create_all)

SessionLocal = async_sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=async_engine
)

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            logger.info(f'подключено к {session}')
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
            logger.info(f'отключено от {session}')

async def main():
    await init_db()

if __name__ == '__main__':
    asyncio.run(main())
