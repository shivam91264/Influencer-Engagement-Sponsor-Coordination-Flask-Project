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
                    return redirect('/influencer_form')
                else:
                    return redirect('/sponsor_form')
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
            return redirect('/campaign')
        elif user.role=='sponsor':
            return redirect('/influencer')


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
                    return redirect('/campaign')
                else:
                    return redirect('/influencer')
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
    

# ===============================================================================================================================
@app.route('/home',methods=["GET", "POST"])
def home():
    if 'username' in session:
        return render_template('home.html') 
    else:
        return redirect('/login')  
#================================================================================================================================


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
        if user.role=='influencer' or user.role=='sponsor':
            return render_template('influencer.html',influencers=influencer,role=user.role)
        else:
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')

@app.route("/campaign", methods=["GET"])
def campaign():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':
            campaign=Campaign.query.filter_by(user_id=user.id)
        else:
            campaign=Campaign.query.all()
        return render_template('campaign.html',campaigns=campaign,role=user.role)
    else:
        return redirect('/login')


# @app.route("/sponsor", methods=["GET", "POST"])
# def sponsor():
#     if "username" in session:
#         user=Register.query.filter_by(username=session['username']).first()
#         if user.role=='sponsor':
#             return render_template('sponsor.html')
#         else:
#             return '<h1>Resticted Entry</h1>'
#     else:
#         return redirect('/login')





@app.route("/add_campaign", methods=["GET", "POST"])
def campaign_add():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':     
            try:
                if request.method == 'POST':
                    user_id = user.id
                    company_name = request.form.get('company_name')
                    desc = request.form.get('desc')
                    industry = request.form.get('industry')
                    start_date = request.form.get('start_date')
                    end_date = request.form.get('end_date')
                    budget = request.form.get('budget')
                    sponsor = Campaign(company_name=company_name,user_id=user_id, desc=desc, industry=industry, start_date=datetime.date.fromisoformat(start_date), end_date=datetime.date.fromisoformat(end_date), budget=budget)
                    db.session.add(sponsor)
                    db.session.commit()
                    flash('Campaign added successfully','success')
                    return redirect('/campaign')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            return render_template('campaign_form.html',role=user.role)
        else:
            return 'Entry restricted'
    else:
        return redirect('/login')
    

@app.route("/influencer_form", methods=["GET", "POST"])
def influencer_form():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='influencer':     
            try:
                if request.method == 'POST':
                    img=request.files['img']
                    if not img:
                        return 'img not uploaded'
                    user_id=user.id
                    name = request.form.get('name')
                    category = request.form.get('category')
                    niche = request.form.get('niche')
                    reach = request.form.get('reach')
                    influencer = Influencers(img=img.read(),user_id=user_id,name=name, category=category, niche=niche, reach=reach)
                    db.session.add(influencer)
                    db.session.commit()
                    flash('Profile Created successfully','success')
                    return redirect('/influencer_profile')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            return render_template('influencer_form.html',role=user.role)
        else:
            return 'Entry restricted'
    else:
        return redirect('/login')
    

@app.route("/sponsor_form", methods=["GET", "POST"])
def sponsor_form():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':     
            try:
                if request.method == 'POST':
                    img=request.files['img']
                    if not img:
                        return 'img not uploaded'
                    user_id=user.id
                    company_name = request.form.get('company_name')
                    desc = request.form.get('desc')
                    industry = request.form.get('industry')
                    sponsor = Sponsors(img=img.read(),user_id=user_id,company_name=company_name, desc=desc, industry=industry)
                    db.session.add(sponsor)
                    db.session.commit()
                    flash('Profile Created successfully','success')
                    return redirect('/sponsor_profile')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            return render_template('sponsor_form.html',role=user.role)
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

@app.route('/image1/<int:image_id>')
def get_image1(image_id):
    image = Sponsors.query.filter_by(sponsor_id = image_id).first()
    if not image:
        return 'Image not found', 404
    return send_file(BytesIO(image.img), mimetype='image/jpeg')


@app.route("/delete_campaign/<int:id>")
def delete_camp(id):
        if "username" in session:
            user=Register.query.filter_by(username=session['username']).first()
            if user.role=='sponsor' or user.role=='admin':     
                Campaign.query.filter_by(sponsor_id=id).delete()
                db.session.commit()
                flash('Card deleted successfully!!')
                return redirect('/campaign')
            else:
                return 'Delete Restricted'
        else:
            return redirect ('/login')


@app.route("/edit_campaign/<int:id>",methods=["GET", "POST"]) # This route handle both GET and POST request and id in url get as an integer and passed to function edit_camp 
def edit_campaign(id):
        if "username" in session:  # This line check  username key present in session or not 
            user=Register.query.filter_by(username=session['username']).first()  # This line check records from register table based on username present in session and store it in user variable
            if user.role=='sponsor' or user.role=='admin': # it will check if user role is sponsor or admin
                if request.method=='GET':     
                    campaign=Campaign.query.filter_by(sponsor_id=id).first() # this line check data from sponnsor table and store it in campaign  varibale
                    return render_template('edit_campaign.html',campaign=campaign,role=user.role) # this line pass the campaign data to edit_campaign page
                elif request.method=='POST':
                    campaign=Campaign.query.filter_by(sponsor_id=id).first()
                    campaign.company_name = request.form.get('company_name')
                    campaign.desc = request.form.get('desc')
                    campaign.industry = request.form.get('industry')
                    campaign.start_date=datetime.date.fromisoformat(request.form.get('start_date'))
                    campaign.end_date=datetime.date.fromisoformat(request.form.get('end_date'))
                    campaign.budget = request.form.get('budget')
                    db.session.commit()  # it will save all the changes in database and flash a msg then it will hit the campaign route
                    flash('Your card updated successfully','success')
                    return redirect('/campaign')
            else:
                return 'Edit Restricted' # if user role is not sponsor or admin then it will return edit restricted
        else:
            return redirect ('/login')  # if username not in session then it redirect to login route
        


