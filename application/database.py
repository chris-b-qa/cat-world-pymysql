#!/usr/bin/python
import pymysql.cursors
import os
from dotenv import load_dotenv

load_dotenv()

db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_host = os.getenv('DB_HOST', '127.0.0.1')
db_port = os.getenv('DB_PORT', '3306')
db_name = os.getenv('DB_NAME')

db = pymysql.connect(host=db_host,
                     user=db_user,
                     password=db_password,
                     database=db_name,
                     charset='utf8mb4',
                     cursorclass=pymysql.cursors.DictCursor)
