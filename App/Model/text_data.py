from App import db
from datetime import datetime

class Textdata(db.Model):
    # Storage For Text Samples
    __tablename__ = 'Text_data'
    
    id = db.Column(db.Integer, primary_key= True)
    source_id = db.Column(db.Integer, db.Foreignkey('data_source.id'), nullable= False)
    
    # Extracted Contents
    text = db.Column(db.Text, nullable= False)
    author = db.Column(db.string(100))
    
    #Metadata
    collected_at = db.Column(db.DateTime, default= datetime.utcnow)
    og_timestamp = db.Column(db.DateTime)
    
    # Analysis Report
    sentiment_score = db.Column(db.Float)
    word_count = db.Column(db.Integer)
    
    def __repr__(self):
        return f'~TextData - {self.id} : {self.text[:50]}~'