"""
The flask application package.
"""

from flask import Flask
import pypyodbc
app = Flask(__name__)

# this is the db connection string. import it in api.py
dbconnection = pypyodbc.connect('DRIVER={SQL Server};'
								'Server=tcp:z6mcia7rsl.database.windows.net;'
								'DATABASE=thisguyfucks;'
                                'UID=ndtndt@z6mcia7rsl;PWD=fuckFuckjun12#;')

import ndtndt.api
