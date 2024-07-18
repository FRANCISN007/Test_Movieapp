
# crud.py
from sqlalchemy.orm import Session
import models, schemas, auth
from models import User, Movie
from schemas import UserCreate

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
    #return {"message": "Movie created successfully!", "data": db_movie}

def get_movies(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Movie).offset(skip).limit(limit).all()

# Read User Movies
def get_user_movies(db: Session, user_id: int):
    return db.query(models.Movie).filter(models.Movie.owner_id == user_id).all()

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

def create_comment(db: Session, comment: schemas.CommentCreate, movie_id: int):
    db_comment = models.Comment(**comment.dict(), movie_id=movie_id)
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

def get_comments_for_movie(db: Session, movie_id: int):
    return db.query(models.Comment).filter(models.Comment.movie_id == movie_id).all()

def create_rating(db: Session, rating: schemas.RatingCreate, movie_id: int):
    db_rating = models.Rating(**rating.dict(), movie_id=movie_id)
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

def get_ratings_for_movie(db: Session, movie_id: int):
    return db.query(models.Rating).filter(models.Rating.movie_id == movie_id).all()




