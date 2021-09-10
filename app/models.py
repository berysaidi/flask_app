''' Table representing our user stations '''
from app import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<{}>'.format(self.name)
