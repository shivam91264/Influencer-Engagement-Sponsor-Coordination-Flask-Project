from main import db





class Register(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    role = db.Column(db.String(),nullable=False)
    username = db.Column(db.String(),nullable=False,unique=True)
    email = db.Column(db.String(),nullable=False)
    password = db.Column(db.String(),nullable=False)
    

class Sponsors(db.Model):
    sponsor_id = db.Column(db.Integer(),primary_key=True)
    company_name = db.Column(db.String(),nullable=False)
    desc = db.Column(db.String(),nullable=False)
    industry = db.Column(db.String(),nullable=False)
    start_date = db.Column(db.Date())
    end_date = db.Column(db.Date())
    budget = db.Column(db.Integer(),nullable=False)


class Influencers(db.Model):
    influencer_id = db.Column(db.Integer(),primary_key=True)
    img = db.Column(db.LargeBinary,nullable=False)
    name = db.Column(db.String(), nullable=False)
    category = db.Column(db.String(), nullable=False)
    niche = db.Column(db.String(),nullable=False)
    reach = db.Column(db.String(),nullable=False)
