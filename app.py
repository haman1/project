#!/usr/bin/python3
import os

from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "mysql+pymysql://matigari:@localhost:3306/liblarydb"
app.config['SECRET_KEY'] = "random string"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SQLALCHEMY_ECHO'] = True
db.init_app(app)
class Rtrn(db.Model):
    __tablename__ = "b_return"
    id = db.Column(db.Integer, primary_key=True)
    St_Name = db.Column(db.String(150), nullable=False)
    Bo_title = db.Column(db.String(150), nullable=False)
    Date = db.Column(db.DATE, default=datetime.now())
    token_no = db.Column(db.String(15), nullable=False)
    charges = db.Column(db.Integer)

class Book(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key=True)
    Title = db.Column(db.String(150), nullable=False)
    Edition = db.Column(db.String(150), nullable=False)
    Author = db.Column(db.String(50))

class Borrow(db.Model):
    __tablename__ = "borrow"
    id = db.Column(db.Integer, primary_key=True)
    S_Name = db.Column(db.String(150), nullable=False)
    B_title = db.Column(db.String(150), nullable=False)
    Date = db.Column(db.DATE, default=datetime.now())
    token_no = db.Column(db.String(15), nullable=False)
    due = db.Column(db.String(12))

class Student(db.Model):
    __tablename__ = "students"
    id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(50), nullable=False)
    Department = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(13), nullable=False)
    gender = db.Column(db.String(7))
    date = db.Column(db.DATE, default=datetime.now())

@app.route("/", methods=['GET'])
def index():
    students = Borrow.query.all()
    return render_template("index.html", students=students)

@app.route('/student' , methods = ['GET','POST'])
def create():
    if request.method == "POST":

        name = request.form.get("name")
        department = request.form.get("department")
        contact = request.form.get("contact")
        gender = request.form.get("gender")

        student = Student(Name=name, Department=department, contact=contact, gender=gender)
        db.session.add(student)
        db.session.commit()

    students = Student.query.all()
    return render_template("student.html", students=students)

@app.route('/student/<int:id>')
def retrieve(id):
    student = Student.query.filter_by(id=id).first()
    if student:
        return render_template('single.html', student = student)
   

@app.route('/update/<int:id>',methods = ['GET','POST'])
def update(id):
    student = Student.query.filter_by(id=id).first()
    if request.method == 'POST':
        if student:
            db.session.delete(student)
            db.session.commit()
 
            name = request.form.get("name")
            department = request.form.get("department")
            contact = request.form.get("contact")
            gender = request.form.get("gender")

            student = Student(Name=name, Department=department, contact=contact, gender=gender)
 
            db.session.add(student)
            db.session.commit()
            return redirect(f'/student')
 
    return render_template('update.html', student = student)


@app.route("/book", methods=['GET', 'POST'])
def book():
    if request.method == "POST":

        title = request.form.get("bt")
        edition = request.form.get("be")
        author = request.form.get("ba")

        # Create new record
        stud = Book(Title = title, Edition=edition, Author=author)
        db.session.add(stud)
        db.session.commit()

    cla = Book.query.all()
    return render_template("book.html", cla=cla)

@app.route("/borrow_book", methods=['GET', 'POST'])
def borrow():
    if request.method == "POST":

        name = request.form.get("sm")
        BT = request.form.get("bt")
        VN = request.form.get("vn")
        DA = request.form.get("date")

        # Create new record
        stud = Borrow(S_Name = name, B_title=BT, token_no=VN, due=DA)
        db.session.add(stud)
        db.session.commit()

        students = Borrow.query.all()
        return render_template("intro.html", students=students)

    c = db.session.query(Student.Name).all()
    b = db.session.query(Book.Title).all()
    return render_template("borrow.html", c=c, b=b)

@app.route("/return_book", methods=['GET', 'POST'])
def rtrn():
    if request.method == "POST":

        name = request.form.get("sm")
        BT = request.form.get("bt")
        VN = request.form.get("vn")
        DA = request.form.get("ch")

        # Create new record
        stud = Rtrn(St_Name = name, Bo_title=BT, token_no=VN, charges=DA)
        db.session.add(stud)
        db.session.commit()

    students = Rtrn.query.all()
    c = db.session.query(Borrow.S_Name).all()
    b = db.session.query(Borrow.B_title).all()
    return render_template("return.html", c=c, b=b, students=students)

if __name__ == "__main__":
    app.run(debug=True)