from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialization
db = SQLAlchemy()

def create_app(config_cls = 'App.Config.config'):
    # App Factory Instance Initialization
    app = Flask(__name__)
    app.config.from_object(config_cls)
    
    # Initialization With The App
    db.init_app(app)
    
    #Blueprint Registration
    """from App.Route import main_bp, api_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix = '/api')"""
    
    return app    
    