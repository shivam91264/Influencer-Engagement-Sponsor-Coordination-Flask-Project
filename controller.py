from flask import render_template,request,redirect,session,flash,send_file
from werkzeug.security import generate_password_hash , check_password_hash
import datetime
from main import *
from model import *
from io import BytesIO




@app.route("/", methods=["GET", "POST"])   # route for register user
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



@app.route("/login", methods=["GET", "POST"])   # route for login user
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
            if user.flag == True :
                flash('You are flaged please contact admin','danger')
                return redirect('/login')
            
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

@app.route('/logout',methods=["GET", "POST"])    # route for logout user
def log_out():
    if 'username' in session:
        session.pop('username')
        return redirect('/login')
    else:
        return redirect('/login')
    

@app.route('/home',methods=["GET", "POST"])    # route for home page
def home():
    if 'username' in session:
            user=Register.query.filter_by(username=session['username']).first()
            if user.role=='influencer' or user.role=='sponsor':
                return render_template('home.html',role=user.role)
            else:
                return '<h1>Resticted Entry</h1>' 
    else:
        return redirect('/login')  


@app.route("/admin", methods=["GET", "POST"])   # route for admin
def admin():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='admin':
            active_user=Register.query.all()
            campaigns=Campaign.query.all()
            statuss=Add_request.query.all()
            count_influencer_active_user=len([user for user in active_user if user.flag==False and user.role=='influencer'])
            count_sponsor_active_user=len([user for user in active_user if user.flag==False and user.role=='sponsor'])
            total_users = count_influencer_active_user + count_sponsor_active_user
            count_campaigns=len([campaign for campaign in campaigns])
            count_pending=len([status for status in statuss if status.status=="pending"])
            count_accepted=len([status for status in statuss if status.status=='accepted'])
            count_rejected=len([status for status in statuss if status.status=='rejected'])
            count_renegotiate=len([status for status in statuss if status.status=='renegotiate'])
            flaged_sponsor=len([flaged for flaged in active_user if flaged.flag==True and flaged.role=='sponsor'])
            flaged_influencer=len([flaged for flaged in active_user if flaged.flag==True and flaged.role=='influencer'])
            return render_template('admin.html',total_users=total_users,count_influencer_active_user=count_influencer_active_user,count_sponsor_active_user=count_sponsor_active_user,count_campaigns=count_campaigns,count_pending=count_pending,count_accepted=count_accepted,count_rejected=count_rejected,count_renegotiate=count_renegotiate,flaged_sponsor=flaged_sponsor,flaged_influencer=flaged_influencer)
        else:
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')

@app.route("/influencer", methods=["GET", "POST"])    # route for influencer
def influencer():
    if "username" in session:
        influencer=Influencers.query.all()
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='influencer' or user.role=='sponsor' or user.role=='admin':
            return render_template('influencer.html',influencers=influencer,role=user.role)
        else:
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')
    

@app.route("/sponsor", methods=["GET", "POST"])   # route for sponsor
def sponsor():
    if "username" in session:
        sponsor=Sponsors.query.all()
        user=Register.query.filter_by(username=session['username']).first()
        if  user.role=='admin' :
            return render_template('sponsor.html',sponsors=sponsor,role=user.role)
        else:
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')


@app.route("/campaign", methods=["GET"])   # route for campaign
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




@app.route("/add_campaign", methods=["GET", "POST"])   # route for add new campaign
def campaign_add():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':     
            try:
                if request.method == 'POST':
                    user_id = user.id
                    company_name = request.form.get('company_name')
                    brand_name = request.form.get('brand_name')
                    desc = request.form.get('desc')
                    industry = request.form.get('industry')
                    start_date = request.form.get('start_date')
                    end_date = request.form.get('end_date')
                    budget = request.form.get('budget')
                    sponsor = Campaign(company_name=company_name,brand_name=brand_name,user_id=user_id, desc=desc, industry=industry, start_date=datetime.date.fromisoformat(start_date), end_date=datetime.date.fromisoformat(end_date), budget=budget)
                    db.session.add(sponsor)
                    db.session.commit()
                    flash('Campaign added successfully','success')
                    return redirect('/campaign')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            return render_template('campaign_form.html',role=user.role)
        else:
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')
    

@app.route("/influencer_form", methods=["GET", "POST"])    # route for create influencer profile
def influencer_form():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='influencer':     
            try:
                if request.method == 'POST':
                    img=request.files['img']
                    if not img:
                        return '<h1> img not uploaded </h1>'
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
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')
    

@app.route("/sponsor_form", methods=["GET", "POST"])   # route for create sponsor profile
def sponsor_form():
    if "username" in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':     
            try:
                if request.method == 'POST':
                    img=request.files['img']
                    if not img:
                        return '<h1> img not uploaded </h1>'
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
            return '<h1>Resticted Entry</h1>'
    else:
        return redirect('/login')


@app.route('/image/<int:image_id>')    # route for upload influencer image
def get_image(image_id):
    image = Influencers.query.filter_by(influencer_id = image_id).first()
    if not image:
        return 'Image not found', 404
    return send_file(BytesIO(image.img), mimetype='image/jpeg')

@app.route('/image1/<int:image_id>')   # route for upload sponsor image
def get_image1(image_id):
    image = Sponsors.query.filter_by(sponsor_id = image_id).first()
    if not image:
        return 'Image not found', 404
    return send_file(BytesIO(image.img), mimetype='image/jpeg')


@app.route("/delete_campaign/<int:id>")  # route for delete exitisting campaign
def delete_camp(id):
        if "username" in session:
            user=Register.query.filter_by(username=session['username']).first()
            if user.role=='sponsor' or user.role=='admin':     
                Campaign.query.filter_by(sponsor_id=id).delete()
                db.session.commit()
                flash('Card deleted successfully!!')
                return redirect('/campaign')
            else:
                return '<h1> Delete Restricted </h1>'
        else:
            return redirect ('/login')


@app.route("/edit_campaign/<int:id>",methods=["GET", "POST"])   # route for edit Exist campaign
def edit_campaign(id):
        if "username" in session:  
            user=Register.query.filter_by(username=session['username']).first()  
            if user.role=='sponsor' or user.role=='admin': 
                if request.method=='GET':     
                    campaign=Campaign.query.filter_by(sponsor_id=id).first() 
                    return render_template('edit_campaign.html',campaign=campaign,role=user.role) 
                elif request.method=='POST':
                    campaign=Campaign.query.filter_by(sponsor_id=id).first()
                    campaign.company_name = request.form.get('company_name')
                    campaign.desc = request.form.get('desc')
                    campaign.industry = request.form.get('industry')
                    campaign.start_date=datetime.date.fromisoformat(request.form.get('start_date'))
                    campaign.end_date=datetime.date.fromisoformat(request.form.get('end_date'))
                    campaign.budget = request.form.get('budget')
                    db.session.commit()  
                    flash('Your card updated successfully','success')
                    return redirect('/campaign')
            else:
                return '<h1> Edit Restricted </h1>' 
        else:
            return redirect ('/login')  
        


@app.route("/edit_influencer/<int:id>",methods=["GET", "POST"])   # route for edit influencer profile
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
                return '<h1> Edit Restricted </h1>'
        else:
            return redirect ('/login')
        
@app.route("/edit_sponsor/<int:id>",methods=["GET", "POST"])  # route for edit sponsor profile
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
                return '<h1> Edit Restricted </h1>'
        else:
            return redirect ('/login')




@app.route("/influencer_profile")   # route for influencer profile
def influ_profile():
    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='influencer':
            influencer=Influencers.query.filter_by(user_id=user.id).first()
            add_requests = Add_request.query.filter_by(too_id=user.id,status='pending')
            renegotiate_requests = Add_request.query.filter_by(too_id=user.id,status='renegotiate')
            return render_template('influencer_profile.html',influencer=influencer,role=user.role,add_requests=add_requests,renegotiate_requests=renegotiate_requests)
    return redirect('/login')




@app.route("/sponsor_profile")   # route for sponsor profile
def sponsor_profile():
    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor':
            sponsor=Sponsors.query.filter_by(user_id=user.id).first()
            request_sponsor = Add_request.query.filter_by(from_id=user.id,status='pending')
            renegotiate_sponsor = Add_request.query.filter_by(from_id=user.id,status='renegotiate')
            
            return render_template('sponsor_profile.html',sponsor=sponsor,role=user.role,request_sponsor=request_sponsor,renegotiate_sponsor=renegotiate_sponsor)
    return redirect('/login')




