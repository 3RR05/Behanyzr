import os

class Config:
    """Main Config"""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or'D_Key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'sqlite:///Behanyzr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Scrapper Config
    
    Max_Pg = 10
    R_Delay = 2    