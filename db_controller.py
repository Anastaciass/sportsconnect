from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_workout = db.Table('user_workout',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('workout_id', db.Integer, db.ForeignKey('workout.id'))
)

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    coach = db.Column(db.String(100), nullable=False)
    workoutPicURL = db.Column(db.String(255))

    # 👇 связи
    likes = db.relationship('Like', backref='workout', lazy=True)
    comments = db.relationship('Comment', backref='workout', lazy=True)
    joined_by = db.relationship('User', secondary=user_workout, back_populates='joined_workouts')


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    workoutsJoined = db.Column(db.Boolean, default=False)
    profilePicURL = db.Column(db.String(255))
    password = db.Column(db.String(100), nullable=False)
    likesPut = db.Column(db.Integer)

    # 👇 связи
    likes = db.relationship('Like', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    joined_workouts = db.relationship('Workout', secondary=user_workout, back_populates='joined_by')



class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    workoutID = db.Column(db.Integer, db.ForeignKey('workout.id'))


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('user.id'))
    workoutID = db.Column(db.Integer, db.ForeignKey('workout.id'))
    content = db.Column(db.String(100), nullable=False)
