import os

class config:
    """Main Config"""
    S_key = os.environ.get('S_Key') or'D_Key'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DB_URL') or 'sqlite:///Behanyzr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Scrapper Config
    Max_Pg = 10
    R_Delay = 2    