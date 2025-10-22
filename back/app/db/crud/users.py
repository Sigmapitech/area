from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from ...services.auth import hash_password
from ..models.user import User


async def get_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Fetch a user by email.

    Args:
        db (AsyncSession): Database session
        email (str): User email

    Returns:
        User | None: User instance if found, else None
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()


async def get_by_id(db: AsyncSession, user_id: int) -> User | None:
    """
    Fetch a user by ID.

    Args:
        db (AsyncSession): Database session
        user_id (int): User ID

    Returns:
        User | None: User instance if found, else None
    """
    result = await db.execute(select(User).where(User.id == user_id))
    return result.scalar_one_or_none()


async def create_user(
    db: AsyncSession, *, email: str, password: str, name: str
) -> User:
    """
    Create a new user.

    Args:
        db (AsyncSession): Database session
        email (str): User email
        password (str): Plain text password
        name (str): User's full name

    Returns:
        User: Newly created user instance
    """
    hashed_password = hash_password(password)
    user = User(email=email, auth=hashed_password, name=name)
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


async def list_users(
    db: AsyncSession, skip: int = 0, limit: int = 100
) -> Sequence[User]:
    """
    List users with optional pagination.

    Args:
        db (AsyncSession): Database session
        skip (int): Offset for pagination
        limit (int): Max number of users to return

    Returns:
        list[User]: List of user instances
    """
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def update_user(db: AsyncSession, user: User, data: dict):
    for key, value in data.items():
        if key == "password":
            hash = hash_password(value)
            setattr(user, "auth", hash)
        else:
            setattr(user, key, value)
    await db.commit()
    await db.refresh(user)
    return user
