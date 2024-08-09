# crud.py
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
import models, schemas
from typing import Optional
from sqlalchemy.orm import Session
from models import Rating


def create_user(db: Session, user: schemas.UserCreate, hashed_password: str):
    db_user = models.User(
        username=user.username, 
        full_name=user.full_name, 
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_movie(db: Session, movie: schemas.MovieCreate, user_id: int):
    db_movie = models.Movie(**movie.dict(), owner_id=user_id)
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie
    
def get_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Movie).offset(skip).limit(limit).all()

# Read User Movies
def get_user_movies(db: Session, user_id: int):
    return db.query(models.Movie).filter(models.Movie.owner_id == user_id).all()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_movie_by_id(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def update_movie(db: Session, movie_id: int, movie: schemas.MovieUpdate):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    if db_movie:
        for var, value in vars(movie).items():
            setattr(db_movie, var, value)
        db.commit()
        db.refresh(db_movie)
    return db_movie

def delete_movie(db: Session, movie_id: int):
    db.query(models.Movie).filter(models.Movie.id == movie_id).delete()
    db.commit()

def create_comment(db: Session, comment: schemas.CommentCreate, movie_id: int, user_id: int):
    db_comment = models.Comment(**comment.dict(), movie_id=movie_id, )
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_for_movie(db: Session, movie_id: int):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()

def get_comment_by_id(db: Session, comment_id: int):
    return db.query(models.Comment).filter(models.Comment.id == comment_id).first()

def delete_comment(db: Session, comment_id: int):
    db_comment = db.query(models.Comment).filter(models.Comment.id == comment_id).first()
    if db_comment:
        db.delete(db_comment)
        db.commit()


def create_rating(db: Session, rating: schemas.RatingCreate, movie_id: int, user_id: int):
    # Check if the user has already rated this movie
    existing_rating = db.query(models.Rating).filter(models.Rating.movie_id == movie_id, models.Rating.user_id == user_id).first()
    
    if existing_rating:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"You have already rated movie_id {movie_id}")
    
     # Check if the rating is within the acceptable range
    if rating.rating < 0 or rating.rating > 5:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=f"{rating} is invalid, Rating range should be from 0 to 5")
       
    new_rating = Rating(movie_id=movie_id, user_id=user_id, rating=rating.rating)
    db.add(new_rating)
    db.commit()
    db.refresh(new_rating)
    return new_rating
    


def get_ratings_for_movie(db: Session, movie_id: int):
   return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()
   



 