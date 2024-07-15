from flask import render_template,request,redirect,session,flash,url_for,send_file
from werkzeug.security import generate_password_hash , check_password_hash
import datetime
from main import *
from model import *
from io import BytesIO




@app.route("/", methods=["GET", "POST"])
def register():

    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='admin':
            return redirect('/admin')
        elif user.role=='influencer':
            return redirect('/influencer')
        elif user.role=='sponsor':
            return redirect('/sponsor')



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
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='admin':
            return render_template('admin.html')
        else:
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')

@app.route("/influencer", methods=["GET", "POST"])
def influencer():
    if "username" in session:
        influencer=Influencers.query.all()
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='influencer':
            return render_template('influencer.html',influencers=influencer,role=user.role)
        else:
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')

@app.route("/campaign", methods=["GET", "POST"])
def campaign():
    if "username" in session:
        sponsor=Sponsors.query.all()
        user=Register.query.filter_by(username=session['username']).first()
        return render_template('campaign.html',sponsors=sponsor,role=user.role)
    else:
        return redirect('/login')


@app.route("/sponsor", methods=["GET", "POST"])
def sponsor():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':
            return render_template('sponsor.html')
        else:
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')





@app.route("/spon_form", methods=["GET", "POST"])
def spon_form():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':     
            try:
                if request.method == 'POST':
                    company_name = request.form.get('company_name')
                    desc = request.form.get('desc')
                    industry = request.form.get('industry')
                    start_date = request.form.get('start_date')
                    end_date = request.form.get('end_date')
                    budget = request.form.get('budget')
                    print(type(start_date))
                    print(type(end_date))
                    sponsor = Sponsors(company_name=company_name, desc=desc, industry=industry, start_date=datetime.date.fromisoformat(start_date), end_date=datetime.date.fromisoformat(end_date), budget=budget)
                    db.session.add(sponsor)
                    db.session.commit()
                    flash('Your card added successfully','success')
                    return redirect('/campaign')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            return render_template('sponsor_form.html')
        else:
            return 'Entry restricted'
    else:
        return redirect('/login')
    

@app.route("/influ_form", methods=["GET", "POST"])
def influ_form():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='influencer':     
            try:
                if request.method == 'POST':
                    img=request.files['img']
                    if not img:
                        return 'img not uploaded'
                    name = request.form.get('name')
                    category = request.form.get('category')
                    niche = request.form.get('niche')
                    reach = request.form.get('reach')
                    influencer = Influencers(img=img.read(),name=name, category=category, niche=niche, reach=reach)
                    db.session.add(influencer)
                    db.session.commit()
                    flash('Your card added successfully','success')
                    return redirect('/campaign')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            return render_template('influencer_form.html')
        else:
            return 'Entry restricted'
    else:
        return redirect('/login')


@app.route('/image/<int:image_id>')
def get_image(image_id):
    image = Influencers.query.filter_by(influencer_id = image_id).first()
    if not image:
        return 'Image not found', 404
    return send_file(BytesIO(image.img), mimetype='image/jpeg')
    # return send_file(BytesIO(image.img), download_name=image.name, mimetype='image/jpeg')


@app.route("/delete_campaign/<int:id>")
def delete_camp(id):
        if "username" in session:
            user=Register.query.filter_by(username=session['username']).first()
            if user.role=='sponsor' or user.role=='admin':     
                Sponsors.query.filter_by(sponsor_id=id).delete()
                db.session.commit()
                flash('Card deleted successfully!!')
                return redirect('/campaign')
            else:
                return 'Delete Restricted'
        else:
            return redirect ('/login')


