from flask import Flask, render_template, request, session, redirect, flash
from flask_sqlalchemy import SQLAlchemy
import json

# Load configuration from JSON
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

local_server = True
app = Flask(__name__)
app.secret_key = 'super-secret-key'

# Configure database URI
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['proud_uri']

db = SQLAlchemy(app)

class Patients(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, nullable=False)
    patient_name = db.Column(db.String(255), nullable=False)
    department = db.Column(db.String(50), nullable=False)
    comments = db.Column(db.Text)
    encrypted_content = db.Column(db.Text)  # Store encrypted file content
    upload_date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())


class ActionLogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.patient_id'), nullable=False)
    action = db.Column(db.String(255), nullable=False)
    date = db.Column(db.TIMESTAMP, server_default=db.func.current_timestamp())

# Flask Routes

@app.route("/")
def hello():
    return render_template('index.html', params=params)

@app.route("/index")
def home():
    return render_template('dashboard.html', params=params)

@app.route("/search", methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        name = request.form.get('search')
        patient = Patients.query.filter_by(patient_name=name).first()
        if patient:
            flash("Patient Found.", "primary")
        else:
            flash("Patient Not Found.", "danger")
    return render_template('search.html', params=params)

@app.route("/details", methods=['GET', 'POST'])
def details():
    if 'user' in session and session['user'] == params['user']:
        logs = ActionLogs.query.all()
        return render_template('details.html', params=params, logs=logs)

@app.route("/aboutus")
def aboutus():
    return render_template('aboutus.html', params=params)

@app.route("/insert", methods=['GET', 'POST'])
@app.route("/insert", methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        patient_id = request.form.get('patient_id')  # Ensure this is not None
        patient_name = request.form.get('patient_name')
        department = request.form.get('department')
        comments = request.form.get('comments')

        # Ensure that patient_id and patient_name are provided
        if not patient_id or not patient_name:
            flash("Patient ID and Name are required!", "danger")
            return render_template('insert.html', params=params)

        new_patient = Patients(patient_id=patient_id, patient_name=patient_name, department=department, comments=comments)
        db.session.add(new_patient)
        db.session.commit()
        flash("Patient Added Successfully", "success")

    return render_template('insert.html', params=params)

@app.route("/logout")
def logout():
    session.pop('user')
    flash("You are logged out", "primary")
    return redirect('/login')

@app.route("/login", methods=['GET', 'POST'])
def login():
    if 'user' in session and session['user'] == params['user']:
        return render_template('dashboard.html', params=params)

    if request.method == 'POST':
        username = request.form.get('uname')
        password = request.form.get('password')
        if username == params['user'] and password == params['password']:
            session['user'] = username
            flash("You are logged in", "primary")
            return redirect('/index')
        else:
            flash("Invalid credentials", "danger")
    return render_template('login.html', params=params)



# Start the application
if __name__ == "__main__":
    app.run(debug=True)
