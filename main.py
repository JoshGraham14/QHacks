from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
import hashlib

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

# Achievement = db.Table('Achievement', db.Column('student_id', db.Integer, db.ForeignKey(
#     'student.id')), db.Column('course_id', db.Integer, db.ForeignKey('course.id')))


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(50))
    name = db.Column(db.String(100))
    password = db.Column(db.String(32))
    program = db.Column(db.String(50))
    year = db.Column(db.String(5))
    courses = db.relationship('Course', backref='student')


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_code = db.Column(db.String(8))
    name = db.Column(db.String(50))
    grade = db.Column(db.String(3))
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))

### TO INITIALIZE NEW DATABASE ###
# pipenv shell
# python
# from main import db
# db.create_all()

### TO INSERT DATA TO DATABASE ###
# from main import *
#
### ADD A NEW STUDENT ###
# <studentname> = Student(student_number='<data>', first_name='<data>', last_name='<data>', password='<data>')
# db.session.add(<studentname>)
# db.session.commit()
#
### ADD A NEW COURSE ###
# <coursename> = Course(course_name='<data>', instructor=<instructorname>)
# db.session.add(<coursename>)
# db.session.commit()
#
### ADD A NEW INSTRUCTOR ###
# <instructorname> = Instructor(first_name='<data>', last_name='<data>', department='<data>')
# db.session.add(<instructorname>)
# db.session.commit()
#
### ADD A STUDENT TO A COURSE ###
# <coursename>.Achievement.append(<studentname>)
# db.session.commit()

### TO UPDATE DATA IN DATABASE ###
# from main import *
# update = <Class>.query.filter_by(id=<#>).first()
# update.<attributename> = '<newdata>'
# db.session.commit()

### TO DELETE DATA FROM DATABASE ###
# db.session.delete(<attributename>)
# db.session.commit()

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

active_initials = ""


@app.route('/index')
def index():
    print(f'active_initials in index function: {active_initials}')
    return render_template('index.html', title='Welcome', courses=courses, initials=active_initials)


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/achievements')
def achievements():
    return render_template('achievements.html', initials=active_initials)


def get_initials(fullname):
    xs = (fullname)
    name_list = xs.split()

    initials = ""

    for name in name_list:  # go through each name
        initials += name[0].upper()  # append the initial

    return initials


def get_courses(student):
    pass


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        id = request.form['username']
        password = request.form['password']
        print(f'username: {id} and password: {password}')
        hash_pw = hashlib.md5(password.encode())
        print(f'hashed password: {hash_pw.hexdigest()}')
        real_pw = Student.query.filter_by(student_number=id).first()
        if real_pw is None:
            return render_template('login.html', title='Login', page_name='Login')
        elif hash_pw.hexdigest() == real_pw.password:
            print('password matches')
            initials = get_initials(real_pw.name)
            print(initials)
            global active_initials
            active_initials = initials
            print(f'active_initials: {active_initials}')
            return redirect(url_for('index', title='Welcome', courses=courses, initials=active_initials))
        else:
            print("passwords don't match")

    return render_template('login.html', title='Login', page_name='Login')


@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        name = request.form['student-name']
        student_id = request.form['student-number']
        program = request.form['student-program']
        year = request.form['student-year']
        password = request.form['student-password']
        password = hashlib.md5(password.encode()).hexdigest()

        str_rep = f'name: {name}, id: {student_id}, program: {program}, year: {year}, password: {password}'
        print(str_rep)

        db.session.add(Student(student_number=str(
            student_id), name=name, password=password, program=program, year=str(year)))
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('signup.html', title='Make Your Account', page_name='Make Your Account')


@app.route('/')
@app.route('/home')
def welcome():
    return render_template('home.html')


@app.route('/classpage')
def classpage():
    return render_template('classpage.html', initials='HL', title='classpage')


if __name__ == '__main__':
    app.run(debug=True)
