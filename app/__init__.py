from flask import Flask
import os
from flask_cors import CORS

app = Flask(__name__)
app.config.from_object("config.DevelopmentConfig")

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')
CORS(app)

from app import views