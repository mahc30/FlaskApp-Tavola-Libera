import urllib.parse
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

# Configure Database URI:
params = urllib.parse.quote_plus(
    "Driver={ODBC Driver 17 for SQL Server};Server=tcp:tavolalibera.database.windows.net,1433;Database=TavolaLiberaDB;Uid=dreamteam;Pwd=Password1;Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;"
)

app = Flask(__name__)
app.config["SECRET_KEY"] = "82c021c5452b33eb5c34b1c9abc2e276"
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)

from tavolalibera import routes