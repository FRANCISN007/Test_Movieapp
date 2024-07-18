# main.py
from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from auth import pwd_context, authenticate_user, create_access_token, get_current_user
from typing import List 
from database import engine, Base, get_db
import crud, models, schemas, auth
from loguru import logger


logger.add("app.log", rotation="500 MB", level="DEBUG")


Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI() 

@app.get("/")
def read_root():
    return {"message":"WELCOME TO MY APP OF MOVIES"}


@app.post("/Registration", response_model=schemas.User)

def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    This Session is for user Registration, fill your details below to signup
    """
    db_user = crud.get_user_by_username(db, username=user.username)
    hashed_password = pwd_context.hash(user.password)
    if db_user:
        logger.error(f"user trying to register but username entered already exist: {user.username}")
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user, hashed_password=hashed_password)
    

@app.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """
    This Session is for user to login and generate a token that expires in 30mins time
    """
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        logger.error(f"Failed login attempt for username: {form_data.username}")
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password! check your spellings or register as a new user ",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}


# Movie endpoints
@app.post("/movies/", response_model=schemas.Movie, status_code =401)
def create_new_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db), current_user: models.User = Depends(auth.get_current_user)):
    """
    This is the Movie creation plaform, enter the movie information below
    """
    logger.info(f"User {current_user.username} creating a movie: {movie.title}")
    return crud.create_movie(db=db, movie=movie, user_id=current_user.id)

@app.get("/movies/", response_model=List[schemas.Movie])
def list_all_movies(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    
    """
    This endpoint lists all available Movies created by all user
    """
    
    logger.info("Fetching list of movies")
    return crud.get_movies(db=db, skip=skip, limit=limit)

# Read User Movies
@app.get("/movies/me", response_model=list[schemas.Movie])
def list_my_movies(skip: int = 0, limit: int = 10, current_user: models.User = Depends(auth.get_current_user), db: Session = Depends(get_db)):
    """
    This endpoint lists all Movies created by the current user
    """
    movies = crud.get_user_movies(db, user_id=current_user.id)
    logger.info(f"Fetching only the list of movie(s) created by the user_id:{current_user.id}")
    return movies

@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie(movie_id: int, db: Session = Depends(get_db)):
    
    """
    This endpoint views one Movie at a time using the movie_id
    """
    movie = crud.get_movie_by_id(db=db, movie_id=movie_id)
    if movie is None:
        logger.warning(f"Movie not found with id: {movie_id}")
        raise HTTPException(status_code=404, detail=f"Movie_id {movie_id} does not exist, Please try another movie_id")
    logger.info(f"Fetching details for movie id: {movie_id}, {movie.title}")   
    return movie



@app.put("/movies/{movie_id}", response_model=schemas.Movie)
def update_movie(movie_id: int, movie: schemas.MovieUpdate, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    This platform updates Movies created by the user using the Movie_id
    """
    
    existing_movie = crud.get_movie_by_id(db=db, movie_id=movie_id)
    if existing_movie is None:
        logger.warning(f"Movie not found with id: {movie_id}")
        raise HTTPException(status_code=404, detail=f"Movie_id {movie_id} does not exist, Please try another movie_id")
    if existing_movie.owner_id != current_user.id:
        logger.warning(f"User {current_user.username} is not authorized to update movie: {movie.title}")
        raise HTTPException(status_code=403, detail="We are sorry, you are not authorized to update this movie")
    logger.info(f"Updating movie details: {movie.title}")
    return crud.update_movie(db=db, movie_id=movie_id, movie=movie)
    
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int, db: Session = Depends(get_db), current_user: models.User = Depends(get_current_user)):
    """
    This endpoint allows the user to Delete its own created movie
    """
    
    existing_movie = crud.get_movie_by_id(db=db, movie_id=movie_id)
    if existing_movie is None:
        logger.warning(f"Movie not found with id: {movie_id}")
        raise HTTPException(status_code=404, detail=f"Movie_id {movie_id} does not exist, Please try another movie_id")
    if existing_movie.owner_id != current_user.id:
        logger.warning(f"User {current_user.username} is not authorized to delete movie_id: {movie_id}")
        raise HTTPException(status_code=403, detail=f"You are not authorized to delete movie_id {movie_id}; you can only delete movie you created")
    
     # Check if there are related ratings or comments
    if crud.get_ratings_for_movie(db=db, movie_id=movie_id):
        logger.warning(f"trying to delete Movie {movie_id} with rating or comments, but operation aborted")
        raise HTTPException(status_code=400, detail=f"You cannot delete movie_id {movie_id} with existing ratings or comments")
    if crud.get_comments_for_movie(db=db, movie_id=movie_id):
        raise HTTPException(status_code=400, detail=f"You cannot delete movie_id {movie_id} with existing ratings or comments")
    
    crud.delete_movie(db=db, movie_id=movie_id)
    logger.info(f"Deleting movie details: {movie_id}")
    return {"message": "Movie deleted successfully"}

