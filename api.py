from flask import Flask, render_template, url_for
from sql import create_connection
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



if __name__ == '__main__':
    app.run(debug=True,port=int(os.getenv('PORT', 4242)))