from sqlalchemy import Column, Integer, String, DateTime, Boolean
from database import db


class Meal(db.Model):
    __tablename__ = 'meals'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String(255), nullable=True)
    date_time = Column(DateTime, nullable=True)
    is_within_diet = Column(Boolean, nullable=True, default=True)

    def __repr__(self):
        return f"<Meal(name={self.name}, date_time={self.date_time}, is_within_diet={self.is_within_diet})>"
