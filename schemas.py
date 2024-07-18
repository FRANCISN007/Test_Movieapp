# schemas.py
from pydantic import BaseModel
from typing import List, Optional

class UserBase(BaseModel):
    username: str
    full_name: str
    
class UserCreate(UserBase):
    
    email: str
    password: str

class User(UserBase):
    id: int

    class Config:
        orm_mode = True

class MovieBase(BaseModel):
    title: str
    description: Optional[str]= None
    genres: Optional[str]= None
    writer: Optional[str]= None
    director: Optional[str]= None
    cast: str
    language: Optional[str]= None
    Runtime: Optional[str]= None
    year_released: int
    

class Movie(MovieBase):
    id: int
    owner_id: int
    

    class Config:
        orm_mode = True

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass


class RatingBase(BaseModel):
    stars: int

class RatingCreate(RatingBase):
    pass

class Rating(RatingBase):
    id: int
    movie_id: int


    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    comment: str

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    movie_id: int

    class Config:
        orm_mode = True
        

