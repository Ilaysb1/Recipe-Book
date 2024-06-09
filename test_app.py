import pytest
from main import app
import mongomock
from unittest.mock import patch

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(scope="session", autouse=True)
def mock_db():
    with patch('main.MongoClient', return_value=mongomock.MongoClient()):
        yield mongomock.MongoClient()

def test_index(client):
    response = client.get('/')
    assert b'Welcome to Recipe Management System' in response.data

def test_register(client, cleanup_db):  # Add cleanup_db as parameter
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

    # No need for cleanup here as it's handled by cleanup_db fixture
            
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

@pytest.fixture(scope="session", autouse=True)
def cleanup_db(mock_db):
    yield  # Execute tests
    # Clean up by removing the test data
    mock_db.db.users.delete_many({'username': 'testuser'})
    # Additional cleanup if needed

def test_delete_entered_recipe(client):
    # Simulate a request to delete the recipe entered during testing
    response = client.post('/delete/Test%20Recipe')
    assert response.status_code == 302  # Check if the redirection happens (status code 302)
    # You may want to further assert if the recipe has been deleted by checking the database

