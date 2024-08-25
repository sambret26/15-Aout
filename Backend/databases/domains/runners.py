from sqlalchemy import Column, Integer, String, CheckConstraint
from databases.base import Base

class Runners(Base):
    __tablename__ = 'Runners'
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    sex = Column(String, nullable=False)
    ranking = Column(Integer)
    category = Column(String, nullable=False)
    category_ranking = Column(Integer)
    sex_ranking = Column(Integer)
    bib_number = Column(Integer)
    time = Column(String)
    oriol = Column(Integer, CheckConstraint('oriol IN (0, 1)'))