# Rating endpoints
@app.post("/movies/{movie_id}/rate/", response_model=schemas.Rating)
def rate_movie(movie_id: int, rating: schemas.RatingCreate, db: Session = Depends(get_db)):
    
    """
    This endpoint allows the public to rate any movie using the movie_id
    """
    movie = crud.get_movie_by_id(db=db, movie_id=movie_id)
    if movie is None:
        logger.warning(f"Movie not found with id: {movie_id}")
        raise HTTPException(status_code=404, detail=f"Movie_id {movie_id} does not exist, Please try again")
    db_rating = crud.create_rating(db=db, rating=rating, movie_id=movie_id)
    logger.info(f"Rating movie details: {movie.title}, {rating}")
    return db_rating

@app.get("/movies/{movie_id}/ratings/", response_model=List[schemas.Rating])
def get_ratings_for_movie(movie_id: int, db: Session = Depends(get_db)):
    
    """
    This endpoint allows the public to view the rated movie using the movie_id
    """
    movie = crud.get_movie_by_id(db=db, movie_id=movie_id)
    if movie is None:
        logger.warning(f"Movie not found with id: {movie_id}")
        raise HTTPException(status_code=404, detail=f"Movie_id {movie_id} does not exist, Please try again")
    logger.info(f"Fetching ratings for movie:{movie.id}, {movie.title}")
    return crud.get_ratings_for_movie(db=db, movie_id=movie_id)

# Comment endpoints
@app.post("/movies/{movie_id}/comments/", response_model=schemas.Comment)
def create_comment(movie_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    
    """
    This endpoint allows the public to comment on any movie using the movie_id
    """
    movie = crud.get_movie_by_id(db=db, movie_id=movie_id)
    if movie is None:
        logger.warning(f"Movie not found with id: {movie_id}")
        raise HTTPException(status_code=404, detail=f"Movie_id {movie_id} does not exist, Please try again")
    db_comment = crud.create_comment(db=db, comment=comment, movie_id=movie_id)
    logger.info(f"Commenting on movie: {movie.id}, {movie.title}")
    return db_comment

@app.get("/movies/{movie_id}/comments/", response_model=List[schemas.Comment])
def get_comments_for_movie(movie_id: int, db: Session = Depends(get_db)):
    
    """
    This endpoint allows the public to view comments attached to any movie using the movie_id
    """
    movie = crud.get_movie_by_id(db=db, movie_id=movie_id)
    if movie is None:
        logger.warning(f"Movie not found with id: {movie_id}")
        raise HTTPException(status_code=404, detail=f"Movie_id {movie_id} does not exist, Please try again")
    logger.info(f"Fetching comments for movie:{movie.id}, {movie.title}")
    return crud.get_comments_for_movie(db=db, movie_id=movie_id)