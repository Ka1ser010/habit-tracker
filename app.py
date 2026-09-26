from datetime import date, timedelta
from flask import Flask, render_template, request, url_for, redirect, flash ,jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import UniqueConstraint

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///habits.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'dev-password-secret-key'

db = SQLAlchemy(app)

class Habit(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, unique=True)
    color = db.Column(db.String(9), default="3b82f6")
    goal_type = db.Column(db.String(20), default='daily')
    target_per_day = db.Column(db.Integer, default=1)
    created_at = db.Column(db.Date, default=date.today)

class Checkin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    habit_id = db.Column(db.Integer, db.ForeignKey('habit.id'), nullable = False)
    date = db.Column(db.Date, nullable = False)
    __table_args__ = (UniqueConstraint('habit_id', 'date', name='uix_habit_name'),)

Habit.Checkins = db.relationship('Checkin', backref='habit', cascade = 'all, delete-orphan')

with app.app_context():
    db.create_all()

def get_streak(habits, today):
    has = {c.date for c in habits.Checkins}
    s, d =0, today
    while d in has:
        s+=1
        d -=timedelta(days=1)
        return s
        


@app.route('/')
def index ():
    today = date.today()
    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    days = [today-timedelta(days=i) for i in reversed(range(7))]  
    check_map = {(c.habit_id, c.date) for c in Checkin.query.filter(Checkin.date >= days[0]).all()}
    streaks = {h.id: get_streak(h, today)for h in habits}

    return render_template("index.html", habits = habits, days= days, check_map = check_map, today = today, streaks = streaks)

@app.route('/habits')
def habits():

    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    return render_template("habits.html", habits = habits)

@app.route('/habits/create', methods=["POST"])
def create_habit():

    name = request.form.get('name', '').strip()
    color = request.form.get('color', '#3b82f6').strip()

    if not name:
        flash('Name is required', 'error')
        return redirect(url_for('habits'))

    try:
        habit = Habit(name= name, color = color)
        db.session.add(habit)
        db.session.commit()
        flash('Habit created', 'success')

    except Exception:
        db.session.rollback()
        flash('Habit name must be uniquique', 'error')


    return redirect(url_for('habits'))


@app.route('/habits/<int:habit_id>/delete', methods=["POST"])
def delete_habit(habit_id):
    habit = Habit.query.get_or_404(habit_id)

    db.session.delete(habit)
    db.session.commit()
    flash("Habit deleted", "success")
    return redirect(url_for('habits'))

@app.route('/toggle', methods=["POST"])
def toggle():
    hid= int(request.form['habit_id'])
    d = date.fromisoformat(request.form['date'])

    existing = Checkin.query.filter_by(habit_id = hid, date = d).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        status = False

    else:
        cheking = Checkin(habit_id = hid , date = d )
        db.session.add(cheking)
        db.session.commit()
        status = True

    return jsonify({'Ok': True, "checked" : status})


@app.route('/analytics.json')
def analytics_json():
    from datetime import timedelta
    today = date.today()
    days = [today-timedelta(days=i) for i in reversed(range(7))]  
    labels = [d.strftime('%a') for d in days]
    counts = [Checkin.query.filter_by(date=d).count() for d in days]
    return jsonify({"labels":  labels, "data": counts})


@app.route('/analytics')
def analytics_page():

    habits = Habit.query.order_by(Habit.created_at.desc()).all()
    return render_template("analytics.html", habits = habits)

if __name__ == '__main__':
    app.run(debug= True)