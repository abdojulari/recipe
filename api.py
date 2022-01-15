from flask import Flask, render_template, url_for
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


if __name__ == '__main__':
    app.run(debug=True,port=int(os.getenv('PORT', 4242)))