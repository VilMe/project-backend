"""V$ fitness tracking app, fitbub
/login
	post
/registration
	post 
/exercises_entries
	post 
    creates new exercise entry for user

/exercise_history
	get all exercises for a user
    sort by date


/logout
    delete user from session
    logout user
"""

from flask import Flask, redirect, request, session, jsonify
from model import connect_to_db, db, User, Exercise, ExerciseEntry
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"





@app.route("/register", methods=[ "POST"])
def register():
	"""Add user email and password to database."""

	email = request.form["email"]
	password = request.form["password"]
	new_user = User(email=email, password=password)
	print(new_user)
	#TO DO check for confirmation, JSX function in form component
	db.session.add(new_user)
	db.session.commit()
    session['user'] = user_id
	return " ", 200

@app.route("/login", methods=["POST"])
def login():
	"""check if user exists and log them in"""

	email = request.form["email"]
	password = request.form["password"]
	user = User.query.filter_by(email= email).one_or_none()
	if password == user.password:
		session['user'] = user.user_id
	else:
		return "wrong password"

	print(email)
	print(password)
	return " ", 200


	

@app.route("/exercise_entry", methods=["POST"])
def exercise_entry():
	""" add user exercise entry"""
	if 'user' in session:
		entry_user_id = session['user']
	else: 
		return redirect('/login')
	exercise_name = request.form["exercise"]
	weight = request.form["weight"]
	num_reps = request.form["num_reps"]

	exercise = Exercise.query.filter_by(exercise_name = exercise_name).first()
	#need to query Exercise table with user_id and exercise name

	if exercise == None:
		new_exercise_name = Exercise(exrs_user_id = entry_user_id,
									 exercise_name = exercise_name,
									 )
		db.session.add(new_exercise_name)
		db.session.commit()
		exercise = Exercise.query.filter_by(exercise_name = exercise_name).first()
	print(exercise.exercise_id, entry_user_id, weight, num_reps)

	new_exercise_entry = ExerciseEntry(entry_user_id = entry_user_id,
									   entry_exercise_id = exercise.exercise_id,
									   num_reps = num_reps,
									   weight = weight,
									   )
	db.session.add(new_exercise_entry)
	db.session.commit()
	return " ", 200

@app.route("/exercise_history", methods=["GET"])
def exercise_history():
	"""get user exercises history"""
	entry_user_id = 4

	all_exercise_entries = db.session.query(ExerciseEntry).\
							  join(Exercise).\
							  filter_by(exrs_user_id = entry_user_id).\
							  all() 

	all_exercises_dict = {}

	for exercise in all_exercise_entries:
		date_of_entry = exercise.entry_datetime.strftime("%b %d %Y")
		if date_of_entry in all_exercises_dict:
			exercise_on_date = all_exercises_dict[date_of_entry]
			exercise_on_date.append(
				{'exercise': exercise.exercises.exercise_name,
				 'weight': exercise.weight,
				 'reps': exercise.num_reps
				})
			all_exercises_dict[date_of_entry] = exercise_on_date
		else: 
			all_exercises_dict[date_of_entry] =\
				[{'exercise': exercise.exercises.exercise_name,
				 'weight': exercise.weight,
				 'reps': exercise.num_reps
				}]


	return jsonify(all_exercises_dict), 200
	#return array of objects 
	






if __name__ == "__main__":
	

	connect_to_db(app)


	app.run(debug = True, port=5000, host='0.0.0.0')


