from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import Config

# Cria a instância do DB
db = SQLAlchemy()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    mail.init_app(app)

    # Importa e registra os Controllers (Rotas)
    from .controllers.agendamento_controller import agendamento_bp
    app.register_blueprint(agendamento_bp)

    return app