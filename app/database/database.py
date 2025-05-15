from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import Annotated
from fastapi import Depends

db_url = 'sqlite+aiosqlite:///test.db'
async_engine = create_async_engine(url=db_url, echo=True)
async_session = async_sessionmaker(bind=async_engine, expire_on_commit=False)
async def get_async_session()->AsyncSession:
    async with async_session() as session:
        yield session
SessionDep = Annotated[AsyncSession, Depends(get_async_session)]


