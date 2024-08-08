# schemas.py
from pydantic import BaseModel, EmailStr, conint
from typing import List, Optional
from datetime import datetime


    
class UserResponse(BaseModel):
    id: int 
    username: str
    full_name: str
    email: EmailStr
    
class UserRating(BaseModel):
    id: int 
    #username: str
    #full_name: str
    #email: EmailStr    
 
class UserBase(BaseModel):
    username: str
    full_name: str  
        
    
class UserCreate(UserBase):
    email: EmailStr
    password: str

class User(UserBase): 
    email: EmailStr
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
    time_created: datetime
    owner: UserResponse
    

    class Config:
        orm_mode = True

class MovieCreate(MovieBase):
    pass

class MovieUpdate(MovieBase):
    pass

    
class MovieResponse(BaseModel):
    title: str
    description: str
    average_rating: Optional[float]
    
 
class Rate(BaseModel):
    movie_id: int
    #dir: conint(le=1)
    rating: float
     
 
    
class RatingResponse(BaseModel):
    user_id: int
    username: str
    title: str
    
    rating: float

class RatingBase(BaseModel):
    rating: float

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
    time_created: datetime

    class Config:
        orm_mode = True
        

