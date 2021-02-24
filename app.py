from flask import Flask, render_template, request
import sqlite3
import os
from flask_cors import CORS

currentDir = os.path.dirname(os.path.abs(__file__))
app= Flask(__name__)
CORS(app)

database_name ="ecco-site.database"

def connect(databases=database_name):

    connecting = sqlite3.connect(databases)
    connecting.row_factory = sqlite3.Row

    return connecting
@app.route('/')
def index():
    return render_template("index")

@app.route('/products')
def index():
    return 'products.html'

if __name__ == "__main__":
    app.run(debug=True)
