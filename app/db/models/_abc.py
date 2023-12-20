from __future__ import annotations

import typing as t

from sqlalchemy import *
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import InstrumentedAttribute

from ._base import Base

T = t.TypeVar("T", bound="AbstractModel")


class AbstractModel(Base):
    """Base class for all models."""

    __abstract__ = True
    __allow_unmapped__ = True

    @staticmethod
    def _get_column(
            model: t.Type[T],
            col: InstrumentedAttribute[t.Any],
    ) -> str:
        """Get the name of a column in a model."""
        name = col.name
        if name not in model.__table__.columns:
            raise ValueError(f"Column {name} not found in {model.__name__}")
        return name

    @classmethod
    def _get_primary_key(cls) -> str:
        """Return the primary key of the model."""
        return cls.__table__.primary_key.columns.values()[0].name

    @classmethod
    async def create(
            cls: t.Type[T],
            async_session: AsyncSession,
            **kwargs,
    ) -> T:
        """Create a new record in the database."""
        instance = cls(**kwargs)
        async_session.add(instance)
        await async_session.commit()
        await async_session.refresh(instance)
        return instance

    @classmethod
    async def get(
            cls: t.Type[T],
            async_session: AsyncSession,
            primary_key: int,
    ) -> T:
        """Get a record from the database by its primary key."""
        return await async_session.get(cls, primary_key)

    @classmethod
    async def get_by_key(
            cls: t.Type[T],
            async_session: AsyncSession,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
    ) -> T | None:
        """Get a record by a key."""
        statement = select(cls).filter_by(**{cls._get_column(cls, key): value})
        result = await async_session.execute(statement)
        return result.scalars().first()

    @classmethod
    async def update(
            cls: t.Type[T],
            async_session: AsyncSession,
            primary_key: int,
            **kwargs,
    ) -> T:
        """Update a record in the database by its primary key."""
        instance = await cls.get(async_session, primary_key)
        if instance:
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            await async_session.commit()
        return instance

    @classmethod
    async def update_by_key(
            cls: t.Type[T],
            async_session: AsyncSession,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
            **kwargs,
    ) -> None:
        """Update a record in the database by a key."""
        instance = await cls.get_by_key(async_session, key, value)
        if instance:
            for attr, value in kwargs.items():
                setattr(instance, attr, value)
            await async_session.commit()

    @classmethod
    async def delete(
            cls: t.Type[T],
            async_session: AsyncSession,
            primary_key: int,
    ) -> None:
        """Delete a record from the database by its primary key."""
        instance = await cls.get(async_session, primary_key)
        if instance:
            await async_session.delete(instance)
            await async_session.commit()

    @classmethod
    async def delete_by_key(
            cls: t.Type[T],
            async_session: AsyncSession,
            key: InstrumentedAttribute[t.Any],
            value: t.Any,
    ) -> None:
        """Delete a record from the database by a key."""
        instance = await cls.get_by_key(async_session, key, value)
        if instance:
            await async_session.delete(instance)
            await async_session.commit()

    @classmethod
    async def create_or_update(
            cls: t.Type[T],
            async_session: AsyncSession,
            **kwargs,
    ) -> T:
        """Get and update a record from the database by its primary key."""
        primary_key = kwargs.get(cls._get_primary_key())
        instance = await cls.get(async_session, primary_key)
        if instance:
            await cls.update(async_session, primary_key, **kwargs)
            return instance
        return await cls.create(async_session, **kwargs)
