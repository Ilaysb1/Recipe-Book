import pytest
from main import app
import mongomock
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def mock_db():
    with patch('main.MongoClient', return_value=mongomock.MongoClient()):
        yield

def test_index(client):
    response = client.get('/')
    assert b'Welcome to Recipe Management System' in response.data

def test_register(client):
    # Ensure the test user does not already exist
    with patch('main.MongoClient', return_value=mongomock.MongoClient()):
        db = mongomock.MongoClient().db
        existing_user = db.users.find_one({'username': 'testuser'})
        if existing_user:
            db.users.delete_one({'username': 'testuser'})

    # Perform the registration
    response = client.post('/register', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)

    # Assert the response contains the error message
    assert b'Username already exists. Please choose a different one.' in response.data

    # Clean up by removing the test user
    with patch('main.MongoClient', return_value=mongomock.MongoClient()):
        db = mongomock.MongoClient().db
        test_user = db.users.find_one({'username': 'testuser'})
        if test_user:
            db.users.delete_one({'username': 'testuser'})
            
def test_login(client):
    response = client.post('/login', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)
    assert b'Welcome to the Dashboard, testuser' in response.data

def test_dashboard(client):
    # Log in first
    client.post('/login', data={'username': 'testuser', 'password': 'password123'}, follow_redirects=True)
    
    # Now access the dashboard
    response = client.get('/dashboard')
    
    # Assert the response
    assert b'Welcome to the Dashboard, testuser' in response.data

def test_recipe_entering(client):
    response = client.post('/recipe_entering', data={'recipe_name': 'Test Recipe', 'recipe_time': '30',
                                                     'recipe_description': 'Test Description', 'difficulty': 'beginner',
                                                     'ingredients': 'Ingredient 1, Ingredient 2'},
                           follow_redirects=True)
    assert b'Test Recipe' in response.data

def test_recipe_book(client):
    response = client.get('/recipe_book')
    assert b'Recipe Book' in response.data



def test_result(client):
    response = client.get('/result/Test%20Recipe')
    assert b'Test Recipe' in response.data

def test_edit_recipe(client):
    response = client.get('/edit/Test%20Recipe')
    assert b'Edit Recipe' in response.data