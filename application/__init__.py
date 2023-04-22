#!/usr/bin/python
import os
from flask import Flask
from dotenv import load_dotenv
from application.database import db

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

from application import routes
