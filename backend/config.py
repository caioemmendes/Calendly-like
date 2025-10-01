import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqlconnector://root@127.0.0.1:3306/calendly_like'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    MAIL_SERVER = 'smtp.example.com' 
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = 'seu_email@example.com'
    MAIL_PASSWORD = 'sua_senha_de_app'
    MAIL_DEFAULT_SENDER = 'seu_email@example.com'