from flask import Flask, render_template, url_for, redirect, request
from wtforms import Form, StringField, validators
from sql import create_connection
from sqlite3 import Error

import os


app = Flask(__name__)

recipes = [
        {
            "title": "BBQ Sweet and Sour Chicken Wings",
            "image": "https://image.freepik.com/free-photo/chicken-wings-barbecue-sweetly-sour-sauce-picnic-summer-menu-tasty-food-top-view-flat-lay_2829-6471.jpg",
            "link": "https://cookpad.com/us/recipes/347447-easy-sweet-sour-bbq-chicken"
        }
    ]
@app.route('/')
def home():
    return render_template("home.html", recipes=recipes)

@app.route('/about')
def about():
    return render_template("about.html")

connection = create_connection('sm_app.sqlite')

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred!")

create_recipe_table = """
CREATE TABLE IF NOT EXISTS recipes (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  image TEXT NOT NULL,
  link TEXT NOT NULL
);
"""
execute_query(connection, create_recipe_table)  

class CreateRecipeForm(Form):
    title = StringField('Recipe Title', [validators.Length(min=4, max=50)])
    image = StringField('Image Address', [validators.Length(min=10)])
    link = StringField('Image Address', [validators.Length(min=10)])
# creating route for recipe

@app.route('/recipe/', methods=['POST', 'GET'])
def create_recipe():
    form = CreateRecipeForm(request.form)
    if request.method == 'POST' and form.validate():
        link = form['link']
        image = form['image']
        title = form['title']
        insert_recipe = '''INSERT INTO recipes (title, image, link) VALUES (?,?,?)'''
        data = (title, image, link)
        execute_query(connection, insert_recipe, data)
        return redirect(url_for('home'))
    return render_template('create-recipe.html', form=form)

@app.route('/recipe/delete/<id>/', methods=['POST'])
def delete_recipe(id):
    execute_query(connection,'''DELETE FROM recipes WHERE id=?''', (id))
    return redirect(url_for('home'))

@app.route('/recipe/<id>', methods=['GET', 'POST'])
def edit_recipe(id):
    form = CreateRecipeForm(request.form)
    if request.method == 'POST': 
        if form.validate():
            title = form.title.data
            image = form.image.data
            link = form.link.data
            update_query = '''UPDATE recipes set title=?, image=?, link=?'''
            execute_query(connection, update_query, (title, image, link))
            return redirect(url_for('home'))
    recipe = execute_read_query(
        connection, '''SELECT * FROM recipes WHERE id=?''', (id))
    form = CreateRecipeForm(link=recipe[0][3], title=recipe[0][1], image=recipe[0][2])
    return render_template('edit-recipe.html', form=form, id=id)

def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print (f"The error '{e}' occurred")


if __name__ == '__main__':
    app.run(debug=True,port=int(os.getenv('PORT', 4242)))