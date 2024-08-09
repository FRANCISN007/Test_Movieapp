# schemas.py
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime


    
class UserResponse(BaseModel):
    id: int 
    username: str
    full_name: str
    email: EmailStr
    
class UserRating(BaseModel):
    id: int 
    username: str
    full_name: str
    
class UserComment(BaseModel):
    id: int 
    username: str
    full_name: str   
       
    
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



class RatingBase(BaseModel):
    rating: float
    
class Rate(BaseModel):
    rating: float
    
     
class Rating(Rate):
    id: int
    movie_id: int
    created_by: UserRating
    
class RatingResponse(BaseModel):
    user_id: int
    username: str
    title: str
    
    rating: float

    

class RatingCreate(RatingBase):
    pass
    

    class Config:
        orm_mode = True

class CommentBase(BaseModel):
    comment: str
    
    
class Comment(CommentBase):
    id: int
    movie_id: int
    time_created: datetime
    posted_by: UserComment
    
    
    class Config:
        orm_mode = True

class CommentCreate(CommentBase):
    pass



    
