import os
from datetime import timedelta

class Config:
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        'mysql+mysqlconnector://root@127.0.0.1:3306/calendly_like'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', '')
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=24)