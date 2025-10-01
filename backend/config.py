import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqlconnector://user:password@localhost/agendamentos_db'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = 'smtp.example.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'seu_email@example.com'
    MAIL_PASSWORD = 'sua_senha_de_app'
    MAIL_DEFAULT_SENDER = 'seu_email@example.com'