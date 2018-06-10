import os
from flask import Flask, render_template, redirect, request, url_for, jsonify
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
    



# GET ROUTINES/WORKOUTS/EXERCISES

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





# ADD/BUILD ROUTINES/WORKOUTS/EXERCISES
    
@app.route('/routines/build')
def build_routine():
    return render_template("build_routine.html",
    workouts=[workout for workout in mongo.db.workouts.find()],
    exercise_categories=[category for category in mongo.db.exercise_categories.find()],
    exercises=[exercise for exercise in mongo.db.exercises.find()])

@app.route('/workouts/build')
def build_workout():
    return render_template("build_workout.html",
    exercise_categories=[category for category in mongo.db.exercise_categories.find()],
    exercises=[exercise for exercise in mongo.db.exercises.find()])

@app.route('/exercises/add')
def add_exercise():
    return render_template("add_exercise.html", categories=mongo.db.exercise_categories.find())
    
# INSERT ROUTINES/WORKOUTS/EXERCISES

@app.route('/routines/insert', methods=["POST"])
def insert_routine():
    new_routine = {
        "routine_name": request.form.get('routine_name'),
        "workout_list": request.form.getlist('workout_list'),
        "routine_length": request.form.get('routine_length'),
        "routine_intensity": request.form.get('routine_intensity')
    }
    inserted = mongo.db.routines.insert_one(new_routine)
    return redirect(url_for('get_routines'))
    
@app.route('/workouts/insert', methods=['POST'])
def insert_workout():
    new_workout = {
        "workout_name": request.form.get('workout_name'),
        "exercise_list": request.form.getlist('exercise_list')
    }
    inserted = mongo.db.workouts.insert_one(new_workout)
    return redirect(url_for('get_workouts'))
    
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





# EDIT ROUTINES/WORKOUTS/EXERCISES

@app.route('/routines/edit/<routine_id>')
def edit_routine(routine_id):
    return render_template("edit_routine.html",
    workouts=[workout for workout in mongo.db.workouts.find()],
    exercise_categories=[category for category in mongo.db.exercise_categories.find()],
    exercises=[exercise for exercise in mongo.db.exercises.find()],
    routine=mongo.db.routines.find_one({'_id': ObjectId(routine_id)}))
    
@app.route('/workouts/edit/<workout_id>')
def edit_workout(workout_id):
    print(workout_id)
    return render_template("edit_workout.html",
    exercise_categories=[category for category in mongo.db.exercise_categories.find()],
    exercises=[exercise for exercise in mongo.db.exercises.find()],
    workout=mongo.db.workouts.find_one({'_id': ObjectId(workout_id)}))
    
@app.route('/exercises/edit/<exercise_id>')
def edit_exercise(exercise_id):
    return render_template("edit_exercise.html",
    categories=[category for category in mongo.db.exercise_categories.find()],
    exercise=mongo.db.exercises.find_one({'_id': ObjectId(exercise_id)}))
    
# UPDATE ROUTINES/WORKOUTS/EXERCISES  

@app.route('/routines/update/<routine_id>', methods=['POST'])
def update_routine(routine_id):
    updated = mongo.db.routines.update(
        {'_id': ObjectId(routine_id)},
        {
            "routine_name": request.form.get('routine_name'),
            "workout_list": request.form.getlist('workout_list'),
            "routine_length": request.form.get('routine_length'),
            "routine_intensity": request.form.get('routine_intensity')
        })
    print(updated)
    return redirect(url_for('get_routines'))

@app.route('/workouts/update/<workout_id>', methods=['POST'])
def update_workout(workout_id):
    updated = mongo.db.workouts.update(
        {'_id': ObjectId(workout_id)},
        {
            "workout_name": request.form.get('workout_name'),
            "exercise_list": request.form.getlist('exercise_list')
        })
    return redirect(url_for('get_workouts'))
    
@app.route('/exercises/update/<exercise_id>', methods=['POST'])
def update_exercise(exercise_id):
    mongo.db.exercises.update(
        {'_id': ObjectId(exercise_id)},
        {
            "exercise_name": request.form.get('exercise_name'),
            "sets": request.form.get('exercise_sets'),
            "reps": request.form.get('exercise_reps'),
            "categories": request.form.getlist('exercise_categories'),
            "exercise_url": request.form.get('exercise_url')
        })
    return redirect(url_for('get_exercises'))
    
    



# DELETE ROUTINES/WORKOUTS/EXERCISES

@app.route('/routines/delete/<routine_id>')
def delete_routine(routine_id):
    mongo.db.routines.remove({'_id': ObjectId(routine_id)})
    return redirect(url_for('get_routines'))
    
@app.route('/workouts/delete/<workout_id>')
def delete_workout(workout_id):
    mongo.db.workouts.remove({'_id': ObjectId(workout_id)})
    return redirect(url_for('get_workouts'))
    
@app.route('/exercises/delete/<exercise_id>')
def delete_exercise(exercise_id):
    mongo.db.exercises.remove({'_id': ObjectId(exercise_id)})
    return redirect(url_for('get_exercises'))





# UTILITY METHODS

@app.route('/exercises/by_cat/<cat>')
def get_exercises_by_cat(cat):
    """Returns a list of exercises in JSON format, given a category from an AJAX request"""
    if request.is_xhr:
        exercise_list = [exercise for exercise in mongo.db.exercises.find({"categories": cat}, {"_id": 0})]
        return jsonify(exercises=exercise_list)
    return redirect(url_for('get_exercises'))
    
    
    
    
    
    
    
# RUN APP
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
        port=int(os.environ.get('PORT')),
        debug=True)