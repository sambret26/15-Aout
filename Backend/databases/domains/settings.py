from sqlalchemy import Column, Integer, String
from databases.base import Base

class Settings(Base):
    __tablename__ = 'Settings'
    id = Column(Integer, primary_key=True)
    data = Column(String, nullable=False)
    state = Column(Integer)