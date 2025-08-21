from sqlalchemy import Table, Column, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class OrderProductAssociation(Base):
    __tablename__ = "order_product_association"
    __table_args__ = (UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),)

    id: Mapped[int] = mapped_column(primary_key=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    count: Mapped[int] = mapped_column(default=1, server_default="1")
    # unit_price: Mapped[int] = mapped_column(default="")



# order_product_association_table = Table(
#     "order_product_association",
#     Base.metadata,

#     Column("id", Integer, primary_key=True),
#     Column("order_id", ForeignKey("orders.id"), nullable=False),
#     Column("product_id", ForeignKey("products.id"), nullable=False),
#     UniqueConstraint("order_id", "product_id", name="idx_unique_order_product"),
# )
