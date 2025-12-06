from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.deps import get_session
from src.users.repository import UserRepository
from src.users.service import UserService


def get_user_repository(
	db: AsyncSession = Depends(get_session),
) -> UserRepository:
	return UserRepository(db)


def get_user_service(
	repository: UserRepository = Depends(get_user_repository),
) -> UserService:
	return UserService(repository)


UserServiceDeps = Annotated[UserService, Depends(get_user_service)]
