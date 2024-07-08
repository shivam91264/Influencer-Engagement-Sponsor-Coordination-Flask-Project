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
        flash('YOU WERE REGISTERED SUCCESFULLY!!')
        return render_template("register.html")
    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method=='POST':
        try:
            username=request.form.get('username')
            password=request.form.get('password')
            role=request.form.get('options')
            user=Register.query.filter_by(role=role,username=username,password=password).first()
            if user:
                if role=='admin':
                    return render_template('admin.html')
                elif role=='influencer':
                    return render_template('influencer.html')
                else:
                    return render_template('sponsor.html')
        except Exception as e:
            print(e)
    return render_template('login.html')

