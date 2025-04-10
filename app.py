from flask import Flask, render_template, send_from_directory, request, redirect, url_for, jsonify
import os
import json
from db_controller import db, Like, Comment, Workout, User 



app = Flask(__name__)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'app.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

@app.route('/join_workout', methods=["POST"])
def join_workout():
    print("🔥 /join_workout called!")
    data = request.json
    print("📦 Data received:", data)

    user_id = data.get("user_id")
    workout_id = data.get("workout_id")

    user = User.query.get(user_id)
    workout = Workout.query.get(workout_id)

    if not user or not workout:
        return jsonify({"error": "User or Workout not found"}), 404

    if workout not in user.joined_workouts:
        user.joined_workouts.append(workout)
        db.session.commit()

    return jsonify({"success": True})

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        identifier = request.form.get('email')  
        password = request.form.get('password')

        user = User.query.filter((User.email == identifier) | (User.name == identifier)).first()

        if user and user.password == password:
            # temporarily store user_id in a cookie/session
            response = redirect(url_for('menu'))
            response.set_cookie('user_id', str(user.id))
            return response

        return render_template('login.html', alert="Invalid username/email or password.")

    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')

        if not all([name, email, password]):
            return render_template('sign_up.html', error="Please fill out all fields.")

        # Check if user already exists
        existing_user = User.query.filter((User.name == name) | (User.email == email)).first()
        if existing_user:
            return render_template('sign_up.html', error="User already exists.")

        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('sign_up.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/menu')
def menu():
    user_id = request.cookies.get("user_id")
    user = User.query.get(user_id)
    
    if not user:
        return redirect(url_for('login'))

    liked_workouts = [like.workoutID for like in user.likes]
    return render_template("menu.html", user_id=user_id, liked_workouts=liked_workouts)



@app.route('/myworkouts')
def myworkouts():
    user_id = request.cookies.get('user_id')
    user = User.query.get(user_id)

    if not user:
        return redirect(url_for('login'))

    workouts = user.joined_workouts
    return render_template('myworkouts.html', workouts=workouts)

@app.route('/logout', methods=["GET", "POST"])
def logout():
    return redirect(url_for('index'))


@app.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'manifest.json')

@app.route('/service-worker.js')
def service_worker():
    return send_from_directory('.', 'service-worker.js')

@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory('static', filename)


from flask import jsonify

@app.route('/toggle_like', methods=["POST"])
def toggle_like():
    try:
        data = request.json
        user_id = data.get("user_id")
        workout_id = data.get("workout_id")

        if not user_id or not workout_id:
            return jsonify({"error": "Missing data"}), 400

        existing = Like.query.filter_by(userID=user_id, workoutID=workout_id).first()

        if existing:
            db.session.delete(existing)
            db.session.commit()
            return jsonify({"liked": False})
        else:
            new_like = Like(userID=user_id, workoutID=workout_id)
            db.session.add(new_like)
            db.session.commit()
            return jsonify({"liked": True})

    except Exception as e:
        # send actual JSON so frontend doesn't crash
        return jsonify({"error": str(e)}), 500
        
    
@app.route('/add_comment', methods=["POST"])
def add_comment():
    data = request.json
    user_id = data.get("user_id")
    workout_id = data.get("workout_id")
    content = data.get("content")

    if not content:
        return jsonify({"error": "Empty comment"}), 400

    new_comment = Comment(userID=user_id, workoutID=workout_id, content=content)
    db.session.add(new_comment)
    db.session.commit()

    return jsonify({"success": True})

@app.route('/get_comments/<int:workout_id>')
def get_comments(workout_id):
    comments = Comment.query.filter_by(workoutID=workout_id).all()
    return jsonify({"comments": [{"content": c.content} for c in comments]})
    


@app.cli.command("routes")
def list_routes():
    import urllib
    from flask import url_for
    output = []
    for rule in app.url_map.iter_rules():
        methods = ','.join(rule.methods)
        line = urllib.parse.unquote(f"{rule.endpoint:50s} {methods:20s} {str(rule)}")
        output.append(line)

    for line in sorted(output):
        print(line)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
