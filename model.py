from main import db





class Register(db.Model):
    id = db.Column(db.Integer(), primary_key=True) 
    role = db.Column(db.String(),nullable=False)
    username = db.Column(db.String(),nullable=False,unique=True)
    email = db.Column(db.String(),nullable=False)
    password = db.Column(db.String(),nullable=False)
    
