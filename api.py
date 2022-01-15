from flask import Flask, render_template
import os

app = Flask(__name__)
@app.route('/')
def get():
    return render_template("home.html")

if __name__ == '__main__':
    app.run(debug=True,port=int(os.getenv('PORT', 4242)))

