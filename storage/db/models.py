from sqlalchemy import Column, Integer, String
from storage.db.database import Base

from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String)
    status = Column(String)

    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)

