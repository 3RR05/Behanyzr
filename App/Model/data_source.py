from App import db
from datetime import datetime

class Datasource(db.Model):
    # Information Storage For Data Collection Sources
    __tablename__ = 'data_source'
    
    id = db.Column(db.Integer, primary_key= True)
    name = db.Column(db.String(100), nullable= False)
    source_type = db.Column(db.String(50))
    url = db.Column(db.String(500))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_scraped = db.Column(db.DateTime)
    
    # Relationship To The Collected Texts
    texts = db.relationship('Textdata', backref='source', lazy='select', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'~Datasource - {self.id}~'
    