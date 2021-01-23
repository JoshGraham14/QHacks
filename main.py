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


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html', title='Welcome')


if __name__ == '__main__':
    app.run(debug=True)
