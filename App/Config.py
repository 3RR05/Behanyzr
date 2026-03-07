import os
from dotenv import load_dotenv

load_dotenv() # Load Keys from .env file

class Config:
    """Main Config"""
    
    SECRET_KEY = os.environ.get('SECRET_KEY') or'D_Key'
    DATABASE_URL = os.environ.get('DATABASE_URL')
    
    if DATABASE_URL and DATABASE_URL.startswith('postgres://'):
        DATABASE_URL = DATABASE_URL.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_DATABASE_URI = DATABASE_URL or 'sqlite:///Behanyzr.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # NewsAPI Key
    NEWS_API_KEY= os.environ.get('NEWS_API_KEY') or 'Let_Me_In_Please'
    
    # Scrapper Config
    Max_Pages = 10
    Request_Delay = 2    