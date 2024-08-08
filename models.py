# models.py
from sqlalchemy import Column, Integer, String, Float, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String)
    email = Column(String, nullable=False, unique=True)
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
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
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="movies")
    comments = relationship("Comment", back_populates="movie")
    ratings = relationship("Rating", back_populates="movie")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    rating = Column(Float, nullable=False)
    
    movie_id = Column(Integer, ForeignKey("movies.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    movie = relationship("Movie", back_populates="ratings")
    
    __table_args__ = (UniqueConstraint('user_id', 'movie_id', name='unique_user_movie_rating'),)
    
#class Rating(Base):
    #__tablename__ = "ratings"

    #user_id = Column(Integer, ForeignKey ("users.id", ondelete = "CASADE"), primary_key=True)
    #movie_id = Column(Integer, ForeignKey ("movies.id", ondelete = "CASADE"), primary_key=True)
    
    #rating = Column(Float)
    
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    comment = Column(String)
    movie_id = Column(Integer, ForeignKey("movies.id"))
    time_created = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    

    movie = relationship("Movie", back_populates="comments")

