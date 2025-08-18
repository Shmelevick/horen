"""
CRUD
"""
from icecream import ic


from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.ext.asyncio import AsyncSession

from core.models import Product as ProductORM

from .schemas import Product, ProductCreate, ProductUpdate, ProductUpdatePartial


async def get_products(session: AsyncSession) -> list[ProductORM]:
    stmt = select(ProductORM).order_by(ProductORM.id)
    result: Result = await session.execute(stmt)
    products = result.scalars().all()
    return list(products)


async def get_product(session: AsyncSession, product_id: int) -> ProductORM | None:
    return await session.get(ProductORM, product_id)


async def create_product(session: AsyncSession, product_in: ProductCreate) -> ProductORM:
    product = ProductORM(**product_in.model_dump())
    session.add(product)
    await session.commit()
    # await session.refresh
    return product


async def update_product(
    session: AsyncSession,
    product: ProductORM,
    product_update: ProductUpdate | ProductUpdatePartial,
    partial: bool = False,
) -> ProductORM:
    for name, value in product_update.model_dump(exclude_unset=partial).items():
        ic(locals())
        setattr(product, name, value)
    await session.commit()
    await session.refresh(product)
    return product


async def delete_product(
        session: AsyncSession,
        product: Product,
) -> None:
    await session.delete(product)
    await session.commit()
