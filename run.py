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
    workouts=mongo.db.workouts.find())

@app.route('/exercises')
def get_exercises():
    return render_template("exercises.html", 
    exercises=mongo.db.exercises.find())
    
@app.route('/exercises/add')
def add_exercise():
    return render_template("add_exercise.html", categories=mongo.db.exercise_categories.find())
    
@app.route('/workouts/build')
def build_workout():
    return render_template("build_workout.html")
    
@app.route('/routines/build')
def build_routine():
    return render_template("build_routine.html")
    
@app.route('/exercises/edit/<exercise_id>')
def edit_exercise(exercise_id):
    print(exercise_id)
    return render_template("edit_exercise.html")
    
@app.route('/workouts/edit')
def edit_workout():
    return render_template("edit_workout.html")
    
@app.route('/routines/edit/<routine_id>')
def edit_routine(routine_id):
    print(routine_id)
    return render_template("edit_routine.html")

@app.route('/exercises/insert', methods=['POST'])
def insert_exercise():
    
    new_exercise = {
        "exercise_name": request.form.get('exercise_name'),
        "sets": request.form.get('exercise_sets'),
        "reps": request.form.get('exercise_reps'),
        "categories": request.form.getlist('exercise_categories'),
        "exercise_url": request.form.get('exercise_url')
    }
    
    inserted = mongo.db.exercises.insert_one(new_exercise)
    return redirect(url_for('get_exercises'))
    
@app.route('/workouts/insert')
def insert_workout():
    return render_template("insert_workout.html")
    
@app.route('/routines/insert')
def insert_routine():
    return render_template("insert_routine.html")
    
@app.route('/exercises/update')
def update_exercise():
    return render_template("update_exercise.html")
    
@app.route('/workouts/update')
def update_workout():
    return render_template("update_workout.html")
    
@app.route('/routines/update')
def update_routine():
    return render_template("update_routine.html")
    
@app.route('/exercises/delete/<exercise_id>')
def delete_exercise(exercise_id):
    print(exercise_id)
    return redirect(url_for('get_exercises'))
    
@app.route('/routines/delete/<routine_id>')
def delete_routine(routine_id):
    print(routine_id)
    return redirect(url_for('get_routines'))
    
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)