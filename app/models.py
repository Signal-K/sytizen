from . import db

class Planet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    moons = db.Column(db.String(50))

    def __init__(self, name, moons):
        self.name = name
        self.moons = moons