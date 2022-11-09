from main import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(50))
    userid = db.Column(db.Integer) # Supabase user id
    # add magic id/address
    # add moralis id/address