@app.route("/edit_influencer/<int:id>",methods=["GET", "POST"])
def edit_influencer(id):
        if "username" in session:
            user=Register.query.filter_by(username=session['username']).first()
            if user.role=='influencer':
                if request.method=='GET':     
                    influencer=Influencers.query.filter_by(influencer_id=id).first()
                    return render_template('edit_influencer.html',influencer=influencer,role=user.role)
                elif request.method=='POST':
                    influencer=Influencers.query.filter_by(influencer_id=id).first()
                    if 'img' in request.files and request.files['img'].filename != '':
                        image = request.files['img']
                        influencer.img = image.read()
                    influencer.name = request.form.get('name')
                    influencer.category = request.form.get('category')
                    influencer.niche = request.form.get('niche')
                    influencer.reach = request.form.get('reach')
                    db.session.commit()
                    flash('Profile updated successfully','success')
                    return redirect('/influencer_profile')
            else:
                return 'Edit Restricted'
        else:
            return redirect ('/login')
        
@app.route("/edit_sponsor/<int:id>",methods=["GET", "POST"])
def edit_sponsor(id):
        if "username" in session:
            user=Register.query.filter_by(username=session['username']).first()
            if user.role=='sponsor':
                if request.method=='GET':     
                    sponsor=Sponsors.query.filter_by(sponsor_id=id).first()
                    return render_template('edit_sponsor.html',sponsor=sponsor,role=user.role)
                elif request.method=='POST':
                    sponsor=Sponsors.query.filter_by(sponsor_id=id).first()
                    if 'img' in request.files and request.files['img'].filename != '':
                        image = request.files['img']
                        sponsor.img = image.read()
                    sponsor.company_name = request.form.get('company_name')
                    sponsor.desc = request.form.get('desc')
                    sponsor.industry = request.form.get('industry')
                    db.session.commit()
                    flash('Profile updated successfully','success')
                    return redirect('/sponsor_profile')
            else:
                return 'Edit Restricted'
        else:
            return redirect ('/login')




@app.route("/influencer_profile")
def influ_profile():
    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='influencer':
            influencer=Influencers.query.filter_by(user_id=user.id).first()
            return render_template('influencer_profile.html',influencer=influencer,role=user.role)
    return redirect('/login')




@app.route("/sponsor_profile")
def sponsor_profile():
    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':
            sponsor=Sponsors.query.filter_by(user_id=user.id).first()
            return render_template('sponsor_profile.html',sponsor=sponsor,role=user.role)
    return redirect('/login')



# @app.route("/add_campaign", methods=["GET", "POST"])
# def campaign_add():
#     if "username" in session:
#         user=Register.query.filter_by(username=session['username']).first()
#         if user.role=='sponsor':     
#             try:
#                 if request.method == 'POST':
#                     user_id = user.id
#                     company_name = request.form.get('company_name')
#                     desc = request.form.get('desc')
#                     industry = request.form.get('industry')
#                     start_date = request.form.get('start_date')
#                     end_date = request.form.get('end_date')
#                     budget = request.form.get('budget')
#                     sponsor = Campaign(company_name=company_name,user_id=user_id, desc=desc, industry=industry, start_date=datetime.date.fromisoformat(start_date), end_date=datetime.date.fromisoformat(end_date), budget=budget)
#                     db.session.add(sponsor)
#                     db.session.commit()
#                     flash('Campaign added successfully','success')
#                     return redirect('/campaign')
#             except Exception as e:
#                 print(e)
#                 return (f"error,{e}")
#             return render_template('campaign_form.html',role=user.role)
#         else:
#             return 'Entry restricted'
#     else:
#         return redirect('/login')

@app.route('/contact_influencer',methods=["GET", "POST"])
def contact_influencer():
    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':
            
            try:
                if request.method=='POST':
                    messages = request.form.get('messages')
                    requirements = request.form.get('requirements')
                    payment_amount = request.form.get('payment_amount')
                    status = request.form.get('status')
                    influencer_request=add_request(messages=messages,requirements=requirements, payment_amount=payment_amount,status=status)
                    db.session.add(influencer_request)
                    db.session.commit()
                    flash('Profile updated successfully','success')
                    return redirect('/influencer')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            query_influencers=Register.query.filter_by(role='influencer')
            return render_template('contact_influencer.html',influencers=query_influencers)

        else:
            return 'Edit Restricted'
    else:
        return redirect('/login')        
    # return render_template('/contact_influencer.html')


@app.route('/contact_campaign')
def contact_campaign():
    return render_template('/contact_campaign.html')