@app.route('/contact_influencer',methods=["GET", "POST"])   # route for contact influencers
def contact_influencer():
    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='sponsor' : 
            try:
                if request.method=='POST':
                    influencer_username = request.form.get('options')
                    from_id = user.id  # from id is come from user
                    get_id = Register.query.filter_by(username=influencer_username).first()
                    too_id = get_id.id
                    brand_name = request.form.get('brand_name')
                    messages = request.form.get('messages')
                    requirements = request.form.get('requirements')
                    payment_amount = float(request.form.get('payment_amount'))
                    status = 'pending'
                    influencer_request=Add_request(from_id=from_id,too_id=too_id,brand_name=brand_name,messages=messages,requirements=requirements, payment_amount=payment_amount,status=status)
                    db.session.add(influencer_request)
                    db.session.commit()
                    flash('Request send successfully','success')
                    return redirect('/influencer')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            campaign=Campaign.query.filter_by(user_id=user.id)
            query_influencers=Register.query.filter_by(role='influencer')
            return render_template('contact_influencer.html',influencers=query_influencers,campaigns=campaign)

        else:
            return '<h1> Edit Restricted </h1>'
    else:
        return redirect('/login')
            
@app.route('/contact_sponsor',methods=["GET", "POST"])    # route for contact sponsors
def contact_sponsor():
    if 'username' in session:
        user=Register.query.filter_by(username=session['username']).first()
        if user.role=='influencer' : 
            try:
                if request.method=='POST':
                    brand_name = request.form.get('brand_name')
                    too_id = user.id
                    get_id = Campaign.query.filter_by(brand_name=brand_name).first()
                    from_id =get_id.user_id
                    messages = request.form.get('messages')
                    requirements = request.form.get('requirements')
                    payment_amount = float(request.form.get('payment_amount'))
                    status = 'renegotiate'
                    sponsor_request=Add_request(from_id=from_id,too_id=too_id,brand_name=brand_name,messages=messages,requirements=requirements, payment_amount=payment_amount,status=status)
                    db.session.add(sponsor_request)
                    db.session.commit()
                    flash('Request send successfully','success')
                    return redirect('/campaign')
            except Exception as e:
                print(e)
                return (f"error,{e}")
            campaign=Campaign.query.all()
            return render_template('contact_campaign.html',campaigns=campaign)
        else:
            return '<h1> Edit Restricted </h1>'
    else:
        return redirect('/login')        





@app.route("/accept_request/<int:id>")    # route for accept request
def accept_request(id):
    if "username" in session:
        user = Register.query.filter_by(username=session['username']).first()
        if user.role == 'influencer':
            request = Add_request.query.filter_by(request_id=id, too_id=user.id).first()
            if request:
                request.status = 'accepted'
                db.session.commit()
                flash('Request accepted ', 'success')
                return redirect('/influencer_profile')
    return redirect('/login')


@app.route("/reject_request/<int:id>")   # route for reject request
def reject_request(id):
    if "username" in session:
        user = Register.query.filter_by(username=session['username']).first()
        if user.role == 'influencer':
            request = Add_request.query.filter_by(request_id=id, too_id=user.id).first()
            if request:
                request.status = 'rejected'
                db.session.commit()
                flash('Request rejected ', 'danger')
                return redirect('/influencer_profile')
    return redirect('/login')


@app.route("/renegotiate_request/<int:id>",methods=["GET", "POST"])   # route for renegotiate request
def renegotiate_request(id):
    if "username" in session:
        user = Register.query.filter_by(username=session['username']).first()
        if user.role == 'influencer':
            if request.method=='GET':
                renegotiate=Add_request.query.filter_by(request_id=id).first()
                return render_template('renegotiate.html',renegotiate=renegotiate)
            elif request.method=='POST':
                new_amount=request.form.get('payment_amount')
                status = 'renegotiate'
                renegotiate=Add_request.query.filter_by(request_id=id).first()
                renegotiate.status=status
                renegotiate.payment_amount=new_amount
                db.session.commit()
                flash('Renegotiate request sent ','success')
                return redirect('/influencer_profile')
    return redirect('/login')


