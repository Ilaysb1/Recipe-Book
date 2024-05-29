from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from pymongo import ASCENDING, DESCENDING

app = Flask(__name__)
client = MongoClient('mongodb+srv://ilaysb:Ilaysb12@cluster0.f1l3dro.mongodb.net/')
db = client['testDB']
collection = db['recipes']

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/recipe_entering', methods=['GET', 'POST'])
def recipe_entering():
    if request.method == 'POST':
        recipe_name = request.form['recipe_name']
        recipe_time = request.form['recipe_time']
        recipe_description = request.form['recipe_description']
        difficulty = request.form['difficulty']
        ingredients = request.form['ingredients']  # Added to get ingredients from form
        # Save recipe details to MongoDB
        collection.insert_one({
            'recipe_name': recipe_name,
            'recipe_time': recipe_time,
            'recipe_description': recipe_description,
            'difficulty': difficulty,
            'ingredients': ingredients  # Added ingredients to document
        })
        return redirect(url_for('result',
                                recipe_name=recipe_name,
                                recipe_time=recipe_time,
                                recipe_description=recipe_description,
                                difficulty=difficulty,
                                ingredients=ingredients))
    return render_template('recipe_entering.html')


@app.route('/recipe_book', methods=['GET'])
def recipe_book():
    # Get query parameters for sorting
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order')

    # Default sorting
    sort_direction = ASCENDING

    if sort_order == 'desc':
        sort_direction = DESCENDING

    if sort_by == 'time':
        recipes = collection.find().sort('recipe_time', sort_direction)
    elif sort_by == 'difficulty':
        recipes = collection.find().sort('difficulty', sort_direction)
    else:
        recipes = collection.find()

    return render_template('recipe_book.html', recipes=recipes, sort_by=sort_by)

@app.route('/result/<recipe_name>', methods=['GET'])
def result(recipe_name):
    recipe = collection.find_one({'recipe_name': recipe_name})
    return render_template('result.html',
                           recipe_name=recipe['recipe_name'],
                           recipe_time=recipe['recipe_time'],
                           recipe_description=recipe['recipe_description'],
                           difficulty=recipe['difficulty'],
                           ingredients=recipe.get('ingredients', ''))

if __name__ == '__main__':
    app.run(debug=True)
