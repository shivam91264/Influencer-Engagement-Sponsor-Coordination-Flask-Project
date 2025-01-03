from main import db





class Register(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    role = db.Column(db.String(),nullable=False)
    username = db.Column(db.String(),nullable=False,unique=True)
    email = db.Column(db.String(),nullable=False)
    password = db.Column(db.String(),nullable=False)
    flag = db.Column(db.Boolean(),nullable=False,default=False)
    

class Campaign(db.Model):
    sponsor_id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.Integer(),nullable=False)
    brand_name = db.Column(db.String(),unique=True)
    company_name = db.Column(db.String(),nullable=False)
    desc = db.Column(db.String(),nullable=False)
    industry = db.Column(db.String(),nullable=False)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    budget = db.Column(db.Integer(),nullable=False)


class Influencers(db.Model):
    influencer_id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.Integer(),nullable=False)
    img = db.Column(db.LargeBinary,nullable=False)
    name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    niche = db.Column(db.String(),nullable=False)
    reach = db.Column(db.String(),nullable=False)


class Sponsors(db.Model):
    sponsor_id = db.Column(db.Integer(),primary_key=True)
    user_id = db.Column(db.Integer(),nullable=False)
    img = db.Column(db.LargeBinary,nullable=False)
    company_name = db.Column(db.String(),nullable=False)
    desc = db.Column(db.String(),nullable=False)
    industry = db.Column(db.String(),nullable=False)


class Add_request(db.Model):
    request_id = db.Column(db.Integer(),primary_key=True)
    from_id = db.Column(db.Integer(),nullable=False)
    too_id = db.Column(db.Integer(),nullable=False)
    brand_name = db.Column(db.String,nullable=False)
    messages = db.Column(db.String(),nullable=False)
    requirements = db.Column(db.String(),nullable=False)
    payment_amount = db.Column(db.Integer(),nullable=False)
    status = db.Column(db.String(),nullable=False)


