import os

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqlconnector://root@127.0.0.1:3306/calendly_like'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False