from sqlalchemy import Column, Integer, String
from storage.db.database import Base

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key = True, index=True)
    description = Column(String, nullable=False)
    status = Column(String, default="todo")  # Possible values: "todo", "in-progress", "done"
    createdAt = Column(String)
    updatedAt = Column(String)
