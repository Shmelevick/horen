from typing import Annotated

from fastapi import Depends, HTTPException, Path, status
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product as ProductORM
from core.models import db_helper

from . import crud


async def product_by_id(
    product_id: Annotated[int, Path], session: AsyncSession = Depends(db_helper.get_scoped_session)
) -> ProductORM:
    product = await crud.get_product(session=session, product_id=product_id)
    if product:
        return product

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Product {product_id} not found!",
    )