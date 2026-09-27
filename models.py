from sqlalchemy import Column, Integer, String, Float
from database import Base


class Pedido(Base):

    __tablename__ = "pedidos"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )

    total = Column(
        Float,
        nullable=False
    )

    status = Column(
        String,
        default="pendente"
    )