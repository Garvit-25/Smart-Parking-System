from flask import Flask
from flask_material import Material
import pymysql
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from oauthlib.oauth2 import WebApplicationClient

app = Flask(__name__)
Material(app)
db = pymysql.connect(
        host= YOUR_ENDPONT, 
        port = PORT,
        user = USERNAME, 
        password = PASSWORD,
        db = DB_NAME,
        )

app.config['SECRET_KEY'] = '968331509722a24aaca4a6ab62dea0cd'
GOOGLE_CLIENT_ID = "813361300800-pakcrlsju32gk2199no3kdqi2r3l8h48.apps.googleusercontent.com"
GOOGLE_CLIENT_SECRET = "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"
GOOGLE_DISCOVERY_URL = (
    "https://accounts.google.com/.well-known/openid-configuration"
)

client = WebApplicationClient(GOOGLE_CLIENT_ID)
login_manager = LoginManager()
cursor = db.cursor()
bcrypt = Bcrypt(app)
login_manager.init_app(app)

from parkingSystemAutomation import routes
