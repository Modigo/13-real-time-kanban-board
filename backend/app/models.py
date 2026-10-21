"""
Persistence models — owned by Member 2 per Team Build Guide.

Member 1 imports these models in routes.py / schemas.py but does
not redefine them.
"""
from sqlalchemy import Column, String, Integer, Text, DateTime, ForeignKey
from sqlalchemy.sql import func
import uuid
from .database import Base

class BoardColumn(Base):
    __tablename__ = "board_columns"

    id = Column(String, primary_key=True)  # todo | doing | done
    title = Column(String, nullable=False)
    position = Column(Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<BoardColumn id={self.id} title={self.title}>"

class Card(Base):
    __tablename__ = "cards"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True, default="")
    column_id = Column(String, ForeignKey("board_columns.id"), nullable=False)
    position = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    def __repr__(self):
        return f"<Card id={self.id} title={self.title} column={self.column_id}>"

class Activity(Base):
    __tablename__ = "activities"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    action = Column(String, nullable=False)  # created | moved
    card_id = Column(String, nullable=False)
    card_title = Column(String, nullable=False)
    from_column = Column(String, nullable=True)
    to_column = Column(String, nullable=False)
    message = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    def __repr__(self):
        return f"<Activity {self.action} {self.card_title}>"
