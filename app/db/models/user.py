from __future__ import annotations

from aiogram.enums import ChatMemberStatus
from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession

from ._abc import AbstractModel


class UserDB(AbstractModel):
    """
    Model representing User table.
    """
    __tablename__ = "users"

    id = Column(
        BigInteger,
        primary_key=True,
        nullable=False,
    )
    state = Column(
        VARCHAR(length=6),
        nullable=False,
        default=ChatMemberStatus.MEMBER,
    )
    full_name = Column(
        VARCHAR(length=128),
        nullable=False,
    )
    username = Column(
        VARCHAR(length=65),
        nullable=True,
    )
    language_code = Column(
        VARCHAR(length=2),
        nullable=True,
    )
    created_at = Column(
        DateTime,
        default=func.now(),
        nullable=False,
    )

    wallet_address = Column(
        VARCHAR(length=48),
        nullable=True
    )
    nickname = Column(
        VARCHAR(length=65),
        nullable=True,
    )
    github_username = Column(
        VARCHAR(length=65),
        nullable=True,
    )
    codeforces_username = Column(
        VARCHAR(length=65),
        nullable=True,
    )
    github_token = Column(
        VARCHAR(length=36),
        nullable=True,
    )
