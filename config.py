import os

BASE_DIR = os.path.dirname(__file__)
# C:\projects\myproject의 위치 db.를 만들어서 저장함
SQLALCHEMY_DATABASE_URI = 'sqlite:///{}'.format(os.path.join(BASE_DIR, 'pybo.db'))

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dev"