from flask import render_template,request,redirect,session,flash,url_for
from werkzeug.security import generate_password_hash , check_password_hash
from main import *
from model import *




@app.route("/", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        pw = generate_password_hash(request.form.get('password'))
        role = request.form.get("options")

        user_exist = Register.query.filter((Register.username == username)).first()
        if user_exist:
            flash('User already exists!','danger')
            
        else:
            try:
                register = Register(username=username, email=email, password=pw, role=role)
                db.session.add(register)
                db.session.commit()
                session['username']=username
                flash('You were registered successfully!','success')
                if role == 'influencer':
                    return redirect('/influencer')
                else:
                    return redirect('/sponsor')
            except Exception as e:
                print(e)

        return render_template("register.html")
    return render_template("register.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='admin':
            return redirect('/admin')
        elif user.role=='influencer':
            return redirect('/influencer')
        elif user.role=='sponsor':
            return redirect('/sponsor')


    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        role = request.form.get('options')

        try:
            user = Register.query.filter_by(role=role, username=username).first()
            
            if user and check_password_hash(user.password, password):
                session['username']=username
                flash('Login successful!','success')
                if role == 'admin':
                    return redirect('/admin')
                elif role == 'influencer':
                    return redirect('/influencer')
                else:
                    return redirect('/sponsor')
            else:
                flash('Invalid username or password','danger')
        except Exception as e:
            print(e)

    return render_template('login.html')

@app.route('/logout',methods=["GET", "POST"])
def log_out():
    if 'username' in session:
        session.pop('username')
        return redirect('/login')
    else:
        return redirect('/login')
    

@app.route("/admin", methods=["GET", "POST"])
def admin():
    if "username" in session:
        return render_template('admin.html')
    else:
        return redirect('/login')

@app.route("/influencer", methods=["GET", "POST"])
def influencer():
    if "username" in session:
        return render_template('influencer.html')
    else:
        return redirect('/login')

@app.route("/sponsor", methods=["GET", "POST"])
def sponsor():
    if "username" in session:
        return render_template('sponsor.html')
    else:
        return redirect('/login')
