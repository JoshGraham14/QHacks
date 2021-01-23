from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image = db.Column(db.String(20), nullable=True, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    courses = db.relationship('Course', backref='student', lazy=True)

    def __repr__(self):
        return f'User({self.username}, {self.email})'


class Achievements(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    description = db.Column(db.String(100), nullable=True)
    students = db.relationship('User', backref='achievement', lazy=True)

    def __repr__(self):
        return f'Achievement({self.name})'


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(8), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    image = db.Column(db.String(20), nullable=False,
                      default='default-course.jpg')
    semester = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'Course({self.name})'

# vvvvvvvvvvvvvvvvvvvvvvvvvvvv THIS IS TEMPORARY vvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvvv

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
