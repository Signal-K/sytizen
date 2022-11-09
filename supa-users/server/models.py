from main import db, ma

class Articles(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nulable = False)
    body = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime(), nullable = False)

    def __repr__(self):
        return "<Articles %r>" % self.title

class ArticlesSchema(ma.Schema): # Generates marshmallow schemas from models
    class Meta:
        fields = ("id", "title", "body", "date") # Expose these fields

article_schema = ArticlesSchema()
articles_schema = ArticlesSchema(many = True)