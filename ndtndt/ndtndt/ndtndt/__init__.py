"""
The flask application package.
"""

from flask import Flask
import pypyodbc
app = Flask(__name__)
# this is the db connection string. import it in api.py
dbconnection = pypyodbc.connect('DRIVER={SQL Server Native Client 11.0};'
								'Server=tcp:SERVER_CONNECTION;'
								'DATABASE=DATABSE_NAME;'
                                'UID=YOUR_USER_NAME;PWD=YOUR_VERY_IMPORTANT_PASSWORD;'
                                'Encrypt=yes;TrustServerCertificate=no;'
                                'Connection Timeout=30;')

import ndtndt.api
