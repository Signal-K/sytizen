from . import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True) # This should match with Supabase?
    email = db.Column(db.String(50))
    magicId = db.Column(db.String(100))