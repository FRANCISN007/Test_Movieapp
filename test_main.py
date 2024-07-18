import json
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from main import app, get_db
from database import SessionLocal, engine
from models import Base, User, Movie, Rating, Comment
import crud

# Create a test client using TestClient
client = TestClient(app)

# Override database dependency for testing
def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message":"WELCOME TO MY APP OF MOVIES"}

# Set up and tear down for tests
def setup_module(module):
    Base.metadata.create_all(bind=engine)

def teardown_module(module):
    Base.metadata.drop_all(bind=engine)

# Test cases for each endpoint
def test_signup():
    # Test successful registration PASSEDXXX
    user = {
        "username": "testuser",
        "full_name": "fcn",
        "password": "testpassword",
        "email": "test@example.com"
    }
    response = client.post("/Registration", json=user)
    assert response.status_code == 200
    assert response.json()["username"] == user["username"]

    # Test duplicate registration
    response = client.post("/Registration", json=user)
    assert response.status_code == 400 

def test_login():
    # Test successful login
    login_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    response = client.post("/login", data=login_data)
    assert response.status_code == 200
    assert "access_token" in response.json()

    # Test invalid login
    user = {
        "username": "testuser",
        "password": "wrongpassword"
    }
    response = client.post("/login", data=user)
    assert response.status_code == 401 
    response_data = response.json()
    assert "detail" in response_data
    

def test_read_movies():
    response = client.get("/movies/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_rate_movie():
    # Assuming movie_id exists in the database
    movie_id = 2
    rating_data = {
        "user_id": 1,
        "stars": 5,
        #"comment": "Great movie!"
    }
    response = client.post(f"/movies/{movie_id}/rate/", json=rating_data)
    assert response.status_code == 404
    rating_response = response.json()
    
    assert rating_response ["stars"]== rating_data ["stars"]
    #assert rating_response["comment"] == rating_data["comment"]
    assert rating_response["movie_id"] == movie_id
