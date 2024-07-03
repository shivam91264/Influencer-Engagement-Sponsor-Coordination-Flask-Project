from flask import render_template,request,redirect,session,flash
from main import *
from model import *




@app.route("/", methods=["GET","POST"])
def register():
    if request.method=="POST":
        try:
            username=request.form.get("username") 
            email=request.form.get("email")
            password=request.form.get('password')
            role=request.form.get("options")
            register=Register(username=username,email=email,password=password,role=role)
            db.session.add(register)
            db.session.commit()
        except Exception as e:
            print(e)
        return render_template("register.html")
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template('login.html')

