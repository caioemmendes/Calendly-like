from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt
from config import Config

db = SQLAlchemy()
mail = Mail()
jwt = JWTManager()
bcrypt = Bcrypt()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)
    
    db.init_app(app)
    mail.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)

    # Importa e registra os Controllers
    from .controllers.agendamento_controller import agendamento_bp
    from .controllers.auth_controller import auth_bp
    
    app.register_blueprint(agendamento_bp)
    app.register_blueprint(auth_bp)

    return app