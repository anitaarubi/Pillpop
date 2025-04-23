from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
import os

app = Flask(__name__)

# SQLite config (local file)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///aaldb.sqlite3"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# MedicationLog model
class MedicationLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    medication_name = db.Column(db.String(100), nullable=False)
    taken_at = db.Column(db.DateTime, nullable=False)

@app.before_request
def create_tables():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get medication name from form
        medication_name = request.form.get('medication_name')
        if medication_name:  # Only add log if medication name is provided
            new_log = MedicationLog(medication_name=medication_name, taken_at=datetime.now())
            db.session.add(new_log)
            db.session.commit()
        return redirect('/')

    today = date.today()
    taken_today = MedicationLog.query.filter(
        db.func.date(MedicationLog.taken_at) == today
    ).count() > 0

    return render_template('index.html', taken_today=taken_today)

if __name__ == '__main__':
    app.run(debug=True)
