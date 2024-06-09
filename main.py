from flask import Flask, render_template, request, redirect, url_for, session
from pymongo import MongoClient
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
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = collection.find_one({'username': username, 'password': password})
        if user:
            session['username'] = username
            return redirect(url_for('dashboard'))
        else:
            error = "Wrong username or password"
    return render_template('login.html', error=error)
 
@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))
 
@app.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        existing_user = collection.find_one({'username': username})
        if existing_user:
            error = "Username already exists. Please choose a different one."
        else:
            collection.insert_one({'username': username, 'password': password})
            return redirect(url_for('index'))
    return render_template('register.html', error=error)
 
@app.route('/recipe_entering', methods=['GET','POST'])
def recipe_entering():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        recipe_time = int(request.form['recipe_time'])
        recipe_description = request.form['recipe_description']
        difficulty = request.form['difficulty']
        ingredients = request.form['ingredients']
        username = session.get('username')
        recipes_collection.insert_one({
            'recipe_name': recipe_name,
            'recipe_time': recipe_time,
            'recipe_description': recipe_description,
            'difficulty': difficulty,
            'ingredients': ingredients,
            'username': username
        })
        return redirect(url_for('result', recipe_name=recipe_name))
    return render_template('recipe_entering.html')
 
@app.route('/recipe_book', methods=['GET'])
def recipe_book():
    sort_by = request.args.get('sort_by', 'none')
    sort_order = request.args.get('sort_order', 'asc')
    sort_key = None
    recipes = list(recipes_collection.find())
    if sort_by == 'time':
        sort_key = 'recipe_time'
        recipes.sort(key=lambda x: x.get(sort_key, 0), reverse=(sort_order == 'desc'))
        for recipe in recipes:
            try:
                recipe_time = int(recipe.get('recipe_time', 0))
                recipe['hours'] = recipe_time // 60
                recipe['minutes'] = recipe_time % 60
            except ValueError:
                recipe['hours'] = 0
                recipe['minutes'] = 0
    elif sort_by == 'difficulty':
        sort_key = 'difficulty'
        difficulty_order = {'beginner': 0, 'intermediate': 1, 'advanced': 2}
        recipes.sort(key=lambda x: difficulty_order.get(x.get(sort_key, ''), 0), reverse=(sort_order == 'desc'))
    return render_template('recipe_book.html', recipes=recipes, sort_by=sort_by, sort_order=sort_order)
 
@app.route('/result/<recipe_name>', methods=['GET'])
def result(recipe_name):
    recipe = recipes_collection.find_one({'recipe_name': recipe_name})
    if recipe is None:
        return render_template('404.html'), 404
    recipe_time = int(recipe.get('recipe_time', 0))
    hours = recipe_time // 60
    minutes = recipe_time % 60
    if hours == 0:
        formatted_time = f"{minutes} minute{'s' if minutes != 1 else ''}"
    else:
        formatted_time = f"{hours} hour{'s' if hours != 1 else ''} and {minutes} minute{'s' if minutes != 1 else ''}"
    return render_template('result.html',
                           recipe_name=recipe.get('recipe_name', ''),
                           recipe_time=formatted_time,
                           recipe_description=recipe.get('recipe_description', ''),
                           difficulty=recipe.get('difficulty', ''),
                           ingredients=recipe.get('ingredients', ''),
                           username=recipe.get('username', 'Unknown'))
 
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        username = session['username']
        return render_template('dashboard.html', username=username)
    return redirect(url_for('login'))
 
@app.route('/edit/<recipe_name>', methods=['GET', 'POST'])
def edit_recipe(recipe_name):
    recipe = recipes_collection.find_one({'recipe_name': recipe_name})
    if request.method == 'POST':
        updated_recipe_name = request.form['recipe_name']
        updated_recipe_time = request.form['recipe_time']
        updated_recipe_description = request.form['recipe_description']
        updated_difficulty = request.form['difficulty']
        updated_ingredients = request.form['ingredients']
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
        return redirect(url_for('result', recipe_name=updated_recipe_name))
    return render_template('edit_recipe.html', title='Edit Recipe', recipe=recipe)
 
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
 