from sqlalchemy import String, Integer, ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, relationship, mapped_column, Mapped
from sqlalchemy.dialects.postgresql import UUID
import uuid
from typing import List

class Base(DeclarativeBase):
    pass

class Player(Base):
     __tablename__ = "players"
     id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
     username: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
     gold: Mapped[str] = mapped_column(Integer, default=0)
     inventory_entries: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="player")

class Item(Base):
     __tablename__ = "items"

     id: Mapped[int] = mapped_column(primary_key=True)
     name: Mapped[str] = mapped_column(String(16), nullable=False, unique=True)
     description: Mapped[str] = mapped_column(String(64), nullable=False)
     in_inventories: Mapped[List["Inventory"]] = relationship("Inventory", back_populates="item")

class Inventory(Base):
     __tablename__ = "inventories"

     player_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("players.id"), primary_key=True)
     item_id: Mapped[int] = mapped_column(ForeignKey("items.id"), primary_key=True)
     quantity: Mapped[int] = mapped_column(Integer, nullable=False)
     player: Mapped["Player"] = relationship("Player", back_populates="inventory_entries")
     item: Mapped["Item"] = relationship("Item", back_populates="in_inventories")

     __table_args__ = (
            CheckConstraint("quantity >= 1", name="check_quantity_positive"),
        )