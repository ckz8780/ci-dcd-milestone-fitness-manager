import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

MONGO_USER = os.environ.get('MONGO_USER')
MONGO_PASS = os.environ.get('MONGO_PASS')

app = Flask(__name__)
app.url_map.strict_slashes = False

app.config["MONGO_DBNAME"] = 'fitness_manager'
app.config["MONGO_URI"] = 'mongodb://{}:{}@ds147890.mlab.com:47890/{}'.format(MONGO_USER, MONGO_PASS, app.config['MONGO_DBNAME'])

mongo = PyMongo(app)

@app.route('/')
@app.route('/home')
def home():
    return render_template("home.html")
    
@app.route('/routines')
def get_routines():
    return render_template("routines.html", 
    routines=mongo.db.routines.find())
    
@app.route('/workouts')
def get_workouts():
    return render_template("workouts.html", 
    routines=mongo.db.routines.find())

@app.route('/exercises')
def get_exercises():
    return render_template("exercises.html", 
    routines=mongo.db.routines.find())
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)