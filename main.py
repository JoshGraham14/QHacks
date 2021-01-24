from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)

Achievement = db.Table('Achievement', db.Column('student_id', db.Integer, db.ForeignKey('student.id')), db.Column('course_id', db.Integer, db.ForeignKey('course.id')))

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_number = db.Column(db.String(50))
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    password = db.Column(db.String(32))
    achievements = db.relationship('Course', secondary='Achievement', backref=db.backref('student'))

class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(50))
    instructor_id = db.Column(db.Integer, db.ForeignKey('instructor.id'))

class Instructor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    department = db.Column(db.String(50))
    courses = db.relationship('Course', backref='instructor')

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

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome', courses=courses)


@app.route('/settings')
def settings():
    return render_template('settings.html')


@app.route('/achievements')
def achievements():
    return render_template('achievements.html')


if __name__ == '__main__':
    app.run(debug=True)