from typing import Any, AsyncGenerator, AsyncIterable, Iterable, List

import aioitertools
from sqlalchemy import Column, Table
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncConnection
from sqlalchemy.sql.base import ReadOnlyColumnCollection
from sqlalchemy.sql.dml import Delete, ReturningDelete

from competera_db.copy_records import copy_records_to_table


class BaseCrud:

    table: Table
    returning_default: bool = False

    def __init__(self, table: Table):
        self.table = table

    def pk_criteria(self, **kwargs) -> tuple:
        return tuple(
            pk_column == kwargs[pk]
            for pk, pk_column in self.table.primary_key.columns.items()
        )

    async def get_by_pk(self, conn: AsyncConnection, **kwargs) -> dict | None:
        query = (
            self.table.select()
            .where(*self.pk_criteria(**kwargs))
        )
        result = await conn.execute(query)
        record = result.mappings().fetchone()
        return dict(record) if record is not None else None

    async def delete_by_pk(
            self,
            conn: AsyncConnection,
            *,
            returning: bool = False,
            **kwargs,
    ) -> int | dict | None:
        result = await self.delete(
            conn,
            where_criteria=self.pk_criteria(**kwargs),
            returning=returning,
        )

        if isinstance(result, int):
            return result

        return result[0] if result else None

    async def create(
            self,
            conn: AsyncConnection,
            *,
            records: Iterable[dict],
    ) -> dict:
        insert_stmt = (
            insert(self.table)
            .values(
                [
                    {
                        k: v
                        for k, v in item.items()
                        if k in self.table.columns
                    }
                    for item in records
                ],
            )
            .returning(self.table)
        )

        result = await conn.execute(insert_stmt)
        return dict(result.fetchone())

    async def delete(
            self,
            conn: AsyncConnection,
            *,
            where_criteria: tuple | None = None,
            returning: bool = False,
    ) -> int | List[dict]:
        query: ReturningDelete | Delete
        query = self.table.delete()
        if where_criteria is not None:
            query = query.where(*where_criteria)

        if returning or self.returning_default:
            query = query.returning(*self.table.columns.values())
            result = await conn.execute(query)
            return [dict(x) for x in result.fetchall()]

        result = await conn.execute(query)
        return result.rowcount

    async def iter_records(
            self,
            conn: AsyncConnection,
            *,
            where_criteria: tuple | None = None,
            order_criteria: tuple | None = None,
    ) -> AsyncGenerator[dict, None]:
        query = self.table.select()
        if where_criteria is not None:
            query = query.where(*where_criteria)
        if order_criteria is not None:
            query = query.order_by(*order_criteria)

        async_result = await conn.stream(query)
        async for record in async_result.mappings():
            yield dict(record)

    async def list(
            self,
            conn: AsyncConnection,
            *,
            where_criteria: tuple | None = None,
            order_criteria: tuple | None = None,
    ) -> List[dict]:
        return await aioitertools.list(self.iter_records(
            conn,
            where_criteria=where_criteria,
            order_criteria=order_criteria,
        ))

    async def update(
            self,
            conn: AsyncConnection,
            *,
            where_criteria: tuple | None = None,
            **values,
    ) -> int:
        query = self.table.update()
        if where_criteria is not None:
            query = query.where(*where_criteria)

        query = query.values(**values)

        result = await conn.execute(query)
        return result.rowcount

    async def upsert(
            self,
            conn: AsyncConnection,
            *,
            records: List[dict],
    ) -> None:
        if not records:
            return

        insert_stmt = (
            insert(self.table)
            .values(
                [
                    {
                        k: v
                        for k, v in item.items()
                        if k in self.columns
                    }
                    for item in records
                ],
            )
        )