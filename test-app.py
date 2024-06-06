import pytest
from flask import Flask

# Import the Flask app
from main import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Recipe Management System' in response.data

# def test_login(client):
#     response = client.get('/login')
#     assert response.status_code == 200
#     assert b'Login' in response.data

# def test_register(client):
#     response = client.get('/register')
#     assert response.status_code == 200
#     assert b'Register' in response.data

def test_recipe_entering(client):
    response = client.get('/recipe_entering')
    assert response.status_code == 200
    assert b'Enter Recipe Details' in response.data

def test_recipe_book(client):
    response = client.get('/recipe_book')
    assert response.status_code == 200
    assert b'Recipe Book' in response.data

def test_result(client):
    # Assuming 'recipe_name' exists in the database for this test
    response = client.get('/result/recipe_name')
    assert response.status_code == 200
    assert b'recipe_name' in response.data
    assert b'recipe_time' in response.data
    assert b'recipe_description' in response.data
    assert b'difficulty' in response.data
    assert b'ingredients' in response.data