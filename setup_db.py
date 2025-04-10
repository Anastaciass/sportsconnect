from app import app
from db_controller import db, Workout

with app.app_context():
    db.create_all()

    if not Workout.query.first():
        w1 = Workout(name="Evening Stretching", coach="Sarah Johnson", workoutPicURL="../static/images/Nude Günlüğü (Yarı Texting).jfif")
        w2 = Workout(name="Retreat Yoga", coach="Alina Korolko", workoutPicURL="../static/images/30 Yoga Photography Tips and Ideas.jfif")
        w3 = Workout(name="Heels Dance", coach="Juliana Honor", workoutPicURL="../static/images/Dance heels.jfif")
        w4 = Workout(name="Kick Boxing", coach="Mike Leuise", workoutPicURL="../static/images/Kickboxing Gear Women _ Aesthetic _ Gloves _ Hand Wraps _ Shin Guards.jfif")
        w5 = Workout(name="HIIT Combo Blast", coach="John Smith", workoutPicURL="../static/images/victor-freitas-1.jfif")
        
        db.session.add_all([w1, w2, w3, w4, w5])
        db.session.commit()
        print("✅ All trainings are added successfuly!.")
