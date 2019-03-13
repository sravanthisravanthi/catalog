import sys
import os
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy import create_engine
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(200), nullable=False)
    email = Column(String(200), nullable=False)
    picture = Column(String(300))


class FilmCategoryName(Base):
    __tablename__ = 'filmcategoryname'
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="filmcategoryname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'name': self.name,
            'id': self.id
        }


class FilmName(Base):
    __tablename__ = 'filmname'
    id = Column(Integer, primary_key=True)
    moviename = Column(String(150), nullable=False)
    year = Column(String(50))
    rating = Column(String(50))
    action = Column(String(50))
    budget = Column(String(20))
    date = Column(DateTime, nullable=False)
    filmcategorynameid = Column(Integer, ForeignKey('filmcategoryname.id'))
    filmcategoryname = relationship(
        FilmCategoryName, backref=backref('filmname', cascade='all, delete'))
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User, backref="filmname")

    @property
    def serialize(self):
        """Return objects data in easily serializeable formats"""
        return {
            'moviename': self. moviename,
            'year': self. year,
            'rating': self. rating,
            'action': self. action,
            'budget': self. budget,
            'date': self. date,
            'id': self. id
        }

engin = create_engine('sqlite:///films.db')
Base.metadata.create_all(engin)