@app.route("/request_sponsor/<int:id>")    # route for send request to sponsor
def request_sponsor(id):
    if "username" in session:
        user = Register.query.filter_by(username=session['username']).first()
        if user.role == 'sponsor':
            request = Add_request.query.filter_by(request_id=id, from_id=user.id).first()
            if request:
                request.status = 'accepted'
                db.session.commit()
                flash('Request accepted ', 'success')
                return redirect('/sponsor_profile')
    return redirect('/login')


@app.route("/edit_request/<int:id>",methods=["GET", "POST"])   # route for edit request 
def edit_request(id):
    if "username" in session:
        user = Register.query.filter_by(username=session['username']).first()
        if user.role == 'sponsor':
            if request.method=='GET':
                requests = Add_request.query.filter_by(request_id=id, from_id=user.id).first()
                return render_template('edit_request.html',requests=requests)
            if request.method == 'POST':
                new_message = request.form.get('messages')
                new_requirement = request.form.get('requirements')
                new_payment = request.form.get('payment_amount')
                fetch = Add_request.query.filter_by(request_id=id).first()
                fetch.messages=new_message
                fetch.requirements=new_requirement
                fetch.payment_amount=new_payment
                db.session.commit()
            return redirect('/sponsor_profile')
    return redirect('/login')

@app.route("/delete_request/<int:id>")    # route for delete request
def delete_request(id):
    if "username" in session:
        user = Register.query.filter_by(username=session['username']).first()
        if user.role == 'sponsor':
                Add_request.query.filter_by(request_id=id).delete()
                db.session.commit()
                flash('Request deleted succesfully ', 'success')
                return redirect('/sponsor_profile')
    return redirect('/login')




@app.route("/renegotiate_sponsor/<int:id>",methods=["GET", "POST"])    # route for renegotiate  request
def renegotiate_sponsor(id):
    if "username" in session:
        user = Register.query.filter_by(username=session['username']).first()
        if user.role == 'sponsor':
            if request.method=='GET':
                renegotiate=Add_request.query.filter_by(request_id=id).first()
                return render_template('sponsor_renegotiate.html',renegotiate=renegotiate)
            elif request.method=='POST':
                new_amount=request.form.get('payment_amount')
                renegotiate=Add_request.query.filter_by(request_id=id).first()
                renegotiate.payment_amount=new_amount
                db.session.commit()
                flash('Renegotiate request sent ','success')
                return redirect('/sponsor_profile')
    return redirect('/login')




@app.route('/flag_user/<int:id>')  # route for flag or unflag user
def flag_user(id):
    if "username" in session:
        admin_user = Register.query.filter_by(username=session['username']).first()
        if admin_user.role=='admin':
            user = Register.query.filter_by(id=id).first()
            if user:
                if user.flag==False:
                    user.flag = True
                    flash('User Flaged Successfully','danger')
                else:
                    user.flag = False
                    flash('User Unflaged Successfully','success')
                db.session.commit()
                if user.role == 'influencer':
                    return redirect('/influencer')
                else:
                    return redirect('/sponsor')
                # return redirect('/influencer')
            else:
                flash('User Not Found','danger')
                return redirect('/influencer')
        else:
            return '<h1> Restricted Entry </h1>'
    else:
        return redirect('/login')
    

@app.route('/search',methods=["GET", "POST"])   # route for search influencers or campaigns
def search():
    if "username" in session:
        if request.method=='POST':
            user = Register.query.filter_by(username=session['username']).first()
            input_query = request.form.get('search')
            if user.role=='sponsor':
                influencers=Influencers.query.filter(Influencers.name.ilike(f"%{input_query}%")).all()
                return render_template('search.html',influencers=influencers,role=user.role)
            elif user.role=='influencer':
                campaign=Campaign.query.filter(Campaign.company_name.ilike(f"%{input_query}%")).all()
                print([campaign1 for campaign1 in campaign])
                return render_template('search.html',campaign=campaign,role=user.role) 
        user = Register.query.filter_by(username=session['username']).first()
        return render_template('search.html',role=user.role)
    return redirect('/login')