from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialization
db = SQLAlchemy()

def create_app(config_cls = 'App.Config.Config'):
    # App Factory Instance Initialization
    app = Flask(__name__,template_folder='Templates', static_folder='Static')
    app.config.from_object(config_cls)
    
    # Initialization With The App
    db.init_app(app)
    
    with app.app_context():
        from App.Model import Datasource, Textdata  # import data models
        db.create_all()
    
    #Blueprint Registration
    from App.Route import m_bp, a_bp
    app.register_blueprint(m_bp)
    app.register_blueprint(a_bp, url_prefix = '/api')
    
    return app    
    