from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY')

mongo_uri = os.environ.get('MONGO_URI')
if not mongo_uri:
    raise ValueError("MONGO_URI environment variable is not set")

client = MongoClient(mongo_uri)
db = client.get_default_database()
collection = db['users']  
recipes_collection = db['recipes']

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None  # Initialize error message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username  # Store the username in the session
            return redirect(url_for('dashboard'))  # Redirect to the dashboard if login is successful
        else:
            error = "Invalid username or password"  # Set error message
    return render_template('login.html', error=error)

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    if 'username' in session:
        session.pop('username')  # Remove the username from the session
    return redirect(url_for('index'))  # Redirect to the index page after logging out


@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None  # Initialize error message
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        # Check if the username already exists in the database
        existing_user = collection.find_one({'username': username})
        if existing_user:
            error = "Username already exists. Please choose a different one."  # Set error message
        else:
            # Save the username and password to the database
            collection.insert_one({'username': username, 'password': password})
            return redirect(url_for('index'))  # Redirect to the index page after successful registration
    return render_template('register.html', error=error)

@app.route('/recipe_entering', methods=['GET','POST'])
def recipe_entering():
    if request.method == 'POST':
        # Retrieve recipe details from the form submission
        recipe_name = request.form['recipe_name']
        recipe_time = int(request.form['recipe_time'])  # Convert to integer
        recipe_description = request.form['recipe_description']
        difficulty = request.form['difficulty']
        ingredients = request.form['ingredients']

        # Retrieve the username of the logged-in user from the session
        username = session.get('username')

        # Insert the recipe details along with the username into the recipes collection
        recipes_collection.insert_one({
            'recipe_name': recipe_name,
            'recipe_time': recipe_time,
            'recipe_description': recipe_description,
            'difficulty': difficulty,
            'ingredients': ingredients,
            'username': username  # Include the username of the user who added the recipe
        })

        # Redirect to the result page for the newly added recipe
        return redirect(url_for('result', recipe_name=recipe_name))

    return render_template('recipe_entering.html')


@app.route('/recipe_book', methods=['GET'])
def recipe_book():
    sort_by = request.args.get('sort_by', 'none')
    sort_order = request.args.get('sort_order', 'asc')

    sort_key = None
    recipes = []

    # Fetch all recipes regardless of sorting parameters
    recipes = list(recipes_collection.find())

    if sort_by == 'time':
        sort_key = 'recipe_time'
        # Sort recipes by time
        recipes.sort(key=lambda x: x.get(sort_key, 0), reverse=(sort_order == 'desc'))
        # Convert time from string to integer and then to hours and minutes format
        for recipe in recipes:
            try:
                recipe_time = int(recipe.get('recipe_time', 0))
                recipe['hours'] = recipe_time // 60
                recipe['minutes'] = recipe_time % 60
            except ValueError:
                # Handle the case where recipe_time is not a valid integer
                recipe['hours'] = 0
                recipe['minutes'] = 0
    elif sort_by == 'difficulty':
        sort_key = 'difficulty'
        # Define custom sorting order
        difficulty_order = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
        # Sort recipes by difficulty using custom sorting order
        recipes.sort(key=lambda x: difficulty_order.get(x.get(sort_key, ''), 0), reverse=(sort_order == 'desc'))

    return render_template('recipe_book.html', recipes=recipes, sort_by=sort_by, sort_order=sort_order)

@app.route('/result/<recipe_name>', methods=['GET'])
def result(recipe_name):
    # Find the recipe by name
    recipe = recipes_collection.find_one({'recipe_name': recipe_name})

    # If the recipe is not found, return a 404 error
    if recipe is None:
        return render_template('404.html'), 404

    # Convert time from minutes to hours and minutes format
    recipe_time = int(recipe.get('recipe_time', 0))  # Convert recipe_time to an integer
    hours = recipe_time // 60
    minutes = recipe_time % 60

    # Format time string
    if hours == 0:
        if minutes == 1:
            formatted_time = f"{minutes} minute"
        else:
            formatted_time = f"{minutes} minutes"
    elif hours == 1:
        if minutes == 0:
            formatted_time = f"{hours} hour"
        elif minutes == 1:
            formatted_time = f"{hours} hour and {minutes} minute"
        else:
            formatted_time = f"{hours} hour and {minutes} minutes"
    else:
        if minutes == 0:
            formatted_time = f"{hours} hours"
        elif minutes == 1:
            formatted_time = f"{hours} hours and {minutes} minute"
        else:
            formatted_time = f"{hours} hours and {minutes} minutes"

    # Pass the recipe details and username to the template for rendering
    return render_template('result.html',
                           recipe_name=recipe.get('recipe_name', ''),
                           recipe_time=formatted_time,
                           recipe_description=recipe.get('recipe_description', ''),
                           difficulty=recipe.get('difficulty', ''),
                           ingredients=recipe.get('ingredients', ''),
                           username=recipe.get('username', 'Unknown'))  # Pass the username




@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    return redirect(url_for('login'))

# Flask route for editing recipes
@app.route('/edit/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe(recipe_name):
    # Retrieve the recipe from the database based on the provided recipe name
    recipe = recipes_collection.find_one({'recipe_name': recipe_name})

    if request.method == 'POST':
        # Retrieve the updated details from the form
        updated_recipe_name = request.form['recipe_name']
        updated_recipe_time = request.form['recipe_time']
        updated_recipe_description = request.form['recipe_description']
        updated_difficulty = request.form['difficulty']
        updated_ingredients = request.form['ingredients']

        # Update the recipe in the database
        recipes_collection.update_one(
            {'recipe_name': recipe_name},
            {'$set': {
                'recipe_name': updated_recipe_name,
                'recipe_time': updated_recipe_time,
                'recipe_description': updated_recipe_description,
                'difficulty': updated_difficulty,
                'ingredients': updated_ingredients
            }}
        )

        # Redirect the user back to the result page for the edited recipe
        return redirect(url_for('result', recipe_name=updated_recipe_name))

    # Render the edit form with the recipe details
    return render_template('edit_recipe.html',
                           title='Edit Recipe',
                           recipe=recipe)  # Pass the recipe variable to the template

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

