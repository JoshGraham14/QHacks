from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.Integer, nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)
    program = db.Column(db.String(50), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    image = db.Column(db.String(50), default='default.jpg')
    achievements = db.relationship('Achievement', backref='student', lazy=True)
    courses = db.relationship('Course', backref='student', lazy=True)

class Achievement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    grade = db.Column(db.Integer)
    num_points = db.Column(db.Integer)
    num_hours = db.Column(db.Integer)

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50))
    image = db.Column(db.String(50), default='default.jpg')

class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))
    section_number = db.Column(db.Integer)
    semester = db.Column(db.String(50))

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    department = db.Column(db.String(50))
    sections = db.relationship('Section', backref='instructor', lazy=True)

# temp Course class


class Crse():
    def __init__(self, code, name):
        self.code = code
        self.name = name


# list of objects to load course info
courses = [Crse('CISC 235', 'Data Structures'),
           Crse('CISC 271', 'Linear Data Analysis'),
           Crse('CISC 365', 'Algorithms I'),
           Crse('CISC 203', 'Discrete Mathematics II'),
           Crse('CISC 204', 'Logic')]

# ^^^^^^^^^^^^^^^^^^^^^^^^^^ THIS IS TEMPORARY ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

@app.route('/index')
def index():
    return render_template('index.html', title='Welcome', courses=courses)


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/achievements')
def achievements():
    return render_template('achievements.html')


@app.route('/login')
def login():
    return render_template('login.html', title='Login', page_name='Login')


@app.route('/signup')
def signup():
    return render_template('signup.html', title='Make Your Account', page_name='Make Your Account')


@app.route('/')
@app.route('/home')
def welcome():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)