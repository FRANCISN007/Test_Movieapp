# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String)
    email = Column(String)
    hashed_password = Column(String, nullable=False)
    
    movies = relationship("Movie", back_populates="owner")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    genres= Column(String)
    writer= Column(String)
    director= Column(String)
    cast= Column(String)
    language=  Column(String)
    Runtime=  Column(String)
    year_released = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="movies")
    comments = relationship("Comment", back_populates="movie")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    stars = Column(Integer)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    

class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    movie_id = Column(Integer, ForeignKey("movies.id"))

    movie = relationship("Movie", back_populates="comments